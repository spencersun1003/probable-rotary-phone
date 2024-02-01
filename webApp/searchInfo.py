import requests
import json
from utilities import text2html,list2text

api_key = ""  # 替换为你的API密钥
cse_id = ""  # 替换为你的自定义搜索引擎ID
def google_search(query, api_key, cse_id, **kwargs):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'cx': cse_id,
        'key': api_key
    }
    params.update(kwargs)
    response = requests.get(url, params=params)
    return response.json()

def contains_keywords(item, keyword_a, keyword_b):
    title = item.get('title', '').lower()
    snippet = item.get('snippet', '').lower()
    return int(keyword_a.lower() in title or keyword_a.lower() in snippet) and \
           int(keyword_b.lower() in title or keyword_b.lower() in snippet)

def searchKeywords(kA,kB,query):
    # print("seaching for ",kA,kB,query)


    results = google_search(query, api_key, cse_id, num=5)  # 获取前3个结果
    keyword_presence = [contains_keywords(item, kA, kB) for item in results.get("items", [])]
    # print(f"关键词出现情况: {keyword_presence}")

    resultsText=""
    resultsText+="关键词出现情况: {}\n".format(list2text(keyword_presence))
    for i, item in enumerate(results.get("items", []), start=1):
        resultsText+="Result {}:".format(i)
        resultsText+="\nTitle: {}".format(item.get('title', 'No Title'))
        resultsText+="\nURL: {}".format(item.get('link', 'No URL'))
        resultsText+="\nSnippet: {}".format(item.get('snippet', 'No Snippet'))
        resultsText+="\n-----------\n"
    return {'keywordMatch:':text2html(list2text(keyword_presence),kA,kB),'results':text2html(resultsText,kA,kB)}

if __name__ == "__main__":
    keywords = ["代建华", "湖南师范大学"]  # 替换为你要检查的关键词
    query = keywords[0] + " " + keywords[1]
    searchKeywords(keywords[0],keywords[1],query)