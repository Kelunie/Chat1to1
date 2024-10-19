import socket
import threading
# headdecks


def handle_cliente(cliente_socket, cliente_address):
    while True:
        try:
            # Recibe datos del cliente
            data = cliente_socket.recv(1024).decode('utf-8')
            print(f"Cliente {cliente_address}:\n {data}")

            if data == "exit":
                break

            # Enviar una respuesta al cliente
            responses = input("respuesta:\n ")
            cliente_socket.send(responses.encode('utf-8'))
        except Exception as e:
            raise e

    # se cierra la conexion con el cliente
    cliente_socket.close()

def runServer():
    # configurar el servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8000))
    server_socket.listen(3)
    print('Servidor iniciando. Esperando conexiones...')


    while True:
        #aceptar una conexion
        cliente_socket, cliente_address = server_socket.accept()
        print(f"Conexión establecida con {cliente_address}")

        # hile para manejar el cliente
        cliente_hilo = threading.Thread(target=handle_cliente, args=(cliente_socket, cliente_address))
        cliente_hilo.start()


if __name__ == '__main__':
    runServer()