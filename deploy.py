from solcx import compile_standard
import solcx
from web3 import Web3
import json
from dotenv import load_dotenv
import os

load_dotenv()

solcx.install_solc("0.8.7")

print("Reading the solidity file", end="\n\n")

with open("./contracts/SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compiling solidity file

print("Compiling the solidity file", end="\n\n")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"./contracts/SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.7",
)

with open("./compiled_sol.json", "w") as file:
    json.dump(compiled_sol, file)

contract = compiled_sol["contracts"]["./contracts/SimpleStorage.sol"]["SimpleStorage"]

bytecode = contract["evm"]["bytecode"]["object"]
abi = contract["abi"]

# connecting to ganache

print("Connecting to Ganache", end="\n\n")

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
my_address = os.environ.get("ADDRESS")
private_key = os.environ.get("PRIVATE_KEY")

# deploying the contract

print("Deploying the contract", end="\n\n")

SimpleStorage = w3.eth.contract(bytecode=bytecode, abi=abi)
nonce = w3.eth.getTransactionCount(my_address)
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

print("Deployed the contract", end="\n\n")

# working with contract

print("Working with the contract", end="\n\n")

simple_storage = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)

# call() is for the view functions
print("Value of num : ", simple_storage.functions.getNum().call(), end="\n\n")

# functions with a state change need to be a signed transaction
nonce = w3.eth.getTransactionCount(my_address)
add_person_transaction = simple_storage.functions.addPerson(
    "Yash", 24
).buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)  # adding a person and favourite number
add_person_signed_txn = w3.eth.account.sign_transaction(
    add_person_transaction, private_key=private_key
)
add_person_txn_hash = w3.eth.send_raw_transaction(add_person_signed_txn.rawTransaction)
add_person_txn_receipt = w3.eth.wait_for_transaction_receipt(add_person_txn_hash)

# getting the back the person details
print(simple_storage.functions.getPerson("Yash").call())
