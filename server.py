import socket
import threading

# Pre-defined bank accounts
accounts = {
    '12345': {'pin': '1111', 'balance': 1000},
    '67890': {'pin': '2222', 'balance': 1500},
    '54321': {'pin': '3333', 'balance': 500},
}

lock = threading.Lock()

def handle_client(client_socket):
    try:
        # Authenticate client
        client_socket.send(b"Enter account number: ")
        account_number = client_socket.recv(1024).decode().strip()
        
        client_socket.send(b"Enter PIN: ")
        pin = client_socket.recv(1024).decode().strip()
        
        if account_number in accounts and accounts[account_number]['pin'] == pin:
            client_socket.send(b"Authentication successful!\n")
        else:
            client_socket.send(b"Authentication failed!\n")
            client_socket.close()
            return
        
        # Handle client operations
        while True:
            client_socket.send(b"Choose operation: 1. Check Balance 2. Deposit 3. Withdraw 4. Exit\n")
            operation = client_socket.recv(1024).decode().strip()
            
            if operation == '1':
                balance = accounts[account_number]['balance']
                client_socket.send(f"Your balance is: ${balance}\n".encode())
            
            elif operation == '2':
                client_socket.send(b"Enter amount to deposit: ")
                amount = float(client_socket.recv(1024).decode().strip())
                
                with lock:
                    accounts[account_number]['balance'] += amount
                
                client_socket.send(b"Deposit successful!\n")
            
            elif operation == '3':
                client_socket.send(b"Enter amount to withdraw: ")
                amount = float(client_socket.recv(1024).decode().strip())
                
                with lock:
                    if amount <= accounts[account_number]['balance']:
                        accounts[account_number]['balance'] -= amount
                        client_socket.send(b"Withdrawal successful!\n")
                    else:
                        client_socket.send(b"Insufficient funds!\n")
            
            elif operation == '4':
                final_balance = accounts[account_number]['balance']
                client_socket.send(f"Final balance: ${final_balance}\n".encode())
                client_socket.send(b"Goodbye!\n")
                client_socket.close()
                break
            
            else:
                client_socket.send(b"Invalid operation!\n")
    
    except Exception as e:
        print(f"Exception: {e}")
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    print("Server started on port 9999")
    
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
