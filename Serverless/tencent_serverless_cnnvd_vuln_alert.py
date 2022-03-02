# -*- coding: utf8 -*-
import xml
import zipfile
import requests
import re
import os
from xml.dom.minidom import parse
import xml.dom.minidom
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


class SendMail():
    def __init__(self,user,passwd):
        self.user_email = user
        self.passwd = passwd

    def run(self,content):
        my_sender = self.user_email
        my_pass = self.passwd
        users = ["xxxxxxxxxxx@qq.com"]
        for user in users:
            try:
                msg = MIMEText(content, 'html', 'utf-8')
                msg['From'] = formataddr(["Hack8", my_sender])
                msg['To'] = formataddr([user,user])
                msg['Subject'] = "您监测的组件今日有新漏洞，请注意查看！"
                server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
                server.login(my_sender, my_pass)
                server.sendmail(my_sender, [user,user], msg.as_string())
                server.quit()
            except Exception as e:
                print(e)

send1 = SendMail("user@xxxx.com","password")


class CNNVD():
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537."
        }
        self.domain_link = "http://www.cnnvd.org.cn"

    def GetAttachedZipLink(self, i=0):
        '''
        :param i:
        最新、当月XML文件每天发布更新，默认下载最新即可
        i：最新0、当月1、本年2依次
        :return:url
        '''

        url1 = "/web/xxk/xmlDown.tag"
        resp1 = requests.get(self.domain_link + url1, headers=self.headers, timeout=20)
        reg1 = re.compile(r'onclick="xmldown\(\'/web\',\'(.+?)\'')
        result = reg1.findall(resp1.text)[i]
        return result

    def ZipToXml(self, link, path=""):
        '''
        从zip文件获取xml，
        :param link:
        :param path:
        :return:path
        '''
        zip_path = path + link.split("//")[-1]
        resp1 = requests.get(self.domain_link + link, headers=self.headers, timeout=20)
        with open(zip_path, "wb") as file:
            file.write(resp1.content)
        zf = zipfile.ZipFile(zip_path)
        try:
            zf.extract("latest.xml", path=path)
        except RuntimeError as e:
            print("解压失败：", e)
        zf.close()
        os.remove(zip_path)
        return "latest.xml"

    def ParseXml(self, file_name):
        DOMTree = xml.dom.minidom.parse(file_name)
        collection = DOMTree.documentElement
        Vulnerabities_in = collection.getElementsByTagName('entry')
        print("共计漏洞：",len(Vulnerabities_in))
        vuln_list = []
        i_count = 1
        for vulnerabit in Vulnerabities_in:
            try:
                number = vulnerabit.getElementsByTagName('vuln-id')[0]
                title = vulnerabit.getElementsByTagName('name')[0]
                product = vulnerabit.getElementsByTagName('product')[0]
                description = vulnerabit.getElementsByTagName('vuln-descript')[0]
                severity = vulnerabit.getElementsByTagName('severity')[0]
                vulntype = vulnerabit.getElementsByTagName('vuln-type')[0]
                other_id = vulnerabit.getElementsByTagName('other-id')[0]
                cve_id = other_id.getElementsByTagName('cve-id')[0]
                for keyword in ["fastjson","apollo","nacos","spring","zookeeper","mysql","nginx","tomcat"]:
                    if keyword in title.childNodes[0].data or keyword in product.childNodes[0].data or keyword in description.childNodes[0].data:
                        vuln_info = "<p style=\"text-align:center\"><b>({})".format(i_count)+title.childNodes[0].data+"</b></p>"
                        vuln_info += "<p><b>漏洞编号：</b>"+"/".join([number.childNodes[0].data,cve_id.childNodes[0].data])+"</p>"
                        vuln_info += "<p><b>漏洞等级：</b>"+severity.childNodes[0].data+"</p>"
                        vuln_info += "<p><b>漏洞类型：</b>"+vulntype.childNodes[0].data+"</p>"
                        vuln_info += "<p><b>影响产品：</b>"+product.childNodes[0].data+"</p>"
                        vuln_info += "<p><b>漏洞描述：</b>"+description.childNodes[0].data+"</p>"
                        vuln_info += "<p><b>详细链接：</b>"+'http://www.cnnvd.org.cn/web/xxk/ldxqById.tag?CNNVD={}</p>'.format(number.childNodes[0].data)
                        vuln_list.append(vuln_info)
                        i_count += 1
            except:
                pass
        global send1
        content = "<p><h3>当前发现漏洞数：{}，漏洞信息如下：</h3></p><hr>".format(len(vuln_list))
        content += "<br/><hr>".join(vuln_list)
        send1.run(content)
        print("邮件发送成功！！！")
            

    def run(self):
        print("下载zip......")
        zip_link = self.GetAttachedZipLink()
        print("解压zip，处理xml中......")
        xml_path = self.ZipToXml(zip_link,path="/tmp/")
        self.ParseXml("/tmp/"+xml_path)

def main():
    obj1 = CNNVD()
    obj1.run()

def main_handler(event, context):
    main()