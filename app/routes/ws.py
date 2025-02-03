from flask import Blueprint
from flask_socketio import emit
from app import socketio

ws_bp = Blueprint('ws', __name__)

@socketio.on('connect')
def handle_connect():
    emit('connection', {'status': 'Connected'})

def notify_bid_update(product_id, new_price):
    socketio.emit('bid_update', {
        'product_id': product_id,
        'new_price': new_price
    })