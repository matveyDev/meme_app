from solana.rpc.api import Client

SOLANA_RPC_URL = "https://mainnet.helius-rpc.com/?api-key=820ceeb3-0336-4058-9108-56b9a327f079"
RECEIVING_WALLET = "EXfzSjYdnRVzEyCxrX4VXm46SAgiRRqSBf41SumPFpnX"
EXPECTED_AMOUNT_SOL = 0.001

client = Client(SOLANA_RPC_URL)
