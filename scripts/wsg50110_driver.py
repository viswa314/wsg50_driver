import socket
import time


class WSG50110Driver:
    def __init__(self, ip='192.168.1.20', port=1000):
        self.ip = ip
        self.port = port
        self.sock = None
        self.connected = False

        # Internal simulated state
        self.current_width = None
        self.min_width = None
        self.max_width = None
        self.speed = 30.0  # mm/s
        self.force = 40.0  # N

        self.homed = False
        self.calibrated = False

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.ip, self.port))
            self.connected = True
            print(f"[INFO] Connected to WSG 50-110 at {self.ip}:{self.port}")
        except socket.error as e:
            print(f"[ERROR] Connection failed: {e}")
            self.connected = False

    def recover_connection(self, retries=3, delay=2):
        print("[ACTION] Attempting to recover connection...")
        for i in range(retries):
            print(f"[RETRY] Attempt {i+1}/{retries}...")
            self.connect()
            if self.connected:
                print("[INFO] Reconnected successfully.")
                return True
            time.sleep(delay)
        print("[ERROR] Failed to recover connection.")
        return False

    def disconnect(self):
        if self.sock:
            self.sock.close()
            print("[INFO] Disconnected.")
        self.connected = False

    def send_command(self, data: bytes):
        if not self.connected:
            print("[WARN] Not connected. Trying to recover...")
            if not self.recover_connection():
                return None

        try:
            self.sock.sendall(data)
            return self.sock.recv(1024)
        except socket.error as e:
            print(f"[ERROR] Communication error: {e}")
            self.connected = False
            return None

    def home(self):
        print("[ACTION] Performing homing sequence...")
        time.sleep(1)  # simulate delay
        self.min_width = 0.0
        self.max_width = 110.0
        self.current_width = self.max_width
        self.homed = True
        print(f"[INFO] Homing complete. Current width set to {self.current_width} mm")

    def calibrate(self):
        print("[ACTION] Calibrating limits...")
        if not self.homed:
            print("[ERROR] Cannot calibrate before homing.")
            return
        self.min_width = 0.0
        self.max_width = 110.0
        time.sleep(1.5)
        self.calibrated = True
        print(f"[INFO] Calibration complete: min = {self.min_width}, max = {self.max_width}")

    def move_to_width(self, target_width, speed=None):
        if not self.homed:
            print("[ERROR] Cannot move: gripper not homed.")
            return
        if not self.calibrated:
            print("[WARN] Moving without calibration.")

        if self.min_width is not None and target_width < self.min_width:
            print(f"[ERROR] Target width {target_width} mm is below min limit.")
            return
        if self.max_width is not None and target_width > self.max_width:
            print(f"[ERROR] Target width {target_width} mm exceeds max limit.")
            return

        if speed is None:
            speed = self.speed

        print(f"[ACTION] Moving to {target_width} mm at {speed} mm/s...")
        time.sleep(abs(self.current_width - target_width) / speed)
        self.current_width = target_width
        print(f"[INFO] Reached {self.current_width:.1f} mm")

    def get_status(self):
        return {
            "connected": self.connected,
            "homed": self.homed,
            "calibrated": self.calibrated,
            "current_width": self.current_width,
            "min_width": self.min_width,
            "max_width": self.max_width,
            "speed": self.speed,
            "force": self.force
        }
