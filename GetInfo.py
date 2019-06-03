# @Author  : ShiRui
import time

import requests
from bs4 import BeautifulSoup
import pymysql
from Spider import spiderChildren


def getInfo(url):
    dic = {}
    status = {}
    people = {}
    tracking = {}
    flags = {}
    details = {}

    html = requests.get(url, headers).content.decode("utf8")
    soup = BeautifulSoup(html, "lxml")
    # 提取statu中的信息
    for i in soup.select("#field-value-bug_id"):
        dic['id'] = i.text.replace("\n", "").replace(" ", "")

    for i in soup.select("#field-value-product .dropdown-button"):
        status['Product'] = i.text.replace("\n", "").replace(" ", "")

    for i in soup.select(".value #field-value-delta_ts .rel-time"):
        status["Reported"] = i.get("title")

    for i in soup.select("#field-value-component .dropdown-button"):
        status["Component"] = i.text.replace("\n", "").replace(" ", "")

    for i in soup.select(".value #field-value-delta_ts .rel-time"):
        status["Modified"] = i.get("title")

    for i in soup.select("#field-value-bug_type"):
        status['Type'] = i.text.replace("\n", "")

    importance = ""
    for i in soup.select(".value #field-value-priority"):
        importance += i.text
    for i in soup.select(".value #field-value-bug_severity"):
        importance += i.text
    status["Importance"] = importance.replace(" ", "").replace("\n", " ")

    for i in soup.select("#field-value-status-view"):
        status["Status"] = i.text.replace("\n", "").replace(" ", "")

    dic['status'] = status

    # 提取People中的信息
    for i in soup.select("#field-value-assigned_to .email .fna"):
        people["Assignee"] = i.text.replace("\n", "").replace(" ", "")

    for i in soup.select("#field-value-reporter .email .fna"):
        people["Reporter"] = i.text.replace("\n", "").replace(" ", "")

    for i in soup.select("#field-value-triage_owner .email .fna"):
        people["Triage Owner"] = i.text.replace("\n", "").replace(" ", "")

    for i in soup.select(".container #cc-summary"):
        people["CC"] = i.text.replace("\n", "").replace(" ", "")
    dic['People'] = people

    # 提取Tracking中的信息
    for i in soup.select(".value #field-value-version"):
        tracking["Version"] = i.text.replace("\n", "").replace(" ", "")

    for i in soup.select(".bug-list .bz_bug_link"):
        tracking["Blocks"] = i.text.replace("\n", "").replace(" ", "")

    for i in soup.select(".value #field-value-target_milestone"):
        tracking["Target"] = i.text.replace("\n", "").replace(" ", "")

    for i in soup.select(".container #field-value-dependencytree"):
        tracking["Dependency"] = i.text.replace("\n", "").replace(" ", "")

    for i in soup.select(".value #field-value-cf_fx_points"):
        tracking["Points"] = i.text.replace("\n", "").replace(" ", "")
    dic['Tracking'] = tracking

    # 提取Tracking中的信息
    for i in soup.select("#module-firefox-tracking-flags-content .fields-lhs .edit-hide"):
        flags["Firefox_Tracking_Flags"] = i.text.replace("\n", "").strip(" ")
    dic["Firefox_Tracking_Flags"] = flags

    # 提取Details中的信息
    for i in soup.select(".value #field-value-status_whiteboard"):
        details['Whiteboard'] = i.text.replace("\n", "").strip(" ")

    for i in soup.select(".field .container"):
        details['Votes'] = i.text.replace("\n", "").strip(" ")
    dic['Details'] = details

    # 提取comment中的信息
    comment = ""
    for i in soup.select(".change-set .comment-text"):
        comment += i.text
    dic['Comment'] = comment.replace("\n", " ")

    return dic


if __name__ == '__main__':
    try:
        db = pymysql.connect(host="127.0.0.1", port=3306, user="yourName", passwd="yourPassword", db="yourDatabase")
        cursor = db.cursor()
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
        for url in spiderChildren():
            info = getInfo(url)

            insert_sql = """
                   insert into info(id, status, People, tracking, Firefox_Tracking_Flags, Details, Comment)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                   """
            params = (
                str(info["id"]), str(info["status"]), str(info["People"]), str(info["Tracking"]), str(info["Firefox_Tracking_Flags"]),
                str(info["Details"]), str(info["Comment"])
            )
            print(params)
            cursor.execute(insert_sql, params)
            db.commit()
            data = cursor.fetchall()
            print(data)
    except Exception as e:
        print(e)
