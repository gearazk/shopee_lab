
# Hướng dẫn: 

Cài đặt đường dẫn database host trong file `shopee/settings.py` dòng 84

        'HOST'      : 'localhost',# DB host

Thay `localhost` bằng ip postgres server ( gửi kèm trong email )

## Hướng dẫn 
- máy đã có sẵn python3.6 và pip3
- chạy lệnh `pip3 install -r ./requirements.txt` để cài đặt các thư viện cần thiết.
- chạy lệnh `python3 ./manage.py shell < tasks.py` để bắt đầu chạy lab với dữ liệu có sẵn trong database
- sau khi xong, chạy lệnh `python3 ./manage.py runserver 8080` để khởi động webapp.
- truy cập trình duyệt vào địa chỉ `localhost:8080` hoặc `127.0.0.1:8080` để xem kết quả và báo cáo.
