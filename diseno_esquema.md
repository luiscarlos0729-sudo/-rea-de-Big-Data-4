# Paso 3 — Diseño del esquema de MongoDB

## Caso de uso

Sistema de pedidos de la tienda de e-commerce del conjunto de datos **Online Retail** (el mismo
usado en las Tareas 2 y 3): se modela el almacenamiento de **clientes** y **pedidos** (facturas con
sus líneas de producto) en MongoDB, para poder consultarlos, filtrarlos y calcular estadísticas
de ventas de forma flexible, algo que en este caso es más natural en un modelo de documentos
que en tablas relacionales rígidas (cada pedido puede tener un número distinto de productos).

Se usan **dos colecciones** a propósito, para poder mostrar las dos técnicas de modelado más
importantes de MongoDB en un mismo proyecto:

- **Documentos embebidos** (`pedidos.items`): cada pedido "contiene" sus propias líneas de
  producto, en lugar de repartirlas en otra colección — así se evita un join para la consulta más
  frecuente ("dame el pedido completo").
- **Referencia entre colecciones** (`pedidos.customerId` → `clientes._id`): el pedido no repite
  los datos del cliente, solo guarda su identificador — así se puede hacer un `$lookup`
  (el "join" que pide la guía) cuando sí se necesite cruzar la información de ambas colecciones,
  por ejemplo "ventas totales por país del cliente".

## Colección `clientes`

Un documento por cliente distinto presente en el conjunto de datos Online Retail.

```json
{
  "_id": 17850,
  "customerId": 17850,
  "country": "United Kingdom",
  "numFacturasHistoricas": 34,
  "clienteDesde": "2010-12-01",
  "segmento": "regular"
}
```

| Campo | Tipo | Descripción |
|---|---|---|
| `_id` / `customerId` | int | CustomerID original del dataset (se usa como `_id`, ya es único) |
| `country` | string | País del cliente |
| `numFacturasHistoricas` | int | Número de facturas del cliente en el conjunto de datos completo (541.909 registros), no solo en la muestra cargada |
| `clienteDesde` | date (string ISO) | Fecha de su primera compra registrada |
| `segmento` | string | `"mayorista"` si alguna de sus compras fue de una sola factura con gasto muy alto (ver Tarea 3, cliente 12346.0), `"regular"` en caso contrario — campo derivado, útil para los filtros |

## Colección `pedidos`

Un documento por factura (`InvoiceNo`), con sus líneas de producto embebidas como arreglo.

```json
{
  "_id": "536365",
  "invoiceNo": "536365",
  "customerId": 17850,
  "country": "United Kingdom",
  "invoiceDate": "2010-12-01T08:26:00Z",
  "estado": "completado",
  "items": [
    {
      "stockCode": "85123A",
      "description": "WHITE HANGING HEART T-LIGHT HOLDER",
      "quantity": 6,
      "unitPrice": 2.55,
      "subtotal": 15.30
    },
    {
      "stockCode": "71053",
      "description": "WHITE METAL LANTERN",
      "quantity": 6,
      "unitPrice": 3.39,
      "subtotal": 20.34
    }
  ],
  "numItems": 2,
  "totalPedido": 35.64
}
```

| Campo | Tipo | Descripción |
|---|---|---|
| `_id` / `invoiceNo` | string | Número de factura original (`InvoiceNo`); las devoluciones en el dataset real empiezan con "C", eso se usa para derivar `estado` |
| `customerId` | int | Referencia al `_id` de `clientes` (no se repiten aquí los datos del cliente) |
| `country` | string | País de la factura (se deja también aquí, duplicado a propósito: es una denormalización típica de MongoDB para no depender de un `$lookup` en la consulta más común, "ventas por país") |
| `invoiceDate` | date | Fecha y hora de la factura |
| `estado` | string | `"completado"` o `"devuelto"` (cuando `InvoiceNo` empieza con "C" o las cantidades son negativas) |
| `items` | array de sub-documentos | Una entrada por línea de producto de la factura |
| `items[].stockCode` / `description` / `quantity` / `unitPrice` / `subtotal` | — | Igual que en el CSV original, más `subtotal` calculado (`quantity * unitPrice`) |
| `numItems` | int | Cantidad de líneas de producto distintas en el pedido (campo derivado, útil para agregaciones) |
| `totalPedido` | number | Suma de los `subtotal` de todos los items (campo derivado, evita recalcularlo en cada consulta) |

## Por qué este diseño (criterio de modelado)

En MongoDB la regla general es: **"los datos que se consultan juntos, se guardan juntos"**. Casi
siempre que se pide un pedido, se necesitan también sus líneas de producto — por eso van
embebidas. En cambio, los datos de un cliente se consultan independientemente de un pedido
puntual (por ejemplo, para listar todos sus pedidos, o para un reporte de clientes), y un mismo
cliente aparece en muchos pedidos — por eso van en su propia colección y se referencian por
`customerId`, evitando repetir el país y otros datos del cliente en cada una de sus facturas.

## Próximo paso

Con este esquema ya definido, lo que sigue (paso 4) es preparar el entorno donde vamos a
instalar y correr MongoDB para crear estas dos colecciones y cargar los datos de prueba.
