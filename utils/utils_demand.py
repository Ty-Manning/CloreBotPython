import requests
import time
import re
from utils.gpu_crack_rates import gpu_crack_rates, blacklist


# Normalize the GPU name for matching, preserving key identifiers
def normalize_gpu_name(gpu_name):
    normalized_name = re.sub(r'[\s\-]', '', gpu_name.lower())
    normalized_name = re.sub(r'(ti|super|ada|xtx)', r' \1', normalized_name)
    normalized_name = re.sub(r'\s+', ' ', normalized_name).strip()
    return normalized_name

# Match the GPU model based on a flexible name search
def match_gpu_model(gpu_spec, gpu_crack_rates):
    normalized_spec = normalize_gpu_name(gpu_spec)
    for model, crack_rate in gpu_crack_rates.items():
        normalized_model = normalize_gpu_name(model)
        if normalized_model in normalized_spec:
            # Check for multiple GPUs in the format '3x NVIDIA GeForce RTX 3070'
            match = re.match(r'(\d+)x', gpu_spec)
            if match:
                num_gpus = int(match.group(1))
                crack_rate *= num_gpus
            return model, crack_rate
    return None, None

# Function to fetch marketplace data
def get_marketplace_data(api_token):
    url = "https://api.clore.ai/v1/marketplace"
    headers = {'auth': api_token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

# Function to find the best price based on crack rate and price criteria
def find_best_price(servers, max_price_per_mkeys):
    best_servers = []
    for server in servers:
        if not server['rented']:  # Filter out rented servers
            gpu_spec = server['specs']['gpu']
            if "laptop" in gpu_spec.lower():  # Filter out laptop GPUs
                continue
            if server['id'] in blacklist:  # Skip blacklisted servers
                continue
            price_on_demand = float(server['price']['on_demand']['bitcoin'])
            model, crack_rate = match_gpu_model(gpu_spec, gpu_crack_rates)
            if crack_rate:
                reduced_crack_rate = crack_rate * 1  # Apply 10% speed reduction for profit calculation
                price_per_mkeys_reduced = (price_on_demand / reduced_crack_rate) * 1000
                price_per_mkeys_normal = (price_on_demand / crack_rate) * 1000
                
                if price_per_mkeys_reduced <= max_price_per_mkeys:
                    best_servers.append({
                        "id": server['id'],
                        "price_per_mkeys_reduced": price_per_mkeys_reduced,
                        "price_per_mkeys_normal": price_per_mkeys_normal,
                        "gpu": gpu_spec,
                        "price_on_demand": price_on_demand,
                        "crack_rate": crack_rate
                    })
    # Sort servers by the lowest price per 1000 MKeys/sec (reduced)
    best_servers.sort(key=lambda x: x['price_per_mkeys_reduced'])
    return best_servers

# Function to create an order
def create_order(api_token, server_id, currency="bitcoin", order_type="on-demand", price=None):
    url = "https://api.clore.ai/v1/create_order"
    headers = {
        'auth': api_token,
        'Content-type': 'application/json'
    }
    data = {
        "currency": currency,
        "image": "cloreai/ubuntu20.04-jupyter", 
        "renting_server": server_id,
        "type": order_type,
        "ports":{
            "22":"tcp",
            "8888":"http"
        },
        "jupyter_token": "abc123abc",
        "ssh_password": "abc123abc",
    }
    if price:
        data["required_price"] = price
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# rent the three cheapest servers
def rent_three_cheapest(api_token, servers):
    cheapest_servers = servers[:3]  # Take the three cheapest servers
    for server in cheapest_servers:
        result = create_order(api_token, server['id'], price=server['price_on_demand'])
        if result['code'] == 0:
            print(f"Successfully rented server ID {server['id']} at {server['price_on_demand']} BTC")
        else:
            print(f"Unsuccessfully rented server ID {server['id']}")
