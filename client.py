import socket
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
from datetime import datetime

HOST = '127.0.0.1'
PORT = 5555

class CalculatorClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Calculator Client")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        self.expression = ""
        self.history = []
        self.connected = False
        self.sock = None
        
        # Color scheme
        self.setup_colors()
        self.root.configure(bg=self.bg_color)
        
        # Create GUI
        self.create_header()
        self.create_display_frame()
        self.create_buttons_frame()
        self.create_status_frame()
        self.create_history_frame()
        
        # Connect to server
        self.connect_to_server()

    def setup_colors(self):
        """Define color scheme."""
        self.bg_color = "#0d1117"
        self.display_color = "#161b22"
        self.text_color = "#e6edf3"
        self.btn_color = "#238636"
        self.btn_hover = "#2ea043"
        self.btn_click = "#1f6feb"
        self.op_color = "#da3633"
        self.op_hover = "#f85149"
        self.func_color = "#6e40aa"
        self.func_hover = "#8957e5"
        self.eq_color = "#1f6feb"
        self.eq_hover = "#388bfd"
        self.status_ok = "#238636"
        self.status_error = "#da3633"
        self.border_color = "#30363d"

    def create_header(self):
        """Create header with title."""
        header = tk.Frame(self.root, bg="#161b22", height=50)
        header.pack(fill="x", padx=0, pady=0)
        
        title_label = tk.Label(
            header,
            text="🧮 NETWORK CALCULATOR",
            font=("Segoe UI", 18, "bold"),
            bg="#161b22",
            fg="#58a6ff"
        )
        title_label.pack(pady=12)

    def create_display_frame(self):
        """Create expression display area."""
        display_frame = tk.Frame(self.root, bg=self.bg_color, bd=1, relief="solid", highlightcolor=self.border_color)
        display_frame.pack(padx=12, pady=(10, 5), fill="x")

        # Expression display
        self.entry = tk.Entry(
            display_frame,
            font=("Consolas", 32, "bold"),
            borderwidth=0,
            relief="flat",
            bg=self.display_color,
            fg=self.text_color,
            justify="right",
            insertbackground="white"
        )
        self.entry.pack(ipady=18, padx=12, pady=12, fill="x")

    def create_buttons_frame(self):
        """Create calculator buttons."""
        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(padx=12, pady=(5, 10), fill="both", expand=True)

        buttons = [
            [('AC', 0, 0, self.func_color, self.func_hover), ('DEL', 0, 1, self.func_color, self.func_hover), ('(', 0, 2, self.op_color, self.op_hover), (')', 0, 3, self.op_color, self.op_hover)],
            [('7', 1, 0, self.btn_color, self.btn_hover), ('8', 1, 1, self.btn_color, self.btn_hover), ('9', 1, 2, self.btn_color, self.btn_hover), ('÷', 1, 3, self.op_color, self.op_hover)],
            [('4', 2, 0, self.btn_color, self.btn_hover), ('5', 2, 1, self.btn_color, self.btn_hover), ('6', 2, 2, self.btn_color, self.btn_hover), ('×', 2, 3, self.op_color, self.op_hover)],
            [('1', 3, 0, self.btn_color, self.btn_hover), ('2', 3, 1, self.btn_color, self.btn_hover), ('3', 3, 2, self.btn_color, self.btn_hover), ('−', 3, 3, self.op_color, self.op_hover)],
            [('0', 4, 0, self.btn_color, self.btn_hover), ('.', 4, 1, self.btn_color, self.btn_hover), ('=', 4, 2, self.eq_color, self.eq_hover), ('+', 4, 3, self.op_color, self.op_hover)]
        ]

        for row_buttons in buttons:
            for (text, r, c, color, hover_color) in row_buttons:
                self.create_button(btn_frame, text, r, c, color, hover_color)

        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)
        for i in range(5):
            btn_frame.rowconfigure(i, weight=1, minsize=50)

    def create_button(self, parent, text, row, col, color, hover_color):
        """Create individual button with hover effects."""
        btn = tk.Button(
            parent,
            text=text,
            font=("Arial", 14, "bold"),
            bg=color,
            fg="white",
            activeforeground="white",
            activebackground=hover_color,
            relief="raised",
            bd=1,
            width=10,
            height=2,
            cursor="hand2",
            command=lambda val=text: self.on_button_click(val)
        )
        btn.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
        
        # Bind hover events
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))

    def create_status_frame(self):
        """Create connection status area."""
        status_frame = tk.Frame(self.root, bg=self.display_color, height=40)
        status_frame.pack(fill="x", padx=12, pady=(5, 10))
        status_frame.pack_propagate(False)

        self.status_indicator = tk.Label(
            status_frame,
            text="● DISCONNECTED",
            font=("Arial", 10, "bold"),
            bg=self.display_color,
            fg=self.status_error,
            anchor="w"
        )
        self.status_indicator.pack(padx=12, pady=8, fill="x")

    def create_history_frame(self):
        """Create calculation history area."""
        history_label = tk.Label(
            self.root,
            text="📋 History",
            font=("Arial", 10, "bold"),
            bg=self.bg_color,
            fg=self.text_color,
            anchor="w"
        )
        history_label.pack(padx=12, pady=(5, 2), fill="x")

        self.history_text = scrolledtext.ScrolledText(
            self.root,
            height=5,
            font=("Consolas", 9),
            bg=self.display_color,
            fg=self.text_color,
            relief="solid",
            bd=1,
            insertbackground="white",
            state="disabled"
        )
        self.history_text.pack(padx=12, pady=(0, 10), fill="both", expand=True)

    def connect_to_server(self):
        """Connect to server in a separate thread."""
        thread = threading.Thread(target=self._connect_async, daemon=True)
        thread.start()

    def _connect_async(self):
        """Asynchronous connection attempt."""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((HOST, PORT))
            self.connected = True
            self.update_status("CONNECTED", True)
            self.add_history(f"[{self.get_timestamp()}] Connected to server")
        except Exception as e:
            self.connected = False
            self.update_status(f"CONNECTION FAILED: {str(e)}", False)
            self.add_history(f"[{self.get_timestamp()}] Error: {str(e)}")

    def update_status(self, message, is_connected):
        """Update connection status display."""
        color = self.status_ok if is_connected else self.status_error
        indicator = "●" if is_connected else "●"
        self.status_indicator.config(
            text=f"{indicator} {message}",
            fg=color
        )

    def on_button_click(self, char):
        """Handle button clicks."""
        if char == 'AC':
            self.expression = ""
        elif char == 'DEL':
            self.expression = self.expression[:-1]
        elif char == '=':
            self.send_expression()
            return
        elif char == '×':
            self.expression += '*'
        elif char == '÷':
            self.expression += '/'
        elif char == '−':
            self.expression += '-'
        else:
            self.expression += str(char)
        
        self.update_display()

    def update_display(self):
        """Update entry display."""
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.expression)

    def send_expression(self):
        """Send expression to server for calculation."""
        expr = self.expression.strip()
        
        if not expr:
            messagebox.showwarning("Warning", "Please enter an expression")
            return
        
        if not self.connected:
            messagebox.showerror("Error", "Not connected to server")
            return

        try:
            self.sock.send(expr.encode())
            result = self.sock.recv(1024).decode()
            
            # Add to history
            self.add_history(f"{expr} = {result}")
            
            # Update display
            self.expression = str(result)
            self.update_display()
            
            # Update status
            if "Error" in result:
                self.update_status(f"ERROR: {result}", True)
            else:
                self.update_status("CONNECTED", True)
                
        except Exception as e:
            self.connected = False
            error_msg = f"Connection error: {str(e)}"
            messagebox.showerror("Error", error_msg)
            self.update_status("DISCONNECTED", False)
            self.add_history(f"[{self.get_timestamp()}] {error_msg}")

    def add_history(self, entry):
        """Add entry to history display."""
        self.history_text.config(state="normal")
        self.history_text.insert(tk.END, entry + "\n")
        self.history_text.see(tk.END)
        self.history_text.config(state="disabled")

    def get_timestamp(self):
        """Get formatted timestamp."""
        return datetime.now().strftime("%H:%M:%S")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorClient(root)
    root.mainloop()
