#!/usr/bin/env python3
"""
Tarea 4 - Carga de datos de prueba en MongoDB (clientes + pedidos)
a partir de online_retail.csv (mismo dataset de las Tareas 2 y 3).

Ejecutar en la VM con:
    python3 /media/sf_Big_Data/Tarea4_mongo/seed_data.py
"""
import csv
import os
from datetime import datetime
from pymongo import MongoClient

CSV_PATH = os.path.expanduser("~/online_retail.csv")
MAX_ROWS = 20000  # suficientes filas del CSV real para tener >100 facturas distintas

WHOLESALE_THRESHOLD = 3000.0  # umbral de "mayorista" (ver cliente 12346.0 en Tarea 3)


def parse_customer_id(raw):
    raw = (raw or "").strip()
    if not raw:
        return None
    try:
        return int(float(raw))
    except ValueError:
        return None


def parse_date(raw):
    raw = (raw or "").strip()
    for fmt in ("%m/%d/%Y %H:%M", "%d/%m/%Y %H:%M", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    return None


def main():
    pedidos_por_factura = {}
    clientes_info = {}

    with open(CSV_PATH, newline="", encoding="latin-1") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= MAX_ROWS:
                break

            invoice_no = (row.get("InvoiceNo") or "").strip()
            customer_id = parse_customer_id(row.get("CustomerID"))
            if not invoice_no or customer_id is None:
                continue

            country = (row.get("Country") or "Desconocido").strip()
            stock_code = (row.get("StockCode") or "").strip()
            description = (row.get("Description") or "").strip()
            invoice_date = parse_date(row.get("InvoiceDate"))

            try:
                quantity = int(float(row.get("Quantity") or 0))
                unit_price = float(row.get("UnitPrice") or 0)
            except ValueError:
                continue

            subtotal = round(quantity * unit_price, 2)

            pedido = pedidos_por_factura.get(invoice_no)
            if pedido is None:
                estado = "devuelto" if invoice_no.upper().startswith("C") else "completado"
                pedido = {
                    "_id": invoice_no,
                    "invoiceNo": invoice_no,
                    "customerId": customer_id,
                    "country": country,
                    "invoiceDate": invoice_date,
                    "estado": estado,
                    "items": [],
                    "numItems": 0,
                    "totalPedido": 0.0,
                }
                pedidos_por_factura[invoice_no] = pedido

            pedido["items"].append({
                "stockCode": stock_code,
                "description": description,
                "quantity": quantity,
                "unitPrice": unit_price,
                "subtotal": subtotal,
            })
            pedido["numItems"] = len(pedido["items"])
            pedido["totalPedido"] = round(pedido["totalPedido"] + subtotal, 2)

            cliente = clientes_info.get(customer_id)
            if cliente is None:
                cliente = {
                    "_id": customer_id,
                    "customerId": customer_id,
                    "country": country,
                    "facturas": set(),
                    "fechas": [],
                    "maxFacturaTotal": 0.0,
                }
                clientes_info[customer_id] = cliente
            cliente["facturas"].add(invoice_no)
            if invoice_date:
                cliente["fechas"].append(invoice_date)

    # Segundo paso: calcular totales por factura para decidir el segmento del cliente
    for pedido in pedidos_por_factura.values():
        cliente = clientes_info.get(pedido["customerId"])
        if cliente and pedido["totalPedido"] > cliente["maxFacturaTotal"]:
            cliente["maxFacturaTotal"] = pedido["totalPedido"]

    clientes_docs = []
    for cliente in clientes_info.values():
        fechas = cliente["fechas"]
        primera_fecha = min(fechas).strftime("%Y-%m-%d") if fechas else None
        segmento = "mayorista" if cliente["maxFacturaTotal"] > WHOLESALE_THRESHOLD else "regular"
        clientes_docs.append({
            "_id": cliente["_id"],
            "customerId": cliente["customerId"],
            "country": cliente["country"],
            "numFacturasHistoricas": len(cliente["facturas"]),
            "clienteDesde": primera_fecha,
            "segmento": segmento,
        })

    pedidos_docs = list(pedidos_por_factura.values())

    print(f"Clientes distintos a insertar: {len(clientes_docs)}")
    print(f"Pedidos (facturas) distintos a insertar: {len(pedidos_docs)}")

    client = MongoClient("localhost", 27017)
    db = client["tienda_ecommerce"]

    db.clientes.drop()
    db.pedidos.drop()

    db.clientes.insert_many(clientes_docs)
    db.pedidos.insert_many(pedidos_docs)

    print("=== Carga completada ===")
    print("Base de datos:", db.name)
    print("clientes:", db.clientes.count_documents({}))
    print("pedidos:", db.pedidos.count_documents({}))


if __name__ == "__main__":
    main()
