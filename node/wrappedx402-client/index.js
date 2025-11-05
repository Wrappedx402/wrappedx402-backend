import fetch from "node-fetch";

export async function request(endpoint, opts = {}) {
  const res = await fetch(endpoint, opts);
  if (res.status === 402) {
    const data = await res.json();
    const { x402 } = data;
    console.log("402 Payment Required:", x402);
    return { paymentRequired: true, x402 };
  }
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return await res.json();
}

export async function retry(endpoint, proof, nonce) {
  const res = await fetch(endpoint, {
    headers: {
      "x402-proof": proof,
      "x402-nonce": nonce,
    },
  });
  return await res.json();
}
