import json
from web3 import Web3

# Configura la connessione alla rete locale Hardhat
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Carica l'ABI
with open('blockchain/abi/Lock.json') as f:
    contract_abi = json.load(f)["abi"]

# Indirizzo del contratto (sostituisci con l'indirizzo del deploy)
contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"

# Inizializza il contratto
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def get_message():
    """Recupera il messaggio salvato nel contratto."""
    return contract.functions.message().call()
