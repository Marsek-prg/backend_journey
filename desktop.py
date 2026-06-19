"""Desktop launcher for the Task Tracker web application."""

import json
import threading
import time
from urllib.error import URLError
from urllib.request import urlopen

import uvicorn
import webview

from app.main import app

HOST = "127.0.0.1"
PORT = 8000
APP_URL = f"http://{HOST}:{PORT}"
APP_TITLE = "Backend Journey Task Tracker"


def task_tracker_is_running() -> bool:
    """Return True when this Task Tracker already uses the desktop port."""
    try:
        with urlopen(f"{APP_URL}/openapi.json", timeout=1) as response:
            schema = json.load(response)
            return schema.get("info", {}).get("title") == APP_TITLE
    except (URLError, TimeoutError, json.JSONDecodeError):
        return False


def wait_for_server(
    server: uvicorn.Server,
    server_thread: threading.Thread,
    timeout: float = 10.0,
) -> None:
    """Wait until this launcher's Uvicorn server accepts requests."""
    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:
        if not server_thread.is_alive():
            raise RuntimeError(
                f"Could not start the local server. Port {PORT} may already be in use."
            )

        if server.started:
            try:
                with urlopen(APP_URL, timeout=0.5) as response:
                    if response.status == 200:
                        return
            except (URLError, TimeoutError):
                pass

        time.sleep(0.1)

    raise RuntimeError(f"The local server did not start at {APP_URL}")


def main() -> None:
    """Start FastAPI in the background and show it in a desktop window."""
    server = None
    server_thread = None

    if not task_tracker_is_running():
        config = uvicorn.Config(app, host=HOST, port=PORT, log_level="info")
        server = uvicorn.Server(config)
        server_thread = threading.Thread(target=server.run, daemon=True)
        server_thread.start()

    try:
        if server is not None and server_thread is not None:
            wait_for_server(server, server_thread)
        webview.create_window(
            "Task Tracker",
            APP_URL,
            width=1000,
            height=700,
            min_size=(700, 500),
        )
        webview.start()
    finally:
        if server is not None and server_thread is not None:
            server.should_exit = True
            server_thread.join(timeout=5)


if __name__ == "__main__":
    main()
