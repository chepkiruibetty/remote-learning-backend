from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

# Create your models here.
class Subject(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering=['title']
    def __str__(self):
      return self.title

class Course(models.Model):
    owner = models.ForeignKey(User,related_name='courses_created', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,related_name='courses',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    post_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='courses/')
    students = models.ManyToManyField(User,related_name='courses_joined',blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
      ordering = ['-created']
    def __str__(self):
       return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=80, blank=True)
    status = models.TextField(max_length=254, blank=True)
    profile_picture = models.ImageField(upload_to='images/', default='default.png')

class Module(models.Model):
    course = models.ForeignKey(Course,related_name='modules',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    def __str__(self):
     return self.title

class Content(models.Model):
   module = models.ForeignKey(Module,related_name='contents',on_delete=models.CASCADE)
   content_type = models.ForeignKey(ContentType,
on_delete=models.CASCADE,
limit_choices_to={'model__in':(
'text',
'video',
'image',
'file')})
   object_id = models.PositiveIntegerField()
   item = GenericForeignKey('content_type', 'object_id')

class ItemBase(models.Model):
   owner = models.ForeignKey(User,related_name='%(class)s_related',on_delete=models.CASCADE)
   title = models.CharField(max_length=250)
   created = models.DateTimeField(auto_now_add=True)
   updated = models.DateTimeField(auto_now=True)
   def render(self):
       return render_to_string('courses/content/{}.html'.format(
              self._meta.model_name), {'item': self})



   class Meta:
    abstract = True
   def __str__(self):
    return self.title

class Text(ItemBase):
  content = models.TextField()

class File(ItemBase):
  file = models.FileField(upload_to='files')

class Image(ItemBase):
 file = models.FileField(upload_to='images')

 class Video(ItemBase):
  url = models.URLField()

