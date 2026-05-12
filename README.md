# bilibili-fav-video
B站收藏视频看板 - 爬虫+MySQL+Flask

##功能特点
-自动爬取收藏夹内视频标题，作者，播放量，视频id
-基于爬取内容进行数据去重存储 
-导出Excel备份
-Flask Web页面展示数据

##技术栈
-Python 3.8+
-Requests (爬虫)
-Flask (Web展示）
-PyMySQL (数据库操作）
-Pandas (Excel导出)
-MySQL 5.7+

·····bash
pip install -r requirements.txt

使用教程：
一.运行代码前需要完成的事项
-利用浏览器F12抓包获取收藏夹api接口地址(通常以list列表开头，注意观察响应里是否有收藏夹名称，然后进入标头复制url地址，并填入主代码的url中)
-右键找到的list包，然后复制为cURL(cmd)，接着进入爬虫工具库（https://spidertools.cn/#/curl2Request），选择curl转requests，最后把获取的伪装信息(headers,cookies,params)替换到主代码中去。
-最后就可以运行代码了

##
初次提交项目，问题可能很多，我会尽量修改，谢谢指教。
