from django.urls import path,re_path

from monitoring import views

from rest_framework.documentation import include_docs_urls




urlpatterns = [
    # 调用函数，周期--接口一（未实现周期更改）
    path('control-period/',views.Control_Period.as_view()),
    # 查看列表，分页，筛选--接口二
    path('status-list/',views.StatusListViews.as_view()),
    # 获取主机ip--接口三
    path('get-host-ip/',views.Host_Ip.as_view()),
    # 获取筛选数据，产生图片--接口四
    path('file-create/',views.File_Create.as_view()),
    # 返回404--接口五
    path('raise-error/',views.Raise_Error.as_view()),

    # 模块coreapi,只针对drf的接口文档
    path('api-docs/', include_docs_urls(title='系统监控-API接口文档')),

]


# 测试数据
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register(r'test',views.TestViews)
urlpatterns+=router.urls


