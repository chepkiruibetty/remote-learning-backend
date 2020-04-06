from django.urls import path,include
from rest_framework import routers
from . import views
from .views import UserList, UserDetail,UserViewSet


app_name = 'courses'
router = routers.DefaultRouter()
router.register('courses', views.CourseViewSet,basename='Course')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
path('subjects/',
    views.SubjectListView.as_view(),
    name='subject_list'),

path('subjects/<pk>/',
    views.SubjectDetailView.as_view(),
    name='subject_detail'),

path('users/', UserList.as_view()), 
path('users/<int:pk>/', UserDetail.as_view()),


path('', include(router.urls)),

]