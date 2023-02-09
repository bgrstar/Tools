import  requests
import  re

#from https://bbs.kanxue.com/thread-275995.htm

try:
    url=input('输入链接地址: ')
    obj=re.compile(r"http.*/",re.S)
    url=obj.finditer(url)
    for i in url:
        pid=i.group()
        print(i.group())
    header={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    print('1',pid)
    resp=requests.get(url=pid,headers=header, allow_redirects=False)
    print(resp.text)
    pid=re.finditer(r"video/(?P<IID>.*?)/",resp.text)
    print('2',pid)
    for i in pid:
        ID=i.group('IID')
        print(i.group('IID'))
 
    resp1='https://www.douyin.com/light/'+ID
    print(resp1)
    resp2=requests.get(url=resp1,headers=header)
    c = re.search(r"video_id%3D(?P<IID1>.*?)%26", resp2.text)
    print(c.group('IID1'))
    zq=c.group('IID1')
    urll=f"https://www.douyin.com/aweme/v1/play/?video_id={zq}"
    with open(f'{zq}'+'.mp4','wb') as f :
        m4=requests.get(url=urll,headers=header).content
        f.write(m4)
except:
    print('解析异常')
