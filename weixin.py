from urllib.parse import urlencode
import requests
from requests.exceptions import ConnectionError

base_url = 'http://weixin.sogou.com/weixin?'

headers = {
    'Cookie': 'CXID=DE52D1959DB9E082639E447D59D76B75; SUID=DF408D3D3765860A5B2202C10002D7C1; SUV=003B17820E9B716F5B417DF8E640E846; IPLOC=CN4403; ld=pZllllllll2bqmNoQCbXzOHQiLPbqmN$5YClblllll9llllxpllll5@@@@@@@@@@; cd=1532421994&1797734bc306ed0ac573cadad037f72e; rd=IZllllllll2bqjXcQCyIMqHQiLPbqmN$5YCxXllllllllllxpllll5@@@@@@@@@@; ad=5lllllllll2bwkaxlllllVHgfOZlllll5YClTZllll9lllllpqxlw@@@@@@@@@@@; SNUID=CE962B93242054D7527CE146254E87D2; ABTEST=0|1532662654|v1; weixinIndexVisited=1; JSESSIONID=aaaMI0Wfdmsbtc04sBHsw; ppinf=5|1532662751|1533872351|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTo1OlNldmVufGNydDoxMDoxNTMyNjYyNzUxfHJlZm5pY2s6NTpTZXZlbnx1c2VyaWQ6NDQ6bzl0Mmx1S1BSSmlCVTkybTR2Mk5rQjcwajd3TUB3ZWl4aW4uc29odS5jb218; pprdig=h3ZvbHjrQkEcyu1xziXpMJCRaId6iiKkId430vpCxPAtCJnSN7m_HOtksc82Mm9wU6B_rUw14UU1ptA_II2ZLMCd18I9fEi4eZufcGcSfuMqmd_UkHERbuA_S1nibT7duBdeOCGEGMfcialnSbWf2pgObJpz-jnEmAjLYzphiQk; sgid=11-30473717-AVtak99xQEShXOEpgc9247U; ppmdig=15326627510000001f9fd0176d7b00545fcbf0868885302d; sct=5',
    'Host': 'weixin.sogou.com',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

keyword = '风景'

def get_html(url):
    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            #Need Proxy
            print('302')
    except ConnectionError:
        return get_html(url)


def get_index(keyword, page):
    data = {
        'query': keyword,
        'type': 2,
        'page': page,
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html

def main():
    for page in range(1, 101):
        html = get_index(keyword, page)
        print(html)

if __name__ == '__main__':
    main()

