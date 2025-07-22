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
                cursor.execute(query, (id_producto))
                resultado = cursor.fetchall()
                return resultado
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
        
    def obtener_corte(self, limite=50):
        """Obtiene hasta 50 pedidos del día"""
        query = """
            SELECT 
                c.id_corte_diario,
                p.nombre_prod,
                c.venta_total_dia,
                c.fecha_corte
            FROM "CorteDiario" c
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
        
