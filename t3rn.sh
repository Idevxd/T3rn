# !bin/bash

# script save path

SCRIPT_PATH="$HOME/t3rn.sh"



# Check if root user

if [ "$EUID" -ne 0 ]; then 

 echo -e "${RED}请使用 sudo run 此 script${NC}"

 exit 1

fi



#Define warehouse address and catalog name

REPO_URL="https://github.com/sdohuajia/t3rn-bot.git"

DIR_NAME="t3rn-bot"

PYTHON_FILE="keys_and_addresses.py"

DATA_BRIDGE_FILE="data_bridge.py"

BOT_FILE="bot.py"

VENV_DIR="t3rn-env" # virtual directory directory



# Check if installed git

if ! command -v git &> /dev/null; then

 echo "Git not installed, 请先 install Git."

 exit 1

fi



# Check if installed python3-pip and python3-venv

if ! command -v pip3 &> /dev/null; then

 echo "pip not installed, currently installing python3-pip..."

 sudo apt update

 sudo apt install -y python3-pip

fi



if ! command -v python3 -m venv &> /dev/null; then

 echo "python3-venv not installed, currently installing python3-venv..."

 sudo apt update

 sudo apt install -y python3-venv

fi



# fetch warehouse

if [ -d "$DIR_NAME" ]; then

 echo "Directory $DIR_NAME exists, download latest updates..."

 cd "$DIR_NAME" || exit

 git pull origin main

otherwise

 echo "Clone repository $REPO_URL..."

 git clone "$REPO_URL"

 cd "$DIR_NAME" || exit

fi



echo " Already entered directory $DIR_NAME"



# create virtual environment and activate

echo "I am creating a virtual environment..."

python3 -m venv "$VENV_DIR"

source "$VENV_DIR/bin/activate"



# upgrade pip

echo "Upgrading pip..."

pip install --upgrade pip



#install dependencies

echo "Currently installing dependencies on web3 and colorama..."

pip install web3 colorama



, alert user private key security

echo "Warning: Please ensure your private key is safe!"

echo "The private key should be stored in a secure location, do not share it openly or disclose it to others."

echo "If your private key is leaked, it may lead to the loss of your assets!"

echo "Please enter your private key, ensure secure operation."



# Let user input private key and label

echo "Enter your private key(multiple private keys)

read -r private_keys_input



echo "Please enter your labels (multiple labels separated by space, matching the order of the private key):"

read -r labels_input



# Check if input matches

IFS=' ' read -r -a private_keys <<< "$private_keys_input"

IFS=' ' read -r -a labels <<< "$labels_input"



if [ "${#private_keys[@]}" -ne "${#labels[@]}" ]; then

 echo "The number of private keys and labels does not match, please re-run the script and ensure that they match!"

 exit 1

fi



# write keys_and_addresses.py file

echo "Writing $PYTHON_FILE file..."

cat > $PYTHON_FILE <<EOL

# Generate this file from script



private_keys = [

$(printf " '%s',\n" "${private_keys[@]}")

,



label= ,

$(printf " '%s',\n" "${labels[@]}")

,

eol



echo "$PYTHON_FILE file is already generated."



# remind user private key security

echo "Script execution completed! All dependencies installed, private keys and labels saved in $PYTHON_FILE 中."

echo "Please save this file to avoid leaking your private key and label information!"



# Get additional user input："ARB - OP SEPOLIA" 和 "OP - ARB"

echo "请 input 'ARB - OP SEPOLIA' value："

read -r arb_op_sepolia_value



echo "请 input 'OP - ARB' value："

read -r op_arb_value



# write data_bridge.py file

echo "Writing $DATA_BRIDGE_FILE file..."

cat > $DATA_BRIDGE_FILE <<EOL

# Generate this file from script



data_bridge = {

 # Data bridge Arbitrum Sepolia

 "ARB - OP SEPOLIA": "$arb_op_sepolia_value",



 # Data bridge OP Sepolia

 "OP - ARB": "$op_arb_value",

,

eol



echo "$DATA_BRIDGE_FILE file is already generated."



# remind user to run bot.py

echo "Configuration complete, running bot.py..."



# run bot.py

python3 $BOT_FILE
