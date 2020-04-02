from django.contrib.auth.models import User, Group
from rest_framework import generics,viewsets,status
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Subject,Course,Profile
from django.contrib.auth import authenticate
from .serializers import  SubjectSerializer,CourseSerializer,ModuleSerializer,CourseWithContentsSerializer,UserSerializer,ProfileSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .permissions import IsEnrolled

class UserViewSet(viewsets.ModelViewSet): # new
      queryset = User.objects.all()
      serializer_class = UserSerializer

class LoginView(APIView):
    permission_classes = ()

    def post(self, request, ):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListCreateAPIView): # new
       queryset = User.objects.all()
       serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView): # new
      queryset = User.objects.all()
      serializer_class = UserSerializer

class DeleteUser(generics.DestroyAPIView):
    def destroy(self, request, *args, **kwargs):
        user= User.objects.get(pk=self.kwargs["id"])
        if user.is_admin:
            try:
                queryset = User.objects.get(pk=self.kwargs["pk"])
            except ObjectDoesNotExist:
                return Response({"User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            queryset.delete()
            return Response({"User deleted"})

        else:
            return Response({"Not authorized"}, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(generics.RetrieveUpdateAPIView):
    def get_queryset(self):
        queryset = Profile.objects.filter(user_id=self.kwargs["pk"])
        return queryset

    serializer_class = ProfileSerializer

    def put(self, request, *args, **kwargs):
        profile = Profile.objects.get(pk=self.kwargs["pk"])
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class SubjectListView(generics.ListAPIView):
  queryset = Subject.objects.all()
  serializer_class = SubjectSerializer

class SubjectDetailView(generics.RetrieveAPIView):
  queryset = Subject.objects.all()
  serializer_class = SubjectSerializer

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action( detail=True, methods=['post'],
                authentication_classes=[BasicAuthentication],
                permission_classes=[IsAuthenticated])
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['get'],
               serializer_class=CourseWithContentsSerializer,
               authentication_classes=[BasicAuthentication],
               permission_classes=[IsAuthenticated,IsEnrolled])
    def contents(self, request, *args, **kwargs):
         return self.retrieve(request, *args, **kwargs)
