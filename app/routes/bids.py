from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import current_user, login_required
from app import db
from app.models import Bid, Product
from app.forms import BidForm
from app.routes.ws import notify_bid_update

bids_bp = Blueprint('bids', __name__)

@bids_bp.route('/product/<int:product_id>/bid', methods=['POST'])
@login_required
def place_bid(product_id):
    product = Product.query.get_or_404(product_id)
    form = BidForm()
    
    if form.validate_on_submit():
        try:
            bid_amount = float(form.amount.data)
            
            if current_user.id == product.seller_id:
                return jsonify({'error': 'Cannot bid on your own product'}), 403
                
            if bid_amount <= product.current_price:
                return jsonify({'error': 'Bid must be higher than current price'}), 400
            
            # Create new bid
            new_bid = Bid(
                amount=bid_amount,
                product_id=product_id,
                user_id=current_user.id
            )
            
            # Update product current price
            product.current_price = bid_amount
            
            db.session.add(new_bid)
            db.session.commit()
            
            notify_bid_update(product_id, bid_amount)
            return jsonify({
                'success': True,
                'new_price': f"{bid_amount:.2f}",
                'message': 'Bid placed successfully!'
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid form submission'}), 400

@bids_bp.route('/suggest_bid/<int:product_id>')
def suggest_bid(product_id):
    product = Product.query.get_or_404(product_id)
    suggested = float(product.current_price) + 10.0
    return jsonify({'suggested': suggested})