import crypto from "crypto";

export class X402Verifier {
  constructor({ minAmount = 0.001 } = {}) {
    this.minAmount = minAmount;
  }

  verify({ receiver, amount, ttl, nonce, signature }) {
    if (!signature || !nonce) throw new Error("Missing signature/nonce");
    if (amount < this.minAmount) throw new Error("Underpaid");
    if (ttl < Date.now() / 1000) throw new Error("TTL expired");
    const hash = crypto.createHash("sha256").update(`${nonce}:${signature}`).digest("hex");
    return { verified: true, hash, receiver, amount };
  }
}
