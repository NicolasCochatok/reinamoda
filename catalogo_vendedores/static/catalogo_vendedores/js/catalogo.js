function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

document.addEventListener("DOMContentLoaded", () => {
    const inputBusqueda = document.getElementById("busqueda");
    const contenedor = document.getElementById("productos-container");

    function cargarProductos(query = "") {
        fetch(`/catalogo-vendedores/api/productos/?q=${query}`)
            .then(response => response.json())
            .then(productos => {
                contenedor.innerHTML = "";

                if (productos.length === 0) {
                    contenedor.innerHTML = "<p class='text-muted'>No se encontraron productos.</p>";
                    return;
                }

                productos.forEach(p => {
                    const col = document.createElement("div");
                    col.className = "col-md-3 col-sm-6";

                    const imgURL = p.image || 'https://via.placeholder.com/150?text=Sin+imagen';

                    col.innerHTML = `
                        <div class="card producto-card shadow-sm h-100">
                            <img src="${imgURL}" class="card-img-top" alt="${p.product_name}">
                            <div class="card-body">
                                <h5 class="card-title">${p.product_name}</h5>
                                <p class="card-text mb-1"><strong>Código:</strong> ${p.codigo_unico || '-'}</p>
                                <p class="card-text mb-1"><strong>Proveedor:</strong> ${p.codigo_proveedor || '-'}</p>
                                <p class="card-text mb-1"><strong>Precio:</strong> $${p.price}</p>
                                <p class="card-text mb-1"><strong>Stock:</strong> ${p.stock}</p>
                                ${p.talle ? `<p class="card-text mb-1"><strong>Talle:</strong> ${p.talle}</p>` : ""}

                                <form class="venta-form mt-3">
                                    <input type="hidden" name="producto" value="${p.id}">
                                    <div class="mb-2">
                                        <input type="number" name="cantidad" class="form-control form-control-sm" placeholder="Cantidad" required min="1" max="${p.stock}">
                                    </div>
                                    <div class="mb-2">
                                        <input type="text" name="cliente" class="form-control form-control-sm" placeholder="Cliente" required>
                                    </div>
                                    <div class="mb-2">
                                        <select name="metodo_pago" class="form-select form-select-sm" required>
                                            <option value="">Seleccionar medio de pago</option>
                                            <option value="efectivo">Efectivo</option>
                                            <option value="mercado_pago">Mercado Pago</option>
                                            <option value="tarjeta">Tarjeta de crédito</option>
                                            <option value="pendiente">Pendiente de pago</option>
                                        </select>
                                    </div>
                                    <div class="mb-2 form-check">
                                        <input type="checkbox" name="pagado" class="form-check-input" id="pagado-${p.id}">
                                        <label class="form-check-label" for="pagado-${p.id}">Pagado</label>
                                    </div>
                                    <button type="submit" class="btn btn-primary btn-sm w-100">Registrar venta</button>
                                </form>
                            </div>
                        </div>
                    `;

                    const form = col.querySelector(".venta-form");
                    const selectPago = form.metodo_pago;
                    const checkboxPagado = form.pagado;

                    selectPago.addEventListener("change", () => {
                        if (selectPago.value === "pendiente") {
                            checkboxPagado.checked = false;
                        }
                    });

                    form.addEventListener("submit", e => {
                        e.preventDefault();

                        const datos = {
                            producto: form.producto.value,
                            cantidad: form.cantidad.value,
                            cliente: form.cliente.value,
                            metodo_pago: form.metodo_pago.value,
                            pagado: form.pagado.checked,
                            precio_unitario: p.price
                        };

                        fetch("/catalogo-vendedores/api/ventas/", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                                "X-CSRFToken": csrftoken
                            },
                            body: JSON.stringify(datos)
                        })
                        .then(res => {
                            if (res.ok) {
                                alert("✅ Venta registrada");
                                form.reset();
                            } else {
                                alert("❌ Error al registrar la venta");
                            }
                        })
                        .catch(err => alert("❌ Error de conexión"));
                    });

                    contenedor.appendChild(col);
                });
            });
    }

    inputBusqueda.addEventListener("input", () => {
        cargarProductos(inputBusqueda.value);
    });

    cargarProductos();
});
