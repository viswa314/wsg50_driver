import socket


class GripperDriver:
    def __init__(self, ip='192.168.1.20', port=1000):
        self.ip = ip
        self.port = port
        self.sock = None
        self.connected = False

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.ip, self.port))
            self.connected = True
            print(f"[INFO] Connected to gripper at {self.ip}:{self.port}")
        except socket.error as e:
            print(f"[ERROR] Connection failed: {e}")
            self.connected = False

    def disconnect(self):
        if self.sock:
            self.sock.close()
            print("[INFO] Disconnected.")
        self.connected = False

    def send_command(self, data: bytes):
        if not self.connected:
            print("[WARN] Not connected.")
            return None
        try:
            self.sock.sendall(data)
            return self.sock.recv(1024)
        except socket.error as e:
            print(f"[ERROR] Communication error: {e}")
            self.connected = False
            return None
