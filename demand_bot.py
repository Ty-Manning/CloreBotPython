from utils.utils_demand import get_marketplace_data, find_best_price, rent_three_cheapest
from utils.api_key import API_KEY

# usage
api_token = API_KEY
marketplace_data = get_marketplace_data(api_token)

if marketplace_data:
    servers = marketplace_data.get('servers', [])
    print(f"Found {len(servers)} servers on the marketplace.")
    best_servers = find_best_price(servers, 0.00000500)
    print(f"Found {len(best_servers)} servers matching the criteria.")
    for server in best_servers:
        # Format the prices to show full decimal notation
        formatted_price_per_mkeys_reduced = "{:.10f}".format(server['price_per_mkeys_reduced'])
        formatted_price_per_mkeys_normal = "{:.10f}".format(server['price_per_mkeys_normal'])
        formatted_price_on_demand = "{:.10f}".format(server['price_on_demand'])
        print(f"Server ID: {server['id']}, GPU: {server['gpu']}, Expected Crack Rate: {server['crack_rate']} MKeys/sec, "
              f"Price per 1000 MKeys/sec (Normal): {formatted_price_per_mkeys_normal} BTC, "
              f"Price on Demand: {formatted_price_on_demand} BTC")
    
    # Rent the three cheapest servers
    rent_three_cheapest(api_token, best_servers)
