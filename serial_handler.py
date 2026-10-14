# serial_handler.py
import serial
import serial.tools.list_ports
import threading
from config import BAUDRATE

class SerialHandler:
    """
    Lớp xử lý giao tiếp Serial (UART) với thiết bị phần cứng (VD: STM32, Arduino).
    Hoạt động độc lập và đẩy dữ liệu nhận được vào một Queue để xử lý.
    """
    def __init__(self, rx_queue, log_callback, error_callback):
        self.ser = None                   # Đối tượng Serial object
        self.rx_queue = rx_queue          # Hàng đợi (Queue) chứa dữ liệu nhận được
        self.log_callback = log_callback  # Hàm gọi ngược (Callback) để in log lên UI
        self.error_callback = error_callback # Hàm gọi ngược hiển thị popup lỗi lên UI
        self.running = False              # Cờ trạng thái chạy của Thread đọc dữ liệu

    @staticmethod
    def get_ports():
        """Lấy danh sách tất cả các cổng COM hiện có trên máy tính."""
        return [p.device for p in serial.tools.list_ports.comports()]

    def connect(self, port):
        """Khởi tạo kết nối tới cổng COM được chỉ định."""
        if self.ser and self.ser.is_open:
            return True
        try:
            # Mở cổng Serial với timeout = 0.2s để không bị treo
            self.ser = serial.Serial(port, BAUDRATE, timeout=0.2)
            self.running = True
            
            # Khởi tạo một Thread chạy ngầm để liên tục đọc dữ liệu trả về từ phần cứng
            threading.Thread(target=self._read_loop, daemon=True).start()
            
            self.log_callback(f"[HỆ THỐNG] Đã kết nối {port}", "ok")
            return True
        except Exception as e:
            self.ser = None
            self.error_callback(str(e))
            return False

    def disconnect(self):
        """Đóng kết nối Serial."""
        self.running = False # Dừng vòng lặp read_loop
        if self.ser:
            try:
                self.ser.close()
            except Exception:
                pass
        self.ser = None
        self.log_callback("[HỆ THỐNG] Đã ngắt kết nối", "warn")

    def _read_loop(self):
        """Vòng lặp chạy trong Thread riêng để đọc dữ liệu từ thiết bị liên tục."""
        while self.running and self.ser and self.ser.is_open:
            try:
                # Đọc từng dòng, giải mã utf-8 và loại bỏ khoảng trắng 2 đầu
                line = self.ser.readline().decode("utf-8", errors="ignore").strip()
                if line:
                    # Nếu có dữ liệu, đưa vào Queue để Controller xử lý sau
                    self.rx_queue.put(line)
            except Exception:
                break # Thoát vòng lặp nếu có lỗi (ví dụ: rút cáp đột ngột)

    def send_command(self, command):
        """Gửi một chuỗi lệnh (thêm \r\n ở cuối) xuống thiết bị."""
        if not self.ser or not self.ser.is_open:
            self.error_callback("Bạn chưa kết nối với thiết bị điều khiển.")
            return False
        try:
            # Gửi dữ liệu dưới dạng byte
            self.ser.write((command + "\r\n").encode("utf-8"))
            self.log_callback(f"→ {command}", "tx") # Ghi log Tx
            return True
        except Exception as e:
            self.error_callback(str(e))
            return False