from rest_framework.routers import DefaultRouter
from .views import ModuleView, ModuleTagView, ModuleAttachementView, CategoryView, CourseView, RoleView, \
    RegisterUserAPIView, ModuleContentView, ModuleCommentView, ModuleMemberView, UserDetailAPI
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)

router = DefaultRouter()
router.register('role', RoleView)

router.register('category', CategoryView)
router.register('course', CourseView)
router.register('module', ModuleView)
router.register('moduletag', ModuleTagView)
router.register('moduleattachement', ModuleAttachementView)
router.register('modulecontent', ModuleContentView)
router.register('modulecomment', ModuleCommentView)
router.register('modulemember', ModuleMemberView)

urlpatterns = [
    path('api/', include(router.urls)),
    path("details", UserDetailAPI.as_view()),
    path('register', RegisterUserAPIView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]

