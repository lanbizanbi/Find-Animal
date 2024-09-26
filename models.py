from app import db 

class User(db.model):
    id = db.Column(db.Interger, primary_key = true)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))