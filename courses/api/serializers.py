from rest_framework import serializers
from ..models import Subject,Course,Module,Content,Profile
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer): # new
   class Meta:
     model = User
     fields = ('id', 'username',)
     
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
       model = Subject
       fields = ['id', 'title', 'slug']

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
       model = Module
       fields = ['order', 'title', 'description']


class CourseSerializer(serializers.ModelSerializer):
  modules = ModuleSerializer(many=True, read_only=True)
  class Meta:
   model = Course
   fields = ['id', 'subject', 'title', 'slug', 'overview',
   'created', 'owner', 'modules']

class ItemRelatedField(serializers.RelatedField):
    def to_representation(self, value):
      return value.render()


class ContentSerializer(serializers.ModelSerializer):
   item = ItemRelatedField(read_only=True)
   class Meta:
     model = Content
     fields = ['order', 'item']

class ModuleWithContentsSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)
    class Meta:
     model = Module
     fields = ['order', 'title', 'description', 'contents']

class CourseWithContentsSerializer(serializers.ModelSerializer):
    modules = ModuleWithContentsSerializer(many=True)
    class Meta:
     model = Course
     fields = ['id', 'subject', 'title', 'slug',
     'overview', 'created', 'owner', 'modules']