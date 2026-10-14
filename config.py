# config.py
# ==================== CONFIG ====================
# Tốc độ truyền baudrate cho giao tiếp UART (Phải khớp với code nạp trên vi điều khiển STM32/Arduino)
BAUDRATE = 115200

# ==================== PALETTE ====================
# Bảng màu giao diện (UI) được quy định sẵn để tạo sự đồng bộ
BG           = "#F1F5F9"    # Màu nền chính của ứng dụng
CARD_BG      = "#FFFFFF"    # Màu nền của các vùng chứa (Card)
HEADER_BG    = "#0F172A"    # Màu nền của thanh Header trên cùng
HEADER_SUB   = "#94A3B8"    # Màu chữ phụ trong Header
HEADER_FG    = "#FFFFFF"    # Màu chữ chính trong Header
PRIMARY      = "#3B82F6"    # Màu xanh lam chủ đạo (nút Kết nối)
PRIMARY_DARK = "#2563EB"    # Màu xanh lam khi di chuột vào (Hover)
SUCCESS      = "#10B981"    # Màu xanh lá (Thành công, Mở cửa)
SUCCESS_DARK = "#059669"    # Màu xanh lá đậm (Hover)
DANGER       = "#EF4444"    # Màu đỏ (Lỗi, Đóng cửa, Ngắt kết nối)
DANGER_DARK  = "#DC2626"    # Màu đỏ đậm (Hover)
WARNING      = "#F59E0B"    # Màu vàng/cam (Cảnh báo, Đang chờ)
TEXT_MAIN    = "#1E293B"    # Màu chữ chính
TEXT_MUTED   = "#64748B"    # Màu chữ nhạt (Mờ)
BORDER       = "#E2E8F0"    # Màu viền của các thành phần

# Bảng màu riêng cho khung Nhật ký (Log)
LOG_BG       = "#0F172A"    # Nền khung log tối màu
LOG_FG       = "#94A3B8"    # Chữ log thông thường (nhận)
LOG_TX       = "#60A5FA"    # Chữ log khi gửi đi (Tx)
LOG_OK       = "#34D399"    # Chữ log khi có phản hồi tốt
LOG_ERR      = "#F87171"    # Chữ log khi có lỗi
LOG_WARN     = "#FBBF24"    # Chữ log cảnh báo

# ==================== TYPOGRAPHY ====================
FONT = "Segoe UI"           # Font chữ chính cho giao diện
MONO = "Consolas"           # Font chữ không gian bằng nhau (Mono) dành cho hiển thị mã Log