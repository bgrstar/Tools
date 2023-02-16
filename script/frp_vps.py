#python3
import socket
import binascii
import json
import threading
import queue
import sqlite3
import hashlib
import time

ipQueue = queue.Queue()


hex1="000100010000000100000000"
hex2="0000000000000001000000c5"
hex3="6f00000000000000bc7b2276657273696f6e223a22302e33372e30222c22686f73746e616d65223a22222c226f73223a2277696e646f7773222c2261726368223a22616d643634222c2275736572223a22222c2270726976696c6567655f6b6579223a223339303037333863396338313762616234333835343866343861366432383233222c2274696d657374616d70223a313632393038323130392c2272756e5f6964223a22222c226d65746173223a6e756c6c2c22706f6f6c5f636f756e74223a317d"

def sqlinit():
        conn=sqlite3.connect("frp.db")
        frp = """CREATE TABLE if not exists frp (
                        ip  text,
                        version  text,
                        country text,
                        as_organization,text)
                        """

        conn.execute(frp)

def execsql(sql):
        conn=sqlite3.connect("frp.db")
        conn.execute(sql)
        conn.commit()


def connect(jsonstr):

        ip=jsonstr['id']

        country=jsonstr['country']
        as_organization=jsonstr['as_organization']

        s1=ip.split(":")
        host=s1[0]
        port=int(s1[1])

        try:
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.settimeout(5)
                s.connect((host,port))
                str1=binascii.unhexlify(hex1)
                s.send(str1)
                str2=binascii.unhexlify(hex2)
                s.send(str2)
                str3=binascii.unhexlify(hex3)
                s.send(str3)
                data1=s.recv(12)
                data2=s.recv(12)
                data2=data2.hex()
                resp=bytes.decode(s.recv(int(data2[-2:],16)))
                s.close()
                json_str=resp[resp.find("{"):]
                k=json.loads(json_str)
                #print(k)
                version=k['version']
                if 'run_id' in k:
                        if k['run_id']!="":
                                # OK
                                sql = "INSERT INTO frp(ip, \
                                version,country,as_organization) \
                                VALUES ('%s', '%s', '%s','%s')" % \
                                (ip,version,country,as_organization)
                                execsql(sql)
                                
                                res='{"ip":"%s","version":"%s","country":"%s","as_organization","%s"}'%(ip,version,country,as_organization)

                                with open('suc.txt','a') as file:        
                                    file.writelines(res+"\n")
                                print(res)

                        else:
                                # fail
                                res='{"ip":"%s","version":"%s","error":"%s"}'%(ip,version,k['error'])
                                print(res)
                                with open('fail.txt','a') as file:        
                                    file.writelines(res+"\n")

                else:
                        # fail
                        res='{"ip":"%s","version":"%s","error":"%s"}'%(ip,version,k['error'])
                        print(res)
                        with open('fail.txt','a') as file:        
                            file.writelines(res+"\n")

        except  Exception as e:
                # Timeout
                print("error: ",ip,e)
                with open('error.txt','a') as file:
                        sss='{"ip":"%s","error":"%s"}'%(ip,e)
                        file.writelines(sss+"\n")                           

def read_json():
        text=open('1.json','r').readlines()
        for json_str in text:
                jsonstr = json.loads(json_str)
                ipQueue.put(jsonstr)


def fetch(ipQueue):

        while True:
                try:
                        jsonstr=ipQueue.get_nowait()
                        connect(jsonstr)
                except Exception as e:
                        break

if __name__ == '__main__':
        sqlinit()
        read_json()

        threads = []
        threadNum = 10
        for i in range(0, threadNum):
                t = threading.Thread(target=fetch, args=(ipQueue,))
                threads.append(t)
        for t in threads:
                t.start()
        for t in threads:
                t.join()