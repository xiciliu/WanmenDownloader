# -*- coding: utf-8 -*-
"""
Created on Wed May 30 17:54:35 2018

@author: xici
"""

import requests
import re
import json,os,shutil
from hyper.contrib import HTTP20Adapter

thecookies={}
proxies = {
  "http": "http://135.245.248.89:8000",
  "https": "http://135.245.248.89:8000",
}
proxies=None

#savein='course/'
savein='I:/Technology/AI/course/'
headers = {
        "Accept": "text/html, application/xhtml+xml, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-GB",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type":"application/json;charset=utf-8",
        "DNT": "1",
        #"Host": 'playback.wanmen.org',
        
        #":authority": "api.wanmen.org",
        #":method": "GET",
        #":path": "/4.0/content/courses/5b74db50d3dd5f78a6289b7f",
        #":scheme": "https",
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjViY2Y0NWUxOWI1NWJiYTk0NTRjYWM2ZSIsImlhdCI6MTU0MDM5NTcwMCwiZXhwIjoxNTQyOTg3NzAwLCJpc3MiOiJ1cm46YXBpIn0.5rPwmkjnEKcKgd4VAA94aDrhWz-u19HlTnCFYuX8YMI",
        "origin": "https://www.wanmen.org",
        "referer": "https://www.wanmen.org/courses/5b74db50d3dd5f78a6289b7f",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36",
        "x-app": "uni",
        "x-time": "5bd092b6",
        "x-token": "eeaf6ad6eef910ff2c7ae3c36806db1b"
      }

def download(url,dir,name):
    print("downloading with requests ",url)
    #print(thecookies)
    if len(name.split('.'))<=1:
        space=url.split('.')
        if len(space)>1:
            prefix=space[len(space)-1]
            name=name+'.'+prefix
    print(dir+name)
    if not os.path.exists(dir+name):
        r = requests.get(url,cookies=thecookies,proxies=proxies) 
        with open(dir+name, "wb") as code:
            code.write(r.content)
    else:
        print('skip down due to existance')

def saveM3u8(text,dir,name):
    #处理/fragments/开头
    text=removeFragment(text)
    with open(dir+name, "w") as f:
        f.write(text)

def removeFragment(text):
    fra=re.findall('/fragments/(.*?)/',text)
    if fra:
        tempfrag=fra[0]
        tempfrag='/fragments/'+tempfrag+'/'
        text=text.replace(tempfrag,'')
    return text
    
#返回.ts列表
def readts(content):
    #return re.search(r'^(.*?)\((.*)\)$', _jsonp).group(2)
    result=re.findall('(.*?)\.ts',content)
    if result:
        print('find ts: %d'%(len(result)))
        return result
    else:
        print('not find ts')

 
#下载ts文件集合
def downts(tslist,dir,name,m3u8):
    
    tsname=''
    j=0
    size=len(tslist)
    for ts in tslist:
        j=j+1
        print('%d of %d'%(j,size))
        tsname=ts.split('/')[-1]
        #tsname=10000+j
        if '/fragments/' in ts:
            download('https://playback.wanmen.org'+ts+'.ts',dir,str(tsname)+'.ts')
        else:
            download('https://media.wanmen.org/'+ts+'.ts',dir,str(tsname)+'.ts')
    
    #合并ts文件
    combile(name,dir,m3u8)
    
#将当前目录下的.ts文件移动到dir目录
def movets(dir):
    files=os.listdir('.')
    for f in files:
        if f.isfile() and os.path.splitext(path)[1]=='.ts':
            shutil.move(f,dir)
        
def combile(name,dir,m3u8):
    #移动所有.ts到对应的dir
    #shutil.move(,dir)
    
    exec_str=r'ffmpeg -allowed_extensions ALL -i '+dir+m3u8+' -c copy '+name
    print(exec_str)
    os.system(exec_str)  # 使用cmd命令将资源整合
    
    '''
    exec_str = r'copy /b  "' + r'*.ts" "'+ name
    print(exec_str)
    os.system(exec_str)  # 使用cmd命令将资源整合
    #exec_str = r'del  "' + r'*.ts"'
    #os.system(exec_str)  # 删除原来的文件
    '''
        
def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)
            
    
def readList(url):
    r = requests.get(url,cookies=thecookies,proxies=proxies)
    print(r.content)

