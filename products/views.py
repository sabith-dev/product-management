from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Category, Product

User = get_user_model()
# ---------------- Authentication ----------------

def login_view(request):
    """Login page. Redirects to dashboard on success."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, 'Both username and password are required.')
            return render(request, 'registration/login.html')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid username or password.')

    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm', '')

        if not username or not password:
            messages.error(request, 'Username and password are required.')
        elif password != confirm:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'Account created! Please log in.')
            return redirect('login')
    return render(request, 'registration/register.html')



# ---------------- Dashboard ----------------

@login_required
def dashboard(request):
    products = Product.objects.all()
    context = {
        'total_products': products.count(),
        'active_products': products.filter(status=Product.STATUS_ACTIVE).count(),
        'inactive_products': products.filter(status=Product.STATUS_INACTIVE).count(),
        'low_stock_products': products.filter(
            stock__gt=0, stock__lte=Product.LOW_STOCK_THRESHOLD
        ).count(),
    }
    return render(request, 'products/dashboard.html', context)


# ---------------- Product CRUD ----------------

@login_required
def product_list(request):
    """List products with search, filters and pagination."""
    products = Product.objects.select_related('category')

    search = request.GET.get('search', '').strip()
    if search:
        products = products.filter(Q(name__icontains=search) | Q(sku__icontains=search))

    category_id = request.GET.get('category', '')
    if category_id:
        products = products.filter(category_id=category_id)

    status = request.GET.get('status', '')
    if status in (Product.STATUS_ACTIVE, Product.STATUS_INACTIVE):
        products = products.filter(status=status)

    paginator = Paginator(products, 8)  # 8 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'search': search,
        'selected_category': category_id,
        'selected_status': status,
    }
    return render(request, 'products/product_list.html', context)


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})


@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('product_list')
        messages.error(request, 'Please fix the errors below.')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Add Product'})


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_list')
        messages.error(request, 'Please fix the errors below.')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Edit Product'})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':  # only delete via POST (confirmation form)
        product.delete()
        messages.success(request, f'Product "{product.name}" deleted.')
        return redirect('product_list')
    return render(request, 'products/product_delete_confirm.html', {'product': product})
