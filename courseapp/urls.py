from rest_framework.routers import DefaultRouter
from .views import ModuleView, ModuleTagView, ModuleAttachementView, CategoryView, CourseView, \
    RegisterUserAPIView, ModuleContentView, ModuleCommentView, ModuleMemberView, UserDetailAPI, \
    CustomTokenObtainPairView
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)

router = DefaultRouter()
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
    path("details/", UserDetailAPI.as_view()),
    path('register/', RegisterUserAPIView.as_view(), name='user_register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]

