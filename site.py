from http.server import HTTPServer, BaseHTTPRequestHandler
import markdown
import subprocess
from typing import List

def shell_out(command: List[str]) -> str:
    return subprocess.run(
        command, capture_output=True, encoding='utf-8'
    ).stdout.strip()

port = 8080
git_url = shell_out(["git","config", "--get", "remote.origin.url"])
git_repo = shell_out(["basename", git_url, ".git"])
git_sha = shell_out(["git", "rev-parse", "HEAD"])
readme = markdown.markdown(open('README.md').read())
html = """
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
""".format(git_repo, git_sha, readme)

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(h):
        h.send_response(200)
        h.end_headers()
        h.wfile.write(html.encode())

def run_server(server_class=HTTPServer, handler_class=MyHandler):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run_server()