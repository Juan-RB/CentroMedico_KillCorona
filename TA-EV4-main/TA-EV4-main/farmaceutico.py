import pymysql
import os
from conexion import *
from datetime import datetime

hora_actual = datetime.now().strftime("%H:%M")          # Ajuste de hora 
fecha_actual = datetime.now().strftime("%d - %m - %Y")  # Ajuste de fecha 

os.system("cls")

class Farmaceutico:                                     # Definicion de clase de Farmaceutico
    def __init__(self, codFar, codTra):
        self.codFar = codFar
        self.codTra = codTra

    def __str__(self) -> str:
        print(f"el codigo de farmaceutico es :{self.codFar} , el codigo de trabajador es {self.codTra} ")

    def asignar_farmaceutico(cod_trabajador):           #Definicion de clase farmaceutico con sus atributos
        conexion = ConexionBD()
        consulta_farmaceutico = """
            SELECT fa.codFar,fa.codTra
            FROM usuario us
            INNER JOIN trabajador tr ON us.codTra = tr.codTra
            INNER JOIN farmaceutico fa ON tr.codTra = fa.codTra
            WHERE us.codTra = %s
        """
        valores_farmaceutico = (cod_trabajador,)
        resultado_farmaceutico = conexion.ejecutar_consulta(
            consulta_farmaceutico, valores_farmaceutico
        )

        if len(resultado_farmaceutico) == 1:
            codFar, codTra = resultado_farmaceutico[0]
            farmaceutico = Farmaceutico(codFar, codTra)
            return farmaceutico
        
        conexion.cerrar_conexion()
        return None


        return None

        
                                                
    def listar_insumos(self):                               # Función para listar los insumos
        
        conexion = ConexionBD()                             # Establecer la conexión a la base de datos
        try:
            query = "SELECT * FROM INSUMO"                  # Consulta SQL para obtener todos los insumos
            
            resultados = conexion.ejecutar_consulta(query)  # Ejecutar la consulta

            if resultados:                                  # Lista los insumos especificamente por codigo, nombre y stock 
                print("Lista de insumos:")
                for insumo in resultados:
                    codIns, codTipoI, codUbi, nombre, stock = insumo
                    print(f" - Código: {codIns} \t Stock: {stock} \t Nombre: {nombre} ")
            else:
                print("No se encontraron insumos.")         # En caso de no encontrar data en base de datos
        finally:
            conexion.cerrar_conexion()                      # Cerrar la conexión

    
    def listar_bajo_stock(self):                            # funcion de listar por bajo stock
        
        conexion = ConexionBD()                             # Establecer la conexión a la base de datos
        try:
            
            query = "SELECT * FROM INSUMO WHERE stock <= 5" # Consulta SQL para obtener los insumos con bajo stock
            
            resultados = conexion.ejecutar_consulta(query)  # Ejecutar la consulta

            
            if resultados:
                print("Insumos con bajo stock:")            # Listar los insumos con bajo stock especificamente por codigo, nombre y stock
                for insumo in resultados:
                    codIns, codTipoI, codUbi, nombre, stock = insumo
                    print(f" - Código: {codIns} \t Stock: {stock} \t Nombre: {nombre} ")
            else:
                print("No se encontraron insumos con bajo stock.") # En caso de no enocontar data en la base de datos
        except pymysql.Error as error:
            print("Error al ejecutar la consulta:", error)  # En caso que la consulta este mal formulada
        finally:
            
            conexion.cerrar_conexion()                      # Cerrar la conexión

    
    def listar_por_tipo(self):                              # Función para listar por tipo de insumo
        
        conexion = ConexionBD()                             # Establecer la conexión a la base de datos
        try:
            
            query_tipos = "SELECT * FROM TIPO_INSUMO"       # Consultar los tipos de insumo disponibles
            tipos_insumo = conexion.ejecutar_consulta(query_tipos)

            while True:                                     # Comienza un buble while donde imprime primero los tipos de insumo 
                print("\n", "Tipos de Insumo: ", "\n")
                for tipo in tipos_insumo:
                    codTipoI, nombre = tipo
                    print(f" - Código: {codTipoI}, Nombre: {nombre} ") # Imprime los Tipos de insumo por codigo y nombre

                
                cod_tipo_elegido = input("Ingrese el código del tipo de insumo deseado (0 para volver al menú): ") # Solicitar al usuario seleccionar el tipo de insumo
                os.system("cls")
                if cod_tipo_elegido == "0":                            # Para salir del menú tendran que ingresar '0'
                    break
                try:
                    cod_tipo_elegido = int(cod_tipo_elegido)           # Covierte el cod_tipo_elegido de varchar a interger   
                    query_insumos = (
                    f"SELECT * FROM INSUMO WHERE codTipoI = {cod_tipo_elegido}") # Consulta SQL para obtener los insumos del tipo seleccionado
                    
                    resultados = conexion.ejecutar_consulta(query_insumos) # Ejecutar la consulta

                    if resultados:
                        print(f"Insumos del tipo {cod_tipo_elegido}:", "\n") # Mostrar los insumos del tipo seleccionado 
                        for insumo in resultados:
                            codIns, codTipoI, codUbi, nombre, stock = insumo 
                            print(f" - Código: {codIns} \t Stock: {stock} \t Nombre: {nombre} ")
                    else:
                        print(f"No se encontraron insumos del tipo {cod_tipo_elegido}.") # En caso de no encontrar datos en la base de datos
                except ValueError:
                    print("Error: Ingrese un número válido.")           # En caso de ingresar mal los datos
                except pymysql.Error as error:
                    print("Error al ejecutar la consulta:", error)      # En caso de que se ejecute mal la consulta 
        finally:
        
            conexion.cerrar_conexion()                                  # Cerrar la conexión

    
    def listar_por_vencimiento_cercano(self):                           # Función para listar los insumos por fecha de vencimiento cercana
    
        conexion = ConexionBD()                                         # Establecer la conexión a la base de datos

        try:
            
            query = "SELECT * FROM REGISTRO_BODEGA WHERE fecVec <= CURDATE() + INTERVAL 30 DAY" # Consulta SQL para obtener los insumos con fecha de vencimiento cercana
            resultados = conexion.ejecutar_consulta(query)              # Ejecutar la consulta

            if resultados:
                print("Insumos con fecha de vencimiento cercana:")      # Mostrar los insumos con fecha de vencimiento cercana
                for insumo in resultados:
                    (
                        codMov,
                        codTipoM,
                        codFar,
                        codIns,
                        fecIns,
                        fecVec,
                        lote,
                        stock,
                    ) = insumo
                    print(
                        f"Código Movimiento: {codMov}, Código Insumo: {codIns}, Fecha Vencimiento: {fecVec}, Stock: {stock}")
            else:
                print("No se encontraron insumos con fecha de vencimiento cercana.")

        except pymysql.Error as error:
            print("Error al ejecutar la consulta:", error)

        finally:
            
            conexion.cerrar_conexion()                                  # Cerrar la conexión


    def filtrar_por_lote(self):                                         # Función para filtrar los insumos por lote
        
        conexion = ConexionBD()  
        resultados=[]
        lote_elegido = input("Ingrese el número de lote deseado: ")
                                            # Establecer la conexión a la base de datos
        try:
            lote_elegido = int(lote_elegido)                      # Intenta convertir la opción a un entero

        except ValueError:
            print("Error: Ingrese un número válido.")
        
            # Solicitar al usuario ingresar el lote deseado
        
            
        try:    
            # Validación para asegurarnos
            query = f"SELECT * FROM REGISTRO_BODEGA WHERE lote = {lote_elegido}"  # Consulta SQL para obtener los insumos del lote seleccionado
            resultados = conexion.ejecutar_consulta(query)              # Ejecutar la consulta

            if resultados:
                print(
                    f"Insumos del lote {lote_elegido}:")                # Mostrar los insumos del lote seleccionado
                for insumo in resultados:
                    (
                        codMov,
                        codTipoM,
                        codFar,
                        codIns,
                        fecIns,
                        fecVec,
                        lote,
                        stock,
                    ) = insumo
                    print(
                        f"Código Movimiento: {codMov}, Código Insumo: {codIns}, Stock: {stock}")
            else:
                print(f"No se encontraron insumos del lote {lote_elegido}.")

        except pymysql.Error as error:
            print("Error al ejecutar la consulta:", error)

        finally:
            conexion.cerrar_conexion()     
        if not resultados:
            print("No se encontró información para el lote especificado.")                               # Cerrar la conexión

    def actualizar_stock_insumo(self, farmaceutico):                       # Función de actualizar el stock de los insumos
        
        conexion = ConexionBD()                                            # Establecer la conexión a la base de datos
        try:
            # query_insumos = "SELECT * FROM INSUMO"                                # Mostrar los insumos disponibles
            # insumos = conexion.ejecutar_consulta(query_insumos)
            # print("Insumos:")
            # for tipo in insumos:
            #     codIns, codTipoI, codUbi, nombre_in, stock= tipo
            #     print(f" - Código: {codIns} \t stock: {stock} \t Nombre: {nombre_in} ") 
            query_tipos = "SELECT * FROM TIPO_INSUMO"       # Consultar los tipos de insumo disponibles
            tipos_insumo = conexion.ejecutar_consulta(query_tipos)
            print("\n", "Tipos de Insumo: ", "\n")
            for tipo in tipos_insumo:
                codTipoI, nombre = tipo
                print(f" - Código: {codTipoI}, Nombre: {nombre} ") # Imprime los Tipos de insumo por codigo y nombre

            cod_tipo_elegido = input("Ingrese el código del tipo de insumo deseado : ") # Solicitar al usuario seleccionar el tipo de insumo
            os.system("cls")
            
            try:
                cod_tipo_elegido = int(cod_tipo_elegido)           # Covierte el cod_tipo_elegido de varchar a interger   
                query_insumos = (
                f"SELECT * FROM INSUMO WHERE codTipoI = {cod_tipo_elegido}") # Consulta SQL para obtener los insumos del tipo seleccionado
                
                resultados = conexion.ejecutar_consulta(query_insumos) # Ejecutar la consulta

                if resultados:
                    print(f"Insumos del tipo {cod_tipo_elegido}:", "\n") # Mostrar los insumos del tipo seleccionado 
                    for insumo in resultados:
                        codIns, codTipoI, codUbi, nombre, stock = insumo 
                        print(f" - Código: {codIns} \t Stock: {stock} \t Nombre: {nombre} ")
                else:
                    print(f"No se encontraron insumos del tipo {cod_tipo_elegido}.") # En caso de no encontrar datos en la base de datos
            except ValueError:
                print("Error: Ingrese un número válido.")           # En caso de ingresar mal los datos
            except pymysql.Error as error:
                print("Error al ejecutar la consulta:", error)  

            codIns = input("Ingrese el código del insumo por actualizar: ")               # Solicitar los datos del insumo a actualizar
            nuevo_stock = int(input("Ingrese el nuevo stock del insumo: "))
            
            query_verificar_insumo = "SELECT codIns FROM INSUMO WHERE codIns = %s" # Consulta para Verificar si el insumo existe en la tabla INSUMO
            resultado_verificacion = conexion.ejecutar_consulta(
                query_verificar_insumo, (codIns,))
            

            if resultado_verificacion:
                
                query_actualizar_stock_insumo = ("UPDATE INSUMO SET stock = %s WHERE codIns = %s")      # Actualizar el stock del insumo existente en la tabla INSUMO
                valores_actualizacion_insumo = (nuevo_stock, codIns)
                
                                                    
                codFar = farmaceutico.codFar

                fecIns = datetime.now().strftime("%Y-%m-%d")

                query_bodega_lote = (f"select * from registro_bodega where codMov = (SELECT MAX(codMov) FROM registro_bodega WHERE codIns = {codIns})")
                valor_bodega_lote = conexion.ejecutar_consulta(query_bodega_lote)
                print('Ultimo registro en bodega del insumo pedido')
                for datos in valor_bodega_lote :
                    codMov, codTipoM, codFar, codIns, fecIns, fecVec, lote, stock= datos
                    print(f'- insumo: {codIns} \t Lote: {lote} \t Stock actual: {stock} fecha de vencimiento: {fecVec}' )
                    
                lote = input("Ingrese el número de lote: ")
                                                                                                                    
                pregunta_fecha = input('¿Desea actualizar la fecha de vencimiento? (si/no): ').lower()  # Verificar si se desea actualizar la fecha de vencimiento

                if pregunta_fecha == 'si':
                    fecVec = input("Ingrese la nueva fecha de vencimiento (yyyy-mm-dd): ")
                elif pregunta_fecha == 'no':
                    # Obtener la fecha de vencimiento existente basada en el código de insumo y lote
                    query_fecha_vencimiento = f"SELECT fecVec FROM registro_bodega WHERE codMov = (SELECT MAX(codMov) FROM registro_bodega WHERE codIns = {codIns} AND lote = {lote})"
                    resultado_fecha_vencimiento = conexion.ejecutar_consulta(query_fecha_vencimiento)
                    
                    if resultado_fecha_vencimiento:
                        fecVec = resultado_fecha_vencimiento[0][0]  # Se asume que solo habrá un resultado
                    else:
                        print("No se encontró la fecha de vencimiento asociada al insumo y lote proporcionados.")
                        return

                codTipoM = 2   # Código para indicar un ingreso de insumo

                query_nuevo_registro_bodega = "INSERT INTO REGISTRO_BODEGA (codTipoM, codFar, codIns, fecIns, fecVec, lote, stock) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                valores_nuevo_registro = (
                    codTipoM,
                    codFar,
                    codIns,
                    fecIns,
                    fecVec,
                    lote,
                    nuevo_stock,)
                pregunta = input('¿Desea guardar los datos? si/no: ').lower()
                
                if pregunta == 'si':
                    conexion.ejecutar_actualizacion(query_actualizar_stock_insumo, valores_actualizacion_insumo)
                    conexion.ejecutar_actualizacion(query_nuevo_registro_bodega, valores_nuevo_registro)

                    print("Stock actualizado y nuevo registro en bodega creado exitosamente.")
                elif pregunta == 'no':
                    print('Actualizacion cancelada')
                    input('Enter para continuar...')
                    
                else:
                    print('Solo puedes ingresar "si" o "no" otro tipo palabra o caracter no será valido')
                    input('Enter para continuar...')

            else:
                print("El insumo con el código proporcionado no existe.")

        except (pymysql.Error, ValueError) as error:
            print("Error al actualizar el stock del insumo:", error)

        finally:
            conexion.cerrar_conexion()                                          # Cerrar la conexión

    
    def ingreso_insumos(self):                                                  # Función para realizar el ingreso de insumos
        
        conexion = ConexionBD()   
                                                    # Establecer la conexión a la base de datos
        try:
            query_tipos = "SELECT * FROM TIPO_INSUMO"                                   # Mostrar los tipos de insumo disponibles
            tipos_insumo = conexion.ejecutar_consulta(query_tipos)
            print("Tipos de Insumo:")
            for tipo in tipos_insumo:
                codTipoI, nombre = tipo
                print(f" - Código: {codTipoI} \t Nombre: {nombre}")                    # Muestra los tipos de insumos, pero solamente el codigo y el nombre

            codTipoI = input("Ingrese el código del tipo de insumo deseado : ")
            codTipoI = int(codTipoI)

            query_insumo= "SELECT MAX(codIns) FROM insumo"                          # Busca el valor maximo de codIns y le suma 1 para asi automatizar el proceso de llenado
            insumo_max = conexion.ejecutar_consulta(query_insumo)
            codIns = insumo_max [0][0] + 1

            query_ubicacion="SELECT * FROM UBICACION_BODEGA"                        # Consulta para tener una previsualización de los tipos de movimientos facilitando el llenado del formulario.
            ubicacion=conexion.ejecutar_consulta(query_ubicacion)
            print('Ubicaciones en bodega:')
            for valor in ubicacion:
                codUbi, nombre_ub = valor
                print(f"- Codigo: {codUbi} \t Nombre: {nombre_ub}")

            codUbi = input("Ingrese el código de ubicación en bodega: ")

            nombre_in = input("Ingrese el nombre del insumo: ").upper()

            query_verificar_insumo_codIns = "SELECT codIns FROM INSUMO WHERE codIns = %s"# Consulta para Verificar si el insumo ya existe en la tabla INSUMO por medio del codIns
            resultado_verificacion_codIns = conexion.ejecutar_consulta(query_verificar_insumo_codIns, (codIns,))

            query_verificar_insumo_nombre_in = "SELECT codIns FROM INSUMO WHERE nombre_in = %s "# Consulta para Verificar si el insumo ya existe en la tabla INSUMO por medio del nombre_in
            nombre_insumo = (nombre_in)
            resultado_verificacion_nombre_in = conexion.ejecutar_consulta(query_verificar_insumo_nombre_in, nombre_insumo)
            
            stock = int(input("Ingrese la cantidad de stock: "))
            
            if resultado_verificacion_codIns:
                input("El insumo ingresado ya existe, enter para continuar...")
                
            elif resultado_verificacion_nombre_in :
                input("El insumo ingresado ya existe, enter para continuar...")
                return
            else:
                # Insertar el nuevo insumo en la tabla INSUMO
                consulta_insumo = "INSERT INTO INSUMO (codIns, codTipoI, codUbi, nombre_in, stock) VALUES (%s, %s, %s, %s, %s)"
                valores_insumo = (codIns, codTipoI, codUbi, nombre_in, stock)
                
            
            # Registrar el ingreso del insumo en la tabla REGISTRO_BODEGA
            codTipoM = 2                                                            # Código para indicar un ingreso de insumo
            fecIns = datetime.now().strftime("%Y-%m-%d")                            # Fecha de ingreso
            fecVec = input("Ingrese la fecha de vencimiento (yyyy-mm-dd): ")
            lote = input("Ingrese el número de lote: ")

            consulta_bodega = "INSERT INTO REGISTRO_BODEGA (codTipoM, codFar, codIns, fecIns, fecVec, lote, stock) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            valores_bodega = (
                codTipoM,
                self.codFar,
                codIns,
                fecIns,
                fecVec,
                lote,
                stock,
            )

            pregunta = input('¿Desea agregar este insumo? si/no: ').lower()
            if pregunta == 'si':
                conexion.ejecutar_actualizacion(consulta_insumo, valores_insumo)
                conexion.ejecutar_actualizacion(consulta_bodega, valores_bodega)
                print("Insumo ingresado exitosamente.")
            elif pregunta == 'no': 
                print('La entrada de datos ha sido cancelada')
                input('Enter para continuar...')
            else:
                print('Solo puedes ingresar "si" o "no" otro tipo palabra o caracter no será valido')
                input('Enter para continuar...')

        except (pymysql.Error, ValueError) as error:
            print("Error al ingresar el insumo:", error)

        finally:
            conexion.cerrar_conexion()

    def retirar_insumos(farmaceutico):                                                  # Función de retirar insumos de la tabla de insumos  
        conexion = ConexionBD()

        try:
            query_tipos = "SELECT * FROM TIPO_INSUMO"                                   # Mostrar los tipos de insumo disponibles
            tipos_insumo = conexion.ejecutar_consulta(query_tipos)

            while True:
                print("Tipos de Insumo:")
                for tipo in tipos_insumo:
                    codTipoI, nombre = tipo
                    print(f" - Código: {codTipoI}, Nombre: {nombre}")                    # Muestra los tipos de insumos, pero solamente el codigo y el nombre

                cod_tipo_elegido = input("Ingrese el código del tipo de insumo deseado (0 para volver al menú): ")

                if cod_tipo_elegido == "0":                                              # Solo se puede salir en caso de ingresar '0'
                    break

                try:
                    cod_tipo_elegido = int(cod_tipo_elegido)

                    query_insumos = f"SELECT * FROM INSUMO WHERE codTipoI = {cod_tipo_elegido} AND stock > 0" # Consultar los insumos disponibles del tipo seleccionado
                    insumos_disponibles = conexion.ejecutar_consulta(query_insumos)

                    if insumos_disponibles:
                        print(f"Insumos disponibles del tipo {cod_tipo_elegido}:")
                        for insumo in insumos_disponibles:
                            codIns, codTipoI, codUbi, nombre, stock = insumo
                            print(f" - Código: {codIns} \t Stock: {stock} \t Nombre: {nombre} ")   #nos muesta los insumos disponibles del tipo de insumo anteriormente ingresado

                        cod_insumo = input("Ingrese el código del insumo a retirar: ")
                        try:
                            cod_insumo = int(cod_insumo)                                    # Intenta convertir la opción a un entero

                            query = f"SELECT * FROM REGISTRO_BODEGA WHERE codIns = {cod_insumo}"   # Consulta SQL para obtener los registros de bodega por el codIns
                            
                            resultados = conexion.ejecutar_consulta(query)

                        except ValueError:
                            input("Error: Ingrese un número válido.")
                        
                        cantidad_retirar = int(input("Ingrese la cantidad a retirar: "))

                        # Verificar si el insumo existe y tiene suficiente stock
                        query_verificar_insumo = ("SELECT codIns, stock FROM INSUMO WHERE codIns = %s")
                        resultado_verificacion = conexion.ejecutar_consulta(query_verificar_insumo, (cod_insumo,))

                        

                        if resultado_verificacion:
                            codIns, stock_actual = resultado_verificacion[0]

                            if stock_actual >= cantidad_retirar:
                            
                                nuevo_stock = stock_actual - cantidad_retirar                 # Actualizar el stock del insumo
                                query_update_stock = ("UPDATE INSUMO SET stock = %s WHERE codIns = %s")
                                valores_update_stock = (nuevo_stock, codIns)
                                
                                # Crear un registro de retiro en la tabla REGISTRO_BODEGA
                                codTipoM = 1                                                # Código para indicar un retiro de insumo
                                codFar = farmaceutico.codFar                                # Código codFar de farmaceutico para verificación de indentidad 
                                fecIns = datetime.now().strftime("%Y-%m-%d")                # fecha del momento en que se hizo
                                fecVec = None                                               # Fecha de vencimiento que queda nula por que es un retiro
                                
                                

                                print("Registros de Bodega:")
                                for registro in resultados:
                                    codMov, codTipoM, codFar, codIns, fecIns, fecVec, lote, stock = registro
                                    print(f"Código Insumo: {codIns}, Fecha Ingreso: {fecIns}, Fecha Vencimiento: {fecVec}, Lote: {lote}, Stock: {stock}")
                                
                                lote = input('Ingrese el lote del insumo a retirar: ')       # lote del insumo a retirar

                                query_registro_retiro = "INSERT INTO REGISTRO_BODEGA (codTipoM, codFar, codIns, fecIns, fecVec, lote, stock) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                                valores_registro_retiro = (
                                    codTipoM,
                                    codFar,
                                    codIns,
                                    fecIns,
                                    fecVec,
                                    lote,
                                    cantidad_retirar,
                                )

                                pregunta = input('¿Desea retirar este insumo? si/no: ').lower()
                                if pregunta == 'si':
                                    conexion.ejecutar_actualizacion(query_update_stock, valores_update_stock)
                                    conexion.ejecutar_actualizacion(query_registro_retiro, valores_registro_retiro)
                                    print("Insumo retirado exitosamente.")

                                elif pregunta == 'no': 
                                    print('La entrada de datos ha sido cancelada')
                                    input('Enter para continuar...')

                                else:
                                    print('Solo puedes ingresar "si" o "no" otro tipo palabra o caracter no será valido')
                                    input('Enter para continuar...')
                            else:
                                print("Stock insuficiente para realizar el retiro.")
                        else:
                            print("El insumo con el código proporcionado no existe.")
                    else:
                        print(
                            f"No se encontraron insumos del tipo {cod_tipo_elegido} disponibles.")

                except ValueError:
                    print("Error: Ingrese un número válido.")

                except pymysql.Error as error:
                    print("Error al ejecutar la consulta:", error)
        finally:
            conexion.cerrar_conexion()


