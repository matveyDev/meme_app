// eslint-disable-next-line no-unused-vars
import { Buffer } from 'buffer';
import {
  Connection,
  Transaction,
  SystemProgram,
  PublicKey,
  LAMPORTS_PER_SOL,
} from "@solana/web3.js";
import { useWalletStore } from '@/stores/walletStore';
import { API_URL } from '@/config';

const SOLANA_RPC_URL = "https://mainnet.helius-rpc.com/?api-key=820ceeb3-0336-4058-9108-56b9a327f079";
const RECIPIENT_WALLET = "EXfzSjYdnRVzEyCxrX4VXm46SAgiRRqSBf41SumPFpnX";
const AMOUNT_SOL = 0.001;

export async function unlockMore(generationStore) {
  let provider;

  const walletStore = useWalletStore();
  const walletType = walletStore.walletType;

  if (walletType === "phantom" && window.solana?.isPhantom) {
    provider = window.solana;
  } else if (walletType === "solflare" && window.solflare?.isSolflare) {
    provider = window.solflare;
  }

  if (!provider || !walletType) {
    alert("Wallet not found");
    return;
  }

  // подключение
  if (!provider.publicKey) {
    try {
      await provider.connect();
    } catch (err) {
      console.error("❌ Failed to connect wallet:", err);
      alert("Wallet not connected");
      return;
    }
  }

  const fromPubkey = provider.publicKey;
  const walletAddress = fromPubkey.toString();

  try {
    const connection = new Connection(SOLANA_RPC_URL);
    const recipient = new PublicKey(RECIPIENT_WALLET);

    const transaction = new Transaction().add(
      SystemProgram.transfer({
        fromPubkey,
        toPubkey: recipient,
        lamports: LAMPORTS_PER_SOL * AMOUNT_SOL,
      })
    );

    transaction.feePayer = fromPubkey;
    const { blockhash } = await connection.getLatestBlockhash();
    transaction.recentBlockhash = blockhash;

    let txid;

    if (walletType === "phantom") {
      const signedTx = await provider.signTransaction(transaction);
      txid = await connection.sendRawTransaction(signedTx.serialize());
    } else if (walletType === "solflare" && provider.signAndSendTransaction) {
      txid = await provider.signAndSendTransaction(transaction);
      txid = txid.signature;
    } else {
      alert("Unsupported wallet");
      return;
    }

    await connection.confirmTransaction(txid, "confirmed");
    console.log("✅ Payment sent, txid:", txid);

    const res = await fetch(`${API_URL}/unlock`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ walletAddress, txid }),
    });

    const data = await res.json();
    if (res.ok && data.success) {
      alert("🔥 Generations unlocked!");
      if (generationStore.refresh) await generationStore.refresh();
    } else {
      console.error("❌ Server error:", data);
      alert("Server did not confirm payment");
    }
  } catch (err) {
    console.error("💥 Error unlocking:", err);
    alert("❌ Payment failed");
  }
}
