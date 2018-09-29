# websqlmap
Based on sqlmapapi and flask.

前端使用的bootstrap+jquery,后端使用的flask.

数据库为了方便用的是sqlite，如果换其他数据库需要注意的是转义符，sqlite中的''等同于mysql中的\'

首先运行sqlmapapi,默认参数即可:python sqlmapapi.py -s 

目前有批量扫描功能，可以在文本框输入url list,也可以上传包含url的文本文件。
