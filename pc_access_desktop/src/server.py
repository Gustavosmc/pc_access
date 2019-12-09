__author__ = 'gustavosmc'
import socket
from threading import Thread, Lock


def get_all_ips():
    """
    :return: List<String>, sendo todos os IPs da rede local
    """
    import netifaces as nf
    ips = []
    interfaces = nf.interfaces()
    for itf in interfaces:
        try:
          ips.append(nf.ifaddresses(itf)[nf.AF_INET][0]['addr'])
        except KeyError as ke:
            print("Error server.get_all_ips " + str(ke))
    if '127.0.0.1' in ips:
        ips.remove('127.0.0.1')
    return ips


class ServerUDP(Thread):
    CONFIRM_CONNECTION = "confirm"

    def __init__(self, ip="", port=24242):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.server_address = (self.ip, self.port)
        self.received_words = []
        self.buffer = ''
        self.sock = None
        self.lock = Lock()
        self.running = False
        self.closed = False

    @staticmethod
    def raspberry_discover(port=22444):
        for ip in get_all_ips():
            ip_host = ""
            hosts = str(ip).split(".")
            lan_ip = "{}.{}.{}.".format(hosts[0], hosts[1], hosts[2])
            for i in range(1, 255):
                ip_host = lan_ip + str(i)
                try:
                    l_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    l_socket.sendto(b"pcaccess", (ip_host, port))
                    l_socket.close()
                except Exception as ex:
                    print("Error ServerUDP.raspberry_discover " + str(ex))

    def close_this(self):
        try:
            l_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            l_socket.sendto(b"close_this", (self.ip, self.port))
            l_socket.close()
        except Exception as ex:
            print("Error ServerUDP.raspberry_discover " + str(ex))

    def _bind_server(self):
        """
        :return: Boolean, True caso consiga fazer bind no endereco e False caso contrario
        """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind(self.server_address)
            return True
        except Exception as e:
            print(str(e))
            return False

    def close_socket(self):
        """
        Fecha o socket UDP
        :return: None
        """
        print("Tentando fechar socket")
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
        except Exception as ex:
            self.sock.close()
            print("Error SocketUDP.close_socket " + str(ex))
        finally:
            self.closed = True
            self.running = False

    def run(self):
        """
        Metodo herdado da classe Thread, para ser implementado em uma classa filha
        :return: None
        """
        pass


class ServerTCP(Thread):
    MAX_CONNECTIONS = 1
    CONFIRM_CONNECTION = "confirm"

    def __init__(self, ip="", port=42424):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.server_address = (self.ip, self.port)
        self.received_words = []
        self.buffer = ''
        self.sock = None
        self.connection = None
        self.client_address = None
        self.lock = Lock()
        self.running = False
        self.connected = False
        self.closed = False

    def recover_received_words(self, is_clear_buffer=True):
        """
        :param is_clear_buffer: Se for True limpa a lista de palavras recebidas
        :return: List<String>, todas as palavras recebidas pelo cliente
        """
        self.lock.acquire()
        if is_clear_buffer:
            return_words, self.received_words = \
                self.received_words, []
        else:
            return_words = self.received_words
        self.lock.release()
        return return_words

    def add_to_received_words(self, words):
        """
        :param words: List<String>, palavras a serem extendidas a lista received_words
        :return: None
        """
        self.lock.acquire()
        self.received_words.extend(words)
        self.lock.release()

    def send_msg(self, msg=""):
        """
        :param msg: String, sendo a mensagem a ser enviada
        :return: None
        """
        try:
            self.lock.acquire()
            self.connection.send(msg.encode())
            self.lock.release()
        except Exception as ex:
            print("Erro Server.send_msg : " + str(ex))

    def _bind_server(self):
        """
        :return: Boolean, True caso consiga fazer bind no endereco e False caso contrario
        """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind(self.server_address)
            self.sock.listen(self.MAX_CONNECTIONS)
            return True
        except Exception as e:
            print(str(e))
            return False

    def close_socket(self):
        try:
            self.connection.shutdown(socket.SHUT_RDWR)
            self.sock.shutdown(socket.SHUT_RDWR)
        except Exception as ex:
            print("Erro SeverTCP.close_socket " + str(ex))
        finally:
            try:
                self.connection.close()
                self.sock.close()
            except Exception as ex:
                print("Erro2 SeverTCP.close_socket " + str(ex))
            self.closed = True

    def run(self):
        """
        Chamado pelo metodo start da clase mae Thread
        :return: None
        """
        self.running = True
        try:
            if self._bind_server():
                self.connection, self.client_address = self.sock.accept()
                self.ip, self.port = self.connection.getsockname()
                print("Server.run -> Cliente connectado a interface: {}".format(self.ip))
            else:
                print("Erro Server.run ao conectar")
                return
        except OSError as ose:
            print("Erro Server.run " + str(ose))
            self.closed = True
            return

        self.connected = True
        print("ENVIANDO CONFIRMAÇÂO")
        self.send_msg(self.CONFIRM_CONNECTION)

        while self.running:
            try:
                data = self.connection.recv(1024)
                if len(data) > 0:
                    msg = str(data, 'utf-8')
                    self.add_to_received_words([msg])
            except Exception as ex:
                print("Erro Executor.run exception " + str(ex))

        if self.connection is not None:
            print("Finalizando aplicação")
            self.close_socket()




