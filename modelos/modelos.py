from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import datetime

db=SQLAlchemy()
now = datetime.datetime.utcnow

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)     # número identificador del usuario
    username = db.Column(db.String(50))              # cadena de caracteres sin espacios y caracteres especiales	nombre de usuario    
    email = db.Column(db.String(140))                # dirección de correo electrónico del usuario
    password = db.Column(db.String())                # password cifrado del usuario
    salt = db.Column(db.String)                      # sal para el cifrado del password leer
    token = db.Column(db.String)                     # valor en dólares de la oferta por llevar el paquete
    expireAt = db.Column(db.DateTime)                # fecha y hora de vencimiento del token
    createdAt = db.Column(db.DateTime, default=now)  # fecha de creación del 
    
class UsuariosSchema(SQLAlchemyAutoSchema):
    class Meta:
        model=Usuario
        include_relationships=True
        load_instance=True

    createdAt =fields.String()
