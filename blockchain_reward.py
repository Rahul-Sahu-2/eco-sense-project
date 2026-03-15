from web3 import Web3
import os
from dotenv import load_dotenv

# .env file load
load_dotenv()

RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# Web3 connection
w3 = Web3(Web3.HTTPProvider(RPC_URL))

account = w3.eth.account.from_key(PRIVATE_KEY)

# Smart Contract ABI
contract_abi = [
    {
        "inputs": [
            {"internalType": "address", "name": "user", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"}
        ],
        "name": "rewardUser",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=contract_abi
)


def reward_user(user_wallet, amount):

    user_wallet = Web3.to_checksum_address(user_wallet)

    nonce = w3.eth.get_transaction_count(account.address)

    tx = contract.functions.rewardUser(
        user_wallet,
        amount
    ).build_transaction({
        "from": account.address,
        "nonce": nonce,
        "gas": 300000,
        "gasPrice": w3.to_wei(35, "gwei"),  # polygon ke liye safe
        "chainId": 80002
    })

    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)

    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    return w3.to_hex(tx_hash)