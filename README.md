# TryHackMe- Anonymous CTF Writeup
สวัสดีครับวันนี้เราจะมาเล่น CTF ชื่อ Anonymous ใน Tryhackme กันนะครับ<br />
CTF Link: https://tryhackme.com/room/anonymous<br />
**Task 1 - PWN:**
![3215325](https://user-images.githubusercontent.com/78845680/222404444-ed8363c8-8776-4e84-8b88-225dcc784e07.PNG)
Deploy the machine <br/>
**Nmap Scan:**<br />
***namp -sV <TARGET_IP><br />***
***-sV : Version detection***

![nmap](https://user-images.githubusercontent.com/78845680/222404903-585ecbdd-7b56-4a85-9dc3-c4f2498a86c5.PNG)<br />
จากรูปจะเห็นว่ามี 4 port ที่เปิดอยู่นะครับ<br />
***21/ftp- vsftpd 2.0.8<br />***
***22/ssh- OpenSSH 7.6p1<br />***
***139/netbios-ssn- Samba smbd 3.X-4.X<br />***
***445/netbios-ssn- Samba smbd 3.X-4.X<br />***

จาก nmap output ทำให้เราได้คำตอบใน Task 1 บางข้อ<br />
***Enumerate the machine.  How many ports are open?<br />***
***Ans:4<br />***
***What service is running on port 21?<br />***
***Ans:ftp<br />***
***What service is running on ports 139 and 445?<br />***
***Ans:smb<br />***

จากนั้นผมก็ลอง login ftp ด้วย user anonymous
![ftp](https://user-images.githubusercontent.com/78845680/222406900-28ccc1df-1125-4298-9987-2f92e880ac74.PNG)<br />
ผลคือเข้าได้และมีไฟล์อยู่ 3 ไฟล์คือ<br />
clean.sh เป็นไฟล์ script อะไรซักอย่างซึ่งผมคิดว่ามันน่าจะมีการตั้งเวลา run ไว้<br />
removed_files.log เป็น log ข้างในไม่มีอะไรเลย<br />
to_do.txt ไม่มีอะไรข้างจากข้อความไม่มีประโยชน์<br />
ผมได้ใช้คำสั่ง get ของ ftp เพื่อโหลด script clean.sh มาไว้เพื่อเราน่าจะทำ reverse shell ได้จาก script นี้<br />
![ftp2](https://user-images.githubusercontent.com/78845680/222409745-4219edab-1d4e-4d3c-83e2-e7ced4613298.PNG)<br />
ก่อนไปทำ reverse shell ผมได้ลอง list smb ดูว่ามีการ share อะไรไว้บ้าง<br />
![smb](https://user-images.githubusercontent.com/78845680/222410183-26cd9fd8-4d90-4ba0-99fe-3bfc56a4778d.PNG)<br />
***smbclient -N -L \\<TARGET_IP><br />***
***-N : no-pass<br />***
***-L : list<br />***
ทำให้เราได้คำตอบบางข้อ<br />
***There's a share on the user's computer.  What's it called?<br />***
***Ans: pics<br />***
ซึ่งใน share pics ไม่มีอะไรนอกจากรูป 2 อัน<br />
ต่อมาผมได้มาแก้ไฟล์ script ที่โหลดมาเพื่อทำ reverse shell<br />
![edit](https://user-images.githubusercontent.com/78845680/222411918-3d4b6d2f-5677-41d3-8eee-4c7bc8ac2dd6.PNG)
![edit](https://user-images.githubusercontent.com/78845680/222411946-37a18e45-0b81-44f6-8d19-72751f25f016.PNG)<br />
จากนั้นเราใช้ netcat listener ตามด้วย port ที่เราใส่ใน script<br />
![nc](https://user-images.githubusercontent.com/78845680/222412863-e73c00ba-7d2c-491f-aeec-a4e337f77804.PNG)<br />
เรา login ftp user anonymous เพื่อ upload script ที่เราแก้มาใหม่โดยใช้คำสั่ง put<br />
![ยีะ](https://user-images.githubusercontent.com/78845680/222413411-8b1ef486-8a95-42e4-997b-565f567f2bc7.PNG)<br />
รอซักพักจะพบว่ามีการเชื่อมต่อกลับมาที่ port ที่เปิดไว้<br />
![ืแ](https://user-images.githubusercontent.com/78845680/222413788-482f29bc-a891-418b-8639-1394192da7a6.PNG)<br />
ถ้าเรา ls ดูก็จะพบว่าเราเจอ user.txt ซึ่งข้างในจะมี flag<br />
![1234124](https://user-images.githubusercontent.com/78845680/222414194-0dfc1f15-d0d5-4210-ab9b-fdbf7dadec51.PNG)<br />
ต่อคือเราจะหา root.txt ซึ่งเดาได้เลยว่าเราต้องมีสิทธิ์ root ถึงจะอ่านได้ดังนั้นเราต้อง privilege escalation เพื่อเอาสิทธิ์ root<br />
โดยผมจะใช้ linpeas ในการดูว่ามีอะไรใช้ทำ privilege escalation ได้บ้าง<br />
***linpeas link:*** https://github.com/carlospolop/PEASS-ng/<br />
ผมได้ใช้ python เปิด local server เพื่อที่จะได้ให้ target machine download ไปใช้ได้<br />
![asdasd](https://user-images.githubusercontent.com/78845680/222416377-0a0cbcfb-7817-4f5c-8ac7-aa78916b4af5.PNG)<br />
ใช้ wget ใน target machine<br />
![asd2](https://user-images.githubusercontent.com/78845680/222416652-42307802-9ce5-4451-95a0-80d3fa757789.PNG)<br />
จากนั้นเปลี่ยน permission เพื่อ run<br />
![58](https://user-images.githubusercontent.com/78845680/222416841-987173c0-ed10-4966-8671-b72a53719962.PNG)<br />
จากการใช้ linpeas จะพบว่ามี env ที่สามารถรันโดยใช้สิทธิ์ superuser ได้<br />
![ev](https://user-images.githubusercontent.com/78845680/222417445-94ec115c-5ca7-4b38-b3e3-29a1b8a11470.PNG)<br />
เราสามารถหาวิธีใช้ได้จาก GTFOBins<br />
***GTFOBins Link:*** https://gtfobins.github.io/<br />
![erhreh](https://user-images.githubusercontent.com/78845680/222417741-afe2a4fb-cc19-4213-a995-8c4362f520d9.PNG)<br />
เรามาลองกันเลย<br />
![asdasdasdasd](https://user-images.githubusercontent.com/78845680/222417795-cfc7336e-d318-4635-9163-4bb5b4ef7c78.PNG)<br />
***-p: Makes the shell privileged<br />***
ถ้า whoami ดูจะพบว่าได้เป็น root user แล้วจากนั้นก็สามารถอ่าน flag ใน root.txt ได้แล้ว<br />
![ans](https://user-images.githubusercontent.com/78845680/222418528-3d4d6dff-21f4-4f7c-804c-50caa686f4f7.PNG)
