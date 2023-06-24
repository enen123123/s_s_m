**系统状态监控项目**        
接口1：查验系统情况记录周期     
接口2：将数据以列表形式展示，具有分页、筛选功能     
接口3：返回本机的ip地址     
接口4：产生一个数据的折线统计图下载路径，可根据传入的参数获取指定的部分数据内容     
接口5：提供404的状态码，例如：下载数据为空时返回404状态码       
测试接口：对数据操作测试        
文档接口：提供各个接口的一些基本数据        

**Python 3.10**     

**依赖组件**        
MySQL      

**MySQL配置，settings中配置文件**       
DATABASES = {       
    'default': {        
        'ENGINE': 'django.db.backends.mysql',   # 数据库引擎        
        'NAME': 'monitoring',         # 你要存储数据的库名，事先要创建      
        'USER': 'root',         # 数据库用户名      
        'PASSWORD': '123456',     # 密码        
        'HOST': '127.0.0.1',    # 主机      
        'PORT': '3306',         # 数据库使用的端口      
    }       
}           

**数据库生成迁移文件,终端中输入**       
python manage.py makemigrations     
python manage.py migrate        

_**步骤：**_        
**1.将文件名匹配**      
将文件名更改为system_status_monitoring，与文件夹中根App名匹配       

**2.安装依赖库**        
终端中输入以下命令，如果下载不成功，命令后增加-i+镜像源     
pip install -r requirements.txt         

**3.增加、选择解释器**      
File->settings->Project:system_status_monitoring->Python Tnterpreter:       
以上路径下，选择一个解释器，推荐：Python 3.10 某路径下\python.exe       


