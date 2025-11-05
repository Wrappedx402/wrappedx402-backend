from langchain.callbacks.base import BaseCallbackHandler
from wrappedx402_core.verifier import X402Verifier, X402Proof

class WrappedX402CallbackHandler(BaseCallbackHandler):
    def __init__(self, receiver:str, amount:float):
        self.verifier = X402Verifier()
        self.receiver = receiver
        self.amount = amount

    def on_chain_start(self, serialized, inputs, **kwargs):
        print(f"[x402] Chain started for {self.receiver} — {self.amount} SOL")

    def on_llm_end(self, response, **kwargs):
        print("[x402] Payment verified & response delivered.")

    def verify_payment(self, proof:X402Proof):
        return self.verifier.verify(proof)
