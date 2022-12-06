import os
import sys
import urllib.request
import urllib.parse
import datetime
import time
import json

client_id = 'SH3HwdwkmEE_HUKzTyxW'
client_secret = 'QOikKo2ZEW'


# ulr 접속 요청 후 응답리턴 함수

def getRequestUrl(url):
    req = urllib.request.Request(url)
    req.add_header('X-Naver-Client-Id',client_id)
    req.add_header('X-Naver-Client-Secret',client_secret)

    try:
        res = urllib.request.urlopen(req)
        if res.getcode() == 200: #200 OK 40X error, 50X Server error
            print(f'[{datetime.datetime.now()}] Url Request success')
            return res.read().decode('utf-8')
    except Exception as e:
        print(e)
        print(f'[{datetime.datetime.now()}] Error for URL : {url}')
        return None
# 핵심함수, 네이버API 검색
def getNaverSerch(node, srcText, start, display):
    base = 'https://openapi.naver.com/v1/search'
    node = f'/{node}.json'
    text = urllib.parse.quote(srcText) # url주소에 맞추서 파싱
    params = f'?query={text}&start={start}&display={display}'


    url = base + node + params

    resDecode = getRequestUrl(url)

    if resDecode == None:
        return None
    else:
        return json.loads(resDecode)

def getPostData(post, jsonResult, cnt):
    title = post['title']
    description = post['description']
    originallink = post['originallink']
    link = post['link']

    pubDate = datetime.datetime.strptime(post['pubDate'], '%a, %d %b %Y %H:%M:%S +0900')
    pubDate = pubDate.strftime('%Y-%m-%d %H:%M:%S') #2022-08-02 15:56:34

    jsonResult.append({'cnt':cnt, 'title':title, 'description':description,
                        'originallink':originallink, 'link':link, 'pubDate':pubDate})


# 실행최초함수
def main():
    node = 'news'
    srcText = input('검색어를 입력하세요: ')
    cnt = 0
    jsonResult=[]

    jsonRes = getNaverSerch(node, srcText, 1 , 50)

    # print(jsonRes)
    total = jsonRes['total'] # 검색된 뉴스 개수

    while ((jsonRes !=None) and (jsonRes['display'] !=0)):
        for post in jsonRes['items']:
            cnt +=1
            getPostData(post, jsonResult, cnt)

        start = jsonRes['start'] + jsonRes['display'] #1+50번째 페이지 부터 다시 시작
        jsonRes = getNaverSerch(node, srcText, start ,50)

    print(f'전체 검색 : {total}건')

    #file output
    with open(f'./{srcText}_naver_{node}.json',mode='w', encoding='utf8') as outfile:
        jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(jsonFile)

    print(f'가져온 데이터 : {cnt}건')
    print(f'{srcText}_naver_{node}.json SAVED')
    
if __name__=='__main__':
    main()