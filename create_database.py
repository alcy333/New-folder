from app import create_app, db
from app.models import User, Product, Bid

app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
    # Create test user
    test_user = User(
        username='admin',
        email='admin@example.com'
    )
    test_user.set_password('admin123')
    db.session.add(test_user)
    db.session.commit()
    print("Test user created:", test_user)