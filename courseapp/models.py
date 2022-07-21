# Create your models here.
import uuid

from django.core.validators import MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from .validators import validate_video_extension, validate_size_mb

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None


""" Role """


class Role(models.Model):
    role_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    role_name = models.CharField(max_length=256)
    role_description = models.CharField(max_length=256)
    level = models.IntegerField(default=1, validators=[MaxValueValidator(8)])
    # right = models.ForeignKey('', related_name='permission', on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(User, related_name='role_user', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.role_name


""" category """


class Category(models.Model):
    category_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    category_name = models.CharField(max_length=256)

    def __str__(self):
        return self.category_name


"""" course """


class Course(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    course_name = models.CharField(max_length=256)
    course_id = models.CharField(max_length=256)
    category = models.ForeignKey('Category', related_name='course_category', on_delete=models.SET_NULL, null=True)
    document = models.FileField(null=True, blank=True, upload_to='images/')
    start_date = models.DateField()
    end_date = models.DateField()
    # member_name = models.ForeignKey('Member', related_name='member', on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=256)
    created_by = models.ForeignKey(User, related_name='course_user', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.course_name


"""" Modules """


class Module(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    module_name = models.CharField(max_length=256)
    parent_id = models.ForeignKey('self', related_name='children', on_delete=models.SET_NULL, null=True)
    course_id = models.ForeignKey('Course', related_name='course_module', on_delete=models.SET_NULL, null=True)
    level = models.IntegerField(default=1)
    created_by = models.ForeignKey(User, related_name='module_user', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.module_name


"""" ModulesTag """


class ModuleTag(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    module_id = models.ForeignKey('Module', related_name='module_tag', on_delete=models.SET_NULL, null=True)
    course_id = models.ForeignKey('course', related_name='course_module_tag', on_delete=models.SET_NULL, null=True)
    tag = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


"""" Course ModulesAttachement with validation """


class ModuleAttachement(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    module_id = models.ForeignKey('Module', related_name='module_attachement', on_delete=models.SET_NULL, null=True)
    course_id = models.ForeignKey('Course', related_name='course_module_attachement', on_delete=models.SET_NULL,
                                  null=True)
    file = models.FileField(null=True, blank=True, upload_to='images/', validators=[validate_video_extension,
                                                                                    validate_size_mb])
    created_by = models.ForeignKey(User, related_name='module_attachement_user',
                                   on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


""" course module content """


class ModuleContent(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    module_id = models.ForeignKey('Module', related_name='module_content', on_delete=models.SET_NULL, null=True)
    course_id = models.ForeignKey('Course', related_name='course_module_content', on_delete=models.SET_NULL, null=True)
    content = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='module_content_user',
                                   on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


""" course module comment """


class ModuleComment(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    module_id = models.ForeignKey('Module', related_name='module_comment', on_delete=models.SET_NULL, null=True)
    course_id = models.ForeignKey('Course', related_name='course_module_comment', on_delete=models.SET_NULL,
                                  null=True)
    comment = models.TextField(max_length=512, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='module_comment_user',
                                   on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


"""Module member"""


class ModuleMember(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    module_id = models.ForeignKey('Module', related_name='module_member', on_delete=models.SET_NULL, null=True)
    course_id = models.ForeignKey('Course', related_name='course_module_member', on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    # member_name = models.ForeignKey('Member', related_name='module_member', on_delete=models.SET_NULL, null=True)
    select_role = models.ForeignKey('Role', related_name='module_role', on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(User, related_name='module_member_user', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
