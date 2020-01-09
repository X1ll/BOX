#爬取豆瓣电影250
import requests # 导入网页请求库
from bs4 import BeautifulSoup # 导入网页解析库
import json

def get_requests(url):
    # 更改请求头，防止反爬
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
    r = requests.get(url, headers=headers)  # 对目标网站发出请求
    return r.content

def parse(text):
    soup = BeautifulSoup(text, 'html.parser') #解析网页
    movie_list = soup.find_all('div', class_ = 'item')

    for movie in movie_list:
        adict = {}
        #电影名
        adict['title'] = movie.find('span', class_ = 'title').text
        #评分
        adict['score'] = movie.find('span', class_ = 'rating_num').text
        #精彩评论
        quote = movie.find('span',class_='inq')
        adict['quote'] = quote.text if quote else None
        #评论人数
        star = movie.find('div',class_='star')
        adict['comment_num'] = star.find_all('span')[-1].text[:-3]
        result_list.append(adict)

    #下一页
    next = soup.find('span',class_='next').a
    if next:
        next_url = base_url+next['href']
        text = get_requests(next_url)
        parse(text)

def write_json(result):
    #写入JSON文件
    s = json.dumps(result, indent=4, ensure_ascii= False)
    with open('movies.json','w',encoding='utf-8') as f:
        f.write(s)

def main():
    text = get_requests(base_url)
    parse(text)
    write_json(result_list)

if __name__ == '__main__':
    base_url = 'https://movie.douban.com/top250'
    result_list=[]
    main()