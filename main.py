# main.py
import tkinter as tk
from tkinter import messagebox
import queue
from config import *
from serial_handler import SerialHandler
from ui import SmartDoorUI

class AppController:
    """
    Controller chính của phần mềm - cầu nối giữa Giao diện (UI) và Giao tiếp phần cứng (Serial).
    """
    def __init__(self):
        self.root = tk.Tk()
        # Hàng đợi trung gian: Tránh lỗi Threading khi Serial luồng phụ gọi cập nhật UI luồng chính
        self.rx_queue = queue.Queue()
        
        # Khởi tạo module Xử lý phần cứng
        self.serial_handler = SerialHandler(
            self.rx_queue, 
            self.log_message, 
            self.show_error
        )
        
        # Khởi tạo giao diện
        self.ui = SmartDoorUI(self.root, self)
        
        # Thiết lập ban đầu
        self.refresh_ports()
        self.log_message("[HỆ THỐNG] Sẵn sàng. Nhấn KẾT NỐI để bắt đầu.", "warn")
        
        # Gán sự kiện khi bấm dấu X tắt cửa sổ
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Bắt đầu vòng lặp quét dữ liệu từ queue mỗi 80ms
        self.root.after(80, self.process_received_data)

    def run(self):
        """Khởi động vòng lặp giao diện Tkinter."""
        self.root.mainloop()

    def refresh_ports(self):
        """Làm mới danh sách cổng COM trên Dropdown."""
        ports = self.serial_handler.get_ports()
        self.ui.port_box["values"] = ports
        if ports and not self.ui.port_var.get():
            self.ui.port_var.set(ports[0])
        elif not ports:
            self.ui.port_var.set("")

    def toggle_connection(self):
        """Bật / Tắt kết nối với thiết bị dựa trên trạng thái hiện tại."""
        if self.serial_handler.ser and self.serial_handler.ser.is_open:
            self.serial_handler.disconnect()
            self.ui.update_connection_state(False)
        else:
            port = self.ui.port_var.get().strip()
            if not port:
                messagebox.showwarning("Thông báo", "Hãy chọn cổng COM.")
                return
            if self.serial_handler.connect(port):
                self.ui.update_connection_state(True, port)

    def send_command(self, command):
        """Hàm trung gian gửi lệnh từ nút bấm UI xuống thiết bị."""
        self.serial_handler.send_command(command)

    def log_message(self, message, tag="rx"):
        """In thông báo/dữ liệu ra bảng Nhật ký trên UI."""
        self.ui.log_box.config(state="normal")
        self.ui.log_box.insert("end", message + "\n", tag)
        self.ui.log_box.see("end") # Tự động cuộn xuống dưới cùng
        self.ui.log_box.config(state="disabled")

    def clear_log(self):
        """Xóa trắng nội dung bảng Nhật ký."""
        self.ui.log_box.config(state="normal")
        self.ui.log_box.delete("1.0", "end")
        self.ui.log_box.config(state="disabled")

    def show_error(self, message):
        """Hiển thị thông báo lỗi dưới dạng Popup."""
        messagebox.showerror("Lỗi", message)

    def process_received_data(self):
        """
        Vòng lặp đọc và xử lý phản hồi từ vi điều khiển theo thời gian thực (Polling).
        Được gọi liên tục mỗi 80ms thông qua hàm after() của Tkinter.
        """
        while not self.rx_queue.empty():
            line = self.rx_queue.get()

            # 1. Đẩy vào Log với định dạng màu tương ứng
            if line.startswith("ACK:") or line.startswith("CARD:OK"):
                self.log_message(f"← {line}", "ok")
            elif line.startswith("ERR:") or line.startswith("WARNING:") or line.startswith("CARD:WRONG"):
                self.log_message(f"← {line}", "err")
            else:
                self.log_message(f"← {line}", "rx")

            # 2. Xử lý logic và cập nhật Giao diện (Card Trạng thái & Sự kiện)
            if line.startswith("STATE:"):
                state = line.split(":", 1)[1]
                # Bảng đối chiếu dịch mã trạng thái sang tiếng Việt và gán màu
                state_names = {
                    "CLOSED":    ("Đã đóng",           DANGER),
                    "OPENING":   ("Đang mở...",        WARNING),
                    "OPEN":      ("Đang mở hoàn toàn", SUCCESS),
                    "CLOSING":   ("Đang đóng...",      WARNING),
                    "REOPENING": ("Đang mở lại...",    WARNING),
                }
                text, color = state_names.get(state, (state, TEXT_MAIN))
                self.ui.state_label.config(text=text, fg=color)
                
            elif line == "CARD:OK":
                self.ui.event_label.config(text="✓   Thẻ RFID hợp lệ", fg=SUCCESS)
            elif line == "CARD:WRONG":
                self.ui.event_label.config(text="✗   Thẻ RFID không hợp lệ", fg=DANGER)
            elif line == "WARNING:OBSTACLE":
                self.ui.event_label.config(text="⚠   Cảnh báo: Có vật cản!", fg=DANGER)
            elif line == "WARNING:RFID_LOCKED":
                self.ui.event_label.config(text="⚠   RFID đang bị khóa", fg=DANGER)
            elif line.startswith("ERR:"):
                self.ui.event_label.config(text="⚠   Không thể thực hiện lệnh", fg=DANGER)

        # Đặt lịch chạy lại sau 80 mili-giây
        self.root.after(80, self.process_received_data)

    def on_close(self):
        """Hành động diễn ra khi thoát phần mềm: Ngắt Serial an toàn và đóng form."""
        self.serial_handler.disconnect()
        self.root.destroy()

# ==================== ĐIỂM KHỞI CHẠY (ENTRY POINT) ====================
if __name__ == "__main__":
    app = AppController()
    app.run()