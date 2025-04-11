from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,PermissionsMixin

# Create your models here.
paystatus=(
    ('pending','pending'),
    ('cancelled','cancelled'),
    ('completed','completed'),
)
ordstatus=(
    ('delivered','delivered'),
    ('shipped','shipped'),
    ('pending','pending'),
)

paymethod=(
    ('cash','cash'),
)

states = (
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'),
    ('Gujarat', 'Gujarat'),
    ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'),
    ('Jammu and Kashmir', 'Jammu and Kashmir'),
    ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'),
    ('Kerala', 'Kerala'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'),
    ('Manipur', 'Manipur'),
    ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'),
    ('Nagaland', 'Nagaland'),

)


class RegisterUserManager(BaseUserManager):
    def create_user(self, name, email, phone_number, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            name = name,
            phone_number = phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, name, email,phone_number, password =None):
        user = self.create_user(name = name , email= email, phone_number= phone_number, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class RegisterUser(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = RegisterUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name', 'phone_number']

    def __str__(self):
        return self.name
    
class PasswordReset(models.Model):
    email = models.EmailField(null=True)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    
class Addresses(models.Model):
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField(max_length=100, null=True)
    address = models.TextField(max_length=600)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200 ,choices=states)
    zipcode = models.IntegerField()
    landmark = models.CharField(max_length=100)

    def __str__(self):
        return self.address

    
class Category(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category,on_delete = models.CASCADE)

    def __str__(self):
        return self.name
    
class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="images/",null= True)

    def __str__(self):
        return self.product.name
    
class Order(models.Model):
    user = models.ForeignKey(RegisterUser, on_delete=models.CASCADE)
    amount = models.DecimalField (max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=ordstatus)

    def __str__(self):
        return self.user.name
    
class Order_item(models.Model):
    addresses = models.ForeignKey(Addresses, on_delete=models.CASCADE, default=1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10,decimal_places= 2)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} pcs"
    
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices= paymethod)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices = paystatus)
    
    def __str__(self):
        return self.order.user.name
    
class Cart(models.Model):
    user = models.OneToOneField(RegisterUser, on_delete=models.CASCADE,unique=True)

    def __str__(self):
        return self.user.name
    
class Cart_items(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.quantity
    
class Inventory (models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product








