#Import Web3 library
from web3 import Web3
from eth_account import Account
import time
import sys
import os
import random # Import random module

# Data bridge configuration
from data_bridge import data_bridge
from keys_and_addresses import private_keys, labels # No longer read my_addresses
from network_config import networks

# Text centering function
def center_text(text):
terminal_width = os.get_terminal_size().columns
lines = text.splitlines()
centered_lines = [line.center(terminal_width) for line in lines]
return "\n".join(centered_lines)

# Clear terminal function
def clear_terminal():
os.system('cls' if os.name == 'nt' else 'clear')

description = """
Automatic bridge robot https://bridge.t1rn.io/
Fuck you Rambeboy, stealing private keys🐶
"""

# Colors and symbols for each chain
chain_symbols = {
'Arbitrum Sepolia': '\033[34m',
'OP Sepolia': '\033[91m',
}

# Color definitions
green_color = '\033[92m'
reset_color = '\033[0m'
menu_color = '\033[95m' # Menu text color

# Block explorer URLs for each network
explorer_urls = {
'Arbitrum Sepolia': 'https://sepolia.arbiscan.io/tx/',
'OP Sepolia': 'https://sepolia-optimism.etherscan.io/tx/',
'BRN': 'https://brn.explorer.caldera.xyz/tx/'
}

# Function to get BRN balance
def get_brn_balance(web3, my_address):
balance = web3.eth.get_balance(my_address)
return web3.from_wei(balance, 'ether')

# Function to check chain balance
def check_balance(web3, my_address):
balance = web3.eth.get_balance(my_address)
return web3.from_wei(balance, 'ether')

# Function to create and send transactions
def send_bridge_transaction(web3, account, my_address, data, network_name):
nonce = web3.eth.get_transaction_count(my_address, 'pending')
value_in_ether = 0.1
value_in_wei = web3.to_wei(value_in_ether, 'ether') try: gas_estimate = web3.eth.estimate_gas({ 'to': networks[network_name]['contract_address'], 'from': my_address, 'data': data, 'value': value_in_wei }) gas_limit = gas_estimate + 50000 # Increase safety margin except Exception as e: print(f"Estimated gas error: {e}") return None base_fee = web3.eth.get_block('latest')['baseFeePerGas'] priority_fee = web3.to_wei(5, 'gwei') max_fee = base_fee + priority_fee transaction = { 'nonce': nonce, 'to': networks[network_name]['contract_address'], 'value': value_in_wei, 'gas': gas_limit, 'maxFeePerGas': max_fee, 'maxPriorityFeePerGas': priority_fee, 'chainId': networks[network_name]['chain_id'], 'data': data } try: signed_txn = web3.eth.account.sign_transaction(transaction, account.key) except Exception as e: print(f"Signature transaction error: {e}") return None try: tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction) tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash) # Get the latest balance balance = web3.eth.get_balance(my_address) formatted_balance = web3.from_wei(balance, 'ether')

# Get the block explorer link
explorer_link = f"{explorer_urls[network_name]}{web3.to_hex(tx_hash)}"

# Display transaction information
print(f"{green_color}📤 Send address: {account.address}")
print(f"⛽ Use Gas: {tx_receipt['gasUsed']}")
print(f"🗳️ Block number: {tx_receipt['blockNumber']}")
print(f"💰 ETH balance: {formatted_balance} ETH")
brn_balance = get_brn_balance(Web3(Web3.HTTPProvider('https://brn.rpc.caldera.xyz/http')), my_address)
print(f"🔵 BRN balance: {brn_balance} BRN")
print(f"🔗 Block Explorer Link: {explorer_link}\n{reset_color}")

return web3.to_hex(tx_hash), value_in_ether
except Exception as e:
print(f"Send transaction error: {e}")
return None, None

# Function to process transactions on a specific network
def process_network_transactions(network_name, bridges, chain_data, successful_txs):
web3 = Web3(Web3.HTTPProvider(chain_data['rpc_url']))
if not web3.is_connected():
raise Exception(f"Unable to connect to network {network_name}")

for bridge in bridges:
for i, private_key in enumerate(private_keys):
account = Account.from_key(private_key)

# Generate address from private key
my_address = account.address

data = data_bridge.get(bridge) # Ensure data_bridge It is a dictionary type
if not data:
print(f"Bridge {bridge} data is not available!")
continue

result = send_bridge_transaction(web3, account, my_address, data, network_name)
if result:
tx_hash, value_sent = result
successful_txs += 1

# Check if value_sent is valid and then format
if value_sent is not None:
print(f"{chain_symbols[network_name]}🚀 Total number of successful transactions: {successful_txs} | {labels[i]} | Bridge: {bridge} | Bridge amount: {value_sent:.5f} ETH ✅{reset_color}\n")
else:
print(f"{chain_symbols[network_name]}🚀 Total number of successful transactions: {successful_txs} | {labels[i]} | Bridge: {bridge} ✅{reset_color}\n")

print(f"{'='*150}")
print("\n")

# Randomly wait 30 to 60 seconds
wait_time = random.uniform(30, 60)
print(f"⏳ Wait for {wait_time:.2f} seconds before continuing...\n")
time.sleep(wait_time) # Random delay time
