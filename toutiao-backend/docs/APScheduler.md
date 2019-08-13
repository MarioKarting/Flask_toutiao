# APScheduler项目中使用

## 1. offline scheduler

独立启动

`common/scheduler/main.py` 为独立启动文件

多进程执行

## 2. online scheduler

在创建Flask app的时候创建scheduler对象，供视图触发scheduler
