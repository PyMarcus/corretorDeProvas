import sys
from Client import Client
from Server import Server


if __name__ == '__main__':
    """
    Por padrão, está implementado o ip 0.0.0.0
    e a porta 9000
    """
    try:
        if sys.argv[1]:
            if sys.argv[1] == "Client":
                client = Client("0.0.0.0", 9000)
                client.connect()
            elif sys.argv[1] == "Server":
                server = Server("0.0.0.0", 9000)
                server.connectToClient()
    except IndexError:
        print("[*] Para executar, abra o terminal e digite:")
        print("[*] python Main.py Client ou Server, lembrando que o servidor deve ser iniciado primeiro")