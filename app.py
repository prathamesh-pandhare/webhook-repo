from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://sampleuser:sample1234@cluster0.gbpkmib.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["githubEvents"]
collection = db["events"]

# Format GitHub timestamp to readable format
def format_time(ts):
    dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
    return dt.strftime("%d %B %Y - %I:%M %p UTC")

# Home page with frontend UI
@app.route('/')
def home():
    return render_template('index.html')

# Webhook endpoint to receive GitHub events
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event = request.headers.get('X-GitHub-Event')

    try:
        if event == 'push':
            author = data['pusher']['name']
            to_branch = data['ref'].split('/')[-1]
            timestamp = data['head_commit']['timestamp']
            msg = f'{author} pushed to {to_branch} on {format_time(timestamp)}'

        elif event == 'pull_request':
            pr = data['pull_request']
            author = pr['user']['login']
            from_branch = pr['head']['ref']
            to_branch = pr['base']['ref']
            timestamp = pr['created_at']
            msg = f'{author} submitted a pull request from {from_branch} to {to_branch} on {format_time(timestamp)}'

            # Bonus: check if PR was merged
            if data['action'] == 'closed' and pr['merged']:
                timestamp = pr['merged_at']
                msg = f'{author} merged branch {from_branch} to {to_branch} on {format_time(timestamp)}'

        else:
            return jsonify({'message': 'Ignored event'}), 200

        # Store event in MongoDB
        collection.insert_one({"message": msg, "timestamp": datetime.utcnow()})
        return jsonify({'message': 'Success'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to get the latest 10 events for the UI
@app.route('/latest', methods=['GET'])
def latest():
    data = collection.find().sort("timestamp", -1).limit(10)
    return jsonify([{"message": d["message"]} for d in data])

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
