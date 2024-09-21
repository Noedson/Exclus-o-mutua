import socket
import time
import threading

class Processo:
    def __init__(self, id_processo, ip_coordenador, porta_coordenador, tamanho_mensagem):
        self.id_processo = id_processo
        self.ip_coordenador = ip_coordenador
        self.porta_coordenador = porta_coordenador
        self.tamanho_mensagem = tamanho_mensagem

    def iniciar(self, repeticoes, k):
        for _ in range(repeticoes):
            # Solicita a secao critica
            self.solicitar_atendimento()
            # Entra na secao critica
            self.iniciar_atendimento()
            # Aguarda um tempo determinado (k)
            time.sleep(k)
            # Sai da secao critica
            self.finalizar_atendimento()

    def solicitar_atendimento(self):
        # Cria a mensagem de solicitacao da secao critica
        # mensagem = f"1|{self.id_processo}|".ljust(self.tamanho_mensagem, '0')
        mensagem = f"{self.id_processo}".ljust(self.tamanho_mensagem, '0')
        # Envia a mensagem para o coordenador
        self.enviar_mensagem(mensagem)

    def enviar_mensagem(self, mensagem):
        # Cria um socket cliente
        socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Conecta ao IP e porta do coordenador
        socket_cliente.connect((self.ip_coordenador, self.porta_coordenador))
        # Envia a mensagem para o coordenador
        socket_cliente.sendall(mensagem.encode())
        # Fecha a conexão do socket
        socket_cliente.close()

    def iniciar_atendimento(self):
        # Abre o arquivo em modo de escrita e anexa os resultados
        with open("resultado.txt", "a") as arquivo:
            # Obtém a hora atual formatada
            hora_atual = time.strftime("%Y/%m/%d %H:%M:%S")
            # Escreve no arquivo que o processo entrou na secao critica
            arquivo.write(f"Processo {self.id_processo} entrou na seção crítica às {hora_atual}\n")

    def finalizar_atendimento(self):
        # Abre o arquivo em modo de escrita e anexa os resultados
        with open("resultado.txt", "a") as arquivo:
            # Obtem a hora atual formatada
            hora_atual = time.strftime("%Y/%m/%d %H:%M:%S")
            # Escreve no arquivo que o processo saiu da secao critica
            arquivo.write(f"Processo {self.id_processo} saiu da seção crítica às {hora_atual}\n")

if __name__ == "__main__":
    # Solicita ao usuario os valores de entrada
    # num_processos = int(input("Digite o número de processos: "))
    num_processos = 5
    # repeticoes = int(input("Digite o número de repetições: "))
    repeticoes = 20
    # k = int(input("Digite o valor de k (em segundos): "))
    k = 1
    # tamanho_mensagem = int(input("Digite o tamanho fixo das mensagens (em bytes): "))
    tamanho_mensagem = 1

    processos = []

    for i in range(num_processos):
        # Cria um ID para cada processo
        id_processo = str(i + 1)
        # Cria uma instancia do processo com os parametros fornecidos
        processo = Processo(id_processo, "localhost", 5000, tamanho_mensagem)
        # Adiciona o processo na lista de processos
        processos.append(processo)

    threads = []

    for processo in processos:
        # Cria uma thread para cada processo, chamando o metodo iniciar
        thread = threading.Thread(target=processo.iniciar, args=(repeticoes, k))
        # Inicia a thread
        thread.start()
        # Adiciona a thread na lista de threads
        threads.append(thread)

    for thread in threads:
        # Espera todas as threads terminarem
        thread.join()