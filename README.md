# 🧮 Network Calculator

A modern, distributed calculator application built with Python that uses a client-server architecture for remote mathematical computations.

## 📋 Overview

**Network Calculator** is a professional-grade calculator application that communicates with a central server to perform mathematical calculations. The client provides a sleek, dark-themed GUI while the server handles secure expression evaluation with comprehensive error handling.

- **Client**: Modern Tkinter GUI with real-time status display and calculation history
- **Server**: Robust socket-based server with client management and detailed logging
- **Communication**: Secure socket communication over TCP/IP
- **Security**: Protected expression evaluation preventing code injection

## ✨ Features

### Client Features

- 🎨 **Modern Dark Theme**: GitHub-inspired dark UI with professional colors
- 📊 **Real-Time Status**: Live connection indicator (Connected/Disconnected)
- 📋 **Calculation History**: Scrollable history panel with timestamps
- 🎯 **Intuitive Interface**: Large, easy-to-click buttons with hover effects
- ⌨️ **Full Calculator Operations**: Addition, subtraction, multiplication, division, parentheses
- 🔐 **Error Handling**: Clear error messages from server
- 🚀 **Async Connection**: Non-blocking server connection prevents UI freezing

### Server Features

- 🛡️ **Safe Evaluation**: Restricted namespace prevents malicious code execution
- 📝 **Detailed Logging**: All calculations logged with client IP and timestamp
- 👥 **Multi-Client Support**: Handles multiple simultaneous connections
- 🎯 **Error Detection**:
  - Division by zero detection
  - Syntax error handling
  - Invalid character filtering
  - Invalid expression validation
- 📡 **Real-Time Monitoring**: Console output shows all server activities
- 🔄 **Graceful Shutdown**: Proper handling of connection resets and interrupts

## 🚀 Quick Start

### Prerequisites

- Python 3.6 or higher
- tkinter (usually included with Python)
- Socket support (standard library)

### Installation

1. Clone or download the project:

```bash
cd "C:\Users\rober\OneDrive\Desktop\IT\GITHUB PROJECT\CALCULATOR"
```

2. No additional dependencies required - uses only Python standard library!

### Running the Application

**Step 1: Start the Server**

```bash
python server.py
```

You should see:

```
============================================================
╔══════════════════════════════════════════════════════════╗
║          CALCULATOR SERVER STARTED SUCCESSFULLY          ║
║  Host: 127.0.0.1                                        ║
║  Port: 5555                                             ║
║  Max Clients: 10                                        ║
║  Status: Ready to accept connections                   ║
╚══════════════════════════════════════════════════════════╝
============================================================
```

**Step 2: Start the Client (in a new terminal)**

```bash
python client.py
```

The calculator GUI will appear with a status indicator showing "● CONNECTED".

## 📖 Usage Guide

### Basic Calculations

1. **Enter Expression**: Click number and operator buttons to build your expression
2. **View Expression**: Your input displays in the text field at the top
3. **Calculate**: Click the `=` button to send the expression to the server
4. **View Result**: Result displays immediately in the expression field
5. **Clear**: Use `AC` to clear or `DEL` to remove last character

### Supported Operations

| Operation      | Symbol | Key |
| -------------- | ------ | --- |
| Addition       | +      | +   |
| Subtraction    | −      | -   |
| Multiplication | ×      | \*  |
| Division       | ÷      | /   |
| Parentheses    | ( )    | ( ) |
| Decimal        | .      | .   |

### Example Calculations

```
5 + 3 = 8
10 * (2 + 3) = 50
100 / 4 = 25
(15 - 5) * 2 = 20
```

### Status Indicators

- **● CONNECTED**: Client is connected to server and ready
- **● ERROR**: Server returned an error (check history panel)
- **● DISCONNECTED**: Lost connection to server (restart server and client)

### History Panel

- Shows all calculations performed in the session
- Displays connection events and errors
- Timestamps for each operation
- Scrollable for viewing past calculations

## 🔧 Configuration

### Server Settings

Modify these in `server.py`:

```python
HOST = '127.0.0.1'  # Server IP address
PORT = 5555         # Server port
LOG_FILE = "server_log.txt"  # Log file location
MAX_CLIENTS = 10    # Maximum concurrent clients
```

### Client Settings

Modify these in `client.py`:

```python
HOST = '127.0.0.1'  # Server IP address
PORT = 5555         # Server port
```

## 📊 Server Logging

The server logs all calculations to `server_log.txt`:

```
[2025-12-29 14:30:45] Client: 127.0.0.1:52891 | Expression: 5 + 3 | Result: 8
[2025-12-29 14:30:48] Client: 127.0.0.1:52891 | Expression: 10 * 2 | Result: 20
```

## 🛡️ Security Features

### Expression Validation

- ✅ Only allows: `0-9`, `+`, `-`, `*`, `/`, `(`, `)`, `.`, and spaces
- ❌ Blocks: Any other characters including variables, function calls, imports
- ❌ Detects: Division by zero before evaluation

### Safe Evaluation

- Uses Python's `eval()` with restricted `__builtins__`
- No access to system functions or dangerous operations
- Prevents code injection attacks

## 🐛 Error Handling

### Common Errors

| Error                         | Cause                       | Solution                          |
| ----------------------------- | --------------------------- | --------------------------------- |
| "Could not connect to server" | Server not running          | Start server in separate terminal |
| "Connection error"            | Server crashed/disconnected | Restart server and client         |
| "Error: Division by zero"     | Expression divides by 0     | Fix expression and try again      |
| "Error: Invalid syntax"       | Malformed expression        | Check parentheses and operators   |
| "Error: Invalid characters"   | Invalid symbols used        | Only use: `0-9 + - * / ( ) .`     |

## 🔧 Troubleshooting

### Port Already in Use

If you get "Address already in use" error:

```bash
# Kill process using port 5555 (Windows PowerShell)
Get-NetTCPConnection -LocalPort 5555 | Stop-Process -Force

# Or restart your computer
```

### GUI Not Displaying

- Ensure tkinter is installed: `python -m pip install tk`
- Try running from a different terminal

### Slow Response

- Check network connectivity
- Ensure server is not overloaded
- Multiple clients may impact performance

## 📁 Project Structure

```
CALCULATOR/
├── server.py           # Calculator server (handles calculations)
├── client.py           # Calculator client (GUI interface)
├── server_log.txt      # Server calculation logs
└── README.md          # This file
```

## 🎨 Color Scheme

### Client GUI

- **Primary Background**: `#0d1117` (Dark gray-blue)
- **Secondary Background**: `#161b22` (Slightly lighter)
- **Text**: `#e6edf3` (Light gray)
- **Numbers**: `#238636` (Green)
- **Operators**: `#da3633` (Red)
- **Functions**: `#6e40aa` (Purple)
- **Equals**: `#1f6feb` (Blue)

## 💡 Tips & Tricks

1. **Complex Calculations**: Use parentheses for complex expressions
   - `(100 + 50) * 2 / 5` calculates correctly
2. **Decimal Numbers**: Fully supported
   - `3.14 * 2` works perfectly
3. **Large Numbers**: Handled automatically

   - `999999 * 999999` displays result in scientific notation if needed

4. **Check History**: Scroll through history panel to see all past calculations

5. **Reconnect**: If disconnected, restart both server and client

## 🚦 System Requirements

- **OS**: Windows, macOS, or Linux
- **Python**: 3.6+
- **RAM**: 10 MB minimum
- **Network**: Local network or localhost

## 📝 License

This project is provided as-is for educational and personal use.

## 👨‍💻 Developer

**GODDDOG**

---

## 📞 Support

For issues or questions:

1. Check the Troubleshooting section above
2. Review the `server_log.txt` for server-side errors
3. Ensure both server and client are running on the same network

## 🎯 Future Enhancements

Potential features for future versions:

- [ ] Scientific calculator functions (sin, cos, sqrt, etc.)
- [ ] Expression history with favorites
- [ ] Multiple calculation modes (binary, hex, etc.)
- [ ] Network security with authentication
- [ ] Mobile client support
- [ ] Cloud-based server deployment

---

**Enjoy your Network Calculator! 🚀**
