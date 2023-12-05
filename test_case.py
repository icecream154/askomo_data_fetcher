import json
import re
import time
import uuid

from bs4 import BeautifulSoup
from playwright.sync_api import Response


def write_file(filename: str, content: str, dir: str = ""):
    with open("./pages/" + dir + filename, "w") as f:
        f.write(content)


def write_fileb(filename: str, content: bytes, dir: str = ""):
    with open("./pages/" + dir + filename, "wb") as f:
        f.write(content)


def save_response(response: Response):
    subdir = "mse/"
    if response is not None:
        resp_body = response.body()
        f_name = str(uuid.uuid4()) + ".txt"
        req_url = response.request.url
        print("REQ URL: " + req_url)
        if req_url.endswith(".json") or req_url.endswith(".png") or req_url.endswith(".css") \
                or req_url.endswith(".jpg") or req_url.endswith(".jpeg"):
            f_name = req_url[req_url.rfind("/") + 1:]
            print("RESP TO FILE: " + f_name)
            write_fileb(f_name, resp_body, dir="req/" + subdir)
        else:
            try:
                req_str = resp_body.decode("utf-8")
                req_json = json.loads(req_str)
                f_name = f_name[:len(f_name) - 4] + ".json"
            except:
                pass
            print("RESP TO FILE: " + f_name)
            write_fileb(f_name, resp_body, dir="req/" + subdir)


if __name__ == '__main__':
    from playwright.sync_api import sync_playwright as playwright, Response

    with playwright() as pw:
        webkit = pw.webkit.launch(headless=False)
        context = webkit.new_context()  # 需要创建一个 context
        page = context.new_page()  # 创建一个新的页面
        page.on("response", save_response)
        page.goto("https://mse.isri.cmu.edu/applicants/mse-as/index.html")
        # 使用 JavaScript 将页面滚动到底部
        page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
        page.wait_for_load_state('networkidle')
        c = page.content()
        # print(c)
        time.sleep(3)
        print(c == page.content())
        write_file("cmu-mse-applicants.html", page.content())
        webkit.close()
