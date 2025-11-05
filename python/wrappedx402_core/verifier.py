import time, base64, hashlib
from dataclasses import dataclass
from typing import Optional

@dataclass
class X402Proof:
    receiver: str
    amount: float
    ttl: int
    nonce: str
    signature: str
    tx: Optional[str] = None

class X402Verifier:
    def __init__(self, rpc_url="https://api.mainnet-beta.solana.com", min_amount=0.001):
        self.rpc_url = rpc_url
        self.min_amount = min_amount

    def verify(self, proof: X402Proof):
        if not proof.signature or not proof.nonce:
            raise ValueError("Missing signature or nonce")
        if proof.amount < self.min_amount:
            raise ValueError("Underpaid amount")
        if proof.ttl < int(time.time()):
            raise ValueError("TTL expired")
        # hash nonce + signature for anti-replay
        h = hashlib.sha256(f"{proof.nonce}:{proof.signature}".encode()).hexdigest()
        return {"verified": True, "hash": h, "receiver": proof.receiver, "amount": proof.amount}
