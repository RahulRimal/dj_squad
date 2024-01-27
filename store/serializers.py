
from rest_framework import serializers

from store.models import Cart, CartItem, Collection, Order, OrderItem, Product


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "name", "featured_product"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "unit_price",
                  "inventory", "description", "collection"]


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "unit_price"]


class CartItemSerialzer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]

    def get_total_price(self, cart_item):
        return cart_item.quantity * cart_item.product.unit_price


class CreateCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ["product_id", "quantity"]


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerialzer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "total_price", "items"]

    def get_total_price(self, cart):
        return sum([item.product.unit_price * item.quantity for item in cart.items.all()])



class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity"]




class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, source="order_items", read_only=True)
    status = serializers.ReadOnlyField()
    cart_id = serializers.CharField(write_only=True)
    class Meta:
        model = Order
        fields = ["id", "status", "items", "cart_id"]

    
    def create(self, validated_data):
        cart_id = validated_data['cart_id']
        cart = Cart.objects.get(id=cart_id)
        cart_items = cart.items.all()
        user = self.context['user']
        order =Order.objects.create(customer=user)

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )
        
        cart.delete()

        return order
