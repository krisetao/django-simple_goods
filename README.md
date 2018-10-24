## 一个以 Django+Xadmin 作为框架搭建的商品管理。

### 网页功能

- django xadmin的后台管理系统，方便对于商品、用户及其他动态内容的管理
- 商品信息展示
- 基于用户权限展示不同字段
- 可导出excel
- mysql作为数据库

### 文档总结

MVC模型

django项目的结构大致如下：

```markdown
|-- managers.py    # 模型处理逻辑
|-- tmall：
    |-- settings.py        # 项目配置
    |-- urls.py            # 项目路由定义
    |-- wsgi.py        # nginx/apache
|--goods/： app应用
    |-- xadmin.py        # django xadminx后台管理系统
    |-- apps.py        # 应用级别的配置
    |-- forms.py        # 表单处理逻辑
    |-- models.py        # 模型定义
    |-- urls.py            # 路由设置
    |-- views.py        # 控制层
templates : 前端模板
|-- static : 静态文件
```



### 项目运行

1.windows创建虚拟环境

~~~markdown
virtualenv env
cd env -> cd Script -> activate
~~~

2.下载pip 包

~~~python
pip install -r requirements
~~~

3.创建数据库

~~~mysql
mysql > CREATE DATABASE `databasename` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
~~~

4.迁移数据库

~~~python
python manage.py makemigrations
python manage.py migrate
~~~

5.创建管理员账号：

```django
python manage.py createsuperuser
```

6.静态文件的收集：

~~~python
python manage.py collectstatic
~~~

7.启动项目

```django
python manage.py runserver 0.0.0.1:8000
#如果你的服务器上面的8000端口开启了，那么可以访问你的服务器 IP 地址的8000端口看看项目是否正常运行：
```

### 开始部署

### 安装和配置 Gunicorn

1、首先需要在虚拟环境中安装 Gunicorn：

```
pip install gunicorn
```

2、创建项目的 Gunicorn 配置文件（退出虚拟环境）：

```
sudo vim /etc/systemd/system/gunicorn_goods.service
```

3、配置信息如下：

~~~shell
[Unit]
Description=Goods daemon
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/upmiao
ExecStart=/upmiao/env/bin/gunicorn --access-logfile - --workers 2 --bind unix:/upmiao/goods.sock goods.wsgi:application

[Install]
WantedBy=multi-user.target


~~~

- User 填写自己当前用户名称

- WorkingDirectory 填写项目的地址

- ExecStart 中第一个地址是虚拟环境中 gunicorn 的目录，所以只需要改前半部分虚拟环境的地址即可

- workers 2 这里是表示2个进程，可以自己改

- unix 这里的地址是生成一个 sock 文件的地址，直接写在项目的根目录即可

- goods.wsgi 表示的是项目中 wsgi.py 的地址，我的项目中就是在 goods文件夹下的

  ### 启动配置文件

  文件配置完成之后，使用下面的命令启动服务：

  ```shell
  ~$ sudo systemctl start gunicorn_goods
  ~$ sudo systemctl enable gunicorn_goods
  ```

  查看服务的状态可以使用命令：

  ```shell
  ~$ sudo systemctl status gunicorn_goods
  ```

  上面的命令启动没有问题可以看看自己的项目的跟目录下面，应该会多一个 tendcod.sock 文件的。

  后续如果对 gunicorn 配置文件做了修改，那么应该先使用这个命令之后重启：

  ```shell
  ~$ sudo systemctl daemon-reload
  ```

  然后再使用重启命令：

  ```shell
  ~$ sudo systemctl restart gunicorn_goods
  ```

### 配置 Nginx

首先创建一个 Nginx 配置文件，不要使用默认的那个：

```
~$ sudo vi /etc/nginx/sites-available/goodsnginx
```

配置信息如下：

~~~shell
server {
    # 端口和域名
    listen 80;
    server_name www.网站名.com;

    # 日志 -- 需要自己创建
    access_log /upmiao/logs/nginx.access.log;
    error_log /upmiao/logs/nginx.error.log;

    # 不记录访问不到 favicon.ico 的报错日志
    location = /favicon.ico { access_log off; log_not_found off; }
    # static 和 media 的地址
    location /static/ {
        root /upmiao/goods;
    }
    location /media/ {
        root /upmiao;
    }
    # gunicorn 中生成的文件的地址
    location / {
        include proxy_params;
        proxy_pass http://unix:/upmiao/goods.sock;
    }
}

server {
    listen 80;
    server_name 网站名.com;
    
~~~

第一个 server 是主要的配置，第二 server 是实现301跳转，即让不带 www 的域名跳转到带有 www 的域名上面。



### 连接 Nginx 配置

上面的配置检查好之后，使用下面的命令来将这个配置跟 Nginx 建立连接，使用命令：

```shell
~$ sudo ln -s /etc/nginx/sites-available/goodsnginx /etc/nginx/sites-enabled
```

运行完毕之后可以查看一下 Nginx 的运营情况，看看会不会报错：

```shell
~$ sudo nginx -t
```

如果上面这句没有报错，那么恭喜你，你的配置文件没有问题，可以继续下一步，如果报错了，需要按照报错的信息去更改配置文件中对应行的代码，好好检查一下吧！

没报错的话，重启一下 Nginx：

```shell
~$ sudo systemctl restart nginx
```

好了，重启 Nginx 之后可以登录自己配置的域名，看看自己的项目是不是已经成功的运行了呢！

## 后续维护

之后的项目维护中，如果更改了 gunicorn 的配置文件，那么需要依次执行下面两条语句去重启服务，如果只是修改了 Django 项目的内容，只需要单独执行第二条重启命令即可：

```shell
~$ sudo systemctl daemon-reload
~$ sudo systemctl restart gunicorn_goods
```

如果修改了 Nginx 的配置文件，那么需要依次执行下面两条语句去重启服务：

```shell
~$ sudo nginx -t
~$ sudo systemctl restart nginx
```




### 报错解决

#### ModuleNotFoundError: No module named 'imagekit.models'

#### 1. 安装

要在 Django 使用 ImageField 模块，必须先安装第三方库 Pillow：

```
pip install pillow
```

然后安装  django-imagekit

```
pip install django-imagekit
```

完成上述步骤后，在 Django 项目的 `settings.py` 文件中的 `INSTALLED_APPS` 添加上： `'imagekit'`。

现在准备工作全部完成，可以在项目中使用 django-imagekit 来处理图片了。

#### 2. 简单例子

承接上一篇的例子，我们在 modles 中这样使用 django-imagekit：

```
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# 用来保存上传图片相关信息的模型
class Profile(models.Model):
    name = models.CharField(max_length = 50)

    # 原图
    picture = models.ImageField(upload_to = 'test_pictures') 

    # 注意：ImageSpecField不会生成数据库中的表
    # 处理后的图片
    picture_90x90 = ImageSpecField(
        source="picture", 
        processors=[ResizeToFill(90, 90)], # 处理后的图像大小
        format='JPEG',  # 处理后的图片格式
        options={'quality': 95} # 处理后的图片质量
        )

    def __str__(self):
        return self.name
```

图片上传后会根据我们的设定生成相应的处理后的图片。

要在前端显示处理后的图片只需这样：

```
src="{{ profile.picture_90x90.url }}
```

#### TypeError: __init__() got an unexpected keyword argument 'processors'

#### ModuleNotFoundError: No module named 'django.core.urlresolvers'

简单来说，原因就是：django2.0 把原来的 django.core.urlresolvers 包 更改为了 django.urls包，所以我们需要把导入的包都修改一下就可以了。

#### xadmin安装

xadmin是Django后台管理系统admin的一个替换方案，xadmin对admin做了一些扩展。界面上有些操作会更方便。比如xadmin自带了导出功能，可以导出excel，csv，json等格式的文档。

##### 1. 安装

首先，我的环境是：python3.6，django2.0

如果直接使用pip install xadmin会报错，因为这样安装默认对应的django版本是1.4的（印象中）。所以我们需要安装xadmin项目django2分支的代码。命令如下：

```
pip install git+git://github.com/sshwsfc/xadmin.git@django2
```

或使用https的地址安装：

```
pip install git+https://github.com/sshwsfc/xadmin.git@django2
```

注意，由于上述命令用到了Git工具，所以请安装Git工具后再执行上述命令（安装Git后可能需要重启电脑才能生效）。

另外，如果上述命令行方式较慢，也可直接下载分支的代码，再安装：

- [进入xadmin项目django2的分支](https://github.com/sshwsfc/xadmin/tree/django2)
- 点击页面上的Download ZIP，下载zip包到本地
- 执行命令安装：`pip install --cache-dir . d:\xadmin-django2.zip(请自行替换)`



#### django修改表的结构，加入DateField类型字段

~~~python
WARNINGS:
goods.Product.interval: (fields.W122) 'max_length' is ignored when used with IntegerField
        HINT: Remove 'max_length' from field
goods.Product.repeat: (fields.W122) 'max_length' is ignored when used with IntegerField
        HINT: Remove 'max_length' from field
You are trying to add the field 'create_date' with 'auto_now_add=True' to product without a default; the database needs something to populate existing rows.

 1) Provide a one-off default now (will be set on all existing rows)
 2) Quit, and let me add a default in models.py
