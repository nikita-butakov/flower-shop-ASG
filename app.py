import boto3
import json
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

s3 = boto3.client('s3', region_name='ca-central-1')
cloudwatch = boto3.client('cloudwatch', region_name='ca-central-1')
BUCKET_NAME = 'flower-shop-frontend-shoppng-online'

def put_order_metric():
    cloudwatch.put_metric_data(
        Namespace='FlowerShop',
        MetricData=[
            {
                'MetricName': 'OrderCount',
                'Value': 1,
                'Unit': 'Count'
            },
        ]
    )

@app.route('/')
def health():
    return 'OK', 200

@app.route('/order', methods=['POST', 'GET'])
def order():
    if request.method == 'POST':
        data = request.json
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S')
        filename = f'orders/order-{timestamp}.json'
        
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body=json.dumps(data),
            ContentType='application/json'
        )
        
        put_order_metric()  # Send metrics to CloudWatch
        
        print("Order saved to S3:", filename)
        return jsonify({"message": "Order received"}), 200
    else:
        return 'Order endpoint OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

