#!/usr/bin/env python3
"""
Simple HTTP server for MS-Attack-Range Dashboard
This script starts a local web server to host the dashboard
"""

import http.server
import socketserver
import os
import webbrowser
import argparse
from urllib.parse import urlparse

# Default port
DEFAULT_PORT = 8080

def start_server(port=DEFAULT_PORT, open_browser=True):
    """Start the HTTP server and optionally open a browser"""
    
    # Get the directory of this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the dashboard directory
    os.chdir(current_dir)
    
    # Create the server
    handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            url = f"http://localhost:{port}"
            print(f"MS-Attack-Range Dashboard is running at: {url}")
            print("Press Ctrl+C to stop the server")
            
            # Open browser if requested
            if open_browser:
                webbrowser.open(url)
            
            # Start the server
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"Error: Port {port} is already in use. Try a different port.")
        else:
            print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MS-Attack-Range Dashboard Server")
    parser.add_argument("-p", "--port", type=int, default=DEFAULT_PORT,
                        help=f"Port to run the server on (default: {DEFAULT_PORT})")
    parser.add_argument("--no-browser", action="store_true",
                        help="Don't open the browser automatically")
    
    args = parser.parse_args()
    
    start_server(port=args.port, open_browser=not args.no_browser)
