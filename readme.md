# HAVA自动部署平台

## 第一步
* source activate hava

##### 导出
* pip freeze >requirements.txt
##### 导入
* pip install -r requirements.txt
* python manage.py makemigrations
* python manage.py migrate

## 定时任务
https://www.jianshu.com/p/f6e80e6125cc
* python manage.py crontab add
* python manage.py crontab show
* python manage.py crontab remove

## 增加脚本
* 脚本目录：havaApp/script