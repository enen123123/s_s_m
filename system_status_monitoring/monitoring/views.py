import os
import time
import socket
import logging
from django.conf import settings
from django.http import FileResponse

import psutil
import threading
import pygal
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from apscheduler.schedulers.background import BackgroundScheduler
from django_filters.rest_framework import DjangoFilterBackend

from monitoring.models import SystemInfo
from monitoring.permissions import SystemPermission
from monitoring.serializers import SystemSerializers
from monitoring.pagination import SystemInfoPagination,SystemInfoListPagination
from monitoring.filters import UserInfoFilter


a = os.path.join(settings.BASE_DIR, 'static\\log_info')
logging.basicConfig(
    # 时间、日志等级、第几行、信息内容
    format='%(asctime)s|%(levelname)s|%(lineno)s|%(message)s',
    # 日志输出级别
    level=logging.INFO,
    #当使用这个可以设置编码方式的属性时，filename和filemode失效，不共存
    stream=open(os.path.join(settings.BASE_DIR, 'static\\logging_info\\log_info.txt'),'a',encoding='utf-8'),

)
logging.info('--------------------这是一条日志记录信息--------------------')

class TestViews(viewsets.ModelViewSet):
    '''独立视图集，测试操作所有数据'''
    queryset = SystemInfo.objects.all()
    serializer_class =SystemSerializers
    pagination_class = SystemInfoPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class =UserInfoFilter
    permission_classes = (SystemPermission,)


class StatusListViews(ListAPIView):
    '''查看数据列表，筛选数据信息并查看'''
    queryset = SystemInfo.objects.all()
    serializer_class = SystemSerializers
    pagination_class = SystemInfoListPagination

    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserInfoFilter

    # 设置一个传输数据的函数，使用APScheduler设置为周期函数
    def post_data(self):
        # 本机ip
        h_i=socket.gethostbyname(socket.gethostname())
        # CPU使用率
        c_u=psutil.cpu_percent()
        # 内存使用率
        m_u=psutil.virtual_memory().percent
        # 硬盘使用率
        h_u=psutil.disk_usage('/').percent
        # 网络I/O速率，读、写
        n_i_r=psutil.net_io_counters().bytes_recv
        n_i_s=psutil.net_io_counters().bytes_sent

        sys_data={
            'host_ip':h_i,
            'cpu_usage':c_u,
            'menory_usage':m_u,
            'hardpan_usage':h_u,
            'network_i':n_i_r/1024,
            'network_o':n_i_s/1024,
        }
        serializer = SystemSerializers(data=sys_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # 查看运行的进程名字
        logging.info({threading.current_thread().name})


class Control_Period(APIView):
    '''调用周期函数，返回系统监控数据的周期'''
    queryset = SystemInfo.objects.all()
    serializer_class = SystemSerializers
    pagination_class = SystemInfoListPagination

    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserInfoFilter

    # 实例化调度器
    scheduler = BackgroundScheduler()
    # 设置定时任务，选择方式为interval，时间间隔为10s
    period_time=10
    scheduler.add_job(StatusListViews().post_data, "interval", seconds=period_time,id='2333',name='2333的定时任务名')
    scheduler.start()
    # 获取定时任务列表,id和name
    logging.info(scheduler.get_jobs())
    def get(self,request):
        return Response('监控系统的周期为:10s一次')

class File_Create(ListAPIView):
    '''获取筛选数据，产生图片文件'''
    queryset = SystemInfo.objects.all()
    serializer_class = SystemSerializers
    pagination_class = SystemInfoListPagination

    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserInfoFilter

    def get(self,request):
        qs = self.get_queryset()
        f_q = self.filter_queryset(qs)
        serializer_obj = self.get_serializer(instance=f_q, many=True)

        #加一个判断无参数时的404报错，不打印文件
        if not serializer_obj.data :
            a=Raise_Error().get(request)
            return Response(status=a.status_code)

        # 返回数据制作列表，制作图像文件
        cpu_list = []
        menory_list = []
        hardpan_list = []
        a=0
        for query in serializer_obj.data:
            cpu_list.append(float(query['cpu_usage']))
            menory_list.append(float(query['menory_usage']))
            hardpan_list.append(float(query['hardpan_usage']))
            a+=1
            if a==100:
                break

        Line_Chart = pygal.Line()
        Line_Chart.title = ' cpu、内存、硬盘使用率 '
        Line_Chart.x_labels = map(str, range(1,101))
        Line_Chart.x_title = '数据/条'
        Line_Chart.y_title = '使用率/%'
        # 当不设置坐标的时候，会自动产生，主要是x轴，y轴自动生成的最好
        Line_Chart.add('cpu使用率', cpu_list)
        Line_Chart.add('内存使用率', menory_list)
        Line_Chart.add('硬盘使用率', hardpan_list)
        # .svg文件需要在浏览器中打开
        # time.time()  获取从1970.1.1 00:00:00到当前时刻的秒数
        svg_file=os.path.join(settings.BASE_DIR, 'static\\svg_info', f'{time.time()}.svg')
        svg_file_name= f'{time.time()}.svg'
        Line_Chart.render_to_file(svg_file)
        # FileResponse需要调用模块
        response = FileResponse(open(svg_file, 'rb'))
        # 选择下载的类型
        response['content_type'] = 'application/octet-stream'
        # 设置文件名
        response['Content-Disposition'] = 'attachment; filename={}'.format(svg_file_name)
        # 经过测试，下载功能本身就处于线程中
        logging.info({threading.current_thread().name})
        # 返回响应
        return response


class Host_Ip(APIView):
    '''获取主机ip'''
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get(self, request):
        host_ip = socket.gethostbyname(socket.gethostname())
        return Response(host_ip)


class Raise_Error(APIView):
    '''返回404状态码'''
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    def get(self,request):
        return Response(status=status.HTTP_404_NOT_FOUND)

