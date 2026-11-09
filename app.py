#Importacion de librerias
from flask import Flask, render_template, request

#Importacion para la base de datos
import sqlite3 
#Importacion para la seguridad de contraseñas
import re 
from werkzeug.security import generate_password_hash, check_password_hash

#Para el manejo de fechas y horas
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def inicio( ):
    return "Laboratorio de Ciberseguridad"

def validar_usuario(usuario):
    # Validar que el nombre de usuario tenga al menos 4 y max 20 caracteres y solo contenga letras, números y guiones bajos
    return re.fullmatch(r'[A-Za-z0-9_]{4,20}', usuario) is not None
    
def validar_correo(correo):
    # Validar que el correo tenga un formato válido
    return re.fullmatch(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", correo) is not None

def validar_contraseña(password):
    # Validar que la contraseña tenga al menos 8 caracteres
    return len(password) >=8 is not None

def registrar_evento(tipo, usuario):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("eventos.log", "a", encoding="utf-8") as archivo:
        archivo.write(f"{fecha},{tipo},{usuario}\n")

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form.get("usuario").strip()
        correo = request.form.get("correo").strip()
        password = request.form.get("password", "")

        if not validar_usuario(usuario):
            return"Usuario inválido."
        if not validar_correo(correo):
            return "Correo electrónico inválido."
        if not validar_contraseña(password):
            return "Contraseña inválida. Debe tener al menos 8 caracteres."
        

        conexion = sqlite3.connect('usuarios.db')
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT id FROM usuarios WHERE usuario = ? OR correo = ?", 
            (usuario,correo)
            )

        existente = cursor.fetchone()

        if existente:
            conexion.close()
            return "El usuario o correo ya existe."

        password_hash = generate_password_hash(password)

        cursor.execute("INSERT INTO usuarios (usuario, correo, password) VALUES (?, ?, ?)",
                       (usuario, correo, password_hash)
                       )
                       
        conexion.commit()
        conexion.close()
        return "Usuario registrado."

    return render_template ("registro.html")

@app.route("/login", methods=["GET", "POST"])
def login(): 
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]

        conexion = sqlite3.connect('usuarios.db')
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE usuario = ?", 
            (usuario,)
        )

        resultado = cursor.fetchone()
        
        conexion.close()

        if resultado and check_password_hash(resultado[3], password):
            registrar_evento("Inicio de sesión", usuario)
            return "Inicio de sesión exitoso."
        else:
            registrar_evento("Intento fallido de inicio de sesión", usuario)
            return "Credenciales incorrectas."

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)    