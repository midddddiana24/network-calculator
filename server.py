import socket
import threading
import datetime
import sys

HOST = '127.0.0.1'
PORT = 5555
LOG_FILE = "server_log.txt"
MAX_CLIENTS = 10

def log_calculation(expression, result, addr):
    """Log calculation to file with timestamp and client info."""
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] Client: {addr} | Expression: {expression} | Result: {result}\n")

def safe_eval(expr):
    """Safely evaluate mathematical expressions."""
    allowed_chars = "0123456789+-*/(). "
    expr = expr.strip()
    
    if not expr:
        return "Error: Empty expression"
    
    if not all(c in allowed_chars for c in expr):
        return "Error: Invalid characters detected"

    try:
        # Check for division by zero
        if "/0" in expr.replace(" ", ""):
            return "Error: Division by zero"
        
        # Evaluate safely with restricted namespace
        result = eval(expr, {"__builtins__": None}, {})
        
        # Format result
        if isinstance(result, float):
            if result == int(result):
                return str(int(result))
            return f"{result:.10g}"
        return str(result)
    except ZeroDivisionError:
        return "Error: Division by zero"
    except SyntaxError:
        return "Error: Invalid syntax"
    except Exception as e:
        return f"Error: {type(e).__name__}"

def handle_client(conn, addr):
    """Handle individual client connections."""
    client_ip = f"{addr[0]}:{addr[1]}"
    print(f"✓ [CONNECTED] Client: {client_ip}")
    
    try:
        with conn:
            while True:
                data = conn.recv(1024).decode().strip()
                if not data:
                    break

                print(f"→ [CALCULATION] {client_ip}: {data}")
                result = safe_eval(data)
                log_calculation(data, result, client_ip)
                
                # Send result back to client
                conn.send(str(result).encode())
                print(f"← [RESULT] {client_ip}: {result}")
    except ConnectionResetError:
        print(f"✗ [ERROR] Connection reset by {client_ip}")
    except Exception as e:
        print(f"✗ [ERROR] {client_ip}: {str(e)}")
    finally:
        print(f"✗ [DISCONNECTED] Client: {client_ip}")

def start_server():
    """Start the calculator server."""
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(MAX_CLIENTS)
        
        print("=" * 60)
        print("╔══════════════════════════════════════════════════════════╗")
        print("║          CALCULATOR SERVER STARTED SUCCESSFULLY          ║")
        print(f"║  Host: {HOST:<48}║")
        print(f"║  Port: {PORT:<48}║")
        print(f"║  Max Clients: {MAX_CLIENTS:<42}║")
        print("║  Status: Ready to accept connections                   ║")
        print("╚══════════════════════════════════════════════════════════╝")
        print("=" * 60)

        while True:
            try:
                conn, addr = server.accept()
                thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                thread.start()
            except KeyboardInterrupt:
                break
    except OSError as e:
        print(f"✗ [FATAL ERROR] {str(e)}")
        print(f"  Make sure port {PORT} is not in use.")
        sys.exit(1)
    except Exception as e:
        print(f"✗ [FATAL ERROR] {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n\n[SERVER SHUTDOWN] Gracefully stopped by user")
    except Exception as e:
        print(f"\n✗ [CRITICAL ERROR] {str(e)}")
        sys.exit(1)
