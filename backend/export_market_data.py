import requests
import csv
from datetime import datetime, timedelta

def export_market_data_to_csv(coin_id, vs_currency='usd', start_date=None, days=None, precision='full'):
    # Calculate the end date based on the start date and number of days
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = start_date + timedelta(days=days) if days else datetime.now()
    else:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days) if days else end_date - timedelta(days=365)

    # Convert start_date and end_date to UNIX timestamps
    start_timestamp = int(start_date.timestamp()) if start_date else None
    end_timestamp = int(end_date.timestamp())

    # Initialize the CSV file
    filename = f'{coin_id}_market_data.csv'
    csv_headers = ['Date', 'Price', 'Total Volume', 'Market Cap']

    # Make API request for market data
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range?vs_currency={vs_currency}&from={start_timestamp}&to={end_timestamp}&precision={precision}'
    response = requests.get(url)
    
    if response.status_code == 200:
        market_data = response.json()
        prices = market_data['prices']
        total_volumes = market_data['total_volumes']
        market_caps = market_data['market_caps']

        # Prepare the data for CSV
        data = []
        for i in range(len(prices)):
            timestamp = datetime.fromtimestamp(prices[i][0] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            price = prices[i][1]
            total_volume = total_volumes[i][1]
            market_cap = market_caps[i][1]
            data.append([timestamp, price, total_volume, market_cap])

        # Write the data to CSV file
        with open(filename, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(csv_headers)
            writer.writerows(data)

        print(f"Market data for {coin_id.upper()} has been exported to {filename}.")
    else:
        print("Failed to retrieve market data.")

# Example usage
export_market_data_to_csv(coin_id='ethereum', start_date="2022-01-01", days=500, precision='full')
