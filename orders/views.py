from rest_framework import viewsets

from .permissions import IsOwner
from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer
from .utils import send_sms
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = CustomerSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes=[IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return self.queryset.filter(customer__user=self.request.user).order_by("-created_at")
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        customer = serializer.validated_data["customer"]
        message = f"Hello {customer.name}, your order for {serializer.validated_data["item"]} has been recieved"
        send_sms(customer.phone_number, message)

        return Response(
            {
                "success": True,
                "message": "Order created successfully",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
