from app import create_app
from app.models import db, Product, Bid
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


app = create_app()


def check_expired_products():
    with app.app_context():
        expired_products = Product.query.filter(
            Product.end_time <= datetime.utcnow(),
            Product.is_sold == False
        ).all()


        for product in expired_products:
            highest_bid = product.bids.order_by(Bid.amount.desc()).first()
            if highest_bid:
                product.winner_id = highest_bid.user_id
                product.is_sold = True
                db.session.commit()


scheduler = BackgroundScheduler()
scheduler.add_job(func=check_expired_products, trigger='interval', minutes=1)
scheduler.start()
