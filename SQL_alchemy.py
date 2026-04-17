from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Compromisso(db.Model):
    __tablename__ = 'compromissos'
    
    id_compromisso = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(45),nullable=False)
    telefone = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    concluido = db.Column(db.Integer, default=0)

class Sessao(db.Model):
    __tablename__ = 'sessoes'
    
    telefone = db.Column(db.String(20), primary_key=True)
    estado = db.Column(db.Integer, default=1)
    nome_temp = db.Column(db.String(100))
    data_temp = db.Column(db.String(10))
    hora_temp = db.Column(db.String(5))