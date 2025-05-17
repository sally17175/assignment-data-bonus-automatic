import socket
import hashlib

HOST = '127.0.0.1'  # localhost
PORT = 5555  # الـ port اللي السيرفر بيشتغل عليه
SECRET = b'supersecretkey'  # المفتاح السري

# دالة بتحسب الـ MAC باستخدام MD5
def calculate_mac(message):
    return hashlib.md5(SECRET + message).hexdigest()

# السيرفر الرئيسي
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server running on port {PORT}")
    
    while True:
        conn, addr = s.accept()
        with conn:
            data = conn.recv(1024)  # بيستقبل الرسالة
            if not data:
                break
            message, mac = data.split(b'|')  # بيفصل الرسالة عن الـ MAC
            computed_mac = calculate_mac(message)  # بيحسب الـ MAC
            
            # بيشوف إذا كان الـ MAC مطابق
            if computed_mac == mac.decode():
                print("MAC verified successfully")
                conn.sendall(b"MAC verified successfully")
            else:
                print("MAC verification failed")
                conn.sendall(b"MAC verification failed")
