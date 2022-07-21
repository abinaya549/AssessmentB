from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Module, ModuleTag, Category, Course, Role, ModuleAttachement, ModuleContent, \
    ModuleComment, ModuleMember
from .serializers import ModuleSerializer, ModuleTagSerializer,  \
    ModuleAttachementSerializer, \
    CategorySerializer, CourseSerializer, RoleSerializer, RegisterSerializer, \
    ModuleContentSerializer, ModuleCommentSerializer, ModuleMemberSerializer

from rest_framework.viewsets import ModelViewSet

""" AuthenticationView """


class UserDetailAPI(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.auth())
        serializer = UserSerializer(user)
        return Response(serializer.data)


""" Class based view to register user """


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


""" role """


class RoleView(ModelViewSet):
    serializer_class = RoleSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Role.objects.all()

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


""" Category """


class CategoryView(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


""" Course """


class CourseView(ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Course.objects.all()

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


""" ModuleView """


class ModuleView(ModelViewSet):
    serializer_class = ModuleSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Module.objects.filter(parent_id=None)

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


""" ModuleTagView """


class ModuleTagView(ModelViewSet):
    serializer_class = ModuleTagSerializer
    queryset = ModuleTag.objects.all()


""" ModuleAttachementView """


class ModuleAttachementView(ModelViewSet):
    serializer_class = ModuleAttachementSerializer
    permission_classes = (IsAuthenticated,)
    queryset = ModuleAttachement.objects.all()

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


""" Module Content """


class ModuleContentView(ModelViewSet):
    serializer_class = ModuleContentSerializer
    permission_classes = (IsAuthenticated,)
    queryset = ModuleContent.objects.all()

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


""" Module Comment """


class ModuleCommentView(ModelViewSet):
    serializer_class = ModuleCommentSerializer
    permission_classes = (IsAuthenticated,)
    queryset = ModuleComment.objects.all()

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


""" Module Comment """


class ModuleMemberView(ModelViewSet):
    serializer_class = ModuleMemberSerializer
    permission_classes = (IsAuthenticated,)
    queryset = ModuleMember.objects.all()

    def get_serializer_context(self):
        return {'user_id': self.request.us}
