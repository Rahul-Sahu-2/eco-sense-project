from web3 import Web3
from backend.config import RPC_URL, PRIVATE_KEY, CONTRACT_ADDRESS

_w3 = None
_contract = None
_account = None

CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "user", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "rewardUser",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    }
]


def _init():
    global _w3, _contract, _account
    if _w3 is None:
        _w3 = Web3(Web3.HTTPProvider(RPC_URL))
        _account = _w3.eth.account.from_key(PRIVATE_KEY)
        _contract = _w3.eth.contract(
            address=Web3.to_checksum_address(CONTRACT_ADDRESS),
            abi=CONTRACT_ABI,
        )


def calculate_tokens(waste_confidence: float) -> int:
    if waste_confidence >= 80:
        return 5
    elif waste_confidence >= 60:
        return 3
    elif waste_confidence >= 40:
        return 1
    return 0


def reward_user(user_wallet: str, amount: int) -> str:
    """Send reward tokens via the smart contract. Returns tx hash or error."""
    try:
        _init()
        user_wallet = Web3.to_checksum_address(user_wallet)
        nonce = _w3.eth.get_transaction_count(_account.address)

        tx = _contract.functions.rewardUser(user_wallet, amount).build_transaction({
            "from": _account.address,
            "nonce": nonce,
            "gas": 300000,
            "gasPrice": _w3.to_wei(35, "gwei"),
            "chainId": 80002,
        })

        signed_tx = _w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = _w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        return _w3.to_hex(tx_hash)
    except Exception as e:
        return f"Error: {e}"


def is_valid_address(address: str) -> bool:
    return Web3.is_address(address)
