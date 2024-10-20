import socket


"""
def run_cliente():
    # conectarnos al server
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect(('localhost', 8000))
    print("Conectado al servidor!")

    while True:
        #enviar mensaje
        message = input("Mensaje: ")
        cliente_socket .send(message.encode('utf-8'))

        if message == 'exit':
            break

        # recibir la respuesta del server
        responses = cliente_socket.recv(1024).decode('utf-8')
        print("Servidor", responses)


    cliente_socket.close()

if __name__ == '__main__':
    run_cliente()
    
"""

# Datos del servidor (IP y Puerto)
server_ip = input("Introduzca la IP del Servidor: ")
port = 5000

# Crear el socket
cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Conectar al servidor
cliente_socket.connect((server_ip, port))

# Obtener el nombre del equipo
nombre_equipo = socket.gethostname()

# Enviar nombre del equipo al servidor
cliente_socket.send(nombre_equipo.encode("utf-8"))

# Bucle para enviar y recibir mensajes
while True:
    message = input(f"{nombre_equipo}: ")
    cliente_socket.send(message.encode("utf-8"))

    data = cliente_socket.recv(1024).decode("utf-8")
    print(f"Servidor: {data}")

    if message == "exit":
        break

cliente_socket.close()