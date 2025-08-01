import socket
import time


class WSG50110Driver:
    def __init__(self, ip='192.168.1.20', port=1000):
        self.ip = ip
        self.port = port
        self.sock = None
        self.connected = False

        # Simulated internal state
        self.current_width = 50.0  # mm (default starting point)
        self.min_width = 0.0
        self.max_width = 110.0
        self.speed = 30.0  # mm/s
        self.force = 40.0  # N (simulated)

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

    def move_to_width(self, target_width, speed=None):
        if speed is None:
            speed = self.speed

        print(f"[ACTION] Moving to {target_width} mm at {speed} mm/s...")
        time.sleep(abs(self.current_width - target_width) / speed)
        self.current_width = target_width
        print(f"[INFO] Reached {self.current_width:.1f} mm")

    def get_status(self):
        return {
            "connected": self.connected,
            "current_width": self.current_width,
            "min_width": self.min_width,
            "max_width": self.max_width,
            "speed": self.speed,
            "force": self.force
        }
