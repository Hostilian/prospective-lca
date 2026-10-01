"""Static local server for the generated dashboard/report."""

from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def serve_directory(directory: str | Path, *, host: str = "127.0.0.1", port: int = 8765) -> None:
    root = Path(directory).resolve()
    if not root.exists():
        raise FileNotFoundError(root)
    handler = partial(SimpleHTTPRequestHandler, directory=str(root))
    server = ThreadingHTTPServer((host, port), handler)
    print(f"Serving {root} at http://{host}:{port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server")
    finally:
        server.server_close()

