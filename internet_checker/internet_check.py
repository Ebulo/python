import socket

def internet_check():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("www.google.com", 80))
        s.close()
        print("online")
        return True
    except:
        print("Offline")
        return False


print(internet_check())
