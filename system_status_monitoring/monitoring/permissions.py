from rest_framework.permissions import BasePermission,IsAuthenticated

class SystemPermission(BasePermission):
    def has_permission(self, request, view):

        # 超级用户和普通用户都可以操作
        # is_authenticated用于判断user是否登录，也可继承模块IsAuthenticated
        return bool(request.user and request.user.is_authenticated)










