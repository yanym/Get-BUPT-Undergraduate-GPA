#-*- coding: utf-8 -*-
import urllib
from bs4 import BeautifulSoup
import http.cookies
import http.cookiejar
from urllib import request,parse
import getpass

class BUPTundergraduateGPA:
	def Login(self):
		cookie = http.cookiejar.CookieJar()
		#声明CookieJar实例保存cookie
		handler = urllib.request.HTTPCookieProcessor(cookie)
		#cookie处理器
		opener = urllib.request.build_opener(handler)
		#用处理器构建opener。一般来说urlopen其实就是一个默认的opener

		CaptchaUrl = "http://jwxt.bupt.edu.cn/validateCodeAction.do?random="
		with open('验证码.jpg', 'wb') as f:
			f.write(opener.open(CaptchaUrl).read())

		zjh = input('学号: ')
		mm = getpass.getpass('密码: ')
		yzm = input('验证码: ')
		postdata = parse.urlencode([
			('zjh', zjh),
			('mm', mm),
			('v_yzm', yzm)])
		headers = {
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '+
		    '(KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36'
		}

		req = request.Request(url = 'http://jwxt.bupt.edu.cn/jwLoginAction.do',
		 	data = postdata.encode(encoding = 'utf-8'),
		 	headers = headers)
		opener.open(req)#将PostData传递给服务器，并且接受cookie储存在内存中，以后再开其他即可
		result2 = opener.open('http://jwxt.bupt.edu.cn/gradeLnAllAction.do?type=ln&oper=qbinfo&lnxndm=2015-2016%D1%A7%C4%EA%B5%DA%B6%FE%D1%A7%C6%DA(%B4%BA)(%C8%FD%D1%A7%C6%DA)')
		soup = BeautifulSoup(result2,'html.parser', from_encoding="gb18030")
		list = soup.findAll('tr',{'class' : 'odd'})
		return list

	def WriteFile(self, list):
		for x in list:
			for y in x.children:
				#print(y)
				with open('Report.txt', 'a') as f:
					f.write('')
					z = str(y)
					z = z.replace('<td align="center">','').replace('<p align="center">','').replace('</td>','').replace('</p>','').replace(' ','').replace('	','').replace('\r\n','').replace('','')
					f.write(z)

	def Cal(self):
		with open('Report.txt', 'r') as f:
			list = f.readlines()
			MAX_NUM = len(list)/10
			n,Credit,Scroes = 0,0,0
			while n < MAX_NUM:
				if list[n*10 + 6][:2] == '必修' or list[n*10 + 6][:2] == '选修':
					Credit += float(list[n*10 + 5])
					Scroes += float(list[n*10 + 8])*float(list[n*10 + 5])
				n += 1
			return (Scroes/Credit)

BYR = BUPTundergraduateGPA()
BYR.WriteFile(BYR.Login())
print('除校任选课，你的GPA为：%f' % BYR.Cal())