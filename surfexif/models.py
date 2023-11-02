from django.contrib.auth.models import AbstractUser
from django.db import models
import os


class User(AbstractUser):
    pass


# Technique for generating a user-specific file upload path from the
# Django documentation below:
# https://docs.djangoproject.com/en/3.1/ref/models/fields/
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/uploads/user_<id>/<filename>
    return 'uploads/user_{0}/{1}'.format(instance.uploader.id, filename)


# Django model for storing the path and characteristics of an image
class Image(models.Model):

    # Field for poster of the image
    uploader = models.ForeignKey('User',
                                 on_delete=models.CASCADE,
                                 related_name='images_uploaded')

    # Field for the file location of the image
    imagepath = models.ImageField(upload_to=user_directory_path)

    # Field for date and time post was made
    timestamp = models.DateTimeField(auto_now_add=True)

    # String representation for easier debugging in the admin interface
    def __str__(self):
        return f'{self.imagepath}'

    # Method for returning a filename
    def filename(self):
        return f'{os.path.basename(self.imagepath.name)}'


# Django model for any tags associated with an image
class Tag(models.Model):

    # Field for relationships between tags and images
    images = models.ManyToManyField('Image',
                                    blank=True,
                                    related_name='tags_with_image')

    # Field for the word used as the tag
    descriptor = models.CharField(max_length=200)

    # Field for the category that a tag belongs to
    category = models.ForeignKey('Category',
                                 on_delete=models.CASCADE,
                                 related_name='tags_with_category')

    # String representation for easier debugging in the admin interface
    def __str__(self):
        return f'{self.category} : {self.descriptor}'


# Django model for the category that a tag is associated with
class Category(models.Model):

    # Field for the word used as the category
    descriptor = models.CharField(max_length=200,
                                  unique=True)

    # String representation for easier debugging in the admin interface
    def __str__(self):
        return f'{self.descriptor}'
