import requests
from bs4 import BeautifulSoup


# def search_google(query):
#     # 构造Google搜索的URL
#     url = f"https://www.google.com/search?q={query}"
#     headers = {'User-Agent': 'Mozilla/5.0'}
#
#     # 发起请求
#     response = requests.get(url, headers=headers)
#     print(response.text)
#     soup = BeautifulSoup(response.text, 'html.parser')
#
#     # 解析前三个搜索结果
#     results = soup.find_all('div', class_='tF2Cxc', limit=3)
#     return results
def search_google(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)
    print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 定位到id为'rso'的元素，然后提取其中的每个div（搜索结果）
    search_results = soup.find('div', id='rso').find_all('div', recursive=False)[:3]

    return search_results


def count_keywords(results, keywords):
    count = 0
    for result in results:
        text = result.get_text().lower()
        if all(keyword.lower() in text for keyword in keywords):
            count += 1
    return count


def main():
    # query = "Your Search Query"  # 替换为你的搜索查询
    keywords = ["代建华", "湖南师范大学"]  # 替换为你要检查的关键词
    query=keywords[0]+" "+keywords[1]

    results = search_google(query)
    print(results)
    count = count_keywords(results, keywords)

    print(f"在前三个搜索结果中，'{keywords[0]}' 和 '{keywords[1]}' 同时出现的次数为: {count}")


if __name__ == "__main__":
    main()