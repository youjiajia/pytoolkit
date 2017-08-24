# pytoolkit
-----------
Individual learning and working scripts.This project has these directories.
> * system
> * study
> * script


### system
> When I reinstall the system like ubuntu or deepin,I always need install and configure the environment.This directory includes commands for config the environment.


### study
> This dirtory is for me to take notes when study.


### script
Small script summary
```
mail.py is the script for sending mails useing python.
	use:python mail.py
	Parameters: -f filepath
                -s if use ssl_smtp
                -t if has file
    install: you need config your mail info in mail.py by class DefaultConfig.
mail.py 使用python来发送邮件的脚本.
    使用: python mail.py
    参数: -t 如果需要上传文件，输入-t
          -f 如果需要上传文件，传入文件路径
          -s 如果使用ssl_smtp，输入-s
    安装：需要文件里修改DefaultConfig类,配置上你的邮箱信息

```
```
pingshu8.py is the script for geting mp3 medias from www.pingshu8.com useing python.
	use:python pingshu8.py YourShowHomePage
pingshu8.py 通过爬虫从www.pingshu8.com下载mp3文件
    使用:python pingshu8.py 需要下载的评书吧节目主页地址
```
```
toQiNiu.py is the script to upload the entire folder to the seven bull cloud.
    use:python toQiNiu.py
    Parameters: -a seven bull ACCESS_KEY
                -s seven bull SCRET_KEY
                -b seven bull BUCKET_NAME which you need to upload
                -d DIRNAME which you will upload
                --filep which you need to upload for filtering unwanted files
                --dirp which you need to upload for filtering unwanted folders
    And you can change these parameters in toQiNiu.py by class DefaultConfig.
toQiNiu.py 通过脚本直接上传整个文件夹到七牛云
    使用:python toQiNiu.py
    参数: -a 七牛 ACCESS_KEY
                -s 七牛 SCRET_KEY
                -b 你需要传入的七牛 BUCKET_NAME
                -d 需要上传的文件夹名称
                --filep 筛选不需要文件的正则表达式
                --dirp 筛选不需要文件夹的正则表达式
    或者你可以直接修改文件里的DefaultConfig类
```

