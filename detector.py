from datetime import datetime

def registrar_respuestas(usuario):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("respuestas.log", "a", encoding="utf-8") as archivo:
        archivo.write(f"{fecha},USUARIO_BLOQUEADO,{usuario}\n")
        return fecha

intentos = {}

with open("eventos.log", "r", encoding="utf-8") as archivo:
    for linea in archivo:
        fecha, tipo, usuario = linea.strip().split(",")

        if tipo == "Intento fallido de inicio de sesión":
            if usuario not in intentos:
                intentos[usuario] =[]
            
            intentos[usuario].append(fecha)

for usuario, registros in intentos.items():

    if len(registros) >= 3:

        print("ALERTA DE SEGURIDAD")
        print("Usuario:", usuario)
        print("Número de intentos fallidos:", len(registros))
        print("Primer intento fallido:", registros[0])
        print("Último intento fallido:", registros[-1])
        print("Detección de múltiples intentos fallidos de inicio de sesión.", registros[2])

        fecha_respuesta = registrar_respuestas(usuario)
        
        inicio =datetime.strptime(registros[0], "%Y-%m-%d %H:%M:%S")
        deteccion = datetime.strptime(registros[2], "%Y-%m-%d %H:%M:%S")
        respuesta = datetime.strptime(fecha_respuesta, "%Y-%m-%d %H:%M:%S")

        mttr= (respuesta - deteccion).total_seconds()
        print("MTTR:", mttr, "Segundos")

        mttd= (deteccion - inicio).total_seconds()
        print("MTTD:", mttd, "Segundos")

        print("Accion aplicada: bloqueo de usuario:", usuario)
        print("Respuesta:", fecha_respuesta)