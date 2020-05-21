#!/usr/bin/python3
#coding:utf-8
import os, time, re, sys
import requests
import threading
import tkinter
from tkinter import messagebox,scrolledtext
from tkinter.simpledialog import askstring
import json
import random

ZS = False


class NEKOZJY:
	def __init__(self, username=None, password=None):
		self.__Page = {
			'LoginAPI':'https://zjy2.icve.com.cn/common/login/login',
			'GetCourseList':'https://zjy2.icve.com.cn/student/learning/getLearnningCourseList',
			'GetModuleId':'https://zjy2.icve.com.cn/study/process/getProcessList',
			'GetTopicID':'https://zjy2.icve.com.cn/study/process/getTopicByModuleId',
			'GetCellID':'https://zjy2.icve.com.cn/study/process/getCellByTopicId',
			'GetDirectory':'https://zjy2.icve.com.cn/common/Directory/viewDirectory',
			'SendContent':'https://zjy2.icve.com.cn/api/common/Directory/addCellActivity',
			'SubmitProcess':'https://zjy2.icve.com.cn/api/common/Directory/stuProcessCellLog',
			'ExceptSubmit':'https://zjy2.icve.com.cn/common/Directory/changeStuStudyProcessCellData'
		}
		self.__username = username
		self.__password = password
		self.school_url = ""
		self.speed = 1
		self.__passnowpage = False
		self.__getcell_count = 0
		self.__name = "NEKOKAMI"
		self.__SchoolName = "NEKOWORKS"
		self.__login_cookie = {'acw_tc':'','auth':'','token':''}
		self.__useLog = False
		self.__debug = False
		self.__Frame = None
		self.setMode(True,False)
		"""设置用户"""
	def setUser(self,username,password):
		self.__username = username
		self.__password = password
		"""设置评论内容"""
	def setContent(self,contents):
		self.Content = contents
		if(self.__debug):
			print(self.Content)
		"""指定窗口"""
	def setFrame(self,Frame):
		self.__Frame = Frame
		self.__useLog = True
		Frame.addLog("辅助线程创建成功")

	def getName(self):
		return self.__name

	def getSchoolName(self):
		return self.__SchoolName
	"""
	{
		'code': 1, 
		'lateCode': 0, 
		'userId': 'datoawyla5lbeeqnwrjoq', 
		'userName': '191308043', 
		'displayName': '张胜勇', 
		'userType': 1, 
		'avator': 'https://file.icve.com.cn/ssykt/909/349/E365763D694A95CB61331666AEF70E4C.jpeg?x-oss-process=image/resize,m_fixed,w_50,h_50,limit_0', 
		'isInitialPwd': 0, 
		'isSecurityLowPwd': 1, 
		'isForceUpdatePwdToSecurity': 0, 
		'schoolId': 'ilqjao6ntkhlrjx88bqrja', 
		'schoolName': '河北软件职业技术学院', 
		'schoolCode': 'hbsi', 
		'schoolLogo': '/common/images/logo.png', 
		'schoolUrl': 'https://hbsi.zjy2.icve.com.cn', 
		'versionMode': 2, 
		'schoolCategory': 0, 
		'isValid': 1, 
		'versionType': '2.0', 
		'isGameTea': 0, 
		'isNeedConfirmUserName': 0, 
		'firstUserName': '191308043', 
		'secondUserName': '', 
		'token': 'ev8pazcrxy9hucbwjlpalg', 
		'isEmail': 1, 
		'mgdCount': 0
	}

	"""
	def login(self):
		form_data = {'userName':self.__username,'userPwd':self.__password,'verifyCode':'2896'}
		cookies = {'verifycode':'42F091B41696DAE91B17C7CBE7B75237@637234987283152046'}
		a = requests.post(self.__Page['LoginAPI'],data=form_data,cookies=cookies)
		content = a.content.decode().replace('\r','').replace('\n','').replace('\t','').replace(' ','')
		aaa = json.loads(a.content)['code']
		bbb = json.loads(a.content)
		"""
		1 登录成功
		-2 用户名或密码错误
		-16 验证码错误
		"""
		if(aaa != 1):
			return aaa
		if(self.__debug):
			try:
				print("acw_tc", a.cookies['acw_tc'])
				print(bbb)
			except BaseException:
				pass
		name = bbb['displayName']
		self.__name = name
		self.__SchoolName = bbb['schoolName']
		token = bbb['token']
		aaa = bbb['code']
		self.__login_cookie['acw_tc'] = a.cookies['acw_tc']
		self.__login_cookie['auth'] = a.cookies['auth']
		self.__login_cookie['token'] = token
		self.school_url = bbb['schoolUrl']
		if self.__debug:
			print(self.__login_cookie)
		return aaa

	def setLog(self, log):
		self.__useLog = True
		self.__log = log

	def setdebug(self,status):
		self.__debug = status
		pass

	def setMode(self,KC,PL=False):
		self.__KC = KC
		self.__PL = PL
		if(self.__debug):
			print(self.__KC,self.__PL)

	def getMode(self):
		return self.__KC,self.__PL

	def getContent(self):
		return self.Content

	def getCourseList(self):
		t = requests.post(self.__Page['GetCourseList'],cookies=self.__login_cookie)
		t = json.loads(t.content)['courseList']
		ret = []
		for i in t:
			ret.append({
				'courseOpenId':i['courseOpenId'],
				'courseName':i['courseName'],
				'process':i['process'],
				'openClassId':i['openClassId']
			})
		return ret

	def getALLCellsByCourseId(self,courseOpenId,openClassId):
		cells = []
		MDM = self.getModuleId(courseOpenId,openClassId)
		for MD in MDM:
			if(self.__debug):
				print("Modules", MD)
			TNM = self.getTopicID(MD['courseOpenId'], MD['openClassId'], MD['moduleId'], MD['percent'])
			cells.append(TNM)
		# for TN in TNM:
		# 	if(self.__debug):print('Topics',TN)
		# 	CN = self.getCellID(TN['courseOpenId'],TN['openClassId'],TN['TopicId'],TN['moduleId'])
		# 	cells.append(CN)
		return cells

	def getModuleId(self,courseOpenId,openClassId):
		form_data = {'courseOpenId':'','openClassId':''}
		form_data['openClassId'] = openClassId
		form_data['courseOpenId'] = courseOpenId
		try:
			a = requests.post(self.__Page['GetModuleId'],data=form_data,cookies=self.__login_cookie)
			t = json.loads(a.content)['progress']['moduleList']
		except BaseException as ex:
			print(a.content)
			print(form_data)
		ret = []
		print(a.content)
		for i in t:
			ret.append({
				'courseOpenId': courseOpenId,
				'openClassId': openClassId,
				'moduleId': i['id'],
				'name': i['name'],
				'percent': i['percent']
			})
		return ret

	def getTopicID(self,courseOpenId,openClassId,moduleId,percent):
		if(percent == 100 and not self.__PL): return []
		form_data = {'courseOpenId':'','moduleId':''}
		form_data['courseOpenId'] = courseOpenId
		form_data['moduleId'] = moduleId
		t = requests.post(self.__Page['GetTopicID'],data=form_data,cookies=self.__login_cookie)
		t = json.loads(t.content)['topicList']
		ret = []
		for i in t:
			ret.append({
				'TopicId':i['id'],
				'courseOpenId':courseOpenId,
				'openClassId':openClassId,
				'moduleId':moduleId,
				'name':i['name'],
			})
		return ret

	def getsonCells(self, childNode, openClassId, moduleId, courseOpenId, topicId):
		ret = []
		for i in childNode:
			if i['cellType'] == 1:
				ret.append({
					'cellId': i['Id'],
					'cellName': i['cellName'],
					'openClassId': openClassId,
					'moduleId': moduleId,
					'courseOpenId': courseOpenId,
					'topicId': topicId,  # topicID
					'categoryName': i['categoryName'],  # 类型
					'stuCellPercent': i['stuCellFourPercent'],
				})
			elif i['cellType'] == 4:
				tmp = self.getsonCells(i['childNodeList'], openClassId, moduleId, courseOpenId)
				for t in tmp:
					ret.append(t)
		return ret

	def getCellID(self,courseOpenId,openClassId,topicId,moduleId):
		form_data = {'courseOpenId':'','openClassId':'','topicId':''}
		form_data['courseOpenId'] = courseOpenId
		form_data['openClassId'] = openClassId
		form_data['topicId'] = topicId
		if (self.__getcell_count == 5*self.speed):
			self.__Frame.addLog("课程列表较多，请耐心等待")
			time.sleep(5)
			self.__getcell_count = 0
		self.__getcell_count += 1
		t = requests.post(self.__Page['GetCellID'],data=form_data,cookies=self.__login_cookie)
		t = json.loads(t.content)['cellList']
		ret = []
		for i in t:
			if i['cellType'] == 1:
				ret.append({
					'cellId': i['Id'],
					'cellName': i['cellName'],
					'openClassId': openClassId,
					'moduleId': moduleId,
					'courseOpenId': courseOpenId,
					'topicId': i['topicId'],  # topicID
					'categoryName': i['categoryName'],  # 类型
					'stuCellPercent': i['stuCellPercent'],
				})
			elif i['cellType'] == 4:
				tmp = self.getsonCells(i['childNodeList'], openClassId, moduleId, courseOpenId, i['topicId'])
				for t in tmp:
					ret.append(t)
		return ret

	def getDirectory(self,courseOpenId,openClassId,topicId,cellId,moduleId):
		form_data = {'courseOpenId':'','openClassId':'','cellId':'','moduleId':'','flag':'s'}
		headers = {
			'Host':'zjy2.icve.com.cn',
			'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
			'Accept-Encoding':'gzip, deflate, br',
			'Referer':'https://zjy2.icve.com.cn/common/directory/directory.html?courseOpenId=%s&openClassId=%s&cellId=%s&flag=s&moduleId=%s'%(courseOpenId,openClassId,cellId,moduleId),
			'Upgrade-Insecure-Requests':'1',
			'X-Requested-With':'XMLHttpRequest'
		}
		if self.__debug:
			print(headers)
		form_data['courseOpenId'] = courseOpenId
		form_data['openClassId'] = openClassId
		form_data['cellId'] = cellId
		form_data['moduleId'] = moduleId
		t = requests.post(self.__Page['GetDirectory'],data=form_data,cookies=self.__login_cookie)
		i = json.loads(t.content)
		cellName = None
		if(i['code']==-100):
			self.ExceptToDo(i)
			t = requests.post(self.__Page['GetDirectory'],data=form_data,cookies=self.__login_cookie, headers=headers)
			i = json.loads(t.content)
			if (i['code'] == -2):
				messagebox.showinfo(title="通知", message=i['msg'])
				self.__Frame.exit(i['msg'])
				return None
		errcount = 0
		try:
			cellName = i['cellName']
		except BaseException as ex:
			if self.__debug:
				print("getDirectory()", "尝试重新获取CellName中")
				print(i)
			errcount += 1
			while cellName is None:
				try:
					t = requests.post(self.__Page['GetDirectory'], data=form_data, cookies=self.__login_cookie)
					i = json.loads(t.content)
					if(i['code'] == -2):
						messagebox.showinfo(title="通知", message=i['msg'])
						self.__Frame.exit(i['msg'])
						return None
					cellName = i['cellName']
				except BaseException as ex:
					errcount += 1
					if self.__debug:
						print("getDirectory()", "尝试重新获取CellName中")
						print(i)
					if errcount == 5:
						messagebox.showinfo(title="异常", message="获取课程信息失败 5次,为确保账户安全，自动退出")
						messagebox.showinfo(title="异常原因", message=i['msg'])
						self.__Frame.exit("获取课程信息失败 5次,为确保账户安全，自动退出")
		ret = {
			'courseOpenId':courseOpenId,
			'openClassId':openClassId,
			'moduleId':moduleId,
			'topicId':i['topicId'],
			'cellId':i['cellId'],
			'cellName':cellName,
			'cellLogId':i['cellLogId'],			#重要
			'categoryName':i['categoryName'],	#课件类型
			'guIdToken':i['guIdToken'],			#重要
			'pageCount':i['pageCount'],			#文档类型总页数
			'audioVideoLong':i['audioVideoLong'],			#音视频类型时长
			'stuCellPicCount':i['stuCellPicCount'],			#文档类型已完成页数
			'stuStudyNewlyTime':i['stuStudyNewlyTime'],		#音视频类型已完成时长
			'cellPercent':i['cellPercent'],		#总进度
			'source_addr':json.loads(i['resUrl'])['urls']['preview'],
			'extension':json.loads(i['resUrl'])['extension']
		}
		if self.__debug:
			print(ret)
		return ret

	def SendContent(self,class_info,tt):
		if not self.__PL:
			return
		if(self.__debug): print(class_info)
		activityTypes={'评价':'1', '问答':'3', '笔记':'2', '纠错':'4'}
		form_data = {'courseOpenId':'','openClassId':'','cellId':'','content':'','docJson':'','star':'0','activityType':''}
		form_data['courseOpenId'] = class_info['courseOpenId']
		form_data['openClassId'] = class_info['openClassId']
		form_data['cellId'] = class_info['cellId']
		for i in self.Content:
			if(self.Content[i] == None or self.Content[i] == ""):
				return
			if(self.__useLog):tt.addLog("%s => 发送[%s]:%s"%(class_info['cellName'],i,self.Content[i]))
			if(activityTypes[i]=='1'):
				form_data['star'] = '5'
			else:
				time.sleep(60)
				###############
				form_data['star'] = '0'
			form_data['content'] = self.Content[i]
			form_data['activityType'] = activityTypes[i]
			t = requests.post(self.__Page['SendContent'],data=form_data,cookies=self.__login_cookie).content
			t =json.loads(t)
			if(self.__debug):
				print(t)
			# time.sleep(60)
			

	def ExceptToDo(self, info):
		form_data = {'courseOpenId': '', 'openClassId': '', 'moduleId': '', 'cellId': '', 'cellName': ''}
		form_data['courseOpenId'] = info['currCourseOpenId']
		form_data['openClassId'] = info['currOpenClassId']
		form_data['moduleId'] = info['currModuleId']
		form_data['cellId'] = info['curCellId']
		form_data['cellName'] = info['currCellName']
		t = requests.post(self.__Page['ExceptSubmit'], data=form_data, cookies=self.__login_cookie)
		t = json.loads(t.content)
		if (self.__debug):
			print(t)

	"""
	POST /api/common/Directory/stuProcessCellLog HTTP/1.1
	Host: zjy2.icve.com.cn
	Connection: keep-alive
	Content-Length: 191
	Accept: application/json, text/javascript, */*; q=0.01
	Sec-Fetch-Dest: empty
	User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36
	Content-Type: application/x-www-form-urlencoded; charset=UTF-8
	Origin: https://hbsi.zjy2.icve.com.cn
	Sec-Fetch-Site: same-site
	Sec-Fetch-Mode: cors
	Referer: https://hbsi.zjy2.icve.com.cn/common/directory/directory.html?courseOpenId=enn0ahrvpdgqcso8am3rw&openClassId=npb8ahrzo1dpmwwilchdw&cellId=iumxaxrv4volcs7w5csag&flag=s&moduleId=vguyaxr04pcvbmt8ouslg
	Accept-Encoding: gzip, deflate, br
	Accept-Language: zh-CN,zh;q=0.9
	Cookie: acw_tc=2f624a0915857235703258231e45f1d552577b95e6c7f34225b104d2982f5f; 
			Hm_lvt_a3821194625da04fcd588112be734f5b=1585557699,1585723577,1585731399,1585732111;
			Hm_lpvt_a3821194625da04fcd588112be734f5b=1585732111; 
			token=74eaazcrg7fhfid3quksg; 
			TY_SESSION_ID=588bfd3a-dc6c-4122-9355-f281dede2212; 
			jwplayer.captionLabel=Off; 
			jwplayer.mute=true; 
			ASP.NET_SessionId=s5dy3j4jewpqs5qnusdaleky; 
			verifycode=760D38D0A12ED8BE04A69C226D102CF5@637213601583388693;
			auth=0102C9F732F421D6D708FEC907DFC575D6D70801156400610074006F006100770079006C00610035006C0062006500650071006E00770072006A006F00710000012F00FF7B4F53A9A7F731E5FC7E95E096CCBB65EFB9FB1B; 
			token=ubulazcri6rhkvrfk9fv7q
			
			
	"""
	def Process(self,class_info,tt):
		if(not self.__KC): return
		if(class_info['cellPercent']==100 and(
				(class_info['pageCount'] == 0 and class_info['stuStudyNewlyTime'] >= class_info['audioVideoLong'])
			or
				(class_info['audioVideoLong'] == 0.0 and class_info['stuCellPicCount'] >= class_info['pageCount'])
			)
		):
			return		#进度已经完成
		if(self.__useLog): self.__Frame.addLog("开始处理课程 [%s]"%class_info['cellName'])
		else:print("开始处理课程 [%s]"%class_info['cellName'])
		form_data={'courseOpenId':'','openClassId':'','cellId':'','cellLogId':'','picNum':'0','studyNewlyTime':'0','studyNewlyPicNum':'0','token':''}
		form_data['courseOpenId'] = class_info['courseOpenId']
		form_data['openClassId'] = class_info['openClassId']
		form_data['cellId'] = class_info['cellId']
		form_data['cellLogId'] = class_info['cellLogId']
		form_data['token'] = class_info['guIdToken']
		moduleId = class_info['moduleId']
		src_addr = class_info['source_addr']
		extension = class_info['extension']
		headers = {
			'Host': 'zjy2.icve.com.cn',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
			'Accept': 'application/json, text/javascript, */*; q=0.01',
			'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
			'Accept-Encoding': 'gzip, deflate, br',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'X-Requested-With': 'XMLHttpRequest',
			'Origin': 'https://zjy2.icve.com.cn',
			'Connection':'keep-alive',
			'Referer': 'https://zjy2.icve.com.cn/common/directory/directory.html?courseOpenId=%s&openClassId=%s&cellId=%s&flag=s&moduleId=%s'%(
				form_data['courseOpenId'], form_data['openClassId'],form_data['cellId'],moduleId),
			'Sec-Fetch-Dest': 'empty',
			'Sec-Fetch-Mode': 'cors',
			'Sec-Fetch-Site': 'same-site'
		}
		if(extension in ("doc",'pdf','pptx','ppt','docx','png','jpg','jpeg','html')):
			error_count = 0
			add_set = 5
			time.sleep(2)
			c=[int(class_info['stuCellPicCount']), int(class_info['pageCount'])]
			pass_time = 0
			while(c[0]<c[1]):
				if(tt.exitd):return
				if self.__passnowpage:
					self.__passnowpage = False
					return
				# if(c[1]==30):
				# 	form_data['picNum'] = 1
				# 	form_data['studyNewlyPicNum'] = 1
				# 	t = json.loads(requests.post(self.__Page['SubmitProcess'],data=form_data,cookies=self.__login_cookie,headers=headers).content)
				# 	break
				form_data['picNum'] = c[0]
				form_data['studyNewlyPicNum'] = c[0]
				t = json.loads(requests.post(self.__Page['SubmitProcess'], data=form_data, cookies=self.__login_cookie, headers=headers).content)
				if(t['code'] < 0):
					add_set = 1
					error_count += 1
					if(self.__debug):print(class_info)
					time.sleep(error_count)
				else:
					error_count = 0
				if(self.__debug):
					print(t)
				time.sleep(8)
				pass_time+=3
				c[0] += add_set*self.speed
			time.sleep(5)
			while pass_time < 13:
				pass_time += 1
				time.sleep(1)
			form_data['picNum'] = class_info['pageCount']
			form_data['studyNewlyPicNum'] = class_info['pageCount']
			t = json.loads(requests.post(self.__Page['SubmitProcess'], data=form_data, cookies=self.__login_cookie, headers=headers).content)
			error_count = 0
			while(t['code']<0):
				if self.__passnowpage:
					self.__passnowpage = False
					return
				time.sleep(error_count)
				t = json.loads(requests.post(self.__Page['SubmitProcess'], data=form_data, cookies=self.__login_cookie).content)
				error_count += 1
			if(self.__debug):print(t)
		elif (extension in ('zip', 'rar')):
			form_data['picNum'] = class_info['pageCount']
			form_data['studyNewlyPicNum'] = class_info['pageCount']
			t = json.loads(requests.post(self.__Page['SubmitProcess'],data=form_data,cookies=self.__login_cookie).content)
			if(self.__debug):print(t)
		elif (extension in ('m4a','mpg','mp4', 'swf','mp3','flv','avi','asf','wmv','mov','wav','rmvb','wma','qlv')):
			sum_time = float(class_info['audioVideoLong'])
			new_time = float(class_info['stuStudyNewlyTime'])
			error_count = 0
			if self.__debug:print("[Media]",new_time,"=>",sum_time)
			while(new_time<=sum_time):
				if(tt.exitd):return
				new_time += 10*self.speed + random.random()
				for _ in range(10):
					time.sleep(1)
					if self.__passnowpage:
						break
				if not new_time <= sum_time:
					break
				if self.__passnowpage:
					self.__passnowpage = False
					return
				form_data['studyNewlyTime'] = str(new_time)
				t = json.loads(requests.post(self.__Page['SubmitProcess'],data=form_data,cookies=self.__login_cookie).content)
				if(self.__debug):
					print(form_data)
					print(t)
				if(self.__useLog):
					self.__Frame.addLog("正在进行的是这个喵～ [%s]"%class_info['cellName']+str(int(float(form_data['studyNewlyTime'])*100/sum_time))+"%")
				else:
					print("正在进行的是这个喵～ [%s]"%class_info['cellName'],int(float(form_data['studyNewlyTime'])*100/sum_time),"%")
				if(t['code']==-1):
					new_time -= error_count
					# error_count += 1
				else:
					error_count = 8
			form_data['studyNewlyTime'] = float(class_info['audioVideoLong'])
			t = json.loads(requests.post(self.__Page['SubmitProcess'], data=form_data, cookies=self.__login_cookie).content)
		else:
			self.__Frame.addLog("发现新课件类型[%s],猫猫没见过,请跟我的主人说一声喵~"%extension)

	def pass_now_page(self):
		self.__passnowpage = True
		self.__Frame.addLog("手动跳过课程")

	def add_speed(self):
		if self.speed < 1024:
			if self.speed < 10:
				self.speed+=1
			elif self.speed == 10:
				self.speed = 16
			else:
				self.speed = int(self.speed*2)
			self.__Frame.addLog("变更速度为%d倍速喵~" % self.speed)
		else:
			self.__Frame.addLog("已经%d倍速了,你果然是个狼灭,猫猫(炸毛)~！"%self.speed)


	def sub_speed(self):
		if self.speed>1:
			if self.speed <= 10:
				self.speed-=1
			elif self.speed == 16:
				self.speed = 10
			else:
				self.speed = int(self.speed/2)
			self.__Frame.addLog("变更速度为%d倍速喵~" % self.speed)
		else:
			self.__Frame.addLog("只剩%d倍速了啦，再慢猫猫就要睡着了啦..."%self.speed)
