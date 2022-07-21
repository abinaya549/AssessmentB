from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Module, ModuleTag, Category, Role, Course, ModuleAttachement, ModuleContent, \
    ModuleComment, ModuleMember


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "email"]


""" to Register User """


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('USERNAME', 'password', 'password2',
                  'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},

        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            user=validated_data['user'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_email(validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user


""" Role """


class RoleSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source="created_by", read_only=True)

    class Meta:
        model = Role
        fields = ['role_id', 'role_name', 'role_description', 'level', 'created_by',
                  'created_by_name', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'created_by_name']

    def create(self, validated_data):
        user_id = self.context.get('user_id')
        auth_user_id = User.objects.get(id=user_id)
        validated_data['created_by'] = auth_user_id
        user = Role.objects.create(**validated_data)
        return user


""" Category """


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'category_name']


""" Course """


class CourseSerializer(serializers.ModelSerializer):
    course_category = CategorySerializer(read_only=True, many=True)
    # member = MemberSerializer(read_only=True, many=True)
    created_by_name = serializers.CharField(source="created_by", read_only=True)

    class Meta:
        model = Course
        fields = ('course_name', 'course_id', 'category', 'document', 'start_date', 'end_date', 'member_name',
                  'description', 'created_by', 'created_by_name', 'course_category', 'updated_at',
                  'created_at',)
        read_only_fields = ['created_by', 'created_by_name']

    def create(self, validated_data):
        user_id = self.context.get('user_id')
        auth_user_id = User.objects.get(id=user_id)
        validated_data['created_by'] = auth_user_id
        user = Course.objects.create(**validated_data)
        return user


""" Module """


class ModuleSerializer(serializers.ModelSerializer):
    course_module = CourseSerializer(read_only=True, many=True)
    created_by_name = serializers.CharField(source="created_by", read_only=True)

    def to_representation(self, instance):
        children = ModuleSerializer(instance.children, many=True, read_only=True).data
        response = super().to_representation(instance)
        response['children'] = children

        return response

    class Meta:
        model = Module
        fields = ['module_name', 'course_id', 'parent_id', 'course_module', 'updated_at',
                  'created_at', 'created_by', 'created_by_name']
        read_only_fields = ['created_by', 'created_by_name']

    def create(self, validated_data):
        user_id = self.context.get('user_id')
        auth_user_id = User.objects.get(id=user_id)
        validated_data['created_by'] = auth_user_id
        user = Module.objects.create(**validated_data)
        return user


""" ModuleTag """


class ModuleTagSerializer(serializers.ModelSerializer):
    module_tag = ModuleSerializer(read_only=True)
    course_module_tag = CourseSerializer(read_only=True)

    class Meta:
        model = ModuleTag
        fields = ['module_id', 'course_id', 'tag', 'module_tag', 'course_module_tag', 'updated_at',
                  'created_at']


""" ModuleAttachement """


class ModuleAttachementSerializer(serializers.ModelSerializer):
    module_attachement = ModuleSerializer(read_only=True)
    course_module_attachement = CourseSerializer(read_only=True)
    created_by_name = serializers.CharField(source="created_by", read_only=True)

    class Meta:
        model = ModuleAttachement
        fields = ['module_id', 'course_id', 'file', 'module_attachement', 'course_module_attachement', 'updated_at',
                  'created_at', 'created_by', 'created_by_name']
        read_only_fields = ['created_by', 'created_by_name']

    def create(self, validated_data):
        user_id = self.context.get('user_id')
        auth_user_id = User.objects.get(id=user_id)
        validated_data['created_by'] = auth_user_id
        user = ModuleAttachement.objects.create(**validated_data)
        return user


""" Course module content serializers """


class ModuleContentSerializer(serializers.ModelSerializer):
    module_content = ModuleSerializer(read_only=True)
    course_module_content = CourseSerializer(read_only=True)
    created_by_name = serializers.CharField(source="created_by", read_only=True)

    class Meta:
        model = ModuleContent
        fields = ['module_id', 'course_id', 'content', 'module_content', 'course_module_content', 'updated_at',
                  'created_at', 'created_by', 'created_by_name']
        read_only_fields = ['created_by', 'created_by_name']

    def create(self, validated_data):
        user_id = self.context.get('user_id')
        auth_user_id = User.objects.get(id=user_id)
        validated_data['created_by'] = auth_user_id
        user = ModuleContent.objects.create(**validated_data)
        return user


""" Course module comment serializers """


class ModuleCommentSerializer(serializers.ModelSerializer):
    module_comment = ModuleSerializer(read_only=True)
    course_module_comment = CourseSerializer(read_only=True)
    created_by_name = serializers.CharField(source="created_by", read_only=True)

    class Meta:
        model = ModuleComment
        fields = ['module_id', 'course_id', 'comment', 'module_comment', 'course_module_comment', 'updated_at',
                  'created_at', 'created_by', 'created_by_name']
        read_only_fields = ['created_by', 'created_by_name']

    def create(self, validated_data):
        user_id = self.context.get('user_id')
        auth_user_id = User.objects.get(id=user_id)
        validated_data['created_by'] = auth_user_id
        user = ModuleComment.objects.create(**validated_data)
        return user


""" Course module member serializers """


class ModuleMemberSerializer(serializers.ModelSerializer):
    module_member = ModuleSerializer(read_only=True)
    course_module_member = CourseSerializer(read_only=True)
    created_by_name = serializers.CharField(source="created_by", read_only=True)

    class Meta:
        model = ModuleMember
        fields = ['module_id', 'course_id', 'module_member', 'start_date', 'end_date', 'member_name',
                  'select_role', 'course_module_member', 'updated_at',
                  'created_at', 'created_by', 'created_by_name']
        read_only_fields = ['created_by', 'created_by_name']

    def create(self, validated_data):
        user_id = self.context.get('user_id')
        auth_user_id = User.objects.get(id=user_id)
        validated_data['created_by'] = auth_user_id
        user = ModuleMember.objects.create(**validated_data)
        return user
