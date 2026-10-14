# Smart Door - Control Panel

Đây là ứng dụng điều khiển cửa thông minh qua giao thức Serial (UART), sử dụng Tkinter cho giao diện người dùng (GUI). 
Dự án đã được tái cấu trúc (Refactored) theo mô hình hướng đối tượng để dễ bảo trì và phát triển.

## Cấu trúc thư mục

*   `main.py`: Điểm vào (entry point) của ứng dụng, chứa logic điều khiển chính (Controller). Khởi tạo giao diện và kết nối các thành phần.
*   `ui.py`: Chứa lớp `SmartDoorUI`, chịu trách nhiệm thiết kế, tạo và quản lý giao diện đồ họa.
*   `serial_handler.py`: Chứa lớp `SerialHandler`, xử lý các thao tác vật lý: quét cổng, kết nối, đọc/ghi dữ liệu qua cổng Serial/COM với luồng (thread) chạy ngầm.
*   `config.py`: File cấu hình chứa các hằng số (Baudrate), bảng màu, font chữ và các thiết lập cơ bản của ứng dụng.

## Yêu cầu (Requirements)

*   **Python:** Phiên bản 3.7 trở lên.
*   **Thư viện:** `pyserial`
    *   Cài đặt qua dòng lệnh: `pip install pyserial`
*   Thư viện `tkinter` (Thường được cài đặt sẵn cùng với Python chuẩn).

## Hướng dẫn sử dụng

1.  **Kết nối phần cứng:** Kết nối mạch điều khiển (ví dụ: STM32, Arduino) vào máy tính qua cổng cáp USB/COM.
2.  **Khởi động phần mềm:** Mở terminal/command prompt tại thư mục dự án và chạy lệnh: 
    ```bash
    python main.py
    ```
3.  **Kết nối phần mềm:** 
    *   Trên giao diện ứng dụng, tại mục "Kết nối thiết bị", nhấn **Quét** để lấy danh sách cổng.
    *   Chọn cổng COM tương ứng với vi điều khiển và nhấn **KẾT NỐI**.
4.  **Điều khiển & Giám sát:** 
    *   Sử dụng các nút **MỞ CỬA**, **ĐÓNG CỬA** để gửi lệnh.
    *   Theo dõi trạng thái cửa, các sự kiện quẹt thẻ RFID và nhật ký giao tiếp UART ngay trên màn hình.