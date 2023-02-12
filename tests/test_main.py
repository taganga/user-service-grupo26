import json
from unittest import TestCase
from faker import Faker
from faker.generator import random
from app import app
import random
import time
from modelos.modelos import db

class UserTestCase(TestCase):

    def setUp(self):
        self.data_factory = Faker()
        self.client = app.test_client()

    def test_CreateUser(self):      
        username= self.data_factory.word()
        password=self.data_factory.password()
        email=self.data_factory.email()      
        login = {
                        "username": username,
                        "password": password,
                        "email": email, 
                        #"size":random.choice(size_list), 
                        #"fragile": 1,
                        #"offer": self.data_factory.pyfloat(left_digits=4, right_digits=2, positive=True),
                        }
        solicitud_validar_login = self.client.post("/users",
                                                    data=json.dumps(
                                                        login),
                                                    headers={'Content-Type': 'application/json'})
        self.assertEqual(solicitud_validar_login.status_code, 201)



    def test_CreateUserUserNameExistente(self):      
        username= self.data_factory.word()
        password=self.data_factory.word()
        email=self.data_factory.email()
       
        login = {
                        "username": username,
                        "password": password,
                        "email": email, 

                        }
        solicitud_validar_login = self.client.post("/users",
                                                    data=json.dumps(
                                                        login),
                                                    headers={'Content-Type': 'application/json'})
        
        solicitud_validar_login2 = self.client.post("/users",
                                                    data=json.dumps(
                                                        login),
                                                    headers={'Content-Type': 'application/json'})
        
        self.assertEqual(solicitud_validar_login2.status_code, 412)
        
     




    def test_CreateToken(self):

        username= self.data_factory.word()
        password=self.data_factory.word()
        email=self.data_factory.email()
       
        login = {
                        "username": username,
                        "password": password,
                        "email": email, 

                        }
        solicitud_validar_login = self.client.post("/users",
                                                    data=json.dumps(
                                                        login),
                                                    headers={'Content-Type': 'application/json'})   
       
        login = {
                        "username": username,
                        "password": password,                       
                        
                        }
        solicitud_validar_login = self.client.post("/users/auth",
                                                    data=json.dumps(
                                                        login),
                                                    headers={'Content-Type': 'application/json'})
        self.assertEqual(solicitud_validar_login.status_code, 200)





    def test_InvalidateAuthentication(self):
        username= self.data_factory.word()
        password=self.data_factory.word()        
        login = {
                        "username": username,
                        "password": password,                       
                        
                        }
        solicitud_validar_login = self.client.post("/users/auth",
                                                    data=json.dumps(
                                                        login),
                                                    headers={'Content-Type': 'application/json'})
        self.assertEqual(solicitud_validar_login.status_code, 404)  


    def test_ValidatePing(self):
     
        solicitud_validar_login = self.client.get("/users/ping",
                                                    headers={'Content-Type': 'application/json'})
        self.assertEqual(solicitud_validar_login.status_code, 200)


    def test_ValidateInvalidateTokenUserMe(self):
        token ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc2MDAyOTA1LCJqdGkiOiIwMWEwNTc0My1jODRhLTQ1MWQtYTE1Zi1jNWZhZDMwMmZmMmUiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjo5OCwibmJmIjoxNjc2MDAyOTA1LCJleHAiOjE2NzYwMDM4MDV9.HsmCMGiXwLy7vRRezWd-I9Wyv8Ol_FHsiNRvNw4ry-g"
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(token)}                   
        solicitud_validar_login = self.client.get("/users/me",                                                
                                                    headers=headers)
        self.assertEqual(solicitud_validar_login.status_code, 401)

    

    def test_ValidateMissingTokenTokenUserMe(self):
        token ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjc2MDAyOTA1LCJqdGkiOiIwMWEwNTc0My1jODRhLTQ1MWQtYTE1Zi1jNWZhZDMwMmZmMmUiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjo5OCwibmJmIjoxNjc2MDAyOTA1LCJleHAiOjE2NzYwMDM4MDV9.HsmCMGiXwLy7vRRezWd-I9Wyv8Ol_FHsiNRvNw4ry-g"
        headers = {'Content-Type': 'application/json', "Authorization": ""}                   
        solicitud_validar_login = self.client.get("/users/me",                                                
                                                    headers=headers)
        self.assertEqual(solicitud_validar_login.status_code, 400)




    def test_ValidateUserMe(self):

        username= self.data_factory.word()
        password=self.data_factory.word()
        email=self.data_factory.email()
       
        login = {
                        "username": username,
                        "password": password,
                        "email": email, 

                        }
        solicitud_validar_login = self.client.post("/users",
                                                    data=json.dumps(
                                                        login),
                                                    headers={'Content-Type': 'application/json'})   
       
        login = {
                        "username": username,
                        "password": password,                       
                        
                        }
        solicitud_validar_login = self.client.post("/users/auth",
                                                    data=json.dumps(
                                                        login),
                                                    headers={'Content-Type': 'application/json'})
        

        respuesta_al_autenticarse = json.loads(solicitud_validar_login.get_data())
        token = respuesta_al_autenticarse['token']        
        headers = {'Content-Type': 'application/json', "Authorization": "Bearer {}".format(token)}                   
        solicitud_validar_login = self.client.get("/users/me",                                                
                                                    headers=headers)
        self.assertEqual(solicitud_validar_login.status_code, 200)    




        







   