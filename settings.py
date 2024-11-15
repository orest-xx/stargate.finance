import json
from web3 import Web3
from web3.auto import w3

# enter slippage as shown => 1 = 0.1%, 5 = 0.5%, 10 = 1%
SLIPPAGE = 5

# L0 chains constants
CHAIN_IDS = {
    "arbitrum": 110,
    "optimism": 111,
    "base": 184,
    "linea": 183,
}

# params for multipliers
FEE_MULTIPLIER_RANGE = {
    "arbitrum": [1.7, 1.9],
    "optimism": [1.7, 1.9],
    "base": [1.3, 1.7],
    "linea": [1.3, 1.7],
}

gasLimitMultiplierMin = 1.3
gasLimitMultiplierMax = 1.7

gasPriceMultiplierMin = 1.2
gasPriceMultiplierMax = 1.3

# ABIs
router_abi = json.load(open('./abis/router_abi.json'))
router_eth_abi = json.load(open('./abis/router_eth_abi.json'))

# RPCs
arbitrum_rpc_url = 'https://rpc.ankr.com/arbitrum/'
optimism_rpc_url = 'https://rpc.ankr.com/optimism/'
base_rpc_url = 'https://rpc.ankr.com/base/'
linea_rpc_url = 'https://rpc.ankr.com/linea/'

# Web3 instances for different networks
arbitrum_w3 = Web3(Web3.HTTPProvider(arbitrum_rpc_url))
optimism_w3 = Web3(Web3.HTTPProvider(optimism_rpc_url))
base_w3 = Web3(Web3.HTTPProvider(base_rpc_url))
linea_w3 = Web3(Web3.HTTPProvider(linea_rpc_url))

# Stargate Router
stargate_arbitrum_address = w3.to_checksum_address('0x53Bf833A5d6c4ddA888F69c22C88C9f356a41614')
stargate_optimism_address = w3.to_checksum_address('0xB0D502E938ed5f4df2E681fE6E419ff29631d62b')
stargate_base_address = w3.to_checksum_address('0x45f1A95A4D3f3836523F5c83673c797f4d4d263B')
stargate_linea_address = w3.to_checksum_address('0x2F6F07CDcf3588944Bf4C42aC74ff24bF56e7590')

# Stargate ETH Router
stargate_arbitrum_eth_address = w3.to_checksum_address('0xbf22f0f184bCcbeA268dF387a49fF5238dD23E40')
stargate_optimism_eth_address = w3.to_checksum_address('0xB49c4e680174E331CB0A7fF3Ab58afC9738d5F8b')
stargate_base_eth_address = w3.to_checksum_address('0x50b6ebc2103bfec165949cc946d739d5650d7ae4')
stargate_linea_eth_address = w3.to_checksum_address('0x8731d54e9d02c286767d56ac03e8037c07e01e98')

# Initialize the Stargate Router Contracts
stargate_arbitrum_router_contract = arbitrum_w3.eth.contract(address=stargate_arbitrum_address, abi=router_abi)
stargate_optimism_router_contract = optimism_w3.eth.contract(address=stargate_optimism_address, abi=router_abi)
stargate_base_router_contract = base_w3.eth.contract(address=stargate_base_address, abi=router_abi)
stargate_linea_router_contract = base_w3.eth.contract(address=stargate_linea_address, abi=router_abi)

# Initialize the Stargate ETH Router Contracts
stargate_arbitrum_router_eth_contract = arbitrum_w3.eth.contract(address=stargate_arbitrum_eth_address, abi=router_eth_abi)
stargate_optimism_router_eth_contract = optimism_w3.eth.contract(address=stargate_optimism_eth_address, abi=router_eth_abi)
stargate_base_router_eth_contract = base_w3.eth.contract(address=stargate_base_eth_address, abi=router_eth_abi)
stargate_linea_router_eth_contract = base_w3.eth.contract(address=stargate_linea_eth_address, abi=router_eth_abi)

print("Stargate contracts initialized successfully.")