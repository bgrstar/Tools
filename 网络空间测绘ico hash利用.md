#  网络空间测绘ico hash利用


## zoomeye
zoomeye使用文件md5，语法：`iconhash:""`

## shodan
shodan使用mmh3，语法：`http.favicon.hash:`
```
# https://twitter.com/brsn76945860/status/1171233054951501824
pip install mmh3

-----------------------------
# python 2
import mmh3
import requests
 
response = requests.get('https://cybersecurity.wtf/favicon.ico')
favicon = response.content.encode('base64')
hash = mmh3.hash(favicon)
print hash

-----------------------------

# python 3

import mmh3
import requests
import codecs
 
response = requests.get('https://cybersecurity.wtf/favicon.ico')
favicon = codecs.encode(response.content,"base64")
hash = mmh3.hash(favicon)
print(hash)

```
## fofa
fofa使用使用mmh3，语法：`icon_hash=""`
和shodan一样也可以使用在线生成mmh3 hash

## quake
quake使用md5，语法：`favicon: ""`

## hunter
hunter使用md5，语法：`web.icon=""`

