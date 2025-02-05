from decouple import config
import json
from pathlib import Path
from web3 import Web3
import datetime
from zoneinfo import ZoneInfo
from accounts.models import Person


WSL_PROJECT_PATH = config('WSL_PROJECT_PATH')

JSON_PATH = Path(WSL_PROJECT_PATH) / 'scripts' / 'address.json'

ABI_PATH = Path(WSL_PROJECT_PATH) / 'artifacts' / 'contracts' / 'SecurityLog.sol' / 'SecurityLog.json'

# Configura la connessione alla rete locale Hardhat
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))


OWNER_ADDRESS = web3.eth.accounts[0]  # Primo account Hardhat

PRIVATE_KEY = config('PRIVATE_KEY')

# Carica l'ABI
with open(ABI_PATH) as f:
    contract_abi = json.load(f)["abi"]

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
    return Person.objects.filter(rfid=uid).exists()

def log_access_on_blockchain(rfid, granted):
    """Registra un accesso RFID sulla blockchain"""
    try:
        
        nonce = web3.eth.get_transaction_count(OWNER_ADDRESS)

        txn = contract.functions.logAccess(rfid, granted).build_transaction({
            "from": OWNER_ADDRESS,
            "nonce": nonce,
            "gas": 200000,
            "gasPrice": web3.to_wei("10", "gwei")
        })

        signed_txn = web3.eth.account.sign_transaction(txn, PRIVATE_KEY)
        txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

        return txn_hash.hex()
    
    except Exception as e:
        raise RuntimeError(f"Errore blockchain: {str(e)}")

def get_access_logs():
    try:
        # Chiamata alla funzione `getAllAccessLogs` del contratto
        access_logs = contract.functions.getAllAccessLogs().call()

        # Formatta i dati in modo leggibile
        logs = []
        for log in access_logs:
            logs.append({
                'rfid': log[0],
                'timestamp': datetime.datetime.fromtimestamp(log[1], tz=ZoneInfo("UTC")).astimezone(ZoneInfo("Europe/Rome")),
                'granted': log[2]
            })

        return logs

    except Exception as e:
        raise RuntimeError(f"Errore nel recupero dei log di accesso: {str(e)}")
    
def log_admin_action_on_blockchain(username_admin, action, user):
    """Registra un'azione amministrativa sulla blockchain"""
    try:
        nonce = web3.eth.get_transaction_count(OWNER_ADDRESS)

        txn = contract.functions.logAdminAction(username_admin, action, user).build_transaction({
            "from": OWNER_ADDRESS,
            "nonce": nonce,
            "gas": 200000,
            "gasPrice": web3.to_wei("10", "gwei")
        })

        signed_txn = web3.eth.account.sign_transaction(txn, PRIVATE_KEY)
        txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

        return txn_hash.hex()
    
    except Exception as e:
        raise RuntimeError(f"Errore blockchain (AdminActionLog): {str(e)}")

def get_admin_action_logs():
    """Recupera tutti i log delle azioni amministrative dalla blockchain"""
    try:
        admin_action_logs = contract.functions.getAllAdminActionLogs().call()

        logs = []
        for log in admin_action_logs:
            logs.append({
                'username_admin': log[0],
                'action': log[1],
                'user': log[2],
                'timestamp': datetime.datetime.fromtimestamp(log[3], tz=ZoneInfo("UTC")).astimezone(ZoneInfo("Europe/Rome"))
            })

        return logs

    except Exception as e:
        raise RuntimeError(f"Errore nel recupero dei log delle azioni amministrative: {str(e)}")

def log_admin_login_on_blockchain(username_admin, granted):
    """Registra un login amministrativo sulla blockchain"""
    try:
        nonce = web3.eth.get_transaction_count(OWNER_ADDRESS)

        txn = contract.functions.logAdminAccess(username_admin, granted).build_transaction({
            "from": OWNER_ADDRESS,
            "nonce": nonce,
            "gas": 200000,
            "gasPrice": web3.to_wei("10", "gwei")
        })

        signed_txn = web3.eth.account.sign_transaction(txn, PRIVATE_KEY)
        txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

        return txn_hash.hex()
    
    except Exception as e:
        raise RuntimeError(f"Errore blockchain (AdminLoginLog): {str(e)}")

def get_access_admin_logs():
    """Recupera tutti i log dei login amministrativi dalla blockchain"""
    try:
        admin_login_logs = contract.functions.getAllAdminLoginLogs().call()

        logs = []
        for log in admin_login_logs:
            logs.append({
                'username_admin': log[0],
                'granted': log[1],
                'timestamp': datetime.datetime.fromtimestamp(log[2], tz=ZoneInfo("UTC")).astimezone(ZoneInfo("Europe/Rome"))
            })

        return logs

    except Exception as e:
        raise RuntimeError(f"Errore nel recupero dei log dei login amministrativi: {str(e)}")

