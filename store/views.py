import json
from django.http import HttpResponse
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from django.db.models import Q, F, ExpressionWrapper, FloatField, DecimalField
from rest_framework.decorators import api_view
from store.serializers import CartItemSerialzer, CartSerializer, CollectionSerializer, CreateCartItemSerializer, OrderSerializer, ProductSerializer, UpdateCartItemSerializer
from store.models import Cart, CartItem, Collection, Order, Product
from rest_framework import status
from rest_framework.views import APIView

from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet


def home(request):

    discounted_price = ExpressionWrapper(
        F("unit_price") * 0.9, output_field=FloatField())

    products = Product.objects.select_related("collection").annotate(
        discounted_price=discounted_price).order_by("-inventory")

    products_count = Product.objects.count()

    return render(request, 'home.html', {"total_products": products_count, "products": list(products)})


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartViewSet(ModelViewSet):
    http_method_names = ["get", "post", "delete"]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):

    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs["cart_pk"])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerialzer



class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_serializer_context(self):
        return {"user": self.request.user}