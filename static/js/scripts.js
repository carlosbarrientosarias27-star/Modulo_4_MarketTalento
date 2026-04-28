function callAPI(url) {
    const loading = document.getElementById('loading');
    const responseDiv = document.getElementById('response');
    
    loading.style.display = 'block';
    responseDiv.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Cargando...';
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            loading.style.display = 'none';
            responseDiv.innerHTML = 
                '<div class="mb-2"><strong>📡 Endpoint:</strong> ' + url + '</div>' +
                '<div class="mb-2"><strong>✅ Status:</strong> ' + (data.status || 'success') + '</div>' +
                '<hr>' +
                '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
        })
        .catch(error => {
            loading.style.display = 'none';
            responseDiv.innerHTML = '<div class="alert alert-danger">❌ Error: ' + error + '</div>';
        });
}

function analizarInventario() {
    const loading = document.getElementById('loading');
    const content = document.getElementById('content');
    
    loading.style.display = 'block';
    content.innerHTML = '<p class="text-center">🔍 Analizando inventario...</p>';
    
    fetch('/api/analizar-inventario')
        .then(response => response.json())
        .then(data => {
            loading.style.display = 'none';
            let html = '<div class="alert alert-success">✅ Análisis completado</div>';
            
            if (data.resumen) {
                html += '<div class="row mb-4">' +
                    '<div class="col-md-4"><div class="stat-card bg-primary"><i class="fas fa-boxes"></i><h3>' + data.resumen.total_productos + '</h3><p>Productos Analizados</p></div></div>' +
                    '<div class="col-md-4"><div class="stat-card bg-danger"><i class="fas fa-exclamation-triangle"></i><h3>' + (data.resumen.productos_criticos || 0) + '</h3><p>Críticos</p></div></div>' +
                    '<div class="col-md-4"><div class="stat-card bg-success"><i class="fas fa-dollar-sign"></i><h3>' + (data.valor_inventario || 0) + '</h3><p>Valor Total</p></div></div>' +
                    '</div>';
            }
            
            if (data.productos && data.productos.length > 0) {
                html += '<h5>📋 Detalle de Productos</h5><div class="table-responsive"><table class="table table-striped"><thead><tr><th>Producto</th><th>Stock</th><th>Días</th><th>Estado</th></tr></thead><tbody>';
                data.productos.forEach(p => {
                    html += `<tr><td>${p.producto}</td><td>${p.stock_actual}</td><td>${p.prediccion?.dias_hasta_agotarse || 'N/A'}</td><td>${p.prediccion?.estado || 'Desconocido'}</td></tr>`;
                });
                html += '</tbody></table></div>';
            }
            content.innerHTML = html;
        });
}

function verProductos() {
    const loading = document.getElementById('loading');
    const content = document.getElementById('content');
    
    loading.style.display = 'block';
    fetch('/api/productos')
        .then(response => response.json())
        .then(data => {
            loading.style.display = 'none';
            if (data.productos) {
                let html = '<h5>📦 Catálogo de Productos</h5><table class="table"><thead><tr><th>Nombre</th><th>Categoría</th><th>Precio</th></tr></thead><tbody>';
                data.productos.forEach(p => {
                    html += `<tr><td>${p.nombre}</td><td>${p.categoria}</td><td>$${p.precio}</td></tr>`;
                });
                html += '</tbody></table>';
                content.innerHTML = html;
            }
        });
}