import datetime
from django.core.management.base import BaseCommand
# import etcd3

class Command(BaseCommand):
    help='hello python'
    # 增加参数
    def add_arguments(self, parser):
        parser.add_argument('place', type=str, help='地点')
    # 命令实际的逻辑函数
    def handle(self, *args, **options):
        # 获取参数
        p=options['place']
        # 控制窗口输出语句，像print()
        self.stdout.write('hello,这是一个测试自定义python manage.py命令的文件')
        date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.stdout.write('%s时间：'%p)
        self.stdout.write('%s'%date)
        # self.stdout.write(self.style.SUCCESS('命令已完成'))
        # self.stdout.write(self.style.ERROR('命令未完成'))

# python manage.py test_hello +参数
