from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating, ProductGallery, SizeOption
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import ReviewForm, ExcelUploadForm
from django.contrib import messages
from orders.models import OrderProduct
from django.utils.text import slugify
from django.http import JsonResponse
import pandas as pd


# ========================== PÁGINA STORE ==========================
def store(request, material_slug=None, category_slug=None):
    if not category_slug and 'categoria' in request.GET:
        category_slug = request.GET.get('categoria')

    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True).order_by('id')
    talles = None

    if material_slug:
        products = products.filter(material=material_slug)

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)
        if selected_category.tipo_talle:
            talles = SizeOption.objects.filter(categoria_aplicable=selected_category.tipo_talle)

    if 'talle' in request.GET:
        talle = request.GET['talle']
        products = products.filter(variation__variation_value__iexact=talle).distinct()

    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
        'talles': talles,
        'categories': categories,
        'material_slug': material_slug,
    }
    return render(request, 'store/store.html', context)


# ========================== DETALLE PRODUCTO ==========================
def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    orderproduct = None
    if request.user.is_authenticated:
        orderproduct = OrderProduct.objects.filter(user=request.user, product__id=single_product.id).exists()

    reviews = ReviewRating.objects.filter(product__id=single_product.id, status=True)
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery,
    }
    return render(request, 'store/product_detail.html', context)


# ========================== BÚSQUEDA ==========================
def search(request):
    products = []
    product_count = 0

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword)
            )
            product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)


# ========================== ENVIAR REVIEW ==========================
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Muchas gracias!, tu comentario ha sido actualizado.')
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Muchas gracias!, tu comentario ha sido publicado.')
    return redirect(url)


# ========================== IMPORTAR EXCEL ==========================
def importar_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo_excel']
            try:
                df = pd.read_excel(archivo)

                for _, fila in df.iterrows():
                    product_name = str(fila.get('product_name', '')).strip()
                    price = fila.get('price')
                    stock = fila.get('stock')
                    description = str(fila.get('description', '')).strip()
                    category_name = str(fila.get('category', '')).strip()

                    if not product_name or pd.isna(price) or pd.isna(stock) or not category_name:
                        messages.warning(request, f"Faltan campos obligatorios en una fila. No se pudo procesar.")
                        continue

                    try:
                        category = Category.objects.get(category_name__iexact=category_name)
                    except Category.DoesNotExist:
                        messages.warning(request, f"Categoría no encontrada: {category_name}")
                        continue

                    producto = Product.objects.filter(product_name__iexact=product_name).first()

                    if producto:
                        producto.price = float(price)
                        producto.stock += int(stock)
                        producto.description = description
                        producto.category = category

                        if not producto.slug:
                            base_slug = slugify(product_name)
                            slug = base_slug
                            contador = 1
                            while Product.objects.filter(slug=slug).exclude(pk=producto.pk).exists():
                                slug = f"{base_slug}-{contador}"
                                contador += 1
                            producto.slug = slug

                        producto.save()
                    else:
                        base_slug = slugify(product_name)
                        slug = base_slug
                        contador = 1
                        while Product.objects.filter(slug=slug).exists():
                            slug = f"{base_slug}-{contador}"
                            contador += 1

                        Product.objects.create(
                            product_name=product_name,
                            slug=slug,
                            description=description,
                            price=float(price),
                            stock=int(stock),
                            category=category,
                            is_available=True,
                        )

                messages.success(request, 'Archivo procesado correctamente.')
                return redirect('importar_excel')

            except Exception as e:
                messages.error(request, f"Ocurrió un error al procesar el archivo: {str(e)}")
    else:
        form = ExcelUploadForm()

    return render(request, 'store/importar_excel.html', {'form': form})


# ========================== OBTENER TALLE POR CATEGORÍA ==========================
def get_sizes_by_category(request):
    category = request.GET.get('category')
    if category:
        talles = SizeOption.objects.filter(categoria_aplicable=category).values_list('valor', flat=True)
        return JsonResponse({'sizes': list(talles)})
    return JsonResponse({'sizes': []})
