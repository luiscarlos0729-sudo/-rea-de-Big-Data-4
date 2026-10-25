# Tarea 4 — Bases de Datos NoSQL: Modelado e Implementación con MongoDB

Curso **Big Data** (código 202016911) · Universidad Nacional Abierta y a Distancia (UNAD)
Estudiante: Luis Carlos Benedetti Hernández

Continuación de las Tareas 2 y 3 de este curso: el mismo caso de un comercio en línea
(dataset **Online Retail**, UCI Machine Learning Repository), ahora modelado con una base
de datos documental (MongoDB) en lugar de tablas relacionales.

## Contenido del repositorio

```
.
├── docs/
│   ├── investigacion_nosql.md   # Investigación: qué son las bases NoSQL, clasificación,
│   │                             # ventajas/desventajas y casos de uso reales
│   └── diseno_esquema.md        # Diseño de las colecciones clientes y pedidos
├── scripts/
│   ├── install_mongodb.sh       # Instala MongoDB 8.0 Community en la VM (Ubuntu 24.04)
│   ├── mongod_override.conf     # Ajuste systemd para el bug de kernel 6.19+ (SERVER-121912)
│   ├── seed_data.py             # Carga clientes y pedidos desde online_retail.csv
│   └── queries.py               # CRUD, filtros, join ($lookup) y agregaciones
└── evidencia/
    ├── 01_mongod_activo.jpg     # systemctl status mongod
    ├── 02_carga_datos_seed.jpg  # Carga de datos (559 clientes, 800 pedidos)
    ├── 03_crud.jpg              # Create / Read / Update / Delete
    ├── 04_filtros_join.jpg      # Filtros compuestos + $lookup
    ├── 05_agregaciones.jpg      # $group con $sum y $avg
    └── queries_output.txt       # Salida completa de queries.py
```

## Esquema de MongoDB

Base de datos `tienda_ecommerce`, dos colecciones:

- **`clientes`**: un documento por cliente (país, segmento, fecha de primera compra).
- **`pedidos`**: un documento por factura, con sus líneas de producto **embebidas**
  (`items`) y una referencia al cliente (`customerId` → `clientes._id`). El país del
  cliente también se repite en `pedidos.country` a propósito (denormalización), para
  evitar un `$lookup` en la consulta más común: "ventas por país".

Detalle completo, con ejemplos de documento JSON y la justificación de cada decisión de
modelado, en [`docs/diseno_esquema.md`](docs/diseno_esquema.md).

## Cómo ejecutarlo

En una VM con Ubuntu 24.04 (probado en `hadoop-node1`, VirtualBox):

```bash
# 1. Instalar MongoDB 8.0
bash scripts/install_mongodb.sh

# 2. Si mongod no arranca por incompatibilidad con kernel 6.19+:
sudo mkdir -p /etc/systemd/system/mongod.service.d
sudo cp scripts/mongod_override.conf /etc/systemd/system/mongod.service.d/override.conf
sudo systemctl daemon-reload
sudo systemctl restart mongod

# 3. Cargar los datos de prueba (requiere online_retail.csv en el home del usuario)
python3 scripts/seed_data.py

# 4. Ejecutar las consultas (CRUD, filtros, join, agregaciones)
python3 scripts/queries.py
```

## Resultados

- **559** documentos cargados en `clientes`, **800** en `pedidos` (desde el dataset
  Online Retail).
- **93** pedidos marcados como devueltos.
- Ventas totales en United Kingdom: **253.462,2**; ticket promedio global: **352,62**.
- Evidencia completa de las cuatro operaciones CRUD, de un join con `$lookup` entre
  `pedidos` y `clientes`, y de agregaciones de conteo, suma y promedio en
  [`evidencia/`](evidencia/) y en [`evidencia/queries_output.txt`](evidencia/queries_output.txt).

## Enlaces

- Video explicativo: *(pendiente)*
- Informe escrito (Tarea4_grupo.docx): entregado en la plataforma UNAD
