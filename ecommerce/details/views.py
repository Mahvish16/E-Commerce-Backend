from django.shortcuts import render
from .models import RegisterUser,Category,Product, ProductImages,Order_item, Addresses,Cart,Cart_items,Order, PasswordReset
from .serializers import RegisterSerializer,LoginSerializer, CategorySerializer, OrderItemSerializer,BulkOrderItemsSerializer, AddressesSerializer, CartItemsSerializer,OrderSerializer,LogoutSerializer, ResetPasswordRequestSerializer,ResetPasswordSerializer
from rest_framework import generics
from django.contrib.auth import authenticate, logout
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.http import JsonResponse
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.tokens import default_token_generator
from rest_framework.exceptions import NotFound
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator



# Create your views here.
# class RegisterView(generics.CreateAPIView):
#     queryset = RegisterUser.objects.all()
#     serializer_class = RegisterSerializer
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args,**kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self,request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



            
            
    

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                })
        else:
            return Response({"message": "Invalid email or password"}, status=401)
        
class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data = request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class RequestPasswordReset(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        print(serializer)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            print('email', email)
            user = RegisterUser.objects.filter(email=email).first()
            print(user)

            if user:
               token_generator = PasswordResetTokenGenerator()
               token = token_generator.make_token(user)
               reset = PasswordReset(email=email, token=token)
               reset.save()
               reset_url = f'http://localhost:9000/resetpassword.html?token={token}'
               send_mail(
                   'Password Reset Request',
                   f'Please go to the following link to reset your password: {reset_url}',
                   'mahvish.ruhi@gmail.com',
                   [email],
                   fail_silently=False
                   )
               return Response({"message": "Password reset link sent to your email"}, status=200)
            else:
               return Response({"message": "User not found"}, status=404)
        return Response(serializer.errors, status=400)
                
class ResetPassword(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        new_password = data['password']
        confirm_password = data['confirmpassword']
        
        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=400)
        
        reset_obj = PasswordReset.objects.filter(token=token).first()
        
        if not reset_obj:
            return Response({'error':'Invalid token'}, status=400)
        
        user = RegisterUser.objects.filter(email=reset_obj.email).first()
        
        if user:
            user.set_password(request.data['password'])
            user.save()
            
            reset_obj.delete()
            
            return Response({'success':'Password updated'})
        else: 
            return Response({'error':'No user found'}, status=404)
       



    

class CategoryView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get (self,request, *args, **kwargs):
        categories = Category.objects.all()
        response_data= []
        for c in categories:
            response_data.append({"id":c.id,'name':c.category_name})
        return Response(response_data)
    
class ProductsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,*args, **kwargs):
        category_ids = request.GET.get('categories')
        print(category_ids)
        if category_ids:
            category_ids = category_ids.split(",")
            print("After split",category_ids)
            products = Product.objects.filter(category__id__in=category_ids)
        else:

            products = Product.objects.all()
        response_data = []
        for p in products:
            images = ProductImages.objects.filter(product=p)
            image_urls = [img.image.url for img in images] if images.exists() else []
            response_data.append({"id":p.id,"name":p.name,"price":p.price, "description": p.description, "category": p.category.id,"images": image_urls })
        return Response(response_data)
    
class ProductsImagesView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,*args, **kwargs):
        product_id = kwargs.get('product_id')
        print(product_id)
        product_image = ProductImages.objects.filter(product= product_id)
        response_data = []
        for p in product_image:
            response_data.append({"id":p.id,"product":p.product.id,"image":p.image.url})
        return Response(response_data)
        
class OrderView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    def get(self,request,*args, **kwargs):
        orders = Order.objects.filter(user=request.user)
        response_data = []
        for i in orders:
            response_data.append({
                "id":i.id,
                "amount":i.amount,
                "status":i.status,
                "order_date": i.order_date
                })
        return Response(response_data)
            