def menu_farmaceutico(
    farmaceutico, codigo_trabajador, nombre_trabajador):  # el menu farmaceutico para iniciar si requiere el objeto farmaceutico, su codigo de trabajo y nombre del trabajador
    while True:
        os.system("cls")
        print(
            f"""
        =================================================
                    Menú Farmacia
        \tNombre: {nombre_trabajador}
        \tCódigo Farmacéutico: {farmaceutico.codFar}
        \tCódigo empleado: {codigo_trabajador}
        \tHora: {hora_actual}\tFecha: {fecha_actual} 
        =================================================
                1 - Filtro de insumos 
                2 - Ingreso de insumos 
                3 - Retiro de insumos 
                4 - Volver al menú principal
                5 - Cambiar password
        """
        )

        opcion_farm = input("Ingrese la opción deseada: ")
        try:
            opcion_farm = int(opcion_farm)                      # Intenta convertir la opción a un entero

        except ValueError:
            print("Error: Ingrese un número válido.")
                                                                # Vuelve al inicio del ciclo sin ejecutar el resto del código                       
        if opcion_farm == 1:
            os.system("cls")
            print(
                """
            ====================================
                        Filtro de insumos
            ====================================
                    1 - Lista de insumos
                    2 - Listar por bajo stock
                    3 - Listar por tipo de insumo
                    4 - Listar por vencimiento cercano
                    5 - Listar por codigo de lote
                    6 - Volver a Menú Farmacia """)

            op_farm = input("Ingrese la opción deseada: ")

            if op_farm == "1":
                os.system("cls")
                print(
                    """
                ====================================
                        Lista de insumos
                ====================================
                """
                )
                farmaceutico.listar_insumos()
                input("Enter para continuar...")
                menu_farmaceutico(farmaceutico, codigo_trabajador, nombre_trabajador)

            elif op_farm == "2":
                os.system("cls")
                print(
                    """
                ====================================
                        Bajo stock
                ====================================
                """
                )
                farmaceutico.listar_bajo_stock()
                input("Enter para continuar...")
                menu_farmaceutico(farmaceutico, codigo_trabajador, nombre_trabajador)

            elif op_farm == "3":
                os.system("cls")
                print(
                    """
                ====================================
                        Tipo de Insumo
                ====================================
                """
                )
                farmaceutico.listar_por_tipo()
                
                menu_farmaceutico(farmaceutico, codigo_trabajador, nombre_trabajador)

            elif op_farm == "4":
                os.system("cls")
                print(
                    """
                ====================================
                        Vencimiento cercano
                ====================================
                """
                )
                farmaceutico.listar_por_vencimiento_cercano()
                input("Enter para continuar...")
                menu_farmaceutico(farmaceutico, codigo_trabajador, nombre_trabajador)

            elif op_farm == "5":
                os.system("cls")
                print(
                    """
                ====================================
                        Codigo de lote
                ====================================
                """
                )
                farmaceutico.filtrar_por_lote()
                input("Enter para continuar...")
                menu_farmaceutico(farmaceutico, codigo_trabajador, nombre_trabajador)

            elif op_farm == "6":
                input(
                    "Saliendo del filtro de insumos... presione enter para volver al menu principal"
                )
                menu_farmaceutico(farmaceutico, codigo_trabajador, nombre_trabajador)
            else:
                print("Opción inválida. Por favor, ingrese una opción válida.")
                input("Presione enter para continuar")

                                                            # fin del filtro de insumos
        elif opcion_farm == 2:
            os.system("cls")
            print(
                """
            ====================================
                    Ingreso de insumos

                1 - Actualizar
                2 - Registrar
                3 - salir 
            ====================================""" )
            op_ingreso = input("Ingrese una opción: ")

            try:
                op_ingreso = int(op_ingreso)                # Intenta convertir la opción a un entero
            
            except ValueError:
                print("Error: Ingrese un número válido.")

            if op_ingreso == 1:
                os.system("cls")

                print(
                    """
                ====================================
                        Actualizar Stock
                ====================================
                """
                )
                codFar = farmaceutico.codFar
                farmaceutico.actualizar_stock_insumo(farmaceutico)

                input("Enter para continuar...")
                menu_farmaceutico(farmaceutico, codigo_trabajador, nombre_trabajador)

            elif op_ingreso == 2:
                os.system("cls")

                print(
                    """
                ====================================
                        Registrar Insumos
                ====================================
                """)
                farmaceutico.ingreso_insumos()

                input("Enter para continuar...")
                menu_farmaceutico(farmaceutico, codigo_trabajador, nombre_trabajador)

            elif op_ingreso == 3:
                break

            else:
                input("Opción invalida")
            

        elif opcion_farm == 3:
            os.system("cls")
            #
            print(
                """
            ====================================
                    Retiro de insumos
            ====================================""" )
            farmaceutico.retirar_insumos()
            menu_farmaceutico(farmaceutico, codigo_trabajador, nombre_trabajador)
                                                                # se debe definir el codTipoM como Retiro = 1

        elif opcion_farm == 4:
            os.system("cls")

            input("Saliendo del menu farmacia... presione enter para volver al menu principal")
            break

        elif opcion_farm == 5:
            os.system("cls")
            cambiar_password(farmaceutico.codTra)

        else:
            print("Opción inválida. Por favor, ingrese una opción válida.")
            input("Presione enter para continuar")
