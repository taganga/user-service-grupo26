import os
from flask import Flask
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_jwt_extended import get_jwt
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from modelos import db
from vistas.vistas import VistaUsuarios, VistaUsuarioAutenticacion, VistaUsuarioMe, VistaUsuarioSalud


app = Flask(__name__)
# db_connection_string = os.environ['DB_CONNECTION_STRING']
#db_name = os.environ['DB_NAME']
#db_host = os.environ['DB_HOST']
#db_port = os.environ['DB_PORT']
#db_user = os.environ['DB_USER']
#db_password =os.environ['DB_PASSWORD']

db_connection_string ='postgresql://postgres:admin123@localhost:5432/userdb'# f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

app.config['SQLALCHEMY_DATABASE_URI'] = db_connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = 'frase-secreta'

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)

api =Api(app)
api.add_resource(VistaUsuarios,'/users')
api.add_resource(VistaUsuarioAutenticacion,'/users/auth')
api.add_resource(VistaUsuarioMe,'/users/me')
api.add_resource(VistaUsuarioSalud,'/users/ping')
jwt = JWTManager(app)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4000))
    app.run(debug=True, host='0.0.0.0', port=port)




       