# 实时推送教务系统成绩信息
主要功能：模拟用户对教务系统进行请求（每三分钟执行一次），对比新出成绩和旧的成绩信息是否一样，若不同则实时推送成绩信息到目的邮箱。

仅对[电子科大成都学院](http://newjw.cduestc.cn/)有效。

## 运行方式
`crontab -e`

添加任务：
```
*/3 * * * * bash /root/python/control.sh
```

**第一次需要手动执行** `get_grades.py`
```python
cd /root/python/
python get_grades.py
mv grades.csv grades_old.csv
```

## 运行环境
- `Linux （云主机）`
- `Python 2/3`
- `Shell`

## 文件介绍
文件目录:  `/root/python/`
```
├── control.sh
├── get_grades.py
├── grades_old.csv
└── send_mail.py
```

- `control.sh`: 负责对比新旧成绩文件，判断成绩是否更新，是否发送邮箱。
- `get_grades.py`: 爬取教务系统，生成 `grades.csv`成绩表。
- `send_mail.py`: 发送邮件。
- `grades_old.csv`: 手动执行`get_grades.py`，生成`grades.csv`，重命名为`grades_old.csv`，目的是与新成绩表形成对比。

## 效果

![](https://ws1.sinaimg.cn/large/b8ddc78bgy1ftm6r2ei3bj20b70igmy0.jpg)

## 解决一些问题

由于Windows和Linux系统天生不同，所以有时候，同样的代码，在Windows上能正常运行，而在Linux上就会出现各种异常。

**1. lxml解析异常**
尝试使用`html.parser`解析

即：
``` python
soup = BeautifulSoup(r.text, 'html.parser')
```
参考：https://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml

**2. Linux发送邮件异常**
- 检查邮箱账号`POP3/SMTP服务`是否开启
- `password`使用的是**授权码**，而非密码
-  服务器开启SMTP服务，检查`iptables`
-  检查xx云的安全组配置出网规则
- **Linux**：登录SMTP服务器使用`SSL 465端口`

``` python
server = smtplib.SMTP_SSL(smtp_server, 465)  # 用SSL 465端口，以防在Linux上出现异常
server.login(from_addr, password)
```

**3. UnicodeEncodeError: 'ascii' codec can't encode ... ordinal not in range(128)**
加入以下代码：

``` python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
```

