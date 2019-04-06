

import socketserver
import http.server as http

PORT=8000
handler = http.SimpleHTTPRequestHandler
handler.extensions_map['.svg']='image/svg+xml'

print('Starting server...', PORT)
httpd = socketserver.TCPServer(('', PORT), handler)
httpd.serve_forever()
