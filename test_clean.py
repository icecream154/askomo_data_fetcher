import markdownify
from bs4 import BeautifulSoup
from html2text import HTML2Text

if __name__ == '__main__':
    html_filename = "stat-uchicago-ms"
    # 读取HTML文件的内容
    with open("./pages/" + html_filename + ".html", "r") as file:
        html_content = file.read()
        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(html_content, 'html.parser')
        # 找到所有的style和script标签并删除它们
        for tag in soup(["style", "script"]):
            tag.decompose()
        # 获取处理后的HTML内容
        new_html_content = str(soup)

    # 将处理后的HTML内容写回文件
    with open("./pages/clean-" + html_filename + ".html", "w") as file:
        file.write(new_html_content)

    converter = HTML2Text()
    raw_text = converter.handle(new_html_content)
    with open("./pages/clean-" + html_filename + ".txt", "w") as file:
        file.write(raw_text)

    with open("./pages/clean-" + html_filename + ".md", "w") as file:
        file.write(markdownify.markdownify(new_html_content))