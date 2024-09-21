# Bitcoin Puzzle Search with Clore.ai Marketplace

This project is a Python program that interacts with the [Clore.ai](https://clore.ai) marketplace API to find and rent machines for performing Bitcoin puzzle searches. The program searches for machines with GPUs capable of cracking private keys at high speeds, optimizing for a specified profit factor.

## Features

- **Marketplace Search**: Uses Clore.ai's API to search for machines in the marketplace based on GPU crack rates and rental prices.
- **Customizable**: Allows users to modify which machines are blacklisted and specify custom crack speeds for any GPU model.
- **Profit Optimization**: The program rents machines that offer the highest profitability based on a user-defined profit value.
- **Multiple Machine Renting**: By default, the program rents the three cheapest servers that meet the required profitability factor.
- **Editable Settings**: Most program behavior can be adjusted by editing a few key files.

## Getting Started

### Prerequisites

- Python 3.8+
- `requests` Python package (can be installed with `pip install requests`)

### Installation

1. Clone this repository

2. Install the required dependencies:

3. Add your Clore API key:
   - Edit the file called `api_key.py` and include your API key as follows:
     ```python
     API_KEY = "your_clore_api_key_here"
     ```

## File Overview

### `gpu_crack_rates.py`

This file contains a table of GPUs along with their cracking speeds (in billion keys per second) for Bitcoin puzzles. It also includes a blacklist of servers that are known to perform poorly. You can edit this file to:

- Add new GPU models.
- Adjust the cracking speeds of existing GPUs.
- Modify the blacklist to skip over specific servers.

### `api_key.py`

This file contains your Clore API key, which is required for the program to interact with Clore.ai's marketplace. **Make sure to add your API key before running the program.**

### `demand_boy.py`

This file is the main entry point of the program. It interacts with the Clore.ai API, finds available servers, and rents the ones that meet your profit factor.

- Modify the profit factor by adjusting the following line:
  ```python
  best_servers = find_best_price(servers, 0.00000500)
  ```
  The profit factor is specified in Bitcoin per 1000 million keys per second (BK/s). Adjust this value as needed.

### `utils_demand.py`

This file contains additional utility functions that handle machine sorting, filtering, and rental logic. By default, the program:

- Rents the **three cheapest** servers that meet the profit criteria.
- **Skips all laptop GPUs** by default.
- Uses default Jupyter and SSH keys (`abc123abc`) for machine access. **It's strongly recommended to change these keys** before renting machines.

To modify this behavior, you can edit the corresponding sections of `utils_demand.py`.

## Default Behavior

- The program rents the three cheapest servers that meet your profit factor.
- Machines with laptop GPUs are skipped by default.
- Jupyter and SSH keys are set to `abc123abc` (please change these before running the program).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
