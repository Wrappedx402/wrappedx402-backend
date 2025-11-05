from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from wrappedx402_core.verifier import X402Verifier, X402Proof
from wrappedx402_core.utils import generate_nonce, ttl

class X402Middleware:
    def __init__(self, app, receiver:str, amount:float):
        self.app = app
        self.receiver = receiver
        self.amount = amount
        self.verifier = X402Verifier()

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        headers = dict(request.headers)
        proof = headers.get("x402-proof")
        nonce = headers.get("x402-nonce")

        if not proof or not nonce:
            # return 402 Payment Required
            content = {
                "x402": {
                    "receiver": self.receiver,
                    "amount": f"{self.amount} SOL",
                    "ttl": ttl(180),
                    "nonce": generate_nonce(),
                }
            }
            res = JSONResponse(content, status_code=402)
            await res(scope, receive, send)
            return

        try:
            verified = self.verifier.verify(X402Proof(
                receiver=self.receiver,
                amount=self.amount,
                ttl=ttl(0)+180,
                nonce=nonce,
                signature=proof
            ))
            scope["x402_verified"] = verified
        except Exception as e:
            raise HTTPException(status_code=403, detail=str(e))

        await self.app(scope, receive, send)
