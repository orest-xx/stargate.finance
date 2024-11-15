import random
from typing import Optional, List

from settings import *


def get_balance_eth_arbitrum(address):
    return arbitrum_w3.eth.get_balance(address)


def get_balance_eth_optimism(address):
    return optimism_w3.eth.get_balance(address)


def get_balance_eth_base(address):
    return base_w3.eth.get_balance(address)


def get_balance_eth_linea(address):
    return linea_w3.eth.get_balance(address)


def get_router_and_provider(from_chain_name, to_chain_name):
    """
    Returns the appropriate Web3 provider and Stargate router contract for the swap,
    based on the chain names (arbitrum, optimism, base, linea).

    Args:
        from_chain_name (str): The name of the chain from which the ETH is being swapped (e.g., "arbitrum").
        to_chain_name (str): The name of the chain to which the ETH is being swapped (e.g., "optimism").

    Returns:
        tuple: (w3_provider, router_contract, router_eth_contract)
            containing the appropriate Web3 provider and router contracts for the swap.
    """
    # Chain-to-provider and router mappings
    chain_mapping = {
        "arbitrum": {
            "optimism": (arbitrum_w3, stargate_arbitrum_router_contract, stargate_arbitrum_router_eth_contract),
            "base": (arbitrum_w3, stargate_arbitrum_router_contract, stargate_arbitrum_router_eth_contract),
            "linea": (arbitrum_w3, stargate_arbitrum_router_contract, stargate_arbitrum_router_eth_contract),
        },
        "optimism": {
            "arbitrum": (optimism_w3, stargate_optimism_router_contract, stargate_optimism_router_eth_contract),
            "base": (optimism_w3, stargate_optimism_router_contract, stargate_optimism_router_eth_contract),
            "linea": (optimism_w3, stargate_optimism_router_contract, stargate_optimism_router_eth_contract),
        },
        "base": {
            "linea": (base_w3, stargate_base_router_contract, stargate_base_router_eth_contract),
            "arbitrum": (base_w3, stargate_base_router_contract, stargate_base_router_eth_contract),
            "optimism": (base_w3, stargate_base_router_contract, stargate_base_router_eth_contract),
        },
        "linea": {
            "optimism": (linea_w3, stargate_linea_router_contract, stargate_linea_router_eth_contract),
            "base": (linea_w3, stargate_linea_router_contract, stargate_linea_router_eth_contract),
            "arbitrum": (linea_w3, stargate_linea_router_contract, stargate_linea_router_eth_contract),
        }
    }

    # Ensure both from_chain_name and to_chain_name are valid
    if from_chain_name not in chain_mapping:
        raise ValueError(f"Unsupported source chain: {from_chain_name}")

    if to_chain_name not in chain_mapping[from_chain_name]:
        raise ValueError(f"Unsupported destination chain: {to_chain_name}")

    # Return the Web3 provider and router contracts based on the chain names
    return chain_mapping[from_chain_name][to_chain_name]


def swap_eth_generic(
        account,
        amount: int,
        from_chain,
        to_chain,
        fee_multiplier_range: Optional[List[float]],
        gas_limit_default: int = 2000000
) -> str:
    """
    General function to swap ETH on any Layer-2 network to another network.

    Args:
        account: The account object containing the address.
        amount: The amount of ETH to transfer.
        from_chain: The LayerZero chain ID of source network.
        to_chain: The LayerZero chain ID of dest network.
        fee_multiplier_range: Range for fee multiplier adjustment.

    Returns:
        The transaction hash of the swap.
    """

    # Get the appropriate provider and contracts based on the chain pair
    w3_provider, router_contract, router_eth_contract = get_router_and_provider(from_chain, to_chain)

    address = w3_provider.to_checksum_address(account.address)
    nonce = w3_provider.eth.get_transaction_count(address)

    # Get fee multiplier range from dict
    fee_multiplier_range = fee_multiplier_range or FEE_MULTIPLIER_RANGE.get(from_chain.lower(), [1.7, 1.9])

    # Get chains id from dict
    from_chain_id = CHAIN_IDS.get(from_chain.lower())
    to_chain_id = CHAIN_IDS.get(to_chain.lower())

    if not from_chain_id or not to_chain_id:
        raise ValueError(f"Invalid chain name provided: {from_chain} or {to_chain}")

    # Fetch fee from the Stargate router contract
    fees = router_contract.functions.quoteLayerZeroFee(
        to_chain_id, 1, address, "0x", [0, 0, address]
    ).call()
    fee = fees[0]

    # Adjust the amount based on the fee multiplier
    adjusted_amount = amount - int(fee * random.uniform(*fee_multiplier_range))

    if adjusted_amount <= 0:
        raise ValueError("Adjusted amount is too low after fee deduction")

    # Calculate minimum output amount after slippage
    amount_out_min = adjusted_amount - (adjusted_amount * SLIPPAGE) // 1000

    print(f"Fee: {fee}, Amount: {adjusted_amount}, AmountOutMin: {amount_out_min}")

    # Build the transaction
    swap_txn = router_eth_contract.functions.swapETH(
        to_chain_id, address, address, adjusted_amount, amount_out_min
    ).build_transaction({
        'from': address,
        'value': adjusted_amount + fee,
        'gas': 0,
        'gasPrice': 0,
        'nonce': nonce,
    })

    # Estimate gas and set gas limit with random multiplier
    try:
        gas_limit = w3_provider.eth.estimate_gas(swap_txn)
    except Exception as e:
        print(f"Gas estimation failed: {e}, using default gas limit.")
        gas_limit = gas_limit_default

    swap_txn['gas'] = int(gas_limit * random.uniform(gasLimitMultiplierMin, gasLimitMultiplierMax))

    # Set gas price with a slight increase
    gas_price = w3_provider.eth.gas_price
    swap_txn['gasPrice'] = int(gas_price * random.uniform(gasPriceMultiplierMin, gasPriceMultiplierMax))

    # Sign and send the transaction
    signed_swap_txn = w3_provider.eth.account.sign_transaction(swap_txn, account.key)
    swap_txn_hash = w3_provider.eth.send_raw_transaction(signed_swap_txn.rawTransaction)

    return swap_txn_hash
