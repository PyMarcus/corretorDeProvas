import sys
from Client import Client
from Server import Server


if __name__ == '__main__':
    """
    Por padrão, está implementado o ip localhost
    e a porta 30000
    """
    try:
        print(sys.argv)
        if sys.argv[0]:
            if sys.argv[1]:
                if sys.argv[1] == "Client":
                    client = Client("localhost", 30000)
                    client.connect()
                elif sys.argv[1] == "Server":
                    server = Server("localhost", 30000)
                    server.connectToClient()
            else:
                if sys.argv[1] == "Client":
                    client = Client(sys.argv[2], int(sys.argv[3]))
                    client.connect()
                elif sys.argv[1] == "Server":
                    client = Server(sys.argv[2], int(sys.argv[3]))
                    client.connectToClient()
    except IndexError:
        print("[*] Para executar, abra o terminal e digite:")
        print("[*] python Main.py Client ou Server ip porta [ip e porta sao opcionais], lembrando que o servidor deve "
              "ser iniciado primeiro")