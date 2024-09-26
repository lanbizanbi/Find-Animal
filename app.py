from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'  # Pode ser um banco MySQL, PostgreSQL etc.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados
db = SQLAlchemy(app)

# Importar os modelos do arquivo models.py
from models import *

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/cadanimal')
def cadanimal():
    return render_template('cadanimal.html')

@app.route('/perfuser')
def perfuser():
    return render_template('perfuser.html')

if __name__ == '__main__':
    app.run(debug=True)
