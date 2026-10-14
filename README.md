# 🚪 Smart Door Control Panel (UART Screen)

Ứng dụng điều khiển và giám sát hệ thống cửa thông minh qua giao tiếp Serial/UART, được phát triển bằng ngôn ngữ Python với giao diện đồ họa Tkinter theo mô hình kiến trúc Hướng đối tượng (OOP).

---

## 1. Giới thiệu

**Smart Door Control Panel** là phần mềm máy tính (Desktop App) kết nối trực tiếp với các hệ thống nhúng/vi điều khiển (như STM32, Arduino) để quản lý vận hành cửa tự động. 

Các tính năng nổi bật:
* Quản lý kết nối UART linh hoạt, tự động dò tìm cổng COM.
* Giao diện trực quan, hiển thị trạng thái cửa theo thời gian thực (Đã đóng, Đang mở, Đang đóng, Cảnh báo vật cản).
* Theo dõi và cảnh báo sự kiện quẹt thẻ RFID.
* Khung nhật ký truyền thông (UART Log) phân loại tín hiệu Tx/Rx bằng màu sắc rõ ràng.
* Luồng xử lý dữ liệu độc lập (Multithreading & Queue), đảm bảo giao diện luôn mượt mà không bị treo lag.

---

## 2. Cấu trúc dự án

Dự án được tổ chức theo cấu trúc module rõ ràng, phân tách nhiệm vụ giữa xử lý dữ liệu và giao diện:

```text
UART Screen/
├── config.py           # Lưu trữ hằng số, cấu hình Baudrate, bảng màu (Palette) và Font chữ
├── serial_handler.py   # Quản lý kết nối vật lý cổng COM, gửi/nhận dữ liệu và chạy Thread ngầm
├── ui.py               # Thiết kế và dựng thành phần giao diện đồ họa (Tkinter GUI)
├── main.py             # Controller chính điều phối ứng dụng, xử lý sự kiện và khởi chạy App
└── README.md           # Tài liệu hướng dẫn sử dụng dự án
```

---

## 3. Cài đặt và chuẩn bị

### Yêu cầu hệ thống
* **Hệ điều hành**: Windows 10/11, macOS, hoặc Linux.
* **Môi trường Python**: Phiên bản Python `3.7` trở lên.

### Cài đặt thư viện phụ thuộc
Ứng dụng sử dụng thư viện `pyserial` để giao tiếp qua cổng COM. Mở Terminal / Command Prompt tại thư mục dự án và thực hiện lệnh cài đặt:

```bash
pip install pyserial
```

*(Lưu ý: Thư viện giao diện `tkinter` đã được tích hợp sẵn trong hầu hết các bản cài đặt Python chuẩn).*

---

## 4. Thông tin giao thức

Hệ thống truyền thông qua chuẩn giao tiếp nối tiếp Serial bất đồng bộ (UART) với thông số cấu hình mặc định:

* **Tốc độ truyền (Baudrate)**: `115200`
* **Data bits**: `8`
* **Parity**: `None`
* **Stop bits**: `1`
* **Định dạng dữ liệu**: Chuỗi ký tự ASCII, kết thúc bằng cặp ký tự `\r\n` (CRLF).

---

## 5. Lệnh điều khiển (PC ➔ Vi điều khiển)

Các lệnh truyền từ ứng dụng xuống mạch điều khiển khi người dùng tương tác trên giao diện:

| Lệnh | Định dạng gửi | Ý nghĩa / Thao tác |
| :--- | :--- | :--- |
| **MỞ CỬA** | `OPEN\r\n` | Yêu cầu vi điều khiển kích hoạt động cơ mở cửa |
| **ĐÓNG CỬA** | `CLOSE\r\n` | Yêu cầu vi điều khiển kích hoạt động cơ đóng cửa |
| **CẬP NHẬT** | `STATUS\r\n` | Yêu cầu vi điều khiển trả về trạng thái cửa hiện tại |

---

## 📥 6. Dữ liệu phản hồi (Vi điều khiển ➔ PC)

Các chuỗi tín hiệu vi điều khiển gửi về để ứng dụng cập nhật thông tin lên màn hình:

### Cập nhật trạng thái cửa
| Chuỗi tín hiệu nhận | Trạng thái hiển thị | Màu sắc hiển thị |
| :--- | :--- | :--- |
| `STATE:CLOSED` | Đã đóng | Đỏ (`DANGER`) |
| `STATE:OPENING` | Đang mở... | Cam (`WARNING`) |
| `STATE:OPEN` | Đang mở hoàn toàn | Xanh lá (`SUCCESS`) |
| `STATE:CLOSING` | Đang đóng... | Cam (`WARNING`) |
| `STATE:REOPENING` | Đang mở lại... | Cam (`WARNING`) |

### Cập nhật sự kiện RFID & Cảnh báo
| Chuỗi tín hiệu nhận | Sự kiện ghi nhận |
| :--- | :--- |
| `CARD:OK` | ✓ Thẻ RFID hợp lệ |
| `CARD:WRONG` | ✗ Thẻ RFID không hợp lệ |
| `WARNING:OBSTACLE` | ⚠ Cảnh báo: Phát hiện vật cản |
| `WARNING:RFID_LOCKED` | ⚠ Cảnh báo: Hệ thống RFID đang bị khóa |
| `ERR:...` | ⚠ Lỗi thao tác hoặc câu lệnh không hợp lệ |

---

## 7. Hướng dẫn sử dụng

### Bước 1: Kết nối phần cứng
1. Nối mạch vi điều khiển (STM32/Arduino) với mạch chuyển đổi USB to UART (CP2102, CH340,...).
2. Đấu nối đúng chân:
   * **TXD** (USB to UART) ➔ **RX** (Vi điều khiển)
   * **RXD** (USB to UART) ➔ **TX** (Vi điều khiển)
   * **GND** (USB to UART) ➔ **GND** (Vi điều khiển)
3. Cắm cáp USB vào máy tính.

### Bước 2: Khởi động ứng dụng
Tại thư mục dự án, gõ lệnh sau để khởi chạy:
```bash
python main.py
```

### Bước 3: Vận hành ứng dụng
1. **Kết nối**:
   * Nhấn nút **Quét** để cập nhật danh sách các cổng COM đang nhận.
   * Chọn cổng COM tương ứng từ danh sách thả xuống.
   * Nhấn **KẾT NỐI**. Đèn báo `UART` ở góc trên màn hình sẽ đổi sang màu xanh lá khi thành công.
2. **Điều khiển**:
   * Nhấn nút **MỞ CỬA** hoặc **ĐÓNG CỬA** để gửi lệnh tương ứng.
   * Nhấn **⟳ Cập nhật trạng thái** để yêu cầu kiểm tra tình trạng cửa tức thời.
3. **Giám sát & Nhật ký**:
   * Theo dõi trạng thái hoạt động thực tế tại khung **Trạng thái cửa** và **Sự kiện gần nhất**.
   * Kiểm tra mã lệnh truyền nhận chi tiết tại bảng **Nhật ký giao tiếp UART**. Nhấn nút **Xóa log** khi muốn làm sạch khung hiển thị.