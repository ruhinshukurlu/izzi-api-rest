from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from core.models import *
from core.serializers import *

# Create your views here.

class ServiceListView(ListAPIView):

    queryset = Service.objects.filter(isActive = True)
    serializer_class = ServiceSerializer

    def get_queryset(self):
       
        return Service.objects.all()

class SubServiceListView(ListAPIView):

    queryset = SubService.objects.filter(isActive = True)
    serializer_class = SubServiceSerializer


class CommentListView(ListAPIView):

    queryset = Comment.objects.filter(isActive = True).order_by('rating')
    serializer_class = CommentSerializer


class CityListView(ListAPIView):

    queryset = City.objects.filter(isActive = True).order_by('name')
    serializer_class = CitySerializer

class OrderListView(APIView):
    # permission_classes = (IsAuthenticated,)
    # queryset = Order.objects.filter(isActive = True)
    # serializer_class = OrderListSerializer

    def get(self, request):
        orders = Order.objects.filter(customer=self.request.user)
        serializer = OrderListSerializer(orders, many=True)
        return Response({"orders":serializer.data})     


    def post(self, request):
        order = request.data

        serializer = OrderCreateSerializer(data=order)
        print(order)
        if serializer.is_valid(raise_exception=True):
            saved_order = serializer.save()

        return Response({"success":"true"})    

    # def get_queryset(self):
    #     user = self.request.user
    #     return Order.objects.filter(customer=user)


class TaskerListView(ListAPIView):

    queryset = Tasker.objects.filter(isActive = True)
    serializer_class = TaskerListSerializer


class SubServiceDetailView(RetrieveAPIView):
    # permission_classes = (AllowAny,)
    queryset = SubService.objects.all()
    serializer_class = SubServiceDetailSerializer


class OrderDetailView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer