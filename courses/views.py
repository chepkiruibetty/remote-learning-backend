from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, \
PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import CreateView, UpdateView, \
DeleteView
from .models import Course

# class CourseListView(ListView):
#     model = Course
#     template_name = '/index.html'
class ManageCourseListView(ListView):
   model = Course
   template_name = 'courses/list.html'
   def get_queryset(self):
       qs = super(ManageCourseListView, self).get_queryset()
       return qs.filter(owner=self.request.user)

class OwnerMixin(object):
   def get_queryset(self):
      qs = super(OwnerMixin, self).get_queryset()
      return qs.filter(owner=self.request.user)
class OwnerEditMixin(object):
    def form_valid(self, form):
      form.instance.owner = self.request.user
      return super(OwnerEditMixin, self).form_valid(form)

class OwnerCourseMixin(OwnerMixin):
      model = Course

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
     fields = ['subject', 'title', 'slug', 'overview']
     success_url = reverse_lazy('manage_course_list')
     template_name = 'courses/form.html'

class ManageCourseListView(OwnerCourseMixin, ListView):
     template_name = 'courses/list.html'

class CourseCreateView(OwnerCourseEditMixin, CreateView):
     pass

class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    pass

class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/delete.html'
    success_url = reverse_lazy('manage_course_list')