"""
	def Process(self,class_info,tt):
		if(not self.__KC): return
		if(class_info['cellPercent']==100): return		#进度已经完成
		if(self.__useLog): self.__Frame.addLog("开始处理课程 [%s]"%class_info['cellName'])
		else:print("开始处理课程 [%s]"%class_info['cellName'])
		form_data={'courseOpenId':'','openClassId':'','cellId':'','cellLogId':'','picNum':'0','studyNewlyTime':'0','studyNewlyPicNum':'0','token':''}
		form_data['courseOpenId'] = class_info['courseOpenId']
		form_data['openClassId'] = class_info['openClassId']
		form_data['cellId'] = class_info['cellId']
		form_data['cellLogId'] = class_info['cellLogId']
		form_data['token'] = class_info['guIdToken']
		moduleId = class_info['moduleId']
		src_addr = class_info['source_addr']
		extension = class_info['extension']
		headers = {
			'Host': 'zjy2.icve.com.cn',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
			'Accept': 'application/json, text/javascript, */*; q=0.01',
			'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
			'Accept-Encoding': 'gzip, deflate, br',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'X-Requested-With': 'XMLHttpRequest',
			'Origin': 'https://zjy2.icve.com.cn',
			'Referer': 'https://zjy2.icve.com.cn/common/directory/directory.html?courseOpenId=%s&openClassId=%s&cellId=%s&flag=s&moduleId=%s'%(form_data['courseOpenId'],form_data['openClassId'],form_data['cellId'],moduleId)
		}
		if(extension in ("doc",'pdf')):
			pagecount = class_info['pageCount']
			addr = src_addr+"/%s."+extension
			for i in range(pagecount):
				addr_tmp = addr % i
				requests.get(addr_tmp,cookies=self.__login_cookie)
				time.sleep(5)
		elif(extension in ('zip','rar','pptx')):
			requests.get(src_addr, cookies=self.__login_cookie)
			time.sleep(5)
		elif(extension in ('mp4','swf')):
			requests.get(src_addr, cookies=self.__login_cookie)
			times = int(class_info['audioVideoLong'])
			if times > 60:
				times = 60
			time.sleep(times)
		elif(extension in ('mp3')):
			addr = src_addr + "\/%s\." + extension
			addr = addr%"file"
			requests.get(src_addr, cookies=self.__login_cookie)
			times = int(class_info['audioVideoLong'])
			if times > 60:
				times = 60
			time.sleep(times)
		else:
			requests.get(src_addr, cookies=self.__login_cookie)
			if not ZS:
				time.sleep(5)
"""


