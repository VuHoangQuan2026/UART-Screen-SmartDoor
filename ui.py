# ui.py
import tkinter as tk
from tkinter import ttk
from config import *

class SmartDoorUI:
    """
    Lớp thiết kế và quản lý các thành phần giao diện người dùng bằng Tkinter.
    """
    def __init__(self, root, controller):
        self.root = root               # Cửa sổ chính
        self.controller = controller   # AppController (Dùng để gọi các hàm kết nối, gửi lệnh)
        
        # Thiết lập cửa sổ chính
        self.root.title("Smart Door - Control Panel")
        self.root.configure(bg=BG)
        self.root.geometry("560x820")
        self.root.resizable(False, False)
        
        self._setup_styles()
        self._build_header()
        self._build_body()
        
    def _setup_styles(self):
        """Thiết lập style tùy chỉnh cho các widget của ttk (ví dụ: Combobox)."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox",
                        fieldbackground=CARD_BG,
                        background=CARD_BG,
                        foreground=TEXT_MAIN,
                        arrowcolor=TEXT_MUTED,
                        bordercolor=BORDER,
                        lightcolor=BORDER,
                        darkcolor=BORDER,
                        padding=6)
        style.map("TCombobox",
                  fieldbackground=[("readonly", CARD_BG)],
                  selectbackground=[("readonly", CARD_BG)],
                  selectforeground=[("readonly", TEXT_MAIN)])
                  
    def _flat_button(self, parent, text, command, bg, hover_bg, fg="white", font=(FONT, 10, "bold"), padx=14, pady=6):
        """Hàm tiện ích giúp tạo nút bấm phẳng (flat) hỗ trợ hiệu ứng di chuột (hover)."""
        btn = tk.Button(parent, text=text, command=command,
                        bg=bg, fg=fg,
                        activebackground=hover_bg, activeforeground=fg,
                        font=font, relief="flat", bd=0, cursor="hand2",
                        padx=padx, pady=pady, highlightthickness=0)
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg)) # Khi chuột vào
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))       # Khi chuột ra
        return btn

    def _make_card(self, parent, title=None, fill="x", expand=False, pady=(0, 12)):
        """Hàm tiện ích tạo các thẻ (Card) có viền để nhóm thông tin."""
        card = tk.Frame(parent, bg=CARD_BG, highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill=fill, expand=expand, pady=pady)
        if title:
            tk.Label(card, text=title.upper(), bg=CARD_BG, fg=TEXT_MUTED,
                     font=(FONT, 9, "bold")).pack(anchor="w", padx=16, pady=(12, 6))
        return card

    def _build_header(self):
        """Tạo phần tiêu đề Header tối màu phía trên cùng ứng dụng."""
        header = tk.Frame(self.root, bg=HEADER_BG, height=76)
        header.pack(fill="x")
        header.pack_propagate(False)

        title_box = tk.Frame(header, bg=HEADER_BG)
        title_box.pack(side="left", padx=24)

        tk.Label(title_box, text="🚪  SMART DOOR", bg=HEADER_BG, fg=HEADER_FG,
                 font=(FONT, 16, "bold")).pack(anchor="w", pady=(14, 0))
        tk.Label(title_box, text="Hệ thống điều khiển cửa thông minh", bg=HEADER_BG, fg=HEADER_SUB,
                 font=(FONT, 9)).pack(anchor="w")

        # Đèn báo trạng thái kết nối trên Header
        hdr_status = tk.Frame(header, bg=HEADER_BG)
        hdr_status.pack(side="right", padx=24)
        self.status_dot = tk.Label(hdr_status, text="●", bg=HEADER_BG, fg=DANGER, font=(FONT, 16))
        self.status_dot.pack(side="left")
        tk.Label(hdr_status, text="  UART", bg=HEADER_BG, fg=HEADER_SUB, font=(FONT, 9)).pack(side="left")

    def _build_body(self):
        """Tạo toàn bộ phần thân ứng dụng (các Card kết nối, nút bấm, log)."""
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=18, pady=16)

        # ====== Card: Kết nối ======
        conn_card = self._make_card(body, "Kết nối thiết bị")
        port_row = tk.Frame(conn_card, bg=CARD_BG)
        port_row.pack(fill="x", padx=16, pady=(0, 6))

        tk.Label(port_row, text="Cổng COM", bg=CARD_BG, fg=TEXT_MAIN, font=(FONT, 10)).pack(side="left", padx=(0, 10))

        self.port_var = tk.StringVar()
        self.port_box = ttk.Combobox(port_row, textvariable=self.port_var, width=10, state="readonly", font=(FONT, 10))
        self.port_box.pack(side="left")

        self.scan_btn = self._flat_button(port_row, "Quét", self.controller.refresh_ports,
                                          bg="#E2E8F0", hover_bg="#CBD5E1", fg=TEXT_MAIN, font=(FONT, 9, "bold"), padx=12, pady=5)
        self.scan_btn.pack(side="left", padx=(8, 0))

        self.connect_btn = self._flat_button(port_row, "KẾT NỐI", self.controller.toggle_connection,
                                             bg=PRIMARY, hover_bg=PRIMARY_DARK, font=(FONT, 9, "bold"), padx=16, pady=5)
        self.connect_btn.pack(side="right")

        status_row = tk.Frame(conn_card, bg=CARD_BG)
        status_row.pack(fill="x", padx=16, pady=(4, 14))

        self.status_conn = tk.Label(status_row, text="Chưa kết nối", bg=CARD_BG, fg=TEXT_MUTED, font=(FONT, 9))
        self.status_conn.pack(side="left")

        # ====== Card: Trạng thái cửa ======
        state_card = self._make_card(body, "Trạng thái cửa")
        self.state_label = tk.Label(state_card, text="— Chưa có dữ liệu —", bg=CARD_BG, fg=TEXT_MUTED, font=(FONT, 22, "bold"))
        self.state_label.pack(pady=(6, 18))

        # ====== Các nút thao tác ======
        action_row = tk.Frame(body, bg=BG)
        action_row.pack(fill="x", pady=(0, 12))

        open_btn = tk.Button(action_row, text="MỞ CỬA", command=lambda: self.controller.send_command("OPEN"),
                             bg=SUCCESS, fg="white", activebackground=SUCCESS_DARK, activeforeground="white",
                             font=(FONT, 12, "bold"), relief="flat", bd=0, cursor="hand2", height=2, highlightthickness=0)
        open_btn.pack(side="left", fill="x", expand=True, padx=(0, 6))
        open_btn.bind("<Enter>", lambda e: open_btn.config(bg=SUCCESS_DARK))
        open_btn.bind("<Leave>", lambda e: open_btn.config(bg=SUCCESS))

        close_btn = tk.Button(action_row, text="ĐÓNG CỬA", command=lambda: self.controller.send_command("CLOSE"),
                              bg=DANGER, fg="white", activebackground=DANGER_DARK, activeforeground="white",
                              font=(FONT, 12, "bold"), relief="flat", bd=0, cursor="hand2", height=2, highlightthickness=0)
        close_btn.pack(side="left", fill="x", expand=True, padx=(6, 0))
        close_btn.bind("<Enter>", lambda e: close_btn.config(bg=DANGER_DARK))
        close_btn.bind("<Leave>", lambda e: close_btn.config(bg=DANGER))

        sub_row = tk.Frame(body, bg=BG)
        sub_row.pack(fill="x", pady=(0, 12))
        status_btn = self._flat_button(sub_row, "⟳  Cập nhật trạng thái", lambda: self.controller.send_command("STATUS"),
                                       bg="#E2E8F0", hover_bg="#CBD5E1", fg=TEXT_MAIN, font=(FONT, 9, "bold"), padx=14, pady=6)
        status_btn.pack()

        # ====== Card: Sự kiện ======
        event_card = self._make_card(body, "Sự kiện gần nhất")
        self.event_label = tk.Label(event_card, text="— Chưa có sự kiện —", bg=CARD_BG, fg=TEXT_MUTED, font=(FONT, 11))
        self.event_label.pack(pady=(2, 16))

        # ====== Card: Khung Nhật ký (Logs) ======
        log_card = tk.Frame(body, bg=CARD_BG, highlightbackground=BORDER, highlightthickness=1)
        log_card.pack(fill="both", expand=True)

        log_head = tk.Frame(log_card, bg=CARD_BG)
        log_head.pack(fill="x", padx=16, pady=(12, 8))

        tk.Label(log_head, text="NHẬT KÝ GIAO TIẾP UART", bg=CARD_BG, fg=TEXT_MUTED, font=(FONT, 9, "bold")).pack(side="left")

        clear_btn = self._flat_button(log_head, "Xóa log", self.controller.clear_log,
                                      bg="#F1F5F9", hover_bg="#E2E8F0", fg=TEXT_MUTED, font=(FONT, 9), padx=10, pady=2)
        clear_btn.pack(side="right")

        log_container = tk.Frame(log_card, bg=LOG_BG)
        log_container.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.log_box = tk.Text(log_container, height=9, bg=LOG_BG, fg=LOG_FG, font=(MONO, 9),
                               relief="flat", bd=0, insertbackground="white", padx=10, pady=8, wrap="word")
        self.log_box.pack(fill="both", expand=True, side="left")

        scrollbar = tk.Scrollbar(log_container, command=self.log_box.yview, bg=LOG_BG, troughcolor=LOG_BG,
                                 activebackground="#334155", relief="flat", bd=0, width=8)
        scrollbar.pack(side="right", fill="y")
        self.log_box.config(yscrollcommand=scrollbar.set)

        # Định nghĩa các Tag màu sắc cho Log
        self.log_box.tag_config("tx",   foreground=LOG_TX)
        self.log_box.tag_config("rx",   foreground=LOG_FG)
        self.log_box.tag_config("ok",   foreground=LOG_OK)
        self.log_box.tag_config("err",  foreground=LOG_ERR)
        self.log_box.tag_config("warn", foreground=LOG_WARN)
        self.log_box.config(state="disabled")

    def update_connection_state(self, connected, port=""):
        """Hàm cập nhật UI khi trạng thái kết nối thay đổi."""
        if connected:
            self.status_conn.config(text=f"Đã kết nối {port}", fg=SUCCESS)
            self.status_dot.config(fg=SUCCESS)
            self.connect_btn.config(text="NGẮT KẾT NỐI", bg=DANGER, activebackground=DANGER_DARK)
            self.connect_btn.bind("<Enter>", lambda e: self.connect_btn.config(bg=DANGER_DARK))
            self.connect_btn.bind("<Leave>", lambda e: self.connect_btn.config(bg=DANGER))
        else:
            self.status_conn.config(text="Chưa kết nối", fg=TEXT_MUTED)
            self.status_dot.config(fg=DANGER)
            self.connect_btn.config(text="KẾT NỐI", bg=PRIMARY, activebackground=PRIMARY_DARK)
            self.connect_btn.bind("<Enter>", lambda e: self.connect_btn.config(bg=PRIMARY_DARK))
            self.connect_btn.bind("<Leave>", lambda e: self.connect_btn.config(bg=PRIMARY))