---
Current repo is only for a learning purpose, review and test before use!

Interact with LayerZero stargate bridge to transfer ETH across LayerZero supported chains


---

# Multi-Chain ETH Swap via Stargate

This repository provides a Python implementation for swapping ETH between multiple Layer 2 networks using the **Stargate Protocol**. The solution allows users to seamlessly transfer ETH across popular Ethereum scaling solutions, including **Arbitrum**, **Optimism**, **Base**, and **Linea**. This functionality is based on the LayerZero protocol and uses Stargate's routers to facilitate cross-chain transactions.

## Key Features:
- **Cross-Chain ETH Swaps**: Swap ETH between Layer 2 networks like Arbitrum, Optimism, Base, and Linea with a single function call.
- **Automated Fee Calculation**: Automatically fetches and adjusts fees based on the LayerZero protocol, ensuring efficient transfers with dynamic fee multipliers.
- **Transaction Customization**: Supports fee and gas adjustments, enabling fine-grained control over transaction parameters such as slippage, gas prices, and gas limits.
- **Universal Swap Function**: Consolidates the logic for swapping ETH across multiple chains into a single generic function, making it easy to integrate and scale for different networks.

## Supported Networks:
- **Arbitrum**
- **Optimism**
- **Base**
- **Linea**

## How It Works:
The code defines **Stargate router contracts** for each supported Layer 2 network and provides functions to swap ETH from one network to another.
- A generic `swap_eth_generic` function is used for ETH swaps, taking parameters such as the sender's account, amount, source and destination networks, and necessary contract information.
- **Fee calculation** is done by interacting with the Stargate router's `quoteLayerZeroFee` function, ensuring accurate cross-chain transfer costs.
- The **gas and transaction management** is handled with automatic gas estimation and gas price adjustment to optimize performance.

## Example Usage:

```python

# Example: Swap ETH from Arbitrum to Optimism
account = Account(private_key="your_private_key_here")
amount = 1 * 10**18  # 1 ETH in Wei
from_chain = "arbitrum"
to_chain = "optimism"

swap_txn_hash = swap_eth_generic(
    account=account,
    amount=amount,
    from_chain=from_chain,
    to_chain=to_chain
)

print(f"Transaction Hash: {swap_txn_hash.hex()}")

```

<h3> How to </h3>
you need python 3.10 version (https://www.python.org/downloads/ )

```
git clone <current repo>

cd stargate.finance

pip install -r requirements.txt
# or (depends on python and pip versions)
pip3 install -r requirements.txt

# edit main method in main.py to configure which module to run
python main.py
or 
python3 main.py
```

1) To configure please edit next:
   - settings.py 

---
Contribution:
Feel free to fork this repository and submit pull requests. Contributions are always welcome! Please ensure your code follows the existing structure, and include tests for any new features or bug fixes.

Steps to Contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request describing the changes you made.

License:
This project is licensed under the MIT License - see the LICENSE file for details.

