from http.server import HTTPServer, BaseHTTPRequestHandler
from subprocess import run as shell_out
from markdown import markdown

PORT = 8080
GIT_URL = shell_out(["git","config","--get","remote.origin.url"], capture_output=True, encoding='utf-8').stdout.strip()
GIT_REPO = shell_out(["basename",GIT_URL,".git"], capture_output=True, encoding='utf-8').stdout.strip()
GIT_SHA = shell_out(["git","rev-parse","HEAD"], capture_output=True, encoding='utf-8').stdout.strip()
README = markdown(open('README.md').read())
HTML = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{}</title>
  </head>
  <body>
    <p>GIT SHA: {}</p>
    <p>
      README.md: </n>
      {}
    </p>
  </body>
</html>
""".format(GIT_REPO, GIT_SHA, README)

class Handler(BaseHTTPRequestHandler):
    def do_GET(h):
        h.send_response(200)
        h.end_headers()
        h.wfile.write(HTML.encode())

def run_server(server_class=HTTPServer, handler_class=Handler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run_server()