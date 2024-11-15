import time

from tqdm import tqdm
from web3 import Account
from bridge.eth_bridge import *


def main(tr):
    with open('wallets.txt', 'r') as f:
        accounts = [Account.from_key(line.replace("\n", "")) for line in f.readlines()]
    random.shuffle(accounts)
    for _ in range(0, tr):
        for account in accounts:
            # #case 1
            stargate_base_op(account)
            stargate_op_base(account)

            ##case2
            # stargate_arb_base(account)
            # stargate_base_op(account)

            sleep(10, 106)
        sleep_time = 100
        print(f"Sleeping {sleep_time} seconds for the next cycle")
        time.sleep(sleep_time)


def sleep(sleep_from: int, sleep_to: int):
    delay = random.randint(sleep_from, sleep_to)
    with tqdm(
            total=delay,
            desc="💤 Sleep",
            bar_format="{desc}: |{bar:20}| {percentage:.0f}% | {n_fmt}/{total_fmt}",
            colour="green"
    ) as pbar:
        for _ in range(delay):
            time.sleep(1)
            pbar.update(1)


# Generalized function for performing swaps
def perform_swap(account, get_balance_func, swap_func, min_amount, max_amount, balance_threshold, sleep_range,
                 network_from, network_to, link_template):
    try:
        balance = get_balance_func(account.address)
        random_amount = round(random.uniform(min_amount, max_amount), 5)
        amount = decimalToInt(balance, 18) - random_amount

        print(f"Account: {account.address}")
        print(f"Prepare Stargate swap from {network_from} to {network_to}")
        print(f"{network_from} balance: {decimalToInt(balance, 18)}, amount to send: {amount}")

        if balance > Web3.to_wei(balance_threshold, 'ether'):
            txn_hash = swap_func(account=account, amount=Web3.to_wei(amount, 'ether'), from_chain=network_from, to_chain=network_to)
            print(f"Waiting for the swap to complete on {network_to}...")
            time.sleep(random.randint(10, 30))
            print(f"Transaction: {link_template}{txn_hash.hex()}")
        else:
            print(f"{network_from} balance is too small for bridge.")

        rndm_time = random.randint(*sleep_range)
        print(f"Sleeping {rndm_time} seconds before the next account")
        time.sleep(rndm_time)

    except Exception as error:
        print(f'{error}', 'red')
        print(f'Retrying account: {account.address}')
        perform_swap(account, get_balance_func, swap_func, min_amount, max_amount, balance_threshold, sleep_range,
                     network_from, network_to, link_template)


# Wrapper functions for each swap type

def stargate_op_arb(account):
    min_amount = 0.005
    max_amount = 0.006
    balance_threshold = 0.005
    sleep_range = (10, 30)
    perform_swap(account, get_balance_eth_optimism, swap_eth_generic, min_amount, max_amount, balance_threshold,
                 sleep_range, "Optimism", "Arbitrum", "https://optimistic.etherscan.io/tx/")


def stargate_op_base(account):
    min_amount = 0.005
    max_amount = 0.006
    balance_threshold = 0.005
    sleep_range = (10, 30)
    perform_swap(account, get_balance_eth_optimism, swap_eth_generic, min_amount, max_amount, balance_threshold,
                 sleep_range, "Optimism", "Base", "https://optimistic.etherscan.io/tx/")


def stargate_op_linea(account):
    min_amount = 0.005
    max_amount = 0.006
    balance_threshold = 0.005
    sleep_range = (10, 30)
    perform_swap(account, get_balance_eth_optimism, swap_eth_generic, min_amount, max_amount, balance_threshold,
                 sleep_range, "Optimism", "Linea", "https://optimistic.etherscan.io/tx/")


def stargate_base_linea(account):
    min_amount = 0.0055
    max_amount = 0.0057
    balance_threshold = 0.005
    sleep_range = (20, 40)
    perform_swap(account, get_balance_eth_base, swap_eth_generic, min_amount, max_amount, balance_threshold,
                 sleep_range, "Base", "Linea", "https://basescan.org/tx/")


def stargate_base_op(account):
    min_amount = 0.00013
    max_amount = 0.00017
    balance_threshold = 0.0009
    sleep_range = (20, 40)
    perform_swap(account, get_balance_eth_base, swap_eth_generic, min_amount, max_amount, balance_threshold,
                 sleep_range, "Base", "Optimism", "https://basescan.org/tx/")


def stargate_base_arb(account):
    min_amount = 0.0055
    max_amount = 0.0058
    balance_threshold = 0.005
    sleep_range = (20, 40)
    perform_swap(account, get_balance_eth_base, swap_eth_generic, min_amount, max_amount, balance_threshold,
                 sleep_range, "Base", "Arbitrum", "https://basescan.org/tx/")


def stargate_linea_arb(account):
    min_amount = 0.005
    max_amount = 0.006
    balance_threshold = 0.005
    sleep_range = (20, 40)
    perform_swap(account, get_balance_eth_linea, swap_eth_generic, min_amount, max_amount, balance_threshold,
                 sleep_range, "Linea", "Arbitrum", "https://lineascan.build/tx/")


def stargate_linea_op(account):
    min_amount = 0.005
    max_amount = 0.006
    balance_threshold = 0.005
    sleep_range = (20, 40)
    perform_swap(account, get_balance_eth_linea, swap_eth_generic, min_amount, max_amount, balance_threshold,
                 sleep_range, "Linea", "Optimism", "https://lineascan.build/tx/")


def stargate_linea_base(account):
    min_amount = 0.005
    max_amount = 0.006
    balance_threshold = 0.005
    sleep_range = (20, 40)
    perform_swap(account, get_balance_eth_linea, swap_eth_generic, min_amount, max_amount, balance_threshold,
                 sleep_range, "Linea", "Base", "https://lineascan.build/tx/")


def stargate_arb_op(account):
    min_amount = 0.005
    max_amount = 0.006
    balance_threshold = 0.005
    sleep_range = (20, 40)
    perform_swap(account, get_balance_eth_arbitrum, swap_eth_generic, min_amount, max_amount,
                 balance_threshold,
                 sleep_range, "Arbitrum", "Optimism", "https://arbiscan.io/tx")


def stargate_arb_base(account):
    min_amount = 0.005
    max_amount = 0.006
    balance_threshold = 0.005
    sleep_range = (20, 40)
    perform_swap(account, get_balance_eth_arbitrum, swap_eth_generic, min_amount, max_amount, balance_threshold,
                 sleep_range, "Arbitrum", "Base", "https://arbiscan.io/tx")


def stargate_arb_linea(account):
    min_amount = 0.005
    max_amount = 0.006
    balance_threshold = 0.005
    sleep_range = (20, 40)
    perform_swap(account, get_balance_eth_arbitrum, swap_eth_generic, min_amount, max_amount, balance_threshold,
                 sleep_range, "Arbitrum", "Linea", "https://arbiscan.io/tx")


def decimalToInt(qty, decimal):
    return qty / int("".join((["1"] + ["0"] * decimal)))


def intToDecimal(qty, decimal):
    return int(qty * int("".join(["1"] + ["0"] * decimal)))


if __name__ == '__main__':
    total_rounds = 1
    main(total_rounds)
