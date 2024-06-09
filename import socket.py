import socket

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))
    
    while True:
        response = client.recv(1024).decode()
        if not response:
            break
        
        print(response, end="")
        
        if "Goodbye!" in response:
            break
        
        user_input = input()
        client.send(user_input.encode())

if __name__ == "__main__":
    start_client()
