from decouple import config
import json
from pathlib import Path
from web3 import Web3
import os

WSL_PROJECT_PATH = config('WSL_PROJECT_PATH')

JSON_PATH = Path(WSL_PROJECT_PATH) / 'scripts' / 'address.json'


print(f"WSL_PROJECT_PATH: {WSL_PROJECT_PATH}")


print(f"Percorso JSON: {JSON_PATH}")


# Configura la connessione alla rete locale Hardhat
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Carica l'ABI
with open('blockchain/abi/Lock.json') as f:
    contract_abi = json.load(f)["abi"]

# Indirizzo del contratto (sostituisci con l'indirizzo del deploy)
#contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"

def get_message():
    """Recupera il messaggio salvato nel contratto."""
    return contract.functions.message().call()

def get_contract_address():
    try:
        with open(JSON_PATH, 'r') as json_file:
            data = json.load(json_file)
            return data.get('contract_address', 'indirizzo_non_trovato')
    except FileNotFoundError:
        raise RuntimeError(f"Il file JSON non è stato trovato nel percorso: {JSON_PATH}")
    except json.JSONDecodeError:
        raise RuntimeError("Errore nella lettura del file JSON: Formato non valido.")
    
# Inizializza il contratto
address=get_contract_address()
print(address)

contract = web3.eth.contract(address=get_contract_address(), abi=contract_abi)