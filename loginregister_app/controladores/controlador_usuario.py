from flask import render_template, request, redirect,session, flash
from loginregister_app import app
from loginregister_app.modelos.modelo_usuario import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt( app )

@app.route("/", methods=["GET"])
def index():
    session["islogged"] = False 
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def registrarUsuario():
    usuario ={
        "nombre":request.form["nombre"],
        "apellido":request.form["apellido"],
        "email":request.form["email"],
        "fecha_nacimiento":request.form["fecha_nacimiento"],
        "password":request.form["password"],
        "confirm_password":request.form["confirm_password"]
    }
    if(Usuario.validarRegistro(usuario)):
        listaDeCheckbox = request.form.getlist("terminos_condiciones")
        if(len(listaDeCheckbox)==0):
            flash("Debes aceptar los terminos y condiciones", "registro")
            return redirect("/")
        passwordEncriptado = bcrypt.generate_password_hash(request.form["password"])
        usuario["password"]=passwordEncriptado
        respuesta = Usuario.crearCuenta(usuario)
        print(respuesta)
        if(type(respuesta) is bool and not respuesta):
            flash("No se pudo lograr la conexión con la base de datos. Intente más tarde.","registro")
            return redirect("/")
        
        session["islogged"] = True 
        session["nombre"] = usuario["nombre"]
        return redirect("/dashboard")
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    passwordUsuario = request.form["password"]
    usuario ={
        "email":request.form["email"]
    }

    resultado = Usuario.verificaUsuario(usuario)

    if resultado == None:
        flash("El email proporcionado no es valido.", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(resultado.password,passwordUsuario):
        flash("La contraseña es incorrecta","login")
        return redirect("/")

    session["islogged"] = True 
    session["nombre"] = resultado.nombre
    return redirect("/dashboard")

@app.route("/dashboard", methods=["GET"])
def showDashboard():
    if(not session["islogged"]):
        return redirect("/")

    return render_template("usuario.html")

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/")
    
