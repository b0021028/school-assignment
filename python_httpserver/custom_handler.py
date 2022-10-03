#!/usr/bin/python
#-*- coding: utf-8 -*-

from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler

from os import path as filepath


#ウェブサーバのルートディレクトリ 例 www/html 例2　/usr/share/www/html 例3 ../html デフォルトで .
ROOTDIRECTORY = "."

# path と query を切り分ける
def splitURN(pathAndQuery="/") -> dict[str, str]:

    query = ""
    path = str(pathAndQuery)

    if "?" in path:
        path, query = path.split("?", 1)


    return {"path":path, "query":query}


class CustomHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        # google 対応
        def defaultFunction():#お手本 orizginal file
            nonlocal self
            f = self.send_head()
            if f:
                try:
                    self.copyfile(f, self.wfile)
                finally:
                    f.close()
            return

        # 要求された path を取得し クエリ―と分けて ルートdirをパスに追加
        path = ROOTDIRECTORY
        path_query = splitURN(self.path)
        path += path_query["path"]


        # ファイルは 存在すれば 開く
        if filepath.isfile(path):

            # ファイルからテキスト読み込み
            # file type check
            tmp = path.rsplit("/", 1)[-1].split(".", 1)
            if len(tmp) == 2 and tmp[1] in ("", "txt", "htm", "html", "php", "xml", "json"):
                self.send_header("Content-type", "text/html; charset=utf-8")
                responseText = open(path, encoding="utf-8").read()

            # unknown file
            else:
                return defaultFunction()




        # ディレクトリは index.html を開く
        elif filepath.isdir(path) or not path:
            if filepath.isfile(path + "index.html"):
                path += "index.html"
                responseText = open(path, encoding="utf-8").read()
    

            else:
                return defaultFunction()
                 

        # 存在しない場合 405 で Not Found と表示
        else:
            self.send_response(405, "Not Found")
            responseText = "Not Found"
            self.end_headers()
            # responseText の byte変換
            html = bytes(responseText, encoding="utf-8")
            # byte変換 した responseText 送信
            self.wfile.write(html)
            return


        print("="*9)
        print(f"requestPath:{self.path}\nresponsPath:{path}\niserror:{not filepath.isfile(path)}")
        print("="*9)

        # response header
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        # responseText の byte変換
        html = bytes(responseText, encoding="utf-8")

        # byte変換 した responseText 送信
        self.wfile.write(html)



# 定数, 及び, インスタンス
ip = "127.0.0.1"
port = 8000

handler = CustomHandler
server = HTTPServer((ip, port), handler)


try:
    server.serve_forever()
except KeyboardInterrupt:
    print("stop server")