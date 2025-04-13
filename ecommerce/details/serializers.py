from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import RegisterUser, Category, Product, ProductImages,Order_item,Order,Addresses,Cart,Cart_items

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    class Meta:
        model = RegisterUser
        fields = ('name', 'email','phone_number', 'password')
    def create(self, validated_data):
        user = RegisterUser.objects.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )
        return user

    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages={
        'bad_token': ('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try:
           RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')

class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.RegexField(
        regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
        write_only=True,
        error_messages={'invalid': ('Password must be at least 8 characters long with at least one capital letter and symbol')})
    confirmpassword = serializers.CharField(write_only=True, required=True)
    





        


class CategorySerializer(serializers.Serializer):
    class Meta:
        model = Category
        fields = ('id', 'category_name')


class ProductSerailizer(serializers.Serializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'category']

class ProductimagesSerializer(serializers.Serializer):
    class Meta:
        model = ProductImages
        fields = ('id', 'product', 'image')

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'amount', 'order_date', 'status']

class OrderItemSerializer (serializers.ModelSerializer):
    class Meta:
        model = Order_item
        fields = '__all__'

class BulkOrderItemsSerializer(serializers.Serializer):
    order_items = OrderItemSerializer(many=True)
    address_id = serializers.IntegerField(write_only=True)
    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        address_id = validated_data.pop('address_id')
        user = self.context.get('user')
        try:
            address = Addresses.objects.get(id=address_id, user=user)
        except Addresses.DoesNotExist:
            raise serializers.ValidationError({"address_id": "Invalid address ID."})
        product_ids = [item['product'].id for item in order_items_data]
        products = {p.id: p for p in Product.objects.filter(id__in=product_ids)}


        total_amount = sum(i['product'].price *i['quantity']for i in order_items_data)
        order = Order.objects.create(
            user=user,
            amount=total_amount,
            status='pending',
        )
        order_items = [
            Order_item(
                order=order,
                addresses= address,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].price,
                total_amount=item['product'].price * item['quantity']
            ) for item in order_items_data
        ]
        Order_item.objects.bulk_create(order_items) 
        
        return order_items
        
class AddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addresses
        fields = ('id', 'name', 'address', 'city', 'state', 'zipcode','landmark')
        read_only_fields = ('id','user')

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('id', 'user')

class CartItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart_items
        fields = ('id', 'cart', 'product', 'quantity')
        read_only_fields = ('id', 'cart')



    
        
        



    




    



        
