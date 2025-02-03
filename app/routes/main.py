from flask import Blueprint, render_template
from flask_login import current_user, login_required
from app.models import Product
from datetime import datetime
from app.forms import BidForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    active_products = Product.query.filter(
        Product.end_time > datetime.utcnow(),
        Product.is_sold == False
    ).order_by(Product.end_time.asc()).all()
    return render_template('index.html', products=active_products)

@main_bp.route('/dashboard')
@login_required
def dashboard():
    user_products = current_user.products.all()
    user_bids = current_user.bids.join(Product).filter(
        Product.is_sold == False
    ).all()
    return render_template('user.html', 
                         products=user_products,
                         bids=user_bids)

@main_bp.route('/product/<int:product_id>')
def product_details(product_id):
    product = Product.query.get_or_404(product_id)
    form = BidForm()  # Create form instance
    return render_template('product_details.html', 
                         product=product,
                         form=form)  # Pass form to template