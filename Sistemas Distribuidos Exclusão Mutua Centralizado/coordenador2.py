import socket
import threading
from time import sleep

class Barbeiro:
    def __init__(self, ip, porta, max_conexoes):
        self.ip = ip
        self.porta = porta
        self.max_conexoes = max_conexoes

        self.cabelo = []
        self.barba = []
        self.bigode = []

        self.processos = {}  # Processos conectados
        self.lock = threading.Lock()  # Lock para sincronização

    def iniciar(self):
        # Inicia a thread para receber conexões de processos
        thread_conexao = threading.Thread(target=self.aceitar_conexoes)
        thread_conexao.start()

        # Inicia a thread para executar o algoritmo de exclusão mútua
        thread_algoritmo = threading.Thread(target=self.executar_algoritmo)
        thread_algoritmo.start()

    def aceitar_conexoes(self):
        # Configura o socket servidor para aceitar conexões de processos
        socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_servidor.bind((self.ip, self.porta))
        socket_servidor.listen(self.max_conexoes)

        print("Aguardando conexões...")

        while True:
            # Aceita conexões e lida com processos
            socket_cliente, endereco = socket_servidor.accept()
            thread_processo = threading.Thread(target=self.lidar_processo, args=(socket_cliente,))
            thread_processo.start()

    def lidar_processo(self, socket_cliente):
        # Lida com um processo conectado
        id_processo = socket_cliente.recv(1024).decode()
        self.processos[id_processo] = socket_cliente  # Adiciona o processo ao dicionario de processos
        self.adicionar_a_fila_cabelo(id_processo)  # Adiciona o processo na fila "cabelos"
        # print("Processo", id_processo, "conectado.")
        print(f"Cliente {id_processo} esperando atendimento")

    def adicionar_a_fila_cabelo(self, id_processo):
        # Adicionar um processo ("cliente") na fila "cabelo"
        self.lock.acquire()
        self.cabelo.append(id_processo)
        self.lock.release()

    def adicionar_a_fila_barba(self, id_processo):
        # Adicionar um processo ("cliente") na fila "barba"
        self.lock.acquire()
        self.barba.append(id_processo)
        self.lock.release()
    
    def adicionar_a_fila_bigode(self, id_processo):
        # Adicionar um processo ("cliente") na fila "bigode"
        self.lock.acquire()
        self.bigode.append(id_processo)
        self.lock.release()

    def executar_algoritmo(self):
        # Executa o algoritmo de exclusão mútua centralizado
        while True:
            if self.cabelo:
                id_processo = self.cabelo[0]
                print(f"Acesso ao barbeiro concedido. Cliente {id_processo} cortou o cabelo")
                # sleep(3)
                self.cabelo.pop(0)
                print(f"Cliente {id_processo} terminou")
                self.adicionar_a_fila_barba(id_processo)

            if self.barba:
                id_processo = self.barba[0]
                print(f"Acesso ao barbeiro concedido. Cliente {id_processo} cortou a barba")
                # sleep(4)
                self.barba.pop(0)
                print(f"Cliente {id_processo} terminou")
                self.adicionar_a_fila_bigode(id_processo)

            if self.bigode:
                id_processo = self.bigode[0]
                print(f"Acesso ao barbeiro concedido. Cliente {id_processo} cortou o bigode")
                # sleep(5)
                self.bigode.pop(0)
                print(f"Cliente {id_processo} terminou")

    def enviar_mensagem(self, id_processo, mensagem):
        # Envia uma mensagem para um processo específico
        if id_processo in self.processos:
            socket_cliente = self.processos[id_processo]
            socket_cliente.send(mensagem.encode())

if __name__ == "__main__":
    barbeiro = Barbeiro("localhost", 5000, 10)
    barbeiro.iniciar()