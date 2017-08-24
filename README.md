# pytoolkit
-----------
Individual learning and working scripts.This project has these directories.
> * system
> * study
> * script


### system
> When I reinstall the system like ubuntu or deepin,I always need install and configure the environment.This directory includes commands for config the environment.


### python
> Like the system dirtory, this dirtory is config for python, include pyenv ,pip,  virtualenv and so on.

### study
> This dirtory is for me to take notes when study.


### script
Small script summary
```
mail.py is the script for sending mails useing python.
	use:python mail.py
	Parameters: -f filepath
				-n filename
                -s if use ssl_smtp
                -t if has file
```
```
pingshu8.py is the script for geting mp3 medias from www.pingshu8.com useing python.
	use:python pingshu8.py YourShowHomePage
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
```

