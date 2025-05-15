import pandas as pd
from .models import Product, Category
from django.utils.text import slugify

def importar_productos_desde_excel(archivo_excel):
    df = pd.read_excel(archivo_excel)

    for _, row in df.iterrows():
        try:
            nombre = str(row.get('producto', '')).strip()
            precio = row.get('precio')
            stock = row.get('stock')
            descripcion = str(row.get('descripcion', '')).strip()
            categoria_nombre = str(row.get('categoria', '')).strip()

            if not nombre or pd.isna(precio) or pd.isna(stock) or not categoria_nombre:
                print(f"Fila incompleta: {row}")
                continue

            try:
                categoria = Category.objects.get(category_name=categoria_nombre)
            except Category.DoesNotExist:
                print(f"Categoría no encontrada: {categoria_nombre}")
                continue

            producto = Product.objects.filter(product_name=nombre).first()

            if producto:
                # Si ya existe, actualizar y acumular stock
                producto.price = float(precio)
                producto.stock += int(stock)
                producto.description = descripcion or producto.description
                producto.category = categoria
                producto.save()
            else:
                # Si no existe, crear nuevo
                base_slug = slugify(nombre)
                slug = base_slug
                contador = 1
                while Product.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{contador}"
                    contador += 1

                Product.objects.create(
                    product_name=nombre,
                    slug=slug,
                    description=descripcion,
                    price=float(precio),
                    stock=int(stock),
                    category=categoria,
                    is_available=True
                )

        except Exception as e:
            print(f"Error procesando fila {row}: {str(e)}")
