# WanmenDownloader
万门课程下载

万门大学的网站有不少比较好的课程。
不管是app还是pc端都只能在线观看，而且很多课程都有不太长的时间性。不能及时观看，就浪费了。
如果能将这些课程下载到本地慢慢看就更好了。

本程序为达到次目标而做。

requirements: 

python 3.x

modules: requests


使用:

修改 savein，课程存储目录

修改 down2()中的courseid

有时需要预先下载m3u8文件，将down参数fromCache设置为True

运行 python SpiderWanmen.py

