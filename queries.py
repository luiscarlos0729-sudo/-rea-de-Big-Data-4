#!/usr/bin/env python3
"""
Tarea 4 - Consultas en MongoDB (CRUD, filtros/join, agregaciones)
sobre la base de datos tienda_ecommerce (clientes, pedidos).

Ejecutar en la VM con:
    python3 /media/sf_Big_Data/Tarea4_mongo/queries.py
"""
from pymongo import MongoClient
from pprint import pprint

client = MongoClient("localhost", 27017)
db = client["tienda_ecommerce"]
pedidos = db.pedidos
clientes = db.clientes


def titulo(txt):
    print("\n" + "=" * 70)
    print(txt)
    print("=" * 70)


# ---------------------------------------------------------------
# 1. CRUD basico
# ---------------------------------------------------------------
titulo("1.1 CREATE - insertar un pedido de prueba")
nuevo_pedido = {
    "_id": "TEST0001",
    "invoiceNo": "TEST0001",
    "customerId": 99999,
    "country": "Colombia",
    "invoiceDate": None,
    "estado": "completado",
    "items": [
        {"stockCode": "ABC123", "description": "PRODUCTO DE PRUEBA",
         "quantity": 2, "unitPrice": 10.0, "subtotal": 20.0},
    ],
    "numItems": 1,
    "totalPedido": 20.0,
}
pedidos.delete_one({"_id": "TEST0001"})
resultado = pedidos.insert_one(nuevo_pedido)
print("Insertado con _id:", resultado.inserted_id)

titulo("1.2 READ - leer el pedido recien insertado")
pprint(pedidos.find_one({"_id": "TEST0001"}))

titulo("1.3 UPDATE - marcar el pedido de prueba como 'devuelto'")
resultado = pedidos.update_one({"_id": "TEST0001"}, {"$set": {"estado": "devuelto"}})
print("Documentos modificados:", resultado.modified_count)
pprint(pedidos.find_one({"_id": "TEST0001"}))

titulo("1.4 DELETE - eliminar el pedido de prueba")
resultado = pedidos.delete_one({"_id": "TEST0001"})
print("Documentos eliminados:", resultado.deleted_count)


# ---------------------------------------------------------------
# 2. Consultas con filtros
# ---------------------------------------------------------------
titulo("2.1 Filtro simple - primeros 5 pedidos de United Kingdom")
for p in pedidos.find({"country": "United Kingdom"}).limit(5):
    print(p["invoiceNo"], p["country"], p["totalPedido"])

titulo("2.2 Filtro compuesto - pedidos completados con total mayor a 100")
cursor = pedidos.find({"estado": "completado", "totalPedido": {"$gt": 100}}).limit(5)
for p in cursor:
    print(p["invoiceNo"], p["estado"], p["totalPedido"])

titulo("2.3 Filtro - pedidos devueltos")
print("Total de pedidos devueltos:", pedidos.count_documents({"estado": "devuelto"}))


# ---------------------------------------------------------------
# 3. Consulta con operador de union ($lookup = "join" en MongoDB)
# ---------------------------------------------------------------
titulo("3. JOIN con $lookup - pedidos + datos del cliente (segmento, pais)")
pipeline_join = [
    {"$limit": 5},
    {"$lookup": {
        "from": "clientes",
        "localField": "customerId",
        "foreignField": "_id",
        "as": "cliente_info",
    }},
    {"$unwind": "$cliente_info"},
    {"$project": {
        "invoiceNo": 1,
        "totalPedido": 1,
        "cliente_pais": "$cliente_info.country",
        "cliente_segmento": "$cliente_info.segmento",
    }},
]
for doc in pedidos.aggregate(pipeline_join):
    pprint(doc)


# ---------------------------------------------------------------
# 4. Consultas de agregacion (count, sum, average)
# ---------------------------------------------------------------
titulo("4.1 COUNT - numero de pedidos por pais (top 5)")
pipeline_count = [
    {"$group": {"_id": "$country", "numPedidos": {"$sum": 1}}},
    {"$sort": {"numPedidos": -1}},
    {"$limit": 5},
]
for doc in pedidos.aggregate(pipeline_count):
    pprint(doc)

titulo("4.2 SUM - ventas totales por pais (top 5)")
pipeline_sum = [
    {"$group": {"_id": "$country", "ventasTotales": {"$sum": "$totalPedido"}}},
    {"$sort": {"ventasTotales": -1}},
    {"$limit": 5},
]
for doc in pedidos.aggregate(pipeline_sum):
    pprint(doc)

titulo("4.3 AVERAGE - ticket promedio por pedido (global y por pais, top 5)")
promedio_global = list(pedidos.aggregate([
    {"$group": {"_id": None, "promedioGlobal": {"$avg": "$totalPedido"}}},
]))
pprint(promedio_global)

pipeline_avg_pais = [
    {"$group": {"_id": "$country", "promedioPorPedido": {"$avg": "$totalPedido"}}},
    {"$sort": {"promedioPorPedido": -1}},
    {"$limit": 5},
]
for doc in pedidos.aggregate(pipeline_avg_pais):
    pprint(doc)

titulo("FIN DE LAS CONSULTAS")
