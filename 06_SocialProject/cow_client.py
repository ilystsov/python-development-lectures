import cmd
import queue
import sys
import socket
import threading
import readline


class CowClient(cmd.Cmd):
    prompt = "Cow Chat >> "

    def __init__(self, socket):
        super().__init__()
        self.socket = socket
        self.running = True
        self.response_queue = queue.Queue()
        self.awaiting_response = False

    def get_message(self):
        try:
            while self.running:
                res = self.socket.recv(1024).decode().rstrip()
                if res == "":
                    print("\nConnection closed by the server.")
                    self.running = False
                    break
                if self.awaiting_response:
                    self.response_queue.put(res)
                    self.awaiting_response = False
                else:
                    print(f"\n{res}\n{self.prompt}{readline.get_line_buffer()}", end='', flush=True)
        except OSError as e:
            if self.running:
                print("\nConnection error:", e)
            self.running = False

    def do_login(self, arg):
        self.socket.sendall(f"login {arg}\n".encode())

    def do_who(self, arg):
        self.socket.sendall("who\n".encode())

    def do_cows(self, arg):
        self.socket.sendall("cows\n".encode())

    def do_quit(self, arg):
        self.socket.sendall("quit\n".encode())
        self.running = False
        return True

    def do_say(self, arg):
        self.socket.sendall(f"say {arg}\n".encode())

    def do_yield(self, arg):
        self.socket.sendall(f"yield {arg}\n".encode())


if __name__ == '__main__':
    host = "127.0.0.1" if len(sys.argv) < 2 else sys.argv[1]
    port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        cmdline = CowClient(s)
        message_getter = threading.Thread(target=cmdline.get_message)
        message_getter.start()
        cmdline.cmdloop()