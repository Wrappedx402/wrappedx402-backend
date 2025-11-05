import { X402Verifier } from "wrappedx402-core";
import crypto from "crypto";

export function x402Middleware({ receiver, amount }) {
  const verifier = new X402Verifier({ minAmount: amount });

  return async (req, res, next) => {
    const proof = req.headers["x402-proof"];
    const nonce = req.headers["x402-nonce"];

    if (!proof || !nonce) {
      const payload = {
        x402: {
          receiver,
          amount: `${amount} SOL`,
          ttl: Math.floor(Date.now() / 1000) + 180,
          nonce: crypto.randomBytes(16).toString("hex"),
        },
      };
      return res.status(402).json(payload);
    }

    try {
      const verified = verifier.verify({
        receiver,
        amount,
        ttl: Math.floor(Date.now() / 1000) + 180,
        nonce,
        signature: proof,
      });
      req.x402_verified = verified;
      next();
    } catch (err) {
      return res.status(403).json({ error: err.message });
    }
  };
}
