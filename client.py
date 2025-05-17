import socket
import hashpumpy

HOST = '127.0.0.1'  # localhost
PORT = 5555  # نفس الـ port
original_message = b"amount=100&to=alice"  # الرسالة الأصلية
original_mac = "614d28d808af46d3702fe35fae67267c"  # الـ MAC الأصلي
append_data = b"&admin=true"  # اللي عايزين نضيفه
key_length = 14  # طول المفتاح السري (supersecretkey)

# بنعمل الـ length extension attack
forged_mac, forged_message = hashpumpy.hashpump(
    original_mac, original_message, append_data, key_length
)

# بنكتب النتيجة في ملف
with open('forged_output.txt', 'w') as f:
    f.write(f"Forged message: {forged_message}\n")
    f.write(f"Forged MAC: {forged_mac}\n")

# بنبعت الرسالة المزورة للسيرفر
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = forged_message + b'|' + forged_mac.encode()
    s.sendall(data)
    response = s.recv(1024)
    print(response.decode())
