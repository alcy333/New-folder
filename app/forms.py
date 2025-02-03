from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Regexp

DAIRY_PRODUCTS = [
    ('Milk', 'Milk - Fresh whole milk'),
    ('Cheese', 'Cheese - Aged cheddar'),
    ('Butter', 'Butter - Unsalted premium butter'),
    ('Yogurt', 'Yogurt - Greek style yogurt'),
    ('Cream', 'Cream - Heavy whipping cream')
]

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="Username is required"),
        Length(min=4, max=25),
        Regexp(r'^\w+$', message="Only letters, numbers and underscores allowed")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Invalid email address"),
        Length(max=120)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required"),
        Length(min=8, message="Password must be at least 8 characters"),
        EqualTo('confirm_password', message="Passwords must match")
    ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Invalid email address")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required")
    ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ProductForm(FlaskForm):
    product_type = SelectField('Product Type', choices=DAIRY_PRODUCTS, validators=[
        DataRequired(message="Please select a product type")
    ])
    description = StringField('Product Description', validators=[
        DataRequired(message="Description is required"),
        Length(max=200)
    ])
    start_price = DecimalField('Start Price', places=2, validators=[
        DataRequired(message="Price is required"),
        NumberRange(min=0.01)
    ])
    weight = DecimalField('Weight (kg)', places=2, validators=[
        DataRequired(message="Weight is required"),
        NumberRange(min=0.1)
    ])
    submit = SubmitField('List Product')
    
class BidForm(FlaskForm):
    amount = DecimalField('Bid Amount', places=2, validators=[
        DataRequired(message="Bid amount is required"),
        NumberRange(min=0.01, message="Bid must be at least $0.01")
    ])
    submit = SubmitField('Place Bid')   