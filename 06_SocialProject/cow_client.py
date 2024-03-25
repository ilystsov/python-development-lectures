import cmd
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

    def get_message(self, socket):
        try:
            while True:
                res = socket.recv(1024).decode().rstrip()
                if res == "":
                    print("\nConnection closed by the server.")
                    break
                print(f"\n{res}\n{self.prompt}{readline.get_line_buffer()}", end='', flush=True)
        except OSError as e:
            if self.running:
                print("\nConnection error:", e)


if __name__ == '__main__':
    host = "127.0.0.1" if len(sys.argv) < 2 else sys.argv[1]
    port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        cmdline = CowClient(s)
        message_getter = threading.Thread(target=cmdline.get_message, args=(s,))
        message_getter.start()
        cmdline.cmdloop()