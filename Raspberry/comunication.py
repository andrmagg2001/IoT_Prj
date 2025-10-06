import socket, time

ARDUINO_IP = "192.168.4.1"   
PORT = 8080

def send(cmd : str) -> None:
    """
    Send a command string to the Arduino Uno R4 WiFi via TCP socket.

    This function opens a short-lived TCP connection to the Arduino 
    (running as a Wi-Fi Access Point with a TCP server) and sends 
    a command string that controls the traffic lights. The connection 
    is automatically closed after each command.

    Args:
        cmd (str): The command to send (e.g., "R1", "G2", "S:RG", "ALL:OFF").

    Behavior:
        - Establishes a TCP connection using ARDUINO_IP and PORT.
        - Sends the command followed by a newline ('\\n').
        - Waits for up to 3 seconds for a response from the Arduino.
        - Prints either the received acknowledgment or '(no resp)' 
          if no reply is detected.

    Example:
        >>> send("S:GR")
        S:GR -> OK

    Raises:
        socket.timeout: If the connection or response times out.
        OSError: For network-related errors (e.g., unreachable host).

    Notes:
        - This function assumes global variables `ARDUINO_IP` and `PORT`
          are defined and point to the Arduino Access Point.
        - Intended for quick one-shot commands, not continuous streaming.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(3)
        s.connect((ARDUINO_IP, PORT))
        s.sendall((cmd + "\n").encode())
        try:
            print(cmd, "->", s.recv(64).decode().strip())
        except Exception:
            print(cmd, "-> (no resp)")



if __name__ == "__main__":    
    for cmd in ["R1","Y1","G1","R2","Y2","G2"]:
        send(cmd); time.sleep(0.8)

    for cmd in ["S:GR","S:RG","S:YY","S:RR","S:GG"]:
        send(cmd); time.sleep(0.8)

    send("ALL:OFF")