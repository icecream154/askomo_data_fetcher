import json
import os
import time
import uuid

import bs4
from playwright.sync_api import Browser, Response, BrowserContext
from playwright.sync_api import sync_playwright as playwright
from bs4 import BeautifulSoup

from page_dealer_context import PageDealerContext

curr_page_url = ""


def write_fileb(filepath: str, content: bytes):
    with open(filepath, "wb") as f:
        f.write(content)


def write_file(filepath: str, content: str):
    with open(filepath, "w") as f:
        f.write(content)


def page_response_dealer(response: Response):
    global curr_page_url
    response_uuid = str(uuid.uuid4())
    if response is not None:
        resp_body = response.body()
        req_url = response.request.url
        print("REQ URL: " + req_url)
        try:
            resp_str = resp_body.decode("utf-8")
            try:
                resp_json = json.loads(resp_str)
                write_file(PageDealerContext.get_json_result_path_map()[curr_page_url] + "/" +
                           response_uuid + "-URL.txt", req_url)
                write_fileb(PageDealerContext.get_json_result_path_map()[curr_page_url] + "/" +
                            response_uuid + ".json", resp_body)
            except Exception:
                try:
                    soup = BeautifulSoup(resp_str, 'html.parser')
                    if soup is not None:
                        write_file(PageDealerContext.get_html_result_path_map()[curr_page_url] + "/" +
                                   response_uuid + "-URL.txt", req_url)
                        write_fileb(PageDealerContext.get_html_result_path_map()[curr_page_url] + "/" +
                                    response_uuid + ".html", resp_body)
                    else:
                        write_file(PageDealerContext.get_utf_result_path_map()[curr_page_url] + "/" +
                                   response_uuid + "-URL.txt", req_url)
                        write_fileb(PageDealerContext.get_utf_result_path_map()[curr_page_url] + "/" +
                                    response_uuid + ".txt", resp_body)
                except Exception:
                    write_file(PageDealerContext.get_utf_result_path_map()[curr_page_url] + "/" +
                               response_uuid + "-URL.txt", req_url)
                    write_fileb(PageDealerContext.get_utf_result_path_map()[curr_page_url] + "/" +
                                response_uuid + ".txt", resp_body)
        except Exception:
            response_file_prefix = ".txt"
            if req_url.endswith(".png") or req_url.endswith(".jpg") or req_url.endswith(".jpeg"):
                response_file_prefix = req_url[req_url.rfind("."):]
            write_file(PageDealerContext.get_resource_result_path_map()[curr_page_url] + "/" +
                       response_uuid + "-URL.txt", req_url)
            write_fileb(PageDealerContext.get_resource_result_path_map()[curr_page_url] + "/" +
                        response_uuid + response_file_prefix, resp_body)


def deal_page(base_result_path: str, page_url: str, page_waiting_list: list[str], context: BrowserContext):
    # 为该页面创建存储路径
    global curr_page_url
    curr_page_url = page_url
    result_uuid = str(uuid.uuid4())
    result_path = base_result_path + "/" + result_uuid
    PageDealerContext.get_result_path_map()[page_url] = result_path
    os.mkdir(result_path)
    write_file(result_path + "/url.txt", page_url)
    # 分别创建 html路径，json路径，utf-8路径，其他资源文件路径
    html_path = result_path + "/html"
    PageDealerContext.get_html_result_path_map()[page_url] = html_path
    os.mkdir(html_path)
    json_path = result_path + "/json"
    PageDealerContext.get_json_result_path_map()[page_url] = json_path
    os.mkdir(json_path)
    utf_path = result_path + "/utf"
    PageDealerContext.get_utf_result_path_map()[page_url] = utf_path
    os.mkdir(utf_path)
    resource_path = result_path + "/resource"
    PageDealerContext.get_resource_result_path_map()[page_url] = resource_path
    os.mkdir(resource_path)

    # 使用 playwright 打开页面
    page = context.new_page()  # 创建一个新的页面
    page.set_default_timeout(6000000)
    page.on("response", page_response_dealer)
    page.goto(page_url)
    # 使用 JavaScript 将页面滚动到底部
    page.evaluate("window.scrollTo({top: document.body.scrollHeight,behavior: 'smooth'});")
    # 等待所有请求完毕
    time.sleep(2)
    page.wait_for_load_state('networkidle')
    write_file(html_path + "/main.html", page.content())
    page.close()


if __name__ == "__main__":
    with playwright() as pw:
        webkit = pw.webkit.launch(headless=False)
        context = webkit.new_context()
        context.set_default_navigation_timeout(12000000)
        context.set_default_timeout(6000000)
        deal_page("../result_data/cmu-ml",
                  "https://www.ml.cmu.edu/academics/primary-ms-machine-learning-masters.html", [],
                  context)
