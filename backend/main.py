from flask import Flask, jsonify
from flask_cors import CORS

import requests

app = Flask(__name__)

@app.route('/fetch_data', methods=['GET'])
def fetch_data():
    api_key = 'UktsMJkMx2Sjz1TycHZ0N8JQyRzCuC1X'
    url = f"https://api.dune.com/api/v1/query/2654450/results?api_key={api_key}"
    
    try:
        response = requests.get(url)
        data = response.json()
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    
CORS(app, support_credentials=True)

if __name__ == '__main__':
    app.run(debug=True)