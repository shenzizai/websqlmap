# websqlmap
Based on sqlmapapi and flask.
首先运行sqlmapapi,默认参数即可:python sqlmapapi.py -s 

写这个东西并不是因为我真正需要它，是因为我只是单纯想写点东西来熟悉下flask/bootstrap,仅此而已。
所以这个websqlmap也只是一个半成品，等想写的时候再写。

数据库为了方便用的是sqlite，如果换其他数据库需要注意的是转义符，sqlite中的''等同于mysql中的\\'

目前来说，最核心的功能就一个批量检测url吧。

后期可能会添加一些功能，例如删除任务，扫描任务文本导入，结果文本导出等。

待续
