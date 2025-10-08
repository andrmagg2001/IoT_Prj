# Import stantment
import socket
import time
import csv
import datetime
import os


# class definition
class TrafficLightClient:
    """
    Persistent TCP client to the Arduino server.

    Args:
        host: Arduino AP IP address (e.g., 192.168.4.1)
        port: Arduino TCP server port (e.g., 8080)
        timeout: Socket timeout in seconds
        reconnect_attempts: Number of reconnection attempts after failures
        reconnect_delay: Delay between reconnection attempts in seconds
        log_path: Optional CSV file path to log timestamp, command, and ACK

    Methods:
        connect(): Open a TCP connection
        close(): Close the connection
        send(cmd): Send a command and return the ACK line
        safe_g1(), safe_g2(): Safe transition to green on signal 1 or 2
        g1(), y1(), r1(), g2(), y2(), r2(): Set single-signal colors
        set_both(x, y): Set both signals via S:XY
        all_off(), all_red(): Global commands
        test_cycle(n_cycles, dwell): Alternate a safe cycle for demo/tests
    """
    def __init__(
            self,
            host : str,
            port : int = 8080,
            timeout : float = 3.0,
            reconnect_attempts : int = 3,
            reconnect_delay : float = 0.5,
            log_path : str = None
    ) -> None:
        self.host = host
        self.port = port
        self.timeout = timeout
        self.reconnect_attempts = reconnect_attempts
        self.reconnect_delay = reconnect_delay
        self.sock = None
        self.log_path = log_path
        if self.log_path:
            os.makedirs(os.path.dirname(self.log_path) or ".", exist_ok=True)
            if not os.path.exists(self.log_path):
                with open(self.log_path, "w", newline="") as f:
                    w = csv.writer(f)
                    w.writerow(["ts", "cmd", "ack"])


    def connect(self) -> None:
        """
        Open a persistent TCP connection to the arduino  
        """
        self.close()
        self.sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
        self.sock.settimeout(self.timeout)

    def close(self) -> None:
        """
        Close the TCP connection if open
        """
        if self.sock:
            try:
                self.sock.close()
            finally:
                self.sock = None
    
    def __enter__(self) -> "TrafficLightClient":
        """
        Context manager entry that ensures a connected client.
        """
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc, tb) -> None:
        """
        Context manager exit that safely closes the connection.
        """
        self.close()

    def _log(self, cmd: str, ack: str) -> None:
        """
        Append a CSV log row if log_path is configured.

        Args:
            cmd: Command that was sent
            ack: Acknowledgment string that was received
        """
        if not self.log_path:
            return
        ts = datetime.datetime.now().isoformat(timespec="seconds")
        with open(self.log_path, "a", newline="") as f:
            w = csv.writer(f)
            w.writerow([ts, cmd, ack])

    def _recv_line(self) -> str:
        """
        Receive a single newline-terminated line from the socket.

        Returns:
            The decoded line without trailing newline characters.
        """
        assert self.sock is not None
        chunks = []
        while True:
            data = self.sock.recv(128)
            if not data:
                break
            chunks.append(data)
            if b"\n" in data:
                break
        return b"".join(chunks).decode(errors="ignore").strip()

    def send(self, cmd: str, retry: int = 1) -> str:
        """
        Send a command and return the ACK string.

        Args:
            cmd: ASCII command without trailing newline
            retry: Number of additional attempts after a failure

        Raises:
            RuntimeError: If no valid ACK is received after all attempts.
        """
        attempt = 0
        last_err = None
        while attempt <= retry:
            try:
                if self.sock is None:
                    self.connect()
                assert self.sock is not None
                self.sock.sendall((cmd + "\n").encode())
                ack = self._recv_line()
                if not ack:
                    raise RuntimeError("Empty ACK")
                self._log(cmd, ack)
                return ack
            except Exception as e:
                last_err = e
                self.close()
                attempt += 1
                if attempt <= retry:
                    time.sleep(self.reconnect_delay)
                    continue
                break
        raise RuntimeError(f"Command failed: {cmd}. Last error: {last_err}")

    def safe_g1(self) -> str:
        """
        Perform a safe transition to green on signal 1.
        """
        return self.send("SAFE:G1")

    def safe_g2(self) -> str:
        """
        Perform a safe transition to green on signal 2.
        """
        return self.send("SAFE:G2")

    def g1(self) -> str:
        """
        Set green on signal 1.
        """
        return self.send("G1")

    def y1(self) -> str:
        """
        Set yellow on signal 1.
        """
        return self.send("Y1")

    def r1(self) -> str:
        """
        Set red on signal 1.
        """
        return self.send("R1")

    def g2(self) -> str:
        """
        Set green on signal 2.
        """
        return self.send("G2")

    def y2(self) -> str:
        """
        Set yellow on signal 2.
        """
        return self.send("Y2")

    def r2(self) -> str:
        """
        Set red on signal 2.
        """
        return self.send("R2")

    def set_both(self, s1: str, s2: str) -> str:
        """
        Set both signals with a single command.

        Args:
            s1: Character among R, Y, G for signal 1
            s2: Character among R, Y, G for signal 2

        Returns:
            The ACK string from the Arduino.

        Raises:
            ValueError: If s1 or s2 is not in {R, Y, G}.
        """
        s1 = s1.upper()
        s2 = s2.upper()
        if s1 not in ("R", "Y", "G") or s2 not in ("R", "Y", "G"):
            raise ValueError("Allowed values: R, Y, G")
        return self.send(f"S:{s1}{s2}")

    def all_off(self) -> str:
        """
        Turn off all LEDs.
        """
        return self.send("ALL:OFF")

    def all_red(self) -> str:
        """
        Force the all-red safe state.
        """
        return self.send("ALL:RED")

    def test_cycle(self, n_cycles: int = 5, dwell: float = 2.0) -> None:
        """
        Alternate a simple safe cycle for quick demos.

        Args:
            n_cycles: Number of alternating cycles
            dwell: Duration in seconds of each green state
        """
        for _ in range(n_cycles):
            self.safe_g1()
            time.sleep(dwell)
            self.safe_g2()
            time.sleep(dwell)