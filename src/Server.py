import multiprocessing
import socket
import sys
import random
import aiofiles
import asyncio


questions = {}  # dicionário que recebe a quantidade de questões que seriam
right = 0  # armazena a quantidade de acertos, por questão
wrong = 0  # armazena a quantidade de erro por questão


async def writeStatistics() -> None:
    """
    Escreve em um arquivo, as estatísticas
    da atividade.Número de acertos e erros
    por questão.
    :return:
    """
    async with aiofiles.open('../response/estatistica.txt', 'w') as statistic:
        for k, v in questions.items():
            await statistic.write('')  # apaga o que tiver
            await statistic.writelines(f"Questao {k}) acertos={v[0]} e erros={v[1]}.\n")


def verify(sock, message, gabarito, host, port) -> dict:
    global questions
    global right
    global wrong
    """
    Verifica as respostas
    :param sock:
    :param message: mensagem enviada pelo cliente
    :param host: ip cliente
    :param port: porta cliente
    :param gabarito:
    :return: dict Métricas da resposta
    """
    k = message.split(';')[0].strip()
    v = message.split(';')[2].strip()
    message = {k: v} # dicionario formado pela questao e resposta do cliente
    try:
        print(f"[*] Conectado ao cliente: {host} na porta {port}")
        print(f"[*] Questões recebidas:")
        for k, v in message.items():
            print(f"[*] Questão {k}= resposta: {v}")
        print("[*] Processando...")
        # compara a resposta com a de chegada pelo cliente
        count = 0
        correct = 0
        error = 0
        itemX, itemV = 0, 0
        for key, value in message.items():
            for question in value:  # para cada questao, verifica se acertou ou não
                if question.lower() == str(gabarito[count]).lower():
                    correct += 1
                else:
                    error += 1
                count += 1
            right += correct
            wrong += error

            if len(questions) > 0 and questions.get(key) is not None:
                itemV = int(questions.get(key)[0])
                itemX = int(questions.get(key)[1])
            questions[key] = [right + itemV, wrong + itemX]   # armazena no dicionario global, o número de acertos e
            # erros por questão
            right, wrong = 0, 0
            message[key] = f"Questão {key}: {correct} corretas e {error} incorretas" # cada questão, armazena o numero de erros e acertos
        asyncio.run(writeStatistics())  # escreve, de forma assíncrona, no arquivo a estatística geral.
        return message
    except KeyboardInterrupt as e:
        sock.sendto(f"fim {e}".encode(), (host, port))  # envia resposta de erro para o cliente nao ficar esperando
        sys.exit(0)
    except AttributeError as e:
        sock.sendto(f"erro {e}".encode(), (host, port))  # envia resposta de erro para o cliente nao ficar esperando
        sys.exit(0)


class Server:
    """
    Servidor que fará as correções da
    prova, com base no gabarito, e a
    enviará para o cliente.
    """
    def __init__(self, host: str, port: int) -> None:
        """
        Inicializa servidor
        :param host: ip deste servidor (str)
        :param port: porta para este servidor (int)
        """
        self.__host = host
        self.__port = port
        self.response = {}

    # métodos get para manter o encapsulamento
    @property
    def host(self) -> str:
        return self.__host

    @property
    def port(self) -> int:
        return self.__port

    def __readGaba(self, lenght) -> None:
        """
        Método PRIVADO gera um gabarito randomicamente
        :param: lenght => tamanho da quantidade de questoes
        :return: str
        """
        possible = ['V', 'F']
        gabarito = random.choices(possible, k=int(lenght))
        print(f"\n[*] GABARITO GERADO: {''.join(str(i) for i in gabarito)}")
        self.response = ''.join(str(i) for i in gabarito)  # converte de lista para string o array randomico gerado

    def connectToClient(self) -> None:
        """
        Método PÚBLICO que conecta ao cliente
        :return:
        """
        print(f"[*] Iniciando o servidor ip: {self.host} port: {self.port}")
        print("[*] Para encerrar, a qualquer momento, precione ctrl + break, em seu teclado.")
        print("[*] Ao finalizar, verifique no diretório 'response' o arquivo gerado")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        sock.bind((self.host, self.port))
        sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # permite reutilizar o ip
        content = []
        cores = multiprocessing.cpu_count()
        for n in range(cores):  # 6 cores na maquina
            self.__threadForMultipleConn(sock, content)  # inicializa threads

    def __threadForMultipleConn(self, sock, content) -> None:
        """
        Cria thread para permitir múltiplas conexões
        :param sock: (socket)
        :param content (list)
        :return:
        """
        address = ''
        try:
            while True:
                try:
                    message, address = sock.recvfrom(65535)  # mensagem e endereco do cliente (maximo de mtu)
                    for item in message.decode().replace('[', '').replace(']', '').replace('\'', '').split(','):
                        lenght = item.split(";")[1]  # quantidade de questoes
                        self.__readGaba(lenght)  # gera um gabarito para este tamanho
                        content.append(verify(sock, item, self.response, address[0], address[1])) # armazena dados a enviar
                    break  # sai do loop para enviar os dados ao cliente
                except Exception as e:
                    print(e)
                    print("Valor inválido.")
                    print("Finalizando...")
                    sock.sendto("Valor inválido".encode(), address)
                    sys.exit(0)
            print("[*] Enviando correção para o cliente")
            sock.sendto(str(content).encode(), address)  # envia a resposta
            print("[*] Enviado")
            content.clear()  # limpa lista na memória
        except KeyboardInterrupt:
            print("Concluído")
            sock.sendto(str(content).encode(), address)  # envia a resposta para o cliente não ficar em espera
            asyncio.run(writeStatistics())  # escreve, de forma assíncrona, no arquivo a estatística geral.
            sys.exit(0)


if __name__ == '__main__':
    server = Server('localhost', 30000)
    server.connectToClient()

