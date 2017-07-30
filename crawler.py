#爬取 wanimal 博客里的照片
import os
import requests
from bs4 import BeautifulSoup
import re

def getHtmlText(url, code="utf-8"):
	try:
		r=requests.get(url, headers=header)
		r.raise_for_status()
		r.encoding=code
		print("已打开博客")
		return r.text
	except:
		return "出错了！"

def getImageUrlList(html, img_list):
	soup = BeautifulSoup(html, 'html.parser')
	imgs = soup.find_all('img')
	for img in imgs:   
		try:
			img_url = re.findall(r'http://[^\s]*?_1280\.jpg', str(img))[0] 
			img_list.append(img_url)
		except:
			continue

def downloadImages(imgUrl, fileNumber):
	filename = "%04d"%(fileNumber) + ".jpg"
	path = photos_folder + filename
	try:
		if not os.path.exists(path):
			image = requests.get(imgUrl, headers=header)
			with open(path,'wb') as f:
				f.write(image.content)
				f.close()
				print("图片 " + str(imgUrl) + " 已保存")
	except:
		pass
		#print("爬取图片 " + str(imgUrl) + " 失败")


if __name__=="__main__":
	header={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4"}
	photos_folder = "./photos/"
	if not os.path.exists(photos_folder):
		os.mkdir(photos_folder)

	fileNumber = 0
	files = os.listdir(photos_folder)
	for file in files:  #循环所有文件，得出最大的文件编号
		file = file.split(".")[0]
		if file.isdigit():
			if int(file)>fileNumber:
				fileNumber=int(file)

	fileNumber = fileNumber + 1

	for i in range(1, 120):  #从第1页抓取到第120页
		blog_url = "http://wanimal1983.org/page/" + str(i)
		print(blog_url)
		html = getHtmlText(blog_url)
		imgList = []
		getImageUrlList(html, imgList)
		for imgUrl in imgList:
			downloadImages(imgUrl, fileNumber)
			fileNumber = fileNumber + 1
	
	print("图片爬取完毕！")
		



