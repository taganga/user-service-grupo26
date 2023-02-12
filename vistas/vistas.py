import flask_cors
from flask_restful import Resource
from modelos import db,Usuario,UsuariosSchema

from flask import request
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime 

from flask import jsonify, make_response
from flask import current_app
import json
import re
from flask_jwt_extended import jwt_required,create_access_token
from flask_jwt_extended import get_jwt,decode_token,get_current_user,get_jwt_identity
usuario_schema=UsuariosSchema()


class VistaUsuarios(Resource):
    
    def get(self):


        return  [usuario_schema.dumps(usuario) for usuario in Usuario.query.all()]
    
    def post(self):

        es_valida_peticion=False     

        if( (request.json.get("password", None) is None) or (request.json.get("username", None) is None) or (request.json.get("email", None)  is None) ):            
            response = current_app.response_class(response='peticion invalida',status=400, mimetype='application/text')            
            return response
        else:
            es_valido_email=False
            es_valido_username=False            
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
            #valida formato email
            if(re.search(regex,request.json['email'])):   
                es_valido_email=True
            else:   
                es_valido_email=False
            #valido formato username solo letras y numeros
            es_valido_username=request.json['username'].isalnum()
            if(es_valido_username and es_valido_email):
                usuario_existe=Usuario.query.filter(Usuario.username == request.json['username'] or Usuario.email == request.json['email'] ).first()
                if(usuario_existe is None):
                    #print("NO existe usuario")
                    es_valida_peticion=True
                else:
                    response = current_app.response_class(response='username o email ya registrados',status=412, mimetype='application/text')            
                    return response             
       
        if(es_valida_peticion):                             
            contrasena=request.json['password']
            temp=generate_password_hash(contrasena,'sha256',50)
            arrayResult=temp.split("$")
            salt=arrayResult[1]
            pass_cifrado=arrayResult[2]
            nuevo_usuario=Usuario(username=request.json['username'],email=request.json['email'],password=pass_cifrado,salt=temp,createdAt=datetime.now())
            db.session.add(nuevo_usuario)        
            db.session.commit()           

            result_json={
                "id":nuevo_usuario.id,
                "createdAt":nuevo_usuario.createdAt
            }
         
            response = current_app.response_class(
            response=json.dumps(result_json,default=str),
            status=201,
            mimetype='application/json'
            )           
            
            #print(check_password_hash(temp,contrasena))
            #print(check_password_hash(temp,"contrasena"))
            #print(check_password_hash("sha256$AMOE856niL9QgGsj81uXSfD4ZHTYB5JMKj5DFprmEkJOk8kvBD$f7fa07d3ad5c5cfa430527028c96b40435d385d05539ed945509bd73a27c1019","xcvvb"))
            return response
        else:
            response = current_app.response_class(response='peticion erronea...',status=500, mimetype='application/text')            
            return response             

    

class VistaUsuarioAutenticacion(Resource):
    #valida la autenticacion que username y password coincidan con lo almacenado en la base de datos
    def post(self):
        es_valida_peticion=False
        if( (request.json.get("password", None) is None  ) or (request.json.get("username", None) is None) ):        
            response = current_app.response_class(response='peticion invalida',status=400, mimetype='application/text')
            return response
        else:
            es_valida_peticion=True

            
        
        if(es_valida_peticion):
            user_name=request.json['username']
            contrasena=request.json['password']
            user_query=Usuario.query.filter(Usuario.username == user_name).first()
            if(user_query==None):            
                response = current_app.response_class(response='usuario no existe',status=404, mimetype='application/text')
                return response
            else:
                #usuario encontrado
                #print(user_query.salt)
                valido_password=check_password_hash(user_query.salt,contrasena)                
                if(valido_password):
                    token_de_acceso=create_access_token(identity=user_query.id,fresh=False)
                    result_json={"id":user_query.id, "expireAt":user_query.createdAt,"token":token_de_acceso }
                    response = current_app.response_class(
                        response=json.dumps(result_json,default=str),
                        status=200,
                        mimetype='application/json'
                    )                   

                    temp2=decode_token(token_de_acceso, None, True)                    
                    #print (json.dumps(temp2,default=str))
                    
                    fecha_expiracion_token=temp2["exp"]
                    user_query.token=token_de_acceso                
                    user_query.expireAt= datetime.fromtimestamp(fecha_expiracion_token)
                    db.session.commit()                      
                    return response
                    
                else:
                    #credenciales incorrectas
                    response = current_app.response_class(response='autenticacion invalida',status=404, mimetype='application/text')
                    return response
        else:
            #no existe alguno de los parametros
            response = current_app.response_class(response='peticion invalida',status=400, mimetype='application/text')
            return response

        

class VistaUsuarioMe(Resource):
    def get(self):
        
        headers = request.headers

        if( (request.headers is None) ):
            response = current_app.response_class(response="headers no existe",status=400,mimetype='application/text')
            return response
        
        if( headers.get('Authorization') is None ):
            response = current_app.response_class(response="Authorization no existe",status=400,mimetype='application/text')
            return response
        

        bearer = headers.get('Authorization')  # Bearer YourTokenHere
        if(bearer is not None):
            if(bearer.split()==[]):
                response = current_app.response_class(response="bearer no existe",status=400,mimetype='application/text')
                return response


            token = bearer.split()[1]  # YourTokenHere
            token_decode=decode_token(token, None, True)
            #print("token_decode->" + str(token_decode))
            id_usuario_token=token_decode["sub"]
            #exp viene en formato timespan 'numerico'
            #fecha_expiracion_timespan=token_decode["exp"]
            #fecha_expiracion_token=datetime.fromtimestamp(fecha_expiracion_timespan)
            usuario_token=Usuario.query.filter(Usuario.id == id_usuario_token).first()
            
            if(usuario_token is None):
                #usuario no existe
                response = current_app.response_class(response="idusuario de token no existe",status=401,mimetype='application/text')
            else:
                if(usuario_token.token==token):
                    #token enviado es el mimso almacenado en BD
                    fecha_expiracion_usuario=usuario_token.expireAt
                    dt_obj1 = datetime.strptime(str(fecha_expiracion_usuario), "%Y-%m-%d %H:%M:%S")
                    #dt_obj2 = datetime.strptime(str(fecha_expiracion_token), "%Y-%m-%d %H:%M:%S")
                    #print("fecha usuario:" + str(dt_obj1))
                    #print("fecha token:" + str(dt_obj1))
                    fecha_actual=datetime.strptime(str(datetime.now().isoformat(' ', 'seconds')), "%Y-%m-%d %H:%M:%S")
                    if(fecha_actual < dt_obj1):
                        #token vigente y valido
                        result_json={"id":usuario_token.id, "username":usuario_token.username,"email":usuario_token.email }
                        response = current_app.response_class(
                        response=json.dumps(result_json,default=str),
                        status=200,
                        mimetype='application/json'
                        )
                    else:
                        #token vencido
                        response = current_app.response_class(response="token vencido",status=401,mimetype='application/text')
                else:
                    #token enviado en el header no coincide con el de la base de datos
                    response = current_app.response_class(response="token no coincide",status=401,mimetype='application/text')
        else:
            #token no existe en el encabezado
            response = current_app.response_class(response="token no existe en encabezado",status=400,mimetype='application/text')

        return response
    
class VistaUsuarioSalud(Resource):
    def get(self):
        response = current_app.response_class(response='pong',status=200, mimetype='application/text')
        return response






             






    



     
            
            