def test():
    str='''#EXTINF:8.341667,
a7e15b93-c3c1-4193-be6b-5dbed204b097_mobile_low0.ts
#EXTINF:3.169833,
a7e15b93-c3c1-4193-be6b-5dbed204b097_mobile_low1.ts
#EXTINF:8.341667,'''
    result=re.findall('\n(.*?)\.ts',str)
    print(result)
    
    #login()
    '''
    print(thecookies)
    S= requests.Session()#自动处理cookie
    c=requests.cookies.RequestsCookieJar()
    print(c)
    c.set('o_cookie','760057995')
    c.set('pgv_info','ssid=s7625432710')
    c.set('pgv_pvi','3783237632')
    c.set('pgv_pvid','8662440280')
    c.set('pgv_si','s1062241280')
    c.set('player_exist','1')
    c.set('qqmusic_fromtag','66')
    c.set('ts_last','y.qq.com/portal/player.html')
    c.set('ts_refer','ADTAGbaiduald')
    c.set('ts_uid','4584336768')
    c.set('tvfe_boss_uuid','018abf599886d5ba')
    c.set('yplayer_open','1')
    c.set('yqq_stat','0')
    c.set('yq_index','0')
    S.cookies.update(c)
    print(thecookies)
    '''
    
    #403
    url='https://media.wanmen.org/94045fee-87bb-40a0-8f37-4b3438023908_pc_mid.m3u8?sign=f7b66bc9a7f20469764023a8474a4e68&t=5bc9f855&r=1f2f2223b901e816569902206ea4aec7'
    
    url='https://playback.wanmen.org/recordings/z1.wanmen.44508051991983044/1536392266_1536393816.m3u8?sign=b544052be99f68b2ce77b454791e130b&t=5bd1ff04&r=7d8e3a18e1ac44538a6d5ab18828d2dc'
    url='https://playback.wanmen.org/recordings/z1.wanmen.44508051991983044/1536370166_1536373477.m3u8?sign=75599270d4a812665e5196e2771c8d26&t=5bd31ba6&r=2a2608a7be5b3f9564aad2874cc4bda1'
    url='https://playback.wanmen.org/recordings/z1.wanmen.44508051991983044/1536370166_1536373477.m3u8?sign=fe54c30a97bf899a58be2aba5b676769&t=5bd582ec&r=bb981fa55905ee11589e065811d3fcb6'
    url='https://media.wanmen.org/a7e15b93-c3c1-4193-be6b-5dbed204b097_pc_high.m3u8?sign=5475bd976cf118c2b93c2a49e33d7539&t=5bd582a4&r=d6dd483afc95e2b541c98128e4472bbf'
    res=requests.get(url,proxies=proxies)
    if res.status_code==200:
        print('get data')
        #print(res)
        #print(res.text)
        m3u8=(url.split('?')[0]).split('/')[-1]
        print(m3u8)
        coursename='0909-强化学习入门（9）'
        dir=savein+coursename+'/'
        print('make dir: '+dir)
        dir=dir.strip()
        dirstr=dir
        if dirstr[-1]=='/':
            dirstr=dirstr[:-1]
        print(dirstr)
        if not os.path.exists(dirstr):
            os.makedirs(dirstr)
        
        print(res.text)
        saveM3u8(res.text,dir,m3u8)
        downts(readts(res.text),dir,savein+coursename+'.mp4',m3u8)
    else:
        print('get data error')
        print(res)
    
    
    #url='https://playback.wanmen.org/fragments/z1.wanmen.44508051991983044/1536392275604-1536392283937.ts'
    #download(url,'','test.ts')
    
    
def login():
    loginurl='https://api.wanmen.org/4.0/main/signin'
    res=requests.post(loginurl,data={"account":"13651819457","password":"1234abcd","code":"","unionid":"","thirdtype":"","nickname":""},proxies=proxies)
    print(res.text)
    thecookies=res.cookies

def readfromfile():
    f=open('./587f469c196f0f565637213e.txt','r',encoding = 'utf-8')
    str=f.read()
    f.close()
    if str.startswith(u'\ufeff'):
        str = str.encode('utf8')[3:].decode('utf8')
    return json.loads(str)

