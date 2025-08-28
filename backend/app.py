from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdb.db'  # Change as needed
db = SQLAlchemy(app)
CORS(app)

# Import your models
from app.driver import Driver

@app.route('/')
def home():
    return "Backend is running!"

if __name__ == '__main__':
    app.run(debug=True)