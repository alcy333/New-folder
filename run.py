from app import create_app, socketio

app = create_app()

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_ECHO'] = True  # Show SQL queries
    socketio.run(app)