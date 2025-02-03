from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.forms import ProductForm
from app.models import Product, db
from datetime import datetime, timedelta

products_bp = Blueprint('products', __name__)

@products_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            product_type=form.product_type.data,
            description=form.description.data,
            start_price=float(form.start_price.data),
            current_price=float(form.start_price.data),  # Initialize current_price
            weight=float(form.weight.data),
            seller_id=current_user.id,
            end_time=datetime.utcnow() + timedelta(minutes=30)
        )
        db.session.add(product)
        db.session.commit()
        flash('Product listed successfully!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('add_product.html', form=form)