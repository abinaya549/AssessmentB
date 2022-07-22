import os

from django.core.exceptions import ValidationError

""" validation for module attachement """


def validate_video_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp4', '.png', '.jpg', '.pdf']
    if ext.lower() not in valid_extensions:
        raise ValidationError('Unsupported file extension. Only mp4,png,jpg,pdf file allowed')


def validate_size_mb(attachment):
    file_size = attachment.size
    limit_mb = 4
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError("Max size of file is %s MB" % limit_mb)
