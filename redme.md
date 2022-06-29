#### 1. 环境准备：
```
# 使用的是pipenv进行环境管理，首先下载安装pipenv模块
1. pip install pipenv

# 创建虚拟环境及安装相关包(ps:执行以下指令需切换至项目目录下)
2.pipenv install
3.pipenv shell

```

#### 2.初始化数据库表
```python
# 修改run.py下的spider类的self.conn参数，修改为自己的数据库连接
self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='spider')

# 进入spider 下的run.py，创建main方法执行，如下代码，创建数据表
 create_sql = "create table url_data(" \
                 "id INT(11) NOT NULL AUTO_INCREMENT," \
                 "url VARCHAR(255) NOT NULL," \
                 "status VARCHAR(255) NULL," \
                 "PRIMARY KEY (`id`))ENGINE=InnoDB AUTO_INCREMENT 1 DEFAULT CHARSET=utf8; "
    test_spider = spider()
    test_spider.mysql_execute(create_sql)
```

#### 3.运行
```python
# 在spider/run.py 的main方法下运行实例化之后的类的get_url,及event方法
test_spider = spider()
test_spider.geturl()
test_spider.event()
```