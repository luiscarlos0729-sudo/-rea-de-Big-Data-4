# Fase 1 — Investigación: Bases de datos NoSQL

*Borrador para revisar antes de publicarlo en el foro y de incorporarlo al informe final. Todo lo que está aquí ya va redactado en el tono formal del informe, listo para copiar y ajustar si quieres agregar algo propio.*

## 1. ¿Qué son las bases de datos NoSQL?

Las bases de datos NoSQL ("Not Only SQL") son sistemas de gestión de datos que se apartan del modelo relacional clásico (tablas, filas y columnas unidas mediante claves foráneas) para almacenar información en estructuras más flexibles: documentos, pares clave-valor, familias de columnas o grafos. No exigen un esquema fijo y predefinido como las bases de datos relacionales, lo que les permite adaptarse a datos semiestructurados o no estructurados y escalar horizontalmente —agregando más servidores— en lugar de depender únicamente de escalar verticalmente un único servidor más potente. Surgieron como respuesta a las necesidades de las aplicaciones web a gran escala de finales de la década de 2000 (Google, Amazon, Facebook), que debían manejar volúmenes de datos, velocidades de escritura y niveles de disponibilidad que los motores relacionales tradicionales no estaban diseñados para sostener de forma económica.

## 2. Ventajas y desventajas frente a las bases de datos relacionales

**Ventajas:**

- **Escalabilidad horizontal:** se distribuyen fácilmente entre varios servidores (sharding), lo que las hace más económicas de escalar que un motor relacional, que típicamente escala verticalmente.
- **Flexibilidad de esquema:** permiten almacenar documentos o registros con estructuras distintas entre sí, e incorporar nuevos campos sin migraciones costosas de esquema.
- **Alto rendimiento en escritura y lectura masiva:** al evitar los joins costosos y la normalización estricta, están optimizadas para operaciones de alto volumen y baja latencia.
- **Adecuadas para datos semiestructurados o no estructurados:** JSON, logs, contenido multimedia, datos de sensores, entre otros.
- **Buena disponibilidad y tolerancia a fallos:** muchas implementaciones replican los datos entre nodos y siguen operando aunque falle alguno.

**Desventajas:**

- **Consistencia más débil:** la mayoría prioriza disponibilidad y tolerancia a particiones sobre la consistencia inmediata (teorema CAP), por lo que suelen ofrecer solo consistencia eventual.
- **Soporte limitado de transacciones ACID complejas:** las operaciones que involucran varias colecciones o documentos no siempre son tan robustas como una transacción SQL multi-tabla.
- **Falta de un lenguaje de consulta estándar:** a diferencia de SQL, cada motor NoSQL (MongoDB, Cassandra, Redis, Neo4j, etc.) tiene su propia API o lenguaje de consulta, lo que dificulta portar conocimiento y consultas entre motores.
- **Menor madurez en herramientas de reporting y BI tradicional:** muchas herramientas de análisis empresarial fueron diseñadas pensando en SQL.
- **Redundancia de datos:** al desnormalizar para optimizar lectura, es común duplicar información, lo que exige más cuidado para mantenerla consistente.

## 3. Problemas que motivaron su aparición

El modelo relacional, dominante desde los años 70, resultó insuficiente frente a varios retos que aparecieron con el crecimiento de internet y las aplicaciones a gran escala:

- **Volumen de datos:** empresas como Google y Amazon comenzaron a manejar petabytes de información, un volumen para el que escalar verticalmente un único servidor relacional se volvía técnica y económicamente inviable.
- **Velocidad de generación de datos:** aplicaciones con millones de usuarios concurrentes (redes sociales, e-commerce) requerían escrituras y lecturas a una velocidad que los joins y los bloqueos propios del modelo relacional no soportaban bien.
- **Variedad y variabilidad de los datos:** gran parte de los nuevos datos (publicaciones de redes sociales, logs, clics, sensores IoT) no encajan naturalmente en un esquema tabular rígido y predefinido.
- **Costo de escalar:** escalar verticalmente (servidores más potentes) tiene un techo de costo y de capacidad física; escalar horizontalmente (más servidores estándar) resultaba más económico, pero el modelo relacional no estaba pensado para distribuirse fácilmente entre nodos.
- **Rigidez del esquema:** cualquier cambio en la estructura de una base de datos relacional en producción (agregar una columna, cambiar un tipo de dato) suele requerir migraciones cuidadosas; los equipos de desarrollo ágil necesitaban iterar más rápido.

Estos factores —resumidos frecuentemente como las "3V" del Big Data: Volumen, Velocidad y Variedad— llevaron a empresas tecnológicas a desarrollar sus propios sistemas de almacenamiento distribuido (el artículo de Google sobre Bigtable en 2006 y el de Amazon sobre Dynamo en 2007 se consideran precursores directos del movimiento NoSQL), que después derivaron en los motores NoSQL de uso público que existen hoy.

## 4. Clasificación de las bases de datos NoSQL

### 4.1 Clave-valor (Key-Value)

Es el modelo más simple: cada registro es un par formado por una clave única y un valor asociado (que puede ser un string, un número, un objeto serializado, etc.). El acceso es extremadamente rápido porque se hace directamente por clave, sin necesidad de recorrer ni indexar estructuras complejas. Ejemplos de motores: Redis, Amazon DynamoDB, Riak, Memcached.

### 4.2 Documentales

Almacenan la información como documentos semiestructurados, típicamente en formato JSON o BSON, donde cada documento puede tener una estructura de campos distinta e incluso campos anidados (sub-documentos y arreglos). Es el modelo más cercano a cómo las aplicaciones manejan los datos en memoria (objetos), lo que facilita el desarrollo. Ejemplos de motores: MongoDB (la base de datos de esta actividad), CouchDB, Firebase Firestore.

### 4.3 Columnas o Column-Family

Organizan los datos por familias de columnas en lugar de por filas completas, lo que optimiza la lectura y escritura de grandes volúmenes de datos dispersos o de series de tiempo, ya que solo se accede a las columnas necesarias en lugar de leer la fila entera. Ejemplos de motores: Apache Cassandra, Apache HBase, Google Bigtable.

### 4.4 Orientadas a grafos

Modelan los datos como nodos (entidades) y relaciones (aristas) entre ellos, con propiedades en ambos. Son especialmente eficientes para consultas que involucran relaciones complejas y de múltiples saltos entre entidades, algo costoso de resolver con joins en un modelo relacional. Ejemplos de motores: Neo4j, Amazon Neptune, ArangoDB.

## 5. Casos de uso reales

- **Clave-valor:** Redis se usa ampliamente como caché de sesiones de usuario y como almacén de carritos de compra en plataformas de e-commerce de alto tráfico, donde la prioridad es la latencia mínima de lectura/escritura; Amazon usa DynamoDB internamente para servicios de altísima disponibilidad como el carrito de compras de Amazon.com.
- **Documentales:** MongoDB es utilizada por empresas como eBay y por numerosos medios de comunicación y plataformas de e-commerce para catálogos de productos y gestión de contenido, donde cada producto o artículo puede tener atributos distintos entre sí.
- **Columnas:** Netflix utiliza Apache Cassandra para almacenar el historial de reproducción y las preferencias de sus suscriptores a escala global, dada su capacidad de escritura masiva y su tolerancia a fallos entre regiones; Facebook desarrolló originalmente Cassandra para el buscador de su bandeja de entrada.
- **Grafos:** LinkedIn utiliza una base de datos orientada a grafos para modelar y recorrer la red de conexiones profesionales entre usuarios; empresas de pagos como PayPal emplean bases de datos de grafos para detectar patrones de fraude, al poder analizar rápidamente relaciones indirectas entre cuentas y transacciones.

## Referencias utilizadas en esta sección (APA)

Miranda, A., Oña, P., Mendoza, K., & Chango, W. (2023). Evaluación comparativa de bases de datos NoSQL: clave/valor en un entorno de creaciones de aplicaciones. *ESPOCH Congresses: The Ecuadorian Journal of S.T.E.A.M*, *3*(2), 129–142. https://doi.org/10.18502/espoch.v4i1.15813

Sarasa, A. (2016). *Introducción a las bases de datos NoSQL usando MongoDB*. https://research-ebsco-com.bibliotecavirtual.unad.edu.co/linkprocessor/plink?id=dd7df4c4-4b47-3d44-bc5e-d891f6b99503

Gutiérrez Hernández, N. I., & Ibarra Limas, E. (2024). *Base de Datos para Proyectos de Big Data*. Congreso Internacional de Investigación Academia Journals. https://research-ebsco-com.bibliotecavirtual.unad.edu.co/linkprocessor/plink?id=b50cb8d0-5036-3c9c-a93d-baee11ae1d5e

Carrascal, F. L., & Varona, M. A. (2024). *Bases de Datos NoSQL* [Objeto virtual de aprendizaje OVA]. Repositorio Institucional UNAD. https://repository.unad.edu.co/handle/10596/62906
