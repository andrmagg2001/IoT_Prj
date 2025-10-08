import argparse
from iot_client import TrafficLightClient


def main() -> None:
    """
    Parse CLI arguments and run either a demo cycle or a single send.
    """
    parser = argparse.ArgumentParser(description="Raspberry → Arduino Smart TL client")
    parser.add_argument("--ip", required=True, help="Arduino AP IP, e.g., 192.168.4.1")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--timeout", type=float, default=3.0)
    parser.add_argument("--log", default=None, help="CSV log path")
    parser.add_argument("--mode", choices=["cycle", "send"], default="cycle")
    parser.add_argument("--cycles", type=int, default=5)
    parser.add_argument("--dwell", type=float, default=2.0)
    parser.add_argument("--send", dest="single_cmd", default=None)
    args = parser.parse_args()

    with TrafficLightClient(
        host=args.ip,
        port=args.port,
        timeout=args.timeout,
        log_path=args.log,
    ) as tl:
        if args.mode == "cycle":
            tl.test_cycle(n_cycles=args.cycles, dwell=args.dwell)
        else:
            if not args.single_cmd:
                raise SystemExit('Specify --send "COMMAND" when mode=send')
            ack = tl.send(args.single_cmd)
            print(ack)


if __name__ == "__main__":
    main()