from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Create your models here.
class Category(models.Model):
    sub_category = models.ForeignKey('self',on_delete=models.CASCADE, related_name='sub_categories', null=True, blank=True)
    is_sup = models.BooleanField(default=False)
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    def __str__(self):
        return self.name

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']
        
class Product(models.Model):
    ownerName = models.CharField(max_length=200, null=True, blank=False)
    img_owerName = models.ImageField(null=True, blank=True)
    
    #################
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null= True, blank=True)
    category =models.ManyToManyField(Category, related_name='product')
    detail = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url =''
        return url


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return str(self.transaction_id)
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all() # ...
        total = sum([item.quantity for item in orderitems])
        return total

    def get_cart_total(self):
        orderitems = self.orderitem_set.all()  # ...
        total = sum([item.get_total for item in orderitems])
        return total
        
    

class OrderItem(models.Model):
    # ForeignKey : khóa ngoại
    # Một bảng nào chứa khóa ngoại tham chiếu đến bảng kia
    # thì bảng kia sẽ có 1 danh sách các đối tượng trong bảng đó 
    # có thể lấy tất cả đối tượng của bảng đó 
    # theo cú pháp  <tên bang>_set.all()
    ######
    # Chẳng hạn, ở đây ta thấy trong class OrderItem chứa khóa ngoại
    # product -> tham chiếu đến bảng Product, và order -> Order
    # vì vậy, ví dụ trong bảng Product
    # ta có thể lấy tất cả đối tượng của bảng OrderItem
    # thông qua cú pháp: 
    # test = Product.orderitem_set.all()
    # chú ý viết thường tên bảng và + _set.all()
    
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)

    quantity = models.IntegerField(default=0,null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    # ForeignKey : khóa ngoại
    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200,null= True)
    city = models.CharField(max_length=200,null= True)
    state = models.CharField(max_length=200, null=True)
    mobile = models.CharField(max_length=10, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.address)




    

    