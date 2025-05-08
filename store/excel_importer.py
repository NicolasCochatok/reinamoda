import pandas as pd
from .models import Product

def importar_productos_desde_excel(archivo_excel):
    df = pd.read_excel(archivo_excel)

    for _, row in df.iterrows():
        try:
            producto = Product.objects.get(product_name=row['producto'])
            producto.price = row['precio']
            producto.stock = row['stock']
            producto.save()
        except Product.DoesNotExist:
            print(f"Producto '{row['producto']}' no encontrado.")
