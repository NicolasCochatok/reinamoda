# 👑 Reina Moda y Accesorios

Bienvenido al repositorio oficial del sitio web de **Reina Moda y Accesorios**, una tienda de e-commerce moderna y minimalista para la venta de joyería, accesorios y productos de moda.

> 🛍️ Desarrollado con Django + Bootstrap + PostgreSQL + HTML5/CSS3  
> 🎯 Optimizado para carga dinámica de stock desde Excel  
> 🔐 Preparado para producción en `reina-moda.com.ar`

---

## 🚀 Funcionalidades

- 🔎 Catálogo con filtros por categoría, tipo, género y material
- 🛒 Carrito de compras con lógica de variaciones (talles, colores, etc.)
- ✅ Registro de usuarios con verificación por mail
- 📦 Gestión de pedidos y dashboard personal
- 📁 Carga masiva de productos vía Excel
- 🖼️ Soporte de imágenes por producto
- 🔐 Login seguro con encriptación y sistema de recuperación de contraseña

---

## 🧰 Tecnologías utilizadas

- **Frontend:** HTML5, CSS3, Bootstrap, JS
- **Backend:** Django 4.x (Python 3.10+)
- **Base de Datos:** PostgreSQL
- **Autenticación:** Django Auth
- **Email:** SMTP (Gmail)
- **Extras:** Pandas, Slugify, Excel import logic

---

## ⚙️ Instalación local

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/NicolasCochatok/reinamoda.git
   cd reinamoda
   ```

2. **Crear entorno virtual:**

   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   ```

3. **Instalar dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**

   Crear un archivo `.env` en la raíz con:

   ```env
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=info.reinamoda@gmail.com
   EMAIL_HOST_PASSWORD=tu_password

   DB_NAME=reinamoda
   DB_USER=postgres
   DB_PASSWORD=tu_password_postgres
   DB_HOST=localhost
   DB_PORT=5432

   DOMAIN=reina-moda.com.ar
   ```

5. **Ejecutar migraciones y crear superusuario:**

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Correr servidor local:**

   ```bash
   python manage.py runserver
   ```

---

## 🧾 Carga masiva de productos desde Excel

1. Accedé a:  
   `http://127.0.0.1:8000/store/importar-excel/`

2. Subí un archivo `.xlsx` con este formato:

   | producto     | precio | stock | descripcion         | categoria   |
   |--------------|--------|-------|---------------------|-------------|
   | Anillo Coral | 2500   | 10    | Anillo de acero...  | anillos     |
   | Collar Luna  | 3200   | 5     | Collar con dije...  | collares    |

3. Las categorías deben existir previamente en el admin (`/securelogin/`).

---

## 🔐 Panel de administración

- URL: `http://127.0.0.1:8000/securelogin/`
- Acceso solo para superusuarios.

---

## 📦 Despliegue

Este proyecto está listo para subir a producción en Hostinger VPS o similar.  
Se recomienda usar **Gunicorn + Nginx + PostgreSQL** y herramientas como **Certbot** para HTTPS.

---

## 📌 Pendientes / Próximas mejoras

- Integración de MercadoPago o Stripe
- Sistema de envíos por código postal
- App móvil sincronizada con el stock
- Wishlist de usuarios
- SEO básico + etiquetas sociales

---

## 🧑‍💻 Autor

Desarrollado por [Nicolás Gauna Cochatok](mailto:nicolas.cochatok@gmail.com)  
Proyecto 100% real, con vistas a comercializar productos de joyería, accesorios y moda desde Argentina.

---

## 🏷️ Licencia

MIT License — libre para uso personal y comercial.
