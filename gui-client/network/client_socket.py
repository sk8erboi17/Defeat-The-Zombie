import socket


class ClientSocket:
    def __init__(self,game, host='127.0.0.1', port=8082):
        self.host = host
        self.port = port
        self.addr = (self.host, self.port)
        self.client_socket = None
        self.running = False
        self.game = game

    def connect(self):
        """Establish a connection to the server."""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.addr)
        print("Connected to the server.")
        self.running = True

    def send_message(self, byte_mark, message):
        """Send a message to the server."""
        if self.client_socket:
            if isinstance(message, str):
                message = message.encode('utf-8')
            self.client_socket.sendall(byte_mark + message)
            print(f"Message sent: {message}")

    def receive_response_continuously(self):
        """Receive responses from the server in a loop and handle based on byte mark."""
        buffer = b''  # Buffer per accumulare i dati ricevuti
        while self.running:
            try:
                # receive packet from the sockets
                response = self.client_socket.recv(4096)

                if not response:
                    self.running = False
                    break

                # add the packets to the buffer
                buffer += response

                while True:
                    # check for the end character
                    termination_index = buffer.find(b'\x00')

                    if termination_index != -1:
                        # extract the data until end character
                        data = buffer[:termination_index]

                        if data:
                            # handle data
                            while len(data) > 0:
                                if data[0] == 0x01:
                                    #  data after the bytebark
                                    message_data = data[1:].decode('utf-8')
                                    self.game.handle_messages(message_data)
                                    #clean buffer for the next read
                                    data = b''
                                else:
                                    print(f"Unexpected byte mark: {data[0]}")
                                    data = b''

                        # remove other charaters after termiantion characater
                        buffer = buffer[termination_index + 1:]
                    else:
                        break

            except Exception as e:
                print(f"Error receiving data: {e}")
                self.running = False

    def close(self):
        """Close the connection to the server."""
        self.running = False
        if self.client_socket:
            self.client_socket.close()
            print("Connection closed.")
