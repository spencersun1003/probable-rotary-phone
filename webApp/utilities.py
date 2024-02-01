import re


def list2text(lst):
    # 将列表转换为字符串
    converted_string = ','.join([str(element) for element in lst])
    text = '['+converted_string+']\n'
    print(text)
    return text


def text2html(text, keyword1, keyword2):
    # 转义特殊字符以避免在正则表达式中出错
    keyword1 = re.escape(keyword1)
    keyword2 = re.escape(keyword2)

    # 将关键词替换为加粗红色文本
    text = re.sub(f'({keyword1})', r'<b style="color:red;">\1</b>', text)
    text = re.sub(f'({keyword2})', r'<b style="color:red;">\1</b>', text)

    # 将换行符转换为HTML换行标签
    text = text.replace('\n', '<br>')

    # 正则表达式匹配网址
    url_pattern = re.compile(r'(https?://[^\s]+)')

    # 将网址转换为超链接
    text = url_pattern.sub(r'<a href="\1" target="_blank">\1</a>', text)

    return text

# def text2html(text):
#     # 将换行符转换为HTML换行标签
#     html_text = text.replace('\n', '<br>')
#
#     # 正则表达式匹配网址
#     url_pattern = re.compile(
#         r'(https?://[^\s]+)'
#     )
#
#     # 将网址转换为超链接
#     html_text = url_pattern.sub(r'<a href="\1" target="_blank">\1</a>', html_text)
#
#     return html_text