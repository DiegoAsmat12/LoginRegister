from flask import flash
from loginregister_app.config.mysqlconnection import MySQLConnection, connectToMySQL
import re
from datetime import datetime
EXP_EMAIL = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
EXP_PASSWORD = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')
EXP_NOMBRE_APELLIDO = re.compile( r'^[A-Z][a-zA-z]+$' )

class Usuario:
    def __init__(self, id, nombre, apellido, email, fecha_nacimiento, password, created_at, updated_at):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.fecha_nacimiento = fecha_nacimiento
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def crearCuenta(self, usuario:dict):
        query = '''
                    INSERT INTO usuarios(nombre,apellido,email,fecha_nacimiento,password,created_at,updated_at)
                    VALUES (%(nombre)s,%(apellido)s,%(email)s,%(fecha_nacimiento)s,%(password)s, NOW(), NOW())
                '''
        resultado = connectToMySQL("esquema_login_registro").query_db(query, usuario)

        return resultado

    @classmethod
    def verificaUsuario(cls, usuario:dict):
        query = '''
                    SELECT * 
                    FROM usuarios
                    WHERE email=%(email)s;
                '''
        resultado = connectToMySQL("esquema_login_registro").query_db(query,usuario)
        if(len(resultado)>0):
            usuarioResultado = Usuario ( resultado[0]["id"], resultado[0]["nombre"],
            resultado[0]["apellido"], resultado[0]["email"], 
            resultado[0]["fecha_nacimiento"], resultado[0]["password"],
            resultado[0]["created_at"], resultado[0]["updated_at"])
            return usuarioResultado
        else:
            return None

    

    @staticmethod
    def validarRegistro(usuario):
        isValid = True
        usuarioEmail = {
            "email": usuario["email"]
        }
        usuarioAComparar = Usuario.verificaUsuario(usuarioEmail)
        if(len(usuario["nombre"])<3):
            flash("El nombre debe tener almenos tres caracteres.","registro")
            isValid=False
        if(not EXP_NOMBRE_APELLIDO.match(usuario["nombre"])):
            flash("El nombre solo puede estar compuesto por letras.","registro")
            isValid=False
        if(len(usuario["apellido"])<3):
            flash("El apellido debe tener almenos tres caracteres.","registro")
            isValid=False
        if(not EXP_NOMBRE_APELLIDO.match(usuario["apellido"])):
            flash("El nombre solo puede estar compuesto por letras.","registro")
            isValid=False
        if(not EXP_EMAIL.match(usuario["email"])):
            flash("Correo no valido.","registro")
            isValid=False
        if(usuarioAComparar!=None):
            flash("El email proporcionado ya existe.","registro")
            isValid=False
        if(not EXP_PASSWORD.match(usuario["password"])):
            flash("La contraseña debe tener almenos 8 caracteres, 1 mayúscula, 1 minúscula y un número.","registro")
            isValid=False
        if(usuario["password"] != usuario["confirm_password"]):
            flash("Has ingresado dos contraseñas diferentes.", "registro")
            isValid=False
        if(len(usuario["fecha_nacimiento"])>3):
            fechaNacimiento = datetime.strptime(usuario["fecha_nacimiento"],'%Y-%m-%d')
            fechaHoy = datetime.now()
            edad = fechaHoy.year - fechaNacimiento.year
            if((fechaHoy.month, fechaHoy.day)<(fechaNacimiento.month,fechaNacimiento.day)):
                edad-=1
            if(edad<=10):
                flash("Usted es muy menor para estar aquí.", "registro")
                isValid=False
        else:
            flash("Registre una fecha valida.", "registro")
            isValid=False
        return isValid
    
    