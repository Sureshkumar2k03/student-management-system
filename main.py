"""Entry point.

    python main.py          -> console menu
    python main.py --web    -> web server + React frontend (http://127.0.0.1:8000)
"""

import sys

import cli
import server

if __name__ == "__main__":
    if "--web" in sys.argv:
        port = int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else 8000
        server.run(port=port)
    else:
        cli.run()
