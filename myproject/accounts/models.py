from mongoengine import Document, StringField, EmailField
from mongoengine import Document, StringField, IntField, ReferenceField, ListField, DecimalField,ImageField
from mongoengine.queryset.visitor import Q

class Cart(Document):
    # Reference to Employee who owns the cart
    employee = ReferenceField('Employee', required=True, unique=True)
    items = ListField(ReferenceField('CartItem'), default=list)

    def __str__(self):
        return f"Cart of {self.employee.name}"

    def add_item(self, product, quantity):
        """Add a product to the cart. If it already exists, increase the quantity."""
        # Check if product already exists in the cart
        existing_item = CartItem.objects(cart=self, product=product).first()
        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
        else:
            new_item = CartItem(cart=self, product=product, quantity=quantity)
            new_item.save()
            self.items.append(new_item)
            self.save()

    def get_total(self):
        """Calculate the total price of all items in the cart."""
        total = sum(item.product.price * item.quantity for item in self.items)
        return total

class Product(Document):
    """Represent a food item in the menu."""
    name = StringField(required=True)
    price = DecimalField(required=True, precision=2)
    image = ImageField()  # This will store the image of the product

    def __str__(self):
        return self.name

class CartItem(Document):
    cart = ReferenceField(Cart, required=True)
    product = ReferenceField(Product, required=True)
    quantity = IntField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class Employee(Document):
    name = StringField(max_length=100, required=True)
    email = EmailField(unique=True, required=True)
    phone = StringField(max_length=15, required=True)
    password = StringField(max_length=100, required=True)

    def __str__(self):
        return self.name