class NEKOFace:
	class Login:
		def __init__(self,nz):
			self.__nz = nz
			self.Content = {'评价':'好','问答':'没问题','笔记':'没话说','纠错':'没错'}
			self.control = [True,False]
			self.__islogin = False
			self.Login()

		def __to_login(self):
			a,b = VersionCheck()
			if a :
				if (b is not None):
					messagebox.showinfo(title='来自猫猫的话',message=b)
			else:
				messagebox.showinfo(title='版本更新提醒',message=b)
				self.__root.destroy()
				sys.exit(-1)

			if(self.__username.get() == "" or self.__password.get() == ""):
				messagebox.showinfo(title='错误',message='用户名或密码为空!')
				return
			self.__nz.setUser(self.__username.get(),self.__password.get())
			code = self.__nz.login()
			if(code == 1):
				messagebox.showinfo(title='通知',message='登陆成功了喵~')
				self.__islogin = True
				data = {"username":self.__username.get(),"password":self.__password.get()}
				self.setSaveData(data)
				self.__root.destroy()
			elif(code == -2):
				messagebox.showinfo(title='错误',message='请检测用户名密码喵~(或确认一下是不是输入法的问题，一定要用英文输入法哦)')
			elif(code == -16):
				messagebox.showinfo(title='错误', message='有新版本了,快去下载喵~')

		def setting(self):
			self.control = [True,False]
			self.control[0] = messagebox.askokcancel(title='设置',message='是否确定要自动【刷课】喵?\n默认【是】')
			if(self.control[0] == None): self.control[0] = False
			self.control[1] = messagebox.askokcancel(title='设置',message='是否确定要自动【评论】喵?\n默认【否】')
			if(self.control[1] == None): self.control[1] = False
			if messagebox.askokcancel(title='设置',message='是否确定要自定义评论内容喵?\n默认评论内容如下:\n评价:%s\n问答:%s\n笔记:%s\n纠错:%s'%(self.Content['评价'],self.Content['问答'],self.Content['笔记'],self.Content['纠错'])):
				self.Content['评价'] = askstring(title="设置",prompt="请输入【评价】内容,为空则不处理")
				self.Content['问答'] = askstring(title="设置",prompt="请输入【问答】内容,为空则不处理")
				self.Content['笔记'] = askstring(title="设置",prompt="请输入【笔记】内容,为空则不处理")
				self.Content['纠错'] = askstring(title="设置",prompt="请输入【纠错】内容,为空则不处理")

		def getSetting(self):
			return self.Content,self.control,self.__islogin

		def getSaveData(self):
			ret = {"code":"-1","username":"","password":""}
			try:
				with open("neko.conf","r") as f:
					tmp = f.read().replace(" ","").split("\n")
					for i in tmp:
						if("username" not in i) and ("password" not in i):
							continue
						sp = i.split("=")
						ret[sp[0]] = sp[1]
				ret['code'] = 0
			except BaseException as ex:
				pass
			return ret

		def setSaveData(self,data):
			with open("neko.conf","w") as f:
				for i in data:
					str = "%s=%s\n"%(i,data[i])
					f.write(str)

		def Login(self):
			self.__root = tkinter.Tk()
			self.__root.title("嗷呜职教云")
			self.__root.geometry('400x180')
			self.__root.resizable(0,0)

			tkinter.Label(text = "用户名").place(x=30,y=30)
			self.__username = tkinter.Entry(self.__root, width=35)
			self.__username.place(x=120,y=30)

			tkinter.Label(text = "密码").place(x=30,y=70)
			self.__password = tkinter.Entry(self.__root, show='*',width=35)
			self.__password.place(x=120, y=65)

			self.__login_b = tkinter.Button(self.__root,text="登录喵~",width=35,command = self.__to_login)
			self.__login_b.place(x=30,y=110)

			self.__login_b = tkinter.Button(self.__root,text="设置",width=5,command = self.setting)
			self.__login_b.place(x=310,y=110)
			data = self.getSaveData()
			if data['code'] == 0:
				self.__username.insert(tkinter.END,data['username'])
				self.__password.insert(tkinter.END,data['password'])
				select = messagebox.askokcancel(title='免责声明',message='本软件完全免费，并只能用作学习和研究用途。严禁用于商业和违法用途。因软件引起的任何纠纷都和作者无关！')
				if not select:
					return
			self.__root.mainloop()

		def __del__(self):
			if not self.__islogin:
				import sys
				sys.exit(0)


	class Main:
		def __init__(self,nz,setting=None):
			self.__nz = nz
			self.__is_start = False
			self.__new_Log = ""
			self.exitd = False
			self.PL_content={'评价':'好','问答':'没问题','笔记':'没话说','纠错':'没错'}
			self.__nz.setFrame(self)
			if(setting != None):
				self.PL_content = setting[0]
				self.__nz.setMode(setting[1])
			self.addLog("*"*50)
			self.addLog("Power By 猫神様のメモ帳")
			self.addLog("本喵的QQ是 964585325，QQ群:983696433")
			self.addLog("本软件是为康酱开发的,所有权在康酱[QQ:2670975267]")
			self.addLog("不允许随意转发，否则直接封禁此脚本")
			self.addLog("*" * 50)
			self.addLog("登录成功")
			self.addLog("自动刷课[%s],自动评论[%s]"%self.__nz.getMode())
			self.addLog("姓名:%s"%self.__nz.getName())
			self.addLog("学校:%s" % self.__nz.getSchoolName())
			if(self.__nz.getMode()[1]):
				l = self.__nz.getContent()
				for i in l:
					t = l[i]
					if((t is None) or (t == "")):
						self.addLog("[%s] 不处理"%i)
					else:
						self.addLog("[%s] 内容设定为:%s"%(i,l[i]))
			self.setPage()

		def LogThread(self):
			if(len(self.__new_Log)>0):
				self.__log.config(state=tkinter.NORMAL)
				self.__log.insert(tkinter.END,self.__new_Log)
				with open("neko.log","a+") as f:
					f.write(self.__new_Log)
				self.__new_Log = ""
				self.__log.config(state=tkinter.DISABLED)
				self.__log.see(tkinter.END)
			self.__log.after(500, self.LogThread)

		def addLog(self, info):
			now_time = time.strftime("[%Y-%m-%d %H:%M:%S] ")
			self.__new_Log += now_time+info+'\n'

		def showMsg(self, info, title='通知'):
			messagebox.showinfo(title=title, message=info)

		def ClassListThread(self):
			self.ALLClass = self.__nz.getCourseList()
			self.__ClassList.delete(0, tkinter.END)
			for i in self.ALLClass:
				self.__ClassList.insert(tkinter.END,("%s [ %d ]"%(i['courseName'],i['process'])+"%"))
			self.__ClassList.after(60000, self.ClassListThread)

		def selectClass(self,event=None):
			self.__Cell.delete(0, tkinter.END)
			if(self.__is_start):
				t = self.__selected_class
			else:
				t = self.ALLClass[self.__ClassList.curselection()[0]]
				self.__selected_class = t
			A = self.__nz.getModuleId(t['courseOpenId'],t['openClassId'])
			for i in A:
				self.__Cell.insert(tkinter.END,(" %s [ %d "%(i['name'],i['percent'])+"% ]"))
			if(self.__is_start):
				self.__Cell.after(10000, self.selectClass)

		def SK_Thread(self,class_info):
			MDM = self.__nz.getModuleId(class_info['courseOpenId'],class_info['openClassId'])
			for MD in MDM:
				if self.exitd:
					return
				time.sleep(1)
				self.addLog("Modules "+MD['name'])
				TNM = self.__nz.getTopicID(MD['courseOpenId'],MD['openClassId'],MD['moduleId'],MD['percent'])
				for TN in TNM:
					time.sleep(1.5)
					if self.exitd:
						return
					self.addLog("Topics "+TN['name'])
					CN = self.__nz.getCellID(TN['courseOpenId'],TN['openClassId'],TN['TopicId'],TN['moduleId'])
					for i in CN:
						time.sleep(1.5)
						if self.exitd:
							return
						a = self.__nz.getDirectory(i['courseOpenId'],i['openClassId'],i['topicId'],i['cellId'],i['moduleId'])
						if a is None:
							return
						if i['stuCellPercent'] != 100:
							self.__nz.Process(a, self)
						self.__nz.SendContent(a, self)
			self.addLog("[==========================================]")
			self.addLog("课程处理完成")

		def startZJY(self,event):
			t = self.__selected_class
			self.__is_start = True
			self.__Cell.after(10000, self.selectClass(None))
			threading.Thread(target=self.SK_Thread, args=(t,), name="SK").start()


		def setPage(self):
			self.__root = tkinter.Tk()
			#self.__root.iconbitmap("./neko.ico")
			self.__root.title("嗷呜职教云")
			self.__root.geometry('1200x550')
			#self.__root.resizable(0, 0)
			self.__root.protocol("WM_DELETE_WINDOW", self.on_closing)
			self.__root.resizable(0,50)
			self.Layout_TOP = tkinter.Label(self.__root)
			self.Layout_TOP.pack(side=tkinter.TOP,fill=tkinter.BOTH)
			self.Layout_BOTTOM = tkinter.Label(self.__root)
			self.Layout_BOTTOM.pack(side=tkinter.BOTTOM,fill=tkinter.X)

			TEMP_LAY = tkinter.Label(self.Layout_TOP)
			TEMP_LAY.pack(side=tkinter.LEFT, fill=tkinter.Y)
			self.ALLClass = self.__nz.getCourseList()
			tkinter.Label(TEMP_LAY, text = "课程列表").pack(side=tkinter.TOP, anchor="w")
			self.__ClassList = tkinter.Listbox(TEMP_LAY, height=20, width=40, listvariable=self.ALLClass)
			self.__ClassList.pack(side=tkinter.LEFT, fill=tkinter.Y)
			self.__ClassList.bind('<Double-Button-1>', func=self.selectClass)
			for i in self.ALLClass:
				self.__ClassList.insert(tkinter.END,("%s [ %d ]"%(i['courseName'],i['process'])+"%"))
			self.__ClassList.after(60000, self.ClassListThread)

			TEMP_LAY = tkinter.Label(self.Layout_TOP)
			TEMP_LAY.pack(side=tkinter.RIGHT,fill='both',expand='yes')
			tkinter.Label(TEMP_LAY, text="课件列表 [双击任意一个课件开始刷课喵～]").pack(side=tkinter.TOP, anchor="w")
			self.__Cell = tkinter.Listbox(TEMP_LAY, height=20, width=140)
			self.__Cell.pack(side=tkinter.LEFT, fill=tkinter.Y)
			self.__Cell.bind('<Double-Button-1>', func=self.startZJY)

			#日志框
			self.__log = scrolledtext.ScrolledText(self.Layout_BOTTOM,height=8, width=170)
			self.__log.pack(side=tkinter.BOTTOM)
			self.__log.config(state=tkinter.DISABLED)
			label1 = tkinter.Label(self.Layout_BOTTOM,text="日志记录:")
			label1.pack(side=tkinter.BOTTOM,anchor=tkinter.W)
			#跳过按钮
			tkinter.Button(self.Layout_BOTTOM, text="跳过当前课程", command=self.__nz.pass_now_page)\
				.pack(side=tkinter.RIGHT)
			tkinter.Button(self.Layout_BOTTOM, text="-", command=self.__nz.sub_speed) \
				.pack(side=tkinter.RIGHT)
			tkinter.Button(self.Layout_BOTTOM, text="+", command=self.__nz.add_speed) \
				.pack(side=tkinter.RIGHT)
			tkinter.Label(self.Layout_BOTTOM, text="调速").pack(side=tkinter.RIGHT)
			tkinter.Label(self.Layout_BOTTOM, text="[ 工具栏 ]").pack(side=tkinter.LEFT)
			self.__log.after(500, self.LogThread)

			self.__root.mainloop()

		def on_closing(self):
			if messagebox.askokcancel("确认", "真的要退出喵~?"):
				self.exitd = True
				self.__root.destroy()

		def exit(self, ans=None):
			self.addLog("异常退出")
			if ans is not None:
				self.addLog(ans)
			self.exitd = True
			self.__root.destroy()
			self.__nz.__destroy__()
			self.__destory__()
			sys.exit()


def VersionCheck():
	version = "62adc05d5373c83d436c984df2dd2805" #md5(neko_3.4.0)
	api = "http://auth.neko.wiki/version.php?version="
	try:
		jsdata = json.loads(requests.get(api+version).content)
		if(jsdata['code'] == 0):
			return True,None
		elif(jsdata['code'] == 1):
			return True,jsdata['msg']
		elif(jsdata['code'] == -1):
			return False,jsdata['msg']
	except:
		pass
	return False,"服务器版本校验异常"



def main():

	nz = NEKOZJY()
	nz.setdebug(False)
	Setting = NEKOFace.Login(nz).getSetting()
	if(Setting[2]==False):
		sys.exit(0)

	nz.setMode(Setting[1][0],Setting[1][1])
	nz.setContent(Setting[0])
	NEKOFace.Main(nz)

if __name__=='__main__':
	main()
