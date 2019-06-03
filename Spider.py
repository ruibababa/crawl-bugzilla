# @Author  : ShiRui
import requests
from bs4 import BeautifulSoup

parent = []
headers = {
    'cookie': 'lastCity=101010100; JSESSIONID=""; __g=-; _uab_collina=155269833969139683439973; __c=1552698410; '
              '__l=r=https%3A%2F%2Fwww.zhipin.com%2F&l=%2Fwww.zhipin.com%2Fjob_detail%2F%3Fquery%3D%25E5%25A4%25A7'
              '%25E6%2595%25B0%25E6 '
              '%258D%25AE%26city%3D101010100%26industry%3D%26position%3D; '
              'Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1552698340, '
              '1552698711; __a=34449685.1552698337.1552698337.1552698410.7.2.6.7; '
              'Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1552698721',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 '
                  'Safari/537.36',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'referedr': 'https://www.zhipin.com/job_detail/?query=%E5%A4%A7%E6%95%B0%E6%8D%AE&city=101010100&industry=&position=',
    'authority': 'www.zhipin.com',
    'x-requested-with': 'XMLHttpRequest',
}


def spiderParentHtml():
    html = requests.get("https://bugzilla.mozilla.org/describecomponents.cgi?product=Firefox&tdsourcetag=s_pcqq_aiomsg",
                        headers).content.decode("utf8")
    soup = BeautifulSoup(html, "lxml")
    for i in soup.select(".component header h2 a"):
        url = "https://bugzilla.mozilla.org/" + i.get("href")
        parent.append(url)
    return parent


def spiderChildren():
    childrenUrl = spiderParentHtml()
    for url in childrenUrl:
        html = requests.get(url, headers).content.decode("utf8")
        soup = BeautifulSoup(html, "lxml")
        for i in soup.select(".bz_short_desc_column a"):
            url = "https://bugzilla.mozilla.org/" + i.get("href")
            yield url
