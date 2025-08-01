# db.py
import psycopg2
from psycopg2 import sql, extras
import logging

class Database:
    def __init__(self, dbname, user, password, host="localhost", port="5432"):
        self.conn_params = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host,
            "port": port
        }
        self.connection = None
        self.connect()
        
    def connect(self):
        """Establece la conexión con la base de datos"""
        try:
            self.connection = psycopg2.connect(**self.conn_params)
            logging.info("Conexión a PostgreSQL establecida")
        except Exception as e:
            logging.error(f"Error al conectar a PostgreSQL: {e}")
            raise

    def close(self):
        """Cierra la conexión con la base de datos"""
        if self.connection:
            self.connection.close()
            logging.info("Conexión a PostgreSQL cerrada")

    def execute_query(self, query, params=None, fetch=False):
        """Ejecuta una consulta SQL"""
        try:
            with self.connection.cursor(cursor_factory=extras.DictCursor) as cursor:
                cursor.execute(query, params or ())
                if fetch:
                    return cursor.fetchall()
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            logging.error(f"Error en la consulta: {e}")
            raise

    # Métodos específicos para la tabla Usuario
    def crear_usuario(self, nombre_usu, matricula_usu, contraseña_usu, aula_usu, salon_usu, aulaIngles_usu, salonIngles_usu):
        """Crea un nuevo usuario en la base de datos"""
        query = sql.SQL("""
            INSERT INTO "Usuario" (nombre_usu, matricula_usu, contraseña_usu, aula_usu, salon_usu, "aulaIngles_usu", "salonIngles_usu")
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_usuario
        """)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (nombre_usu, matricula_usu, contraseña_usu, aula_usu, salon_usu, aulaIngles_usu, salonIngles_usu))
                id_usuario = cursor.fetchone()[0]
                self.connection.commit()
                return id_usuario
        except Exception as e:
            self.connection.rollback()
            logging.error(f"Error al crear usuario: {e}")
            raise

    def actualizar_usuario(self, aula_usu, salon_usu,aulaIngles_usu, salonIngles_usu, matricula_usu):
        query = sql.SQL("""
            UPDATE "Usuario"
	        SET aula_usu=%s, salon_usu=%s, "aulaIngles_usu"=%s, "salonIngles_usu"=%s
	        WHERE matricula_usu=%s;
        """)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (aula_usu, salon_usu, aulaIngles_usu, salonIngles_usu, matricula_usu))
                self.connection.commit()
                
        except Exception as e:
            self.connection.rollback()
            logging.error(f"Error al crear usuario: {e}")
            raise
        

    def obtener_usuario_por_matricula(self, matricula_usu):
        """Obtiene un usuario por su matrícula"""
        query = sql.SQL("""
            SELECT * FROM "Usuario" WHERE matricula_usu = %s
        """)
        try:
            return self.execute_query(query, (matricula_usu,), fetch=True)
        except Exception as e:
            logging.error(f"Error al obtener usuario: {e}")
            return None
        

    def verificar_credenciales(self, matricula_usu, contraseña_usu):
        """Verifica si las credenciales son correctas"""
        query = """
            SELECT id_usuario FROM "Usuario" 
            WHERE matricula_usu = %s AND contraseña_usu = %s
        """
        try:
            result = self.execute_query(query, (matricula_usu, contraseña_usu), fetch=True)
            return bool(result)
        except Exception as e:
            logging.error(f"Error al verificar credenciales: {e}")
            return False
        
    def obtener_usuario_completo_por_matricula(self, matricula_usu):
        """Obtiene todos los datos de un usuario por su matrícula"""
        query = """
            SELECT 
                id_usuario,
                nombre_usu as "nombre_usu",
                matricula_usu as "matricula_usu",
                aula_usu as "aula_usu",
                salon_usu as "salon_usu",
                "aulaIngles_usu" as "aulaIngles_usu",
                "salonIngles_usu" as "salonIngles_usu"
            FROM "Usuario" WHERE matricula_usu = %s
        """
        try:
            with self.connection.cursor(cursor_factory=extras.DictCursor) as cursor:
                cursor.execute(query, (matricula_usu,))
                result = cursor.fetchone()
                if result:
                    return [dict(result)]  # Convertir a lista de dict
                return None
        except Exception as e:
            logging.error(f"Error al obtener usuario completo: {e}")
            return None
    
    # db.py (métodos actualizados para la tabla Producto)
    def obtener_stock_productos(self, ids_productos):
        """Obtiene el stock de múltiples productos"""
        query = sql.SQL("""
            SELECT id_producto, existencia_prod 
            FROM "Producto" 
            WHERE id_producto = ANY(%s)
        """)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (ids_productos,))
                resultados = cursor.fetchall()
                
                # Convertir a diccionario {id: existencia}
                return {row[0]: row[1] for row in resultados}
                
        except Exception as e:
            logging.error(f"Error al obtener stock: {e}")
            # Opcional: Reconectar si hay error de conexión
            self.connect()
            return None

    def actualizar_stock_producto(self, id_producto, disponible):
        """Actualiza el stock (existencia) de un producto en la base de datos"""
        query = sql.SQL("""
            UPDATE "Producto"
            SET existencia_prod = %s
            WHERE id_producto = %s
        """)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (disponible, id_producto))
                self.connection.commit()
                logging.info(f"Stock actualizado para producto {id_producto}: {disponible}")
                return True
        except Exception as e:
            self.connection.rollback()
            logging.error(f"Error al actualizar stock: {e}")
            return False
        
    def existenciaText_producto(self, id_producto):
        query = sql.SQL("""    
            SELECT existencia_prod FROM "Producto"
            where id_producto = %s
        """)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (id_producto,))
                resultado = cursor.fetchone()  # Cambiado de fetchall() a fetchone()
                if resultado:
                    return bool(resultado[0])  # Devuelve el valor booleano del primer campo
                return False  # Si no hay resultados
        except Exception as e:
            self.connection.rollback()
            logging.error(f"Error al actualizar stock: {e}")
            return False       
        
    def obtener_pedidos(self, limite=50):
        """Obtiene hasta 50 pedidos del día"""
        query = """
            SELECT p.id_pedido, u.nombre_usu, p.fecha_pedido, p.total_pedido
            FROM "Pedido" p
            JOIN "Usuario" u ON p.id_usuario = u.id_usuario
            ORDER BY p.id_pedido DESC 
            LIMIT %s
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query,(limite,))
                return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error al obtener pedidos del día: {e}")
            return []
    def obtener_pedidos_fecha(self, fecha_pedido, limite1=50, limite2=50):
        query = """
            WITH pedidos_por_fecha AS (
                SELECT p.id_pedido, u.nombre_usu, p.fecha_pedido, p.total_pedido
                FROM "Pedido" p
                JOIN "Usuario" u ON p.id_usuario = u.id_usuario
                WHERE p.fecha_pedido = %s
                ORDER BY p.id_pedido DESC 
                LIMIT %s
            )
            SELECT * FROM pedidos_por_fecha
            UNION ALL
            SELECT p.id_pedido, u.nombre_usu, p.fecha_pedido, p.total_pedido
            FROM "Pedido" p
            JOIN "Usuario" u ON p.id_usuario = u.id_usuario
            WHERE NOT EXISTS (SELECT 1 FROM pedidos_por_fecha)
            LIMIT %s;
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query,(fecha_pedido, limite1,limite2))
                return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error al obtener pedidos del día: {e}")
            return []
        
    def obtener_pedido_ultimos_dias(self, ultimosDias):
        query = """
            SELECT p.id_pedido, u.nombre_usu, p.fecha_pedido, p.total_pedido
            FROM "Pedido" p
            JOIN "Usuario" u ON p.id_usuario = u.id_usuario
            WHERE p.fecha_pedido >= CURRENT_DATE - (INTERVAL '1 day' * %s)
            ORDER BY p.fecha_pedido DESC;
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (ultimosDias,))
                return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error al obtener pedidos de los últimos días: {e}")
            return []
        
    def obtener_pedidoDestales(self, limite=50):
        """Obtiene hasta 50 pedidos del día"""
        query = """
            SELECT d.id_detalle, d.id_pedido, p.nombre_prod, d.cantidad_detalle, d.subtotal_detalle
			FROM "DetallePedido" d
            JOIN "Producto" p ON d.id_producto = p.id_producto
            LIMIT %s
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query,(limite,))
                return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error al obtener pedidos del día: {e}")
            return []
    def pedidoDestalles_por_Idpedido(self, id_pedido, limite=3):
        query = """
            WITH primera_consulta AS (
                SELECT * FROM "DetallePedido" WHERE id_pedido = %s LIMIT %s
            )
            SELECT * FROM primera_consulta
            UNION ALL
            SELECT * FROM "DetallePedido" 
            WHERE NOT EXISTS (SELECT 1 FROM primera_consulta);
            """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query,(id_pedido,limite))
                return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error al obtener pedidos del día: {e}")
            return []
        
    def obtener_corte(self, limite=50):
        query = """
            SELECT 
                c.id_corte_diario,
                p.nombre_prod,
                c.venta_total_dia,
                c.fecha_corte
            FROM "Corte" c
            JOIN "Producto" p ON c.producto_mas_vendido = p.id_producto
            LIMIT %s;
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query,(limite,))
                return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error al obtener pedidos del día: {e}")
            return []
        
    def registrar_pedido(self, id_usuario, total_pedido):
        """agregar un nuevo pedido en la base de datos"""
        query = sql.SQL("""
            INSERT INTO "Pedido" (id_usuario, total_pedido)
            VALUES (%s, %s)
            RETURNING id_pedido
        """)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (id_usuario, total_pedido))
                id_pedido = cursor.fetchone()[0]
                self.connection.commit()
                return id_pedido
        except Exception as e:
            self.connection.rollback()
            logging.error(f"Error al hacer pedido: {e}")
            raise
    
    def registrar_detalle_pedido(self, id_pedido, id_producto, cantidad_detalle, subtotal_detalle):
        """agregar un nuevo pedido en la base de datos"""
        query = sql.SQL("""
            INSERT INTO "DetallePedido" (id_pedido, id_producto, cantidad_detalle, subtotal_detalle)
            VALUES (%s, %s, %s, %s)   
        """)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (id_pedido, id_producto, cantidad_detalle, subtotal_detalle))
                self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            logging.error(f"Error al hacer pedido: {e}")
            raise


    def obtener_todos_productos(self):
        """Obtiene todos los productos ordenados por ID"""
        query = sql.SQL("""
            SELECT * FROM "Producto"
            ORDER BY id_producto
        """)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error al obtener todos los productos: {e}")
            return []

    def crear_producto(self, nombre_prod, descripcion_prod, precio_prod, existencia_prod):
        """Crea un nuevo producto en la base de datos"""
        query = sql.SQL("""
            INSERT INTO "Producto" (nombre_prod, descripcion_prod, precio_prod, existencia_prod)
            VALUES (%s, %s, %s, %s)
            RETURNING id_producto
        """)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (nombre_prod, descripcion_prod, precio_prod, existencia_prod))
                id_producto = cursor.fetchone()[0]
                self.connection.commit()
                return id_producto
        except Exception as e:
            self.connection.rollback()
            logging.error(f"Error al crear producto: {e}")
            return None

    def actualizar_producto(self, id_producto, nombre_prod=None, descripcion_prod=None, 
                        precio_prod=None, existencia_prod=None):
        """Actualiza un producto existente"""
        updates = []
        params = []
        
        if nombre_prod is not None:
            updates.append(sql.SQL("nombre_prod = %s"))
            params.append(nombre_prod)
        if descripcion_prod is not None:
            updates.append(sql.SQL("descripcion_prod = %s"))
            params.append(descripcion_prod)
        if precio_prod is not None:
            updates.append(sql.SQL("precio_prod = %s"))
            params.append(float(precio_prod))
        if existencia_prod is not None:
            updates.append(sql.SQL("existencia_prod = %s"))
            params.append(existencia_prod)
        
        if not updates:
            return False  # No hay nada que actualizar
        
        params.append(id_producto)
        
        query = sql.SQL("""
            UPDATE "Producto"
            SET {updates}
            WHERE id_producto = %s
        """).format(updates=sql.SQL(', ').join(updates))
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            self.connection.rollback()
            logging.error(f"Error al actualizar producto: {e}")
            return False
        
    def obtener_producto(self, id_producto):
        """Obtiene un producto por su ID"""
        query = sql.SQL("""
            SELECT id_producto, nombre_prod, descripcion_prod, precio_prod, existencia_prod
            FROM "Producto"
            WHERE id_producto = %s
        """)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (id_producto,))
                return cursor.fetchone()  # Retorna una tupla con los datos del producto
        except Exception as e:
            logging.error(f"Error al obtener producto por ID: {e}")
            return None

    def eliminar_producto(self, id_producto):
        """Elimina un producto por su ID"""
        query = sql.SQL("""
            DELETE FROM "Producto"
            WHERE id_producto = %s
        """)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (id_producto,))
                self.connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            self.connection.rollback()
            logging.error(f"Error al eliminar producto: {e}")
            return False

    def buscar_productos_por_nombre(self, nombre):
        """Busca productos por coincidencia en el nombre"""
        query = sql.SQL("""
            SELECT * FROM "Producto"
            WHERE nombre_prod ILIKE %s
            ORDER BY nombre_prod
        """)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (f"%{nombre}%",))
                return cursor.fetchall()
        except Exception as e:
            logging.error(f"Error al buscar productos por nombre: {e}")
            return []
        
