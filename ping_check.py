import os
import time
from send_to_qq import sendmail4
from config import configs
message = configs['message'] 
n = 0
while True:
	s = os.system("ping www.baidu.com")
	print("第{0}次ping 检测 时间{1} 结果{2}".format(n, time.time(), s))
	n+=1
	if not s:
		sendmail3("ping 通了", message)
		break
	time.sleep(5)
