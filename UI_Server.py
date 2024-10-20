import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

class ServidorChat:
    def __init__(self, master):
        self.master = master
        self.master.title("Servidor de Chat")
        self.master.geometry("400x500")

        # Variables
        self.server_socket = None
        self.conn = None

        # Botón para iniciar el servidor
        self.start_button = tk.Button(master, text="Iniciar Servidor", command=self.iniciar_servidor)
        self.start_button.pack(pady=5, fill=tk.X)

        # Área de texto con scroll para mostrar el chat
        self.chat_area = scrolledtext.ScrolledText(master, wrap=tk.WORD)
        self.chat_area.pack(pady=10, fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)  # Deshabilitar la edición en el área de chat

        # Campo para escribir mensajes
        self.message_entry = tk.Entry(master)
        self.message_entry.pack(pady=5, fill=tk.X)

        # Botón para enviar mensaje
        self.send_button = tk.Button(master, text="Enviar", command=self.enviar_mensaje)
        self.send_button.pack(pady=5, fill=tk.X)

    def iniciar_servidor(self):
        host = '0.0.0.0'  # Escuchar en todas las interfaces
        port = 5000

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(1)

        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"Esperando conexiones en {host}:{port} ...\n")
        self.chat_area.config(state=tk.DISABLED)

        # Iniciar un hilo para aceptar conexiones
        threading.Thread(target=self.aceptar_conexion).start()

    def aceptar_conexion(self):
        self.conn, addr = self.server_socket.accept()
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"Conectado por {addr}\n")
        self.chat_area.config(state=tk.DISABLED)

        threading.Thread(target=self.recibir_mensajes).start()

    def enviar_mensaje(self):
        mensaje = self.message_entry.get().strip()  # Obtener el mensaje escrito y eliminar espacios en blanco
        if mensaje == "":  # No enviar si el mensaje está vacío
            return

        self.message_entry.delete(0, tk.END)  # Limpiar la entrada de mensaje
        self.conn.send(mensaje.encode('utf-8'))  # Enviar el mensaje al cliente

        # Habilitar el área de texto para insertar mensaje y luego deshabilitarla de nuevo
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"Tú: {mensaje}\n")  # Mostrar el mensaje en el área de chat
        self.chat_area.config(state=tk.DISABLED)

    def recibir_mensajes(self):
        while True:
            try:
                # Recibir mensaje del cliente
                data = self.conn.recv(1024).decode("utf-8")
                if data:
                    # Habilitar el área de texto para insertar mensaje y luego deshabilitarla de nuevo
                    self.chat_area.config(state=tk.NORMAL)
                    self.chat_area.insert(tk.END, f"Cliente: {data}\n")  # Mostrar mensaje recibido en el chat
                    self.chat_area.config(state=tk.DISABLED)
            except:
                break

# Ejecutar la interfaz del servidor
if __name__ == "__main__":
    root = tk.Tk()
    servidor_app = ServidorChat(root)
    root.mainloop()
