# Bare-minimum demo of a "new internet protocol" idea:
# - JSON messages over TCP (newline-delimited)
# - Client sends a semantic QUERY (ask by meaning, not by URL)
# - Server resolves from a tiny in-memory "object store" and replies
#
# Usage:
#   python weblet.py server 127.0.0.1 8088
#   python weblet.py client 127.0.0.1 8088 '{"type":"quote","mood":"motivational"}'
#
# Notes:
# - Local-only toy. No security. Just for play.

import sys
import json
import socket
import threading

HELLO = {"v": 0, "kind": "HELLO", "id": "srv", "negotiate": {"offer": ["object/json", "object/text"]}}

# Tiny "semantic object store"
STORE = [
    {"id": "q1", "type": "quote", "mood": "motivational", "text": "Stay curious. Build boldly."},
    {"id": "q2", "type": "quote", "mood": "calm", "text": "Slow is smooth, smooth is fast."},
    {"id": "w1", "type": "weather", "location": "Vadodara", "time": "now", "temp_c": 33.5},
]


def resolve(intent):
    """Naively resolve a query intent against the in-memory store."""
    for obj in STORE:
        if all(obj.get(k) == v for k, v in intent.items()):
            return obj
    return None


def handle_client(conn, addr):
    """Handle a single client connection."""
    conn.sendall((json.dumps(HELLO) + "\n").encode())
    buf = b""
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            buf += data
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                if not line.strip():
                    continue
                try:
                    msg = json.loads(line.decode())
                except Exception as exc:  # pylint: disable=broad-except
                    err = {"v": 0, "kind": "ERROR", "id": "srv", "error": f"bad json: {exc}"}
                    conn.sendall((json.dumps(err) + "\n").encode())
                    continue

                if msg.get("kind") == "QUERY":
                    intent = msg.get("intent", {})
                    obj = resolve(intent)
                    if obj:
                        rep = (msg.get("negotiate") or {}).get("pref", "object/json")
                        if rep == "object/text":
                            out = {
                                "v": 0,
                                "kind": "RESULT",
                                "id": msg.get("id"),
                                "object": {"text": obj.get("text", str(obj))},
                            }
                        else:
                            out = {"v": 0, "kind": "RESULT", "id": msg.get("id"), "object": obj}
                    else:
                        out = {"v": 0, "kind": "ERROR", "id": msg.get("id"), "error": "no-match"}
                    conn.sendall((json.dumps(out) + "\n").encode())
    finally:
        conn.close()


def server(host, port):
    """Run the toy server."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, int(port)))
    sock.listen(5)
    print(f"[server] listening on {host}:{port}")
    try:
        while True:
            conn, addr = sock.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    finally:
        sock.close()


def client(host, port, query_json, pref="object/json"):
    """Run the toy client."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, int(port)))
    file = sock.makefile("rwb", buffering=0)

    line = file.readline()
    if line:
        print(line.decode().strip())

    msg = {
        "v": 0,
        "kind": "QUERY",
        "id": "cli-1",
        "intent": json.loads(query_json),
        "negotiate": {"pref": pref},
    }
    file.write((json.dumps(msg) + "\n").encode())
    resp = file.readline()
    if resp:
        print(resp.decode().strip())
    sock.close()


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(
            "Usage:\n  python weblet.py server <host> <port>\n  python weblet.py client <host> <port> '<query_json>'"
        )
        sys.exit(1)

    mode = sys.argv[1]
    if mode == "server":
        server(sys.argv[2], sys.argv[3])
    elif mode == "client":
        if len(sys.argv) < 5:
            print("client needs a JSON query, e.g. '{\"type\":\"quote\",\"mood\":\"motivational\"}'")
            sys.exit(1)
        client(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print("mode must be 'server' or 'client'")
