import socket
import hashpumpy
import hashlib

HOST = '127.0.0.1'  # localhost
PORT = 5555  # نفس الـ port
SECRET = b'supersecretkey'  # المفتاح السري (للحساب فقط)
original_message = b"amount=100&to=alice"  # الرسالة الأصلية
append_data = b"&admin=true"  # اللي عايزين نضيفه
key_length = 14  # طول المفتاح السري (supersecretkey)

# دالة بتحسب الـ MAC زي السيرفر
def calculate_mac(message):
    return hashlib.md5(SECRET + message).hexdigest()

# بنطلب الـ MAC من السيرفر
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"GET_MAC")
    original_mac = s.recv(1024).decode()  # بنستقبل الـ MAC
    print(f"Received MAC from server: {original_mac}")

# بنعمل الـ length extension attack
forged_mac, forged_message = hashpumpy.hashpump(
    original_mac, original_message, append_data, key_length
)

# بنحسب الـ MAC للرسالة المزورة بنفسنا
computed_mac = calculate_mac(forged_message)
print(f"Computed MAC for forged message: {computed_mac}")
print(f"Hashpumpy forged MAC: {forged_mac}")
if computed_mac == forged_mac:
    print("MACs match! The length extension attack is successful.")
else:
    print("MACs do not match! Something went wrong.")

# بنكتب النتيجة في ملف
with open('forged_output.txt', 'w') as f:
    f.write(f"Forged message: {forged_message}\n")
    f.write(f"Forged MAC: {forged_mac}\n")
    f.write(f"Computed MAC: {computed_mac}\n")
    f.write(f"MACs match: {computed_mac == forged_mac}\n")

# بنبعت الرسالة المزورة للسيرفر
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = forged_message + b'|' + forged_mac.encode()
    s.sendall(data)
    response = s.recv(1024)
    print(f"Server response: {response.decode()}")
