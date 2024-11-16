from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from .forms import RegistrationForm, LoginForm
from .models import Employee  # Ensure you're importing from mongoengine

def login_register_view(request):
    login_form = LoginForm()  # Initialize login form
    registration_form = RegistrationForm()  # Initialize registration form

    if request.method == 'POST':
        if 'login' in request.POST:
            # Handle login form submission
            login_form = LoginForm(request.POST)  # Re-initialize login form with POST data
            if login_form.is_valid():
                email = login_form.cleaned_data['email']  # Get email from form
                password = login_form.cleaned_data['password']  # Get password from form

                try:
                    # Try to find the employee by email (acting as username)
                    employee = Employee.objects.get(email=email)

                    # Check if the entered password matches the stored hashed password
                    if check_password(password, employee.password):  # Use check_password for hashed password comparison
                        # Simulate login by storing the employee ID in session
                        request.session['employee_id'] = str(employee.id)
                        return redirect('home')  # Redirect to home page after successful login
                    else:
                        messages.error(request, 'Invalid email or password')  # Invalid password

                except Employee.DoesNotExist:
                    messages.error(request, 'Employee not found')  # No employee with that email

        elif 'register' in request.POST:
            # Handle registration form submission
            registration_form = RegistrationForm(request.POST)
            if registration_form.is_valid():
                # Hash the password before saving it
                password = registration_form.cleaned_data['password']
                hashed_password = make_password(password)  # Hash the password

                # Create a new employee and save to the database
                employee = Employee(
                    name=registration_form.cleaned_data['name'],
                    email=registration_form.cleaned_data['email'],
                    phone=registration_form.cleaned_data['phone'],
                    password=hashed_password  # Store hashed password
                )
                employee.save()  # Save to MongoDB (via mongoengine)
                messages.success(request, 'Registration successful! Please login now.')
                return redirect('login_register')  # Redirect to login page after successful registration
            else:
                messages.error(request, 'Registration failed. Please try again.')

    # Pass the forms to the template context
    return render(request, 'login_register.html', {
        'login_form': login_form,
        'registration_form': registration_form,
    })

def home_view(request):
    # Check if the employee is logged in by checking the session data
    employee_id = request.session.get('employee_id')
    
    if employee_id:
        try:
            # Try to fetch the employee from the database using the stored session ID
            employee = Employee.objects.get(id=employee_id)
            return render(request, 'home.html', {'employee': employee})  # Render the home page with employee data
        except Employee.DoesNotExist:
            return redirect('login_register')  # If session ID is invalid, redirect to login page
    else:
        return redirect('login_register')  # If no session exists, redirect to login page


def logout_view(request):
    # Log the user out by clearing the session
    if 'employee_id' in request.session:
        del request.session['employee_id']  # Delete the employee_id from session
    return redirect('login_register')  # Redirect to login page after logout


from django.shortcuts import render, redirect
from .models import Employee, Product, Cart
from django.contrib import messages

def menu_view(request):
    # Get all products from the database
    products = Product.objects.all()
    return render(request, 'menu.html', {'products': products})
def add_to_cart(request, product_id):
    """Handles adding a product to the cart."""
    
    # Check if the user is logged in
    employee_id = request.session.get('employee_id')
    if not employee_id:
        messages.error(request, 'You need to be logged in to add items to your cart.')
        return redirect('login_register')

    # Fetch the employee based on the session
    try:
        employee = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        messages.error(request, 'Employee not found.')
        return redirect('login_register')

    # Fetch the product to add to the cart
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, 'Product not found.')
        return redirect('home')

    # Get or create a cart for the employee manually
    cart = Cart.objects(employee=employee).first()
    
    if not cart:
        # If no cart exists, create a new one
        cart = Cart(employee=employee)
        cart.save()

    # Add the product to the cart (with quantity 1)
    cart.add_item(product, 1)
    
    # Success message
    messages.success(request, f'{product.name} added to your cart.')

    # Redirect to the cart view
    return redirect('view_cart')

def view_cart(request):
    """Displays the items in the cart."""
    # Get the logged-in employee's cart
    employee_id = request.session.get('employee_id')
    if not employee_id:
        messages.error(request, 'You need to be logged in to view your cart.')
        return redirect('login_register')

    try:
        employee = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        messages.error(request, 'Employee not found.')
        return redirect('login_register')

    # Get the cart associated with the employee
    try:
        cart = Cart.objects.get(employee=employee)
    except Cart.DoesNotExist:
        cart = None

    # Add a calculated field for the total price of each cart item
    if cart:
        for item in cart.items:
            item.total_price = item.product.price * item.quantity
        cart_items = cart.items  # Now cart items contain the total price

    return render(request, 'view_cart.html', {'cart': cart, 'cart_items': cart_items})


# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProductForm
from .models import Product

def add_product(request):
    """Handles adding a new product to the menu."""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            # Save the product to MongoDB
            product = Product(
                name=form.cleaned_data['name'],
                price=form.cleaned_data['price'],
                image=form.cleaned_data.get('image', None)  # Handle image if provided
            )
            product.save()
            messages.success(request, 'New product added successfully!')
            return redirect('menu')  # Redirect to the menu or another page
        else:
            messages.error(request, 'There was an error adding the product.')
    else:
        form = ProductForm()

    return render(request, 'add_product.html', {'form': form})