class OrderItemView (generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderItemSerializer
    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        print("order:",order_id)
        if order_id:
            order_items = Order_item.objects.filter(order_id=order_id) 
        
            if not order_items.exists():
                return Response({"message": "No order items found for this order"}, status=status.HTTP_404_NOT_FOUND)
        else:
            order_items = Order_item.objects.filter(order__user= request.user)
        serializer = self.get_serializer(order_items, many=True)  
        response_data = []
        for item in serializer.data:
            product_id = item.get('product', None)
            print(product_id)
            address_id = item.get('addresses', None)
            product_data = None
            if product_id:
                try:
                    product = Product.objects.get(id=product_id)
                    product_images = product.images.all()
                    image_urls = [image.image.url for image in product_images if image.image]
                    product_data = {
                        'id': product.id,
                        'name': product.name, 
                        'price': product.price, 
                        'images': image_urls if image_urls else None
                        
                    }
                except Product.DoesNotExist:
                    product_data = {"error": "Product not found"}
            address_data = None
            if address_id:
                try:
                    address = Addresses.objects.get(id=address_id)
                    address_data = {
                        'id': address.id,
                        'street': address.address, 
                        'city': address.city,
                        'state': address.state,
                        'zipcode': address.zipcode,
                        'landmark':address.landmark,
                    }
                except Address.DoesNotExist:
                    address_data = {"error": "Address not found"}
            item_data = {
                'id': item.get('id'),
                'product': product_data,
                'quantity': item.get('quantity'),
                'address': address_data,
                }
            response_data.append(item_data)

        return Response(response_data, status=status.HTTP_200_OK)
    def post (self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BulkOrderItemView(generics.GenericAPIView):
    serializer_class = BulkOrderItemsSerializer
    print(serializer_class)
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,context={'user': request.user})
        if serializer.is_valid():
            order_items_data = serializer.save()
            print(order_items_data)
            orders_serializer_data = OrderItemSerializer(order_items_data, many = True).data
            print(orders_serializer_data)
            return Response({"order_items":orders_serializer_data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class AddressesView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressesSerializer
    def get(self, request, *args, **kwargs):
        address_id = kwargs.get('pk')
        print(f"kwargs: {kwargs}")
        print('id =',address_id)

        if address_id :
            try:
               address = Addresses.objects.get(id=address_id, user =  request.user)
               response_data={
                   'id': address.id,
                   'name': address.name,
                   'address': address.address,
                   'city': address.city,
                   'state': address.state,
                   'zipcode': address.zipcode,
                   'landmark':address.landmark,
               }
               return Response(response_data, status=status.HTTP_200_OK)
            except Addresses.DoesNotExist:
                return Response({"error": "Address not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            addresses = Addresses.objects.filter(user=request.user)
            response_data = []
            for a in addresses:
                response_data.append({"id":a.id,"name":a.name,"address":a.address,"city":a.city,"states":a.state,"zipcode":a.zipcode,"landmark":a.landmark})
            return Response(response_data)
            
    def post(self,request,*args,**kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,pk):
        try:
            address = Addresses.objects.get(pk=pk)
        except Addresses.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(address, data=request.data,context={'user':request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,pk):
        try:
            address = Addresses.objects.get(pk=pk)
        except Addresses.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(address, data=request.data,context={'user':request.user},partial =True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        try:
            address = Addresses.objects.get(pk=pk)
        except Addresses.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CartItemView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemsSerializer
    def get(self, request,*args, **kwargs):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = Cart_items.objects.filter(cart=cart)
            response_data = []
            for c in cart_items:
                product = c.product
                product_images = ProductImages.objects.filter(product=product)
                images =[i.image.url for i in product_images]
                product_data = {
                    'id':product.id,
                    'name':product.name,
                    "description": product.description,
                    'price':product.price,
                    'images':images
                }
                response_data.append({"id":c.id,"product":product_data , "quantity": c.quantity})
                print(response_data)
            return Response(response_data)      
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
                        
    def post(self,request,*args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        serializer = self.get_serializer(data=request.data,context={'user':request.user})
        if serializer.is_valid():
            serializer.save(cart=cart)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch (self,request,pk):
        try:
            cart_item = Cart_items.objects.get(pk=pk)
        except Cart_items.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        try:
            cart_item = Cart_items.objects.get(pk=pk)
        except Cart_items.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        



    

        
    
            
    
    
    

    
    



    

        
        
        

    
    

