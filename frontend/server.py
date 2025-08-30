#!/usr/bin/env python3
"""
简单的前端服务器，支持单页应用路由
"""

import os
import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote
import re

class SinglePageAppHandler(BaseHTTPRequestHandler):
    """支持SPA路由的HTTP请求处理器"""

    def __init__(self, *args, **kwargs):
        self.static_dir = os.path.dirname(os.path.abspath(__file__))
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """处理GET请求"""
        parsed_path = urlparse(self.path)
        path = unquote(parsed_path.path)

        # 如果路径匹配 /offer/* 格式，返回index.html
        if re.match(r'^/offer/[a-zA-Z0-9_-]+/?$', path):
            self.serve_spa_route()
            return

        # 处理静态文件
        if path == '/' or path == '':
            path = '/index.html'

        # 构建文件路径
        file_path = os.path.join(self.static_dir, path.lstrip('/'))

        # 检查文件是否存在
        if os.path.isfile(file_path):
            self.serve_static_file(file_path)
        else:
            self.send_404()

    def serve_spa_route(self):
        """为SPA路由提供index.html"""
        index_path = os.path.join(self.static_dir, 'index.html')
        self.serve_static_file(index_path)

    def serve_static_file(self, file_path):
        """提供静态文件"""
        try:
            with open(file_path, 'rb') as file:
                content = file.read()

            # 获取MIME类型
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type is None:
                mime_type = 'application/octet-stream'

            # 发送响应
            self.send_response(200)
            self.send_header('Content-Type', mime_type)
            self.send_header('Content-Length', str(len(content)))

            # CORS headers for development
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')

            self.end_headers()
            self.wfile.write(content)

        except Exception as e:
            print(f"Error serving file {file_path}: {e}")
            self.send_500()

    def send_404(self):
        """发送404错误"""
        self.send_response(404)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

        error_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>404 - 页面不存在</title>
            <meta charset="UTF-8">
        </head>
        <body>
            <h1>404 - 页面不存在</h1>
            <p>请求的页面未找到。</p>
            <p><a href="/">返回首页</a></p>
        </body>
        </html>
        """
        self.wfile.write(error_html.encode('utf-8'))

    def send_500(self):
        """发送500错误"""
        self.send_response(500)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()

        error_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>500 - 服务器错误</title>
            <meta charset="UTF-8">
        </head>
        <body>
            <h1>500 - 服务器错误</h1>
            <p>服务器处理请求时出现错误。</p>
        </body>
        </html>
        """
        self.wfile.write(error_html.encode('utf-8'))

    def do_OPTIONS(self):
        """处理OPTIONS请求（CORS预检）"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server(port=3000):
    """启动服务器"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, SinglePageAppHandler)

    print(f"🌐 前端服务器启动成功")
    print(f"📍 地址: http://localhost:{port}")
    print(f"🎯 邀请码页面: http://localhost:{port}/offer/fellou")
    print(f"🔧 后端API: http://localhost:8000")
    print(f"📚 API文档: http://localhost:8000/docs")
    print("按 Ctrl+C 停止服务器")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
        httpd.shutdown()

if __name__ == '__main__':
    run_server()
