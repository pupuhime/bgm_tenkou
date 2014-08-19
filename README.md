##tenkou転校##

###批量导出/删除收藏条目###

Bangumi有时候连接情况不太好，会一直卡在某个地方

Don't panic!

如果是网络情况不好可以换个时间再试

###使用###

Python 3 脚本

参数说明：

```
tenkou.py [-h] [-d {chii.in,bgm.tv,bangumi.tv}] [-u UID]
          [--password PASSWORD] [--wipe] [-p PATH] [--auth AUTH]
          [--useragent USERAGENT] [--authfile AUTHFILE] [-v]
```

```
-h, --help                  帮助
-d DOMAIN, --domain DOMAIN  选择域名，默认bgm.tv, 还可选择bangumi.tv或chii.in
-u UID, --uid UID           你的id
--password PASSWORD         你的网站登录密码
--wipe                      删除所有条目！谨慎使用！
-p PATH, --path PATH        本地保存目录，必须事先建立
--auth AUTH                 auth字符串
--useragent USERAGENT       你浏览器的User-Agent
--authfile AUTHFILE         保存User-Agent和Auth字符串的文件（Authfile）位置
-v, --version               程序版本
```

只有id是必须的，不需要导出进度的话，不必输入密码

###使用举例###

以下只是举例，你可以自由搭配

```
1. tenkou.py -u 9999999                  导出id为9999999那人的条目

2. tenkou.py -u 9999999 -p ./bgm_backup  备份到当前位置的bgm_backup目录

3. tenkou.py -u 9999999 --password 123
                                         使用密码登录，导出id为9999999的条目，包括观看进度

4. tenkou.py -u 9999999 --useragent Mozilla --auth LFJDSLAF%LFASJD
                                         使用auth，导出id为9999999的条目，包括观看进度

5. tenkou.py -u 9999999 --authfile ./authfile.txt
                                         使用authfile，导出id为9999999的条目，包括观看进度

6. tenkou.py -u 9999999 --password 123 --wipe
                                         使用密码，导出id为9999999的条目，包括观看进度
                                         完全删除条目

7. tenkou.py -u 9999999 --useragent Mozilla --auth LFJDSLAF%LFASJD --wipe
                                         使用auth，导出id为9999999的条目，包括观看进度
                                         完全删除条目

8. tenkou.py -u 9999999 --authfile ./authfile.txt --wipe
                                         使用authfile，导出id为9999999的条目，包括观看进度
                                         完全删除条目
```

###获取Auth和User-Agent的方法###

直接查看你浏览器的调试工具，这个Auth就是cookie里的Auth

###什么是Authfile###

只是一个文本文件，保存了User-Agent和Auth字符串

其中，第一行是User-Agent；第二行是Auth字符串

authfile文件名任意，上面只是举例而用了authfile.txt

###需要同时提供密码和Auth吗？###

不需要，密码、User-Agent和Auth、Authfile三选一即可

可以参考上面的使用举例

###有更简单的方法获取Auth和User-Agent吗？###

和tenkou.py同时提供了一个getcookie.user.js的greasemonkey/tampermonkey脚本

安装后在bangumi页面可以查看并自动复制你的User-Agent/Auth，你可以手动分拆开来输入，或者直接新建一个authfile

如图所示：

Firefox GM

![Firefox选项](http://i.imgur.com/2GdaRSn.jpg)

Chrome Tampermonkey

![Chrome选项](http://i.imgur.com/Qwk6ff0.jpg)

结果

![结果](http://i.imgur.com/NW3IYnc.jpg)

###安全性？你会知道我的密码吗？###

不会，只是你本地和网站的通信，没有什么信息会传到我这里

至于密码和Auth方式，因为这个只是用cookie的auth，没什么大的差别


###最后生出的备份文件说明###

最后的备份文件按

A段：

* 动画（anime）
* 音乐（music）
* 游戏（game）
* 书籍（book）
* 三次元（real）

以及B段：

* 在看（do）
* 看过（collect）
* 想看（wish）
* 搁置（on_hold）
* 抛弃（dropped）

来命名

组成形式为```bangumi_A段_B段.txt```

比如

```
bangumi_anime_do.txt
bangumi_book_collect.txt
```