# Use Python for this example with Flask to handle HTTP requests
from flask import Flask, request, jsonify
import pandas as pd
from google.cloud import storage

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Connect to Google Cloud Storage
    client = storage.Client()
    bucket = client.get_bucket('bucko107')
    blob = bucket.blob('gs://bucko107/Clean Data - Sheet1.csv')
    
    # Load the Excel file into a pandas DataFrame
    data = pd.read_excel(blob.open('rb'))

    # Extract query parameters
    query = request.json.get('query')
    filtered_data = data[data['Actor'].str.contains(query, case=False, na=False)]

    # Return the result as a JSON response
    return jsonify(filtered_data.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
