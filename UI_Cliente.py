import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox


class ClienteChat:
    def __init__(self, master):
        self.master = master
        self.master.title("Cliente de Chat")
        self.master.geometry("400x700")

        # Variables
        self.cliente_socket = None

        # Campo para ingresar la IP del servidor
        self.ip_label = tk.Label(master, text="IP del Servidor:")
        self.ip_label.pack(pady=5, anchor="w")

        self.ip_entry = tk.Entry(master)
        self.ip_entry.pack(pady=5, fill=tk.X)

        # Botón para conectarse al servidor
        self.connect_button = tk.Button(master, text="Conectar", command=self.conectar_servidor)
        self.connect_button.pack(pady=5, fill=tk.X)

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

    def conectar_servidor(self):
        server_ip = self.ip_entry.get()  # Obtener la IP del servidor de la entrada de texto
        port = 5000

        try:
            # Intentar conectarse al servidor
            self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.cliente_socket.connect((server_ip, port))

            # Enviar el nombre del equipo al servidor
            nombre_equipo = socket.gethostname()
            self.cliente_socket.send(nombre_equipo.encode("utf-8"))

            # Mostrar mensaje de conexión exitosa
            messagebox.showinfo("Conexión Exitosa", "Te has conectado al servidor correctamente.")

            # Iniciar un hilo para recibir mensajes
            threading.Thread(target=self.recibir_mensajes).start()
        except:
            # Mostrar mensaje de error si falla la conexión
            messagebox.showerror("Error de Conexión", "Servidor apagado o IP incorrecta.")
            return  # Salir de la función si la conexión falla

    def enviar_mensaje(self):
        mensaje = self.message_entry.get().strip()  # Obtener el mensaje escrito y eliminar espacios en blanco
        if mensaje == "":  # No enviar si el mensaje está vacío
            return

        self.message_entry.delete(0, tk.END)  # Limpiar la entrada de mensaje
        self.cliente_socket.send(mensaje.encode('utf-8'))  # Enviar el mensaje al servidor

        # Habilitar el área de texto para insertar mensaje y luego deshabilitarla de nuevo
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"Tú: {mensaje}\n")  # Mostrar el mensaje en el área de chat
        self.chat_area.config(state=tk.DISABLED)

        if mensaje == "exit":
            self.cliente_socket.close()

    def recibir_mensajes(self):
        while True:
            try:
                # Recibir mensaje del servidor
                data = self.cliente_socket.recv(1024).decode("utf-8")
                if data:
                    # Habilitar el área de texto para insertar mensaje y luego deshabilitarla de nuevo
                    self.chat_area.config(state=tk.NORMAL)
                    self.chat_area.insert(tk.END, f"Servidor: {data}\n")  # Mostrar mensaje recibido en el chat
                    self.chat_area.config(state=tk.DISABLED)
            except:
                break


# Ejecutar la interfaz del cliente
if __name__ == "__main__":
    root = tk.Tk()
    cliente_app = ClienteChat(root)
    root.mainloop()
