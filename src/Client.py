import socket
import time

import colorama


class Client:
    """
    Cliente UDP que envia a prova a ser
    corrigida pelo servidor.
    """
    def __init__(self, server_ip: str, port: int) -> None:
        """
        Inicializa um cliente
        :param server_ip: IP do servidor (str)
        :param port: porta do servidor (str)
        """
        self.__server = server_ip
        self.__port = port

    # métodos get para manter encapsulamento.
    @property
    def server(self) -> str:
        return self.__server

    @property
    def port(self) -> int:
        return self.__port

    # métodos públicos com funcionalidades
    def connect(self) -> None:
        """
        Conecta ao servidor e solicita a mensagem a
        ser enviada.
        :return: None
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # soquete UDP
        data = []
        while True:
            try: # interação com o usuário
                amount = int(input("Quantidade de questões: "))
                for n in range(amount): # salva no vetor as respostas
                    data.append(input("Insira: <número da questão>; <numero alternativas>; <resposta> ").strip())
                break
            except ValueError:  # trata entradas inválidas
                print("Valor inválido")
        print("[*] Enviando prova...")
        sock.sendto(str(data).encode(), (self.server, self.port))  # envia os dados ao servidor
        # recebe os dados do servidor:
        try:
            time.sleep(1)
            response, address = sock.recvfrom(65535)  # resposta do servidor, quantidade de bytes do mtu da rede
            time.sleep(1)
            print("[*] Aguardando a correção...")
            time.sleep(1)
            print("[*] O servidor respondeu:")
            print('-' * 50)
            for index, data in enumerate(response.decode().replace('[', '').replace(']', '').replace('{', '').replace('}', '').split(',')):
                data = response.decode().replace('[', '').replace(']', '').replace('{', '').replace('}', '').split(',')[index]
                print(f"{data.strip().split(':')[1]} )" + f"{data.strip().split(':')[2]}")
            print('-' * 50)
            print("[*] Encerrando a conexão.")
        except ConnectionResetError:
            print("[*] [ERROR] Inicie o servidor primeiro")
        finally:
            sock.close()  # fecha a conexão para encerrar o processo


if __name__ == '__main__':
    client = Client("localhost", 30000)  # ip 0.0.0.0 permite qualquer dispositivo na rede, conecte à rede interna
    client.connect()