def down2(courseid,fromCache):
    login()
    
    js={}
    if fromCache:
        #加载已经下载到本地的json清单文件
        js=readfromfile()
    else:
        #courseid='590c489571b2262ac78f1d75'
        urlconfig='https://api.wanmen.org/4.0/content/courses/'+courseid
        res = requests.get(urlconfig,cookies=thecookies,proxies=proxies)
        #res.text
        print(res.json())
        js=res.json()
    
    #ok, 下载课程说明和ppt课件
    global savein
    name=js['name']
    savein=savein+name+'/'
    if not fromCache:
        with open(savein+courseid+'.txt', "w") as f:
            f.write(res.text)
        
    presentationVideo=js['presentationVideo']['hls']['pcHigh']
    if os.path.exists(savein+name+'.mp4'):
        print(name+'.mp4 already exists')
    else:
        res=requests.get(presentationVideo,headers=headers,cookies=thecookies,proxies=proxies)
        url=presentationVideo
        if res.status_code==200:
                m3u8=(url.split('?')[0]).split('/')[-1]
                print(m3u8)
                dir=savein+name+'/'
                print('make dir: '+dir)
                dir=dir.strip()
                dirstr=dir
                if dirstr[-1]=='/':
                    dirstr=dirstr[:-1]
                print(dirstr)
                if not os.path.exists(dirstr):
                    os.makedirs(dirstr)
                
                saveM3u8(res.text,dir,m3u8)
                downts(readts(res.text),dir,savein+name+'.mp4',m3u8)
        else:
            print('get data error')
    
    documents=js['documents']
    
    if documents:
        for doc in documents:
            if os.path.exists(savein+doc['name']):
                print(doc['name']+' already exists')
                continue
            else:
                download(doc['url'],'',savein+doc['name'])
    
    
    parentlecs=js['lectures']
    index_p=0
    for parentlec in parentlecs:
        index_p=index_p+1
        lecturename=str(index_p)+"_"+parentlec['name']
        if not os.path.exists(savein+lecturename):
            os.makedirs(savein+lecturename)
        lectures=parentlec['children']
        #print(js)
        if lectures:
            print(len(lectures))
            index_v=0
            for video in lectures:
                print(video)
                index_v=index_v+1
                coursename=str(index_v)+"_"+video['name']
                print('get data '+coursename)
                if os.path.exists(savein+lecturename+'/'+coursename+'.mp4'):
                    print(coursename+'.mp4 is downloaded')
                    continue
                url=video['hls']['pcHigh']
                res=requests.get(url,headers=headers,cookies=thecookies,proxies=proxies)
                if res.status_code==200:
                    m3u8=(url.split('?')[0]).split('/')[-1]
                    print(m3u8)
                    dir=savein+lecturename+'/'+coursename+'/'
                    print('make dir: '+dir)
                    dir=dir.strip()
                    dirstr=dir
                    if dirstr[-1]=='/':
                        dirstr=dirstr[:-1]
                    print(dirstr)
                    if not os.path.exists(dirstr):
                        os.makedirs(dirstr)
                    
                    saveM3u8(res.text,dir,m3u8)
                    downts(readts(res.text),dir,savein+lecturename+'/'+coursename+'.mp4',m3u8)
                else:
                    print('get data error')
                print(res)
                #break

#测试创建目录，即使有/结尾
def testCreateDir():
    str='course/0908-强化学习入门（1）/'
    str=str.strip()
    if str[-1]=='/':
        str=str[:-1]
    print(str)
    os.makedirs(str)

#ok
def testRemoveFragment():
    file_object = open(r'course\0908-强化学习入门（1）\1536370166_1536373477.m3u8')
    text=''
    try:
        text = file_object.read()
        
    except e:
        print(e)
    finally:
        file_object.close()
    print(text)
    text=removeFragment(text)
    print(text)
#测试获取正确的课程清单，需要含hls
def testGetList():
    courseid='5aaf651d77ae46495090ba57'
    urlconfig='https://api.wanmen.org/4.0/content/courses/'+courseid
    res = requests.get(urlconfig,cookies=thecookies,proxies=proxies)
    #res.text
    print(res.json())
    #check
    hls=res.json()['lectures'][0]['children'][0]['hls']
    print(hls)
    ok=False
    if hls:
        if len(hls)>0:
            ok=True
        else:
            ok=False
    else:
        ok=False
    if ok:
        print('fine data')
    else:
        print('bad data')
        
#testCreateDir()
#test()
#testRemoveFragment()
#testGetList()
down2('590c489571b2262ac78f1d75',False)



