from flask import Flask
from routes.owner import register_bp
from routes.public import register_public_bp

app = Flask(__name__)
app.register_blueprint(register_bp)
app.register_blueprint(register_public_bp)
app.secret_key = 'your_secret_key'  # Change this in production!

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    