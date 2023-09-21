from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return ('Chatterbox messages')

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    messages_serialized = [message.to_dict() for message in messages]
    return jsonify(messages_serialized)

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.json

    # Check if the required fields are present in the request JSON
    if 'body' not in data or 'username' not in data:
        return jsonify({'message': 'Missing required fields'}), 400

    # Create a new message and add it to the database
    message = Message(
        body=data['body'],
        username=data['username']
    )
    db.session.add(message)
    db.session.commit()

    # Return the newly created message as JSON
    return jsonify(message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)

    if message is None:
        return jsonify({'message': 'Message not found'}), 404

    data = request.json

    # Update the message body if it exists in the request JSON
    if 'body' in data:
        message.body = data['body']
        db.session.commit()

    # Return the updated message as JSON
    return jsonify(message.to_dict())

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)

    if message is None:
        return jsonify({'message': 'Message not found'}), 404

    # Delete the message from the database
    db.session.delete(message)
    db.session.commit()

    # Return a JSON message confirming the deletion
    return jsonify({'message': 'Message deleted successfully'})

if __name__ == '__main__':
    app.run(port=5555)