Select an option: 1
Please enter the default value now, as valid Python
You can accept the default 'timezone.now' by pressing 'Enter' or you can provide another value.
The datetime and django.utils.timezone modules are available, so you can do e.g. timezone.now
Type 'exit' to exit this prompt
[default: timezone.now] >>>

~~~

解决办法：
选择1，然后下一步提示符后面回车：

之后运行python manage.py migrate即可。



#### TypeError: int() argument must be a string, a bytes-like object or a number, not 'datetime.datetime'









#### Field 'create_date' doesn't have a default value

解决方法一：（足够用了）

 在数据库中对报错的字段设置默认值， 整数：0 ，字符串：设为NULL，

找到对应的表--->设计表--->默认选择框（设置默认值）

解决二：Django model 从新设计表

#### TypeError: __str__ returned non-string (type int)

更改app models的字段     

~~~python
def __str__(self):
        return str(self.pid)
~~~

#### TypeError: _path() got an unexpected keyword argument 'namespace'



### Django2 URL Namespace名称空间定义新方法

在Django2 URL Namespace名称空间定义有了新的写法， 我在升级完devecho.com后，添加新的app时遇到这个问题，需要大家注意。Django2.0新增了在urls.py中app_name来指定namespace。
我们之前通过reverse函数来反向获取url
reverse语法

```python
reverse("<namespace>:<url-name>", kwargs={"<kwarg>": "<val>"})
```

在Django <= 1.11 我们通过关键词namespace参数定义名称空间

```python
urlpatterns = [
    url(r'^posts/', include('posts.urls', namespace='posts')) 
]
```

在Django 2.0+ 我们可以省略namespace=

```python
urlpatterns = [
    re_url(r'^posts/', include(('posts.urls', 'posts'))) 
]
```

更进一步 我们把namespace定义到被include的urls.py中去
使用app_name定义名称空间

```python
urlpatterns = [
    re_path(r'^posts/', include('posts.urls')) 
]
```

posts/urls.py

```python
from django.urls import re_path, path
from posts.views import YearArchive, ArchiveListView

app_name = 'posts'

urlpatterns = [
    ...
    re_path(r'^$', ArchiveListView.as_view(), name='archive-list'),
    re_path(r'^user/(?P<year>[0-9]{4})/$', YearArchive.as_view(), name='year-archive'),
    path('user/<int:year>/', YearArchive.as_view(), name='year-archive-path'),
]
```

现在我们仍然可以用reverse函数和模板中的url获取URL

```python
reverse("posts:archive-list")
reverse("posts:archive-list", kwargs={"year": 2017})
{% url "posts:archive-list" %}
{% url "posts:year-archive" year=2017 %}
```

#### python No migrations to apply

第一步：
删除该app名字下的migrations文件。

第二步：
进入数据库，找到django_migrations的表，删除该app名字的所有记录。
delete from django_migrations;

第三步:
python manage.py makemigrations
python manage.py migrate

#### django admin 后台丢失样式

找到admin 包的static文件夹下的样式文件 copy到自身的static的文件夹下

#### django 显示字段为空

{{ field | default:'' }}