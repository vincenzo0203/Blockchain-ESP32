from decouple import config
import json
from pathlib import Path
from web3 import Web3

WSL_PROJECT_PATH = config('WSL_PROJECT_PATH')

JSON_PATH = Path(WSL_PROJECT_PATH) / 'scripts' / 'address.json'

ABI_PATH = Path(WSL_PROJECT_PATH) / 'artifacts' / 'contracts' / 'SecurityLog.sol' / 'SecurityLog.json'

# Configura la connessione alla rete locale Hardhat
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Carica l'ABI
with open(ABI_PATH) as f:
    contract_abi = json.load(f)["abi"]

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

contract = web3.eth.contract(address=get_contract_address(), abi=contract_abi)

def is_valid_uid(uid):
    # Puoi personalizzare questa lista o spostare la logica sul database in futuro
    valid_uids = ["f3620c35", "another_valid_uid"]  # Lista statica come esempio
    return uid in valid_uids
