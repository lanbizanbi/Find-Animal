import logging
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configurações do Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'almondega'

# Configuração para uploads
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite de 16MB para uploads

# Configuração de logging
logging.basicConfig(
    level=logging.DEBUG,  
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_url = db.Column(db.String(256))  # URL da imagem do post
    user = db.relationship('User', back_populates='posts')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
    
User.posts = db.relationship('Post', back_populates='user', lazy=True)

def allowed_file(filename):
    """Verifica se o arquivo tem uma extensão permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        app.logger.info(f"Tentando fazer login com o email: {email}")

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('home'))
        else:
            app.logger.warning(f"Falha no login para o email: {email}")
            flash('Email ou senha inválido.', 'error')
            return render_template('login.html')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Verifica duplicação de usuário ou email
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Nome de usuário ou email já cadastrado', 'error')
            return redirect(url_for('register'))

        # Cria o novo usuário e adiciona ao banco de dados
        new_user = User(username=username, email=email)
        new_user.set_password(password)  
        db.session.add(new_user)
        db.session.commit()

        flash('Cadastro realizado com sucesso! Por favor, faça login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        content = request.form['content']
        image = request.files.get('image') 

        image_url = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_url)

        if content:
            new_post = Post(content=content, user_id=session['user_id'], image_url=image_url)
            db.session.add(new_post)
            db.session.commit()
            flash('Postagem realizada com sucesso!', 'success')
            return redirect(url_for('home'))
    
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('home.html', posts=posts)
@app.route('/cadanimal')
def cadanimal():
    return render_template('cadanimal.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None) 
    return jsonify({'success': True})

@app.route('/perfuser')
def perfuser():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    user = User.query.get(user_id)
    
    return render_template('perfuser.html', user=user)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)