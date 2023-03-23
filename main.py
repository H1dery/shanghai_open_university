import requests
from lxml import etree
import time
from selenium import webdriver 
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

import json

# 下载firefox驱动https://github.com/mozilla/geckodriver/releases
# linux 解压到 /usr/local/bin ，chmod a+x /usr/local/bin/geckodriver
# windows 下载好firefox驱动，添加环境变量

username = ""
password = ""



# path_to_chromedriver = "/Users/markjayden/Downloadswww/chromedriver_mac64/chromedriver"
options = webdriver.FirefoxOptions()
options = Options()
options.set_preference("general.useragent.override","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36")

browser = webdriver.Firefox(options=options)

#html_data = html.xpath('//*[@id="dform"]/div/div[2]/table/tbody/tr[2]/td[3]/div/div/table/tbody/tr/td/div/div[1]/div/a')
def browser_login():

	browser.get("https://ids.shou.org.cn/authserver/login?service=https%3a%2f%2fl.shou.org.cn%2fcommon%2flogin.aspx%3fredirectUrl%3d%7e%2fcommon%2findex.aspx")
	time.sleep(3)
	name = browser.find_element("xpath","//*[@id='username']")
	name.send_keys(username)
	passwd = browser.find_element("xpath","//*[@id='password']")
	passwd.send_keys(password)
	login_button = browser.find_element("xpath","//*[@id='login_submit']")
	login_button.click()
	time.sleep(2)
	cookie = browser.get_cookies()
	return(cookie)
shou_url_list = []

login_cookie = browser_login()
cookie_get = (login_cookie[0]["value"])
user_cookie = {"auth": "%s"%cookie_get}
brow_header = {"Sec-Ch-Ua": "\"Chromium\";v=\"97\", \" Not;A Brand\";v=\"99\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"macOS\"", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://l.shou.org.cn/study/HomeWorkNew.aspx?courseOpenId=cw0eay2v-ybah4e4y4mpkq&minorcourseopenid=cw0eay2v-ybah4e4y4mpkq", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "close"}

def get_kecheng_name():

	kecheng_url = "https://l.shou.org.cn/student/LearningSpaceNew.aspx"
	req_res1 = requests.get(kecheng_url, headers=brow_header, cookies=user_cookie)
	selector = etree.HTML(req_res1.content)
	kecheng_content = selector.xpath('//div[@class="sh-coursename"]/a/@href')
	return(kecheng_content)
for kk in get_kecheng_name():
	shou_url = ("https://l.shou.org.cn"+kk)
	req_res = requests.get(shou_url, headers=brow_header, cookies=user_cookie)
	selector = etree.HTML(req_res.content)
	content = selector.xpath('//div[@class="sh-res-h"]')
	for div in content:
		img = div.find('img')
		if img is not None and img.get('title') == '未看':
			a = div.find('a')
			if a is not None:
				#print(a.get('title'),"未看")
				url = (a.get('href'))
				if "/study/directory.aspx" in url:
					shou_url = "https://l.shou.org.cn"+url
					shou_url_list.append(shou_url)
		else:
			a = div.find('a')
			print(a.get('title'),"已看")
			#print(a.get('href'))
		
		
#shou_url = "https://l.shou.org.cn/study/learnCatalogNew.aspx?courseOpenId=sa0eay2vi4tktcncyksqjq&minorcourseopenid=sa0eay2vi4tktcncyksqjq"
def t2s(t):
	h,m,s = t.strip().split(":")
	return int(h) * 3600 + int(m) * 60 + int(s)
def run_video(url_list):
	browser.get(url_list)
	time.sleep(5)
	try:
		
		play_video = browser.find_element("xpath","//*[@id='doc_box']")
		play_video.click()
		page_html = browser.page_source
		selector = etree.HTML(page_html)
		content = selector.xpath('//*[@id="doc_box"]/@data-url')
		video_time = (content[0])
		print(video_time)
		time_url = json.loads(video_time)
		status_url = time_url["urls"]["status"]
		get_video_time = requests.get(status_url,timeout=10)
		time_video = (get_video_time.json()["args"]["duration"].split(".")[0])
		calc_time = t2s(time_video)
		print(calc_time)
		time.sleep(calc_time)
	except Exception as e:
		#print(e)
		if "doc_box" in str(e):
			print("判断为不是视频，10秒后下一个")
			time.sleep(5)
			pass

for url_list in shou_url_list:
	run_video(url_list)
