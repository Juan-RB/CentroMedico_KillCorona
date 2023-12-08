import os
from datetime import *
from conexion import *
import calendar
import locale

hora_actual = datetime.now().strftime("%H:%M")
fecha_actual = datetime.now().strftime("%d - %m - %Y")


class Recepcionista:  # clase de recepcionista
    def __init__(self,codRep,codTra):
        self.codRep = codRep
        self.codTra = codTra

    def asignar_recepcionista(cod_trabajador):  # crea objeto recepcionista
        conexion = ConexionBD()
        consulta_recepcionista = """
            SELECT re.codRep, re.codTra
            FROM usuario us
            INNER JOIN trabajador tr ON us.codTra = tr.codTra
            INNER JOIN recepcionista re ON tr.codTra = re.codTra
            WHERE us.codTra = %s
        """
        valores_recepcionista = (cod_trabajador,)
        resultado_recepcionista = conexion.ejecutar_consulta(consulta_recepcionista, valores_recepcionista)


        if len(resultado_recepcionista) == 1:

            codRep, codTra = resultado_recepcionista[0]
            recepcionista = Recepcionista(codRep, codTra)
            return recepcionista

        return None

        return None


    def obtener_ficha_paciente(self, rut_P):  # obtiene la ficha del paciente

        conexion = ConexionBD() # conexion base de datos

        consulta = '''SELECT  ci.rut_P, ci.codCit, ci.codBox, tc.nomTc, tr.nombre_T, tr2.nombre_T, ci.hora, ci.fecha
                    FROM cita ci
                    INNER JOIN tipo_cita tc ON ci.codTc = tc.codTc
                    INNER JOIN medico me ON ci.codPm = me.codPm
                    INNER JOIN trabajador tr ON me.codTra = tr.codTra
                    INNER JOIN recepcionista re ON ci.codRep = re.codRep
                    INNER JOIN trabajador tr2 ON re.codTra = tr2.codTra
                    WHERE ci.rut_P = %s'''

        valores = (rut_P,)

        resultado = conexion.ejecutar_consulta(consulta, valores)

        conexion.cerrar_conexion()

        return resultado
    
    


    def agregar_paciente(self,rut_P):  # crea un paciente nuevo en la base de datos

        conexion = ConexionBD()

        try: # Solicitar los datos del paciente al usuario

            nombre = input("Ingrese el nombre del paciente: ").upper()

            domicilio = input("Ingrese el domicilio del paciente: ").upper()

            comuna = input("Ingrese la comuna del paciente: ").upper()

            telefono = input("Ingrese el teléfono del paciente: ").upper()

            while not telefono.isdigit(): # validacion para verificar que el telefono sean numeros enteros

                print("Error: El teléfono debe contener solo números.")
                telefono = input("Ingrese nuevamente el teléfono del paciente: ").upper()
        
            email = input("Ingrese el email del paciente: ").lower()
            while "@" not in email:   # Validación para verificar que el correo electrónico contenga "@"
                print("Error: El email debe contener el símbolo '@'.")
                email = input("Ingrese nuevamente el email del paciente: ").lower()

            

            if not nombre.strip(): # Validaciones para verificar que las variables no estén vacías
                print("Error: El nombre no puede estar vacío.")
        
            elif not domicilio.strip():

                print("Error: El domicilio no puede estar vacío.")

            elif not comuna.strip():

                print("Error: La comuna no puede estar vacía.")

            elif not telefono.strip():

                print("Error: El teléfono no puede estar vacío.")

            elif not email.strip():

                print("Error: El email no puede estar vacío.")

            else:
                print("\n")
                print("-------------------------")
                print("Datos del paciente nuevo")
                print("-------------------------")
                print(f"Nombre: {nombre}")
                print(f"Domicilio: {domicilio}")
                print(f"Comuna: {comuna}")
                print(f"Teléfono: {telefono}")
                print(f"Email: {email}")
                print("\n")
            
                respuesta=input("¿Desea confirmar la operación? (si/no): ").capitalize()

                if respuesta == "Si":

                    consulta = f"INSERT INTO PACIENTE (rut_P, nombre_P, direccion_P, comuna_P, telefono_P, email_P) VALUES (%s, %s, %s, %s, %s, %s)"  # Consulta SQL para insertar los datos del paciente

                    valores = (rut_P, nombre, domicilio, comuna, telefono, email)

                    conexion.ejecutar_actualizacion(consulta, valores) # Ejecutar la consulta de inserción

                    print("Nuevo paciente creado en base de datos.")

                    input("Presione enter para continuar")

                elif respuesta =="No":

                    print("La operacion ha sido cancelada, no se ha agregado el nuevo paciente a la base de datos")

                    input("Presione enter para continuar")


        except pymysql.Error as error: # si falla la conexion da este error

            print("Error al insertar los datos del paciente:", error)

        finally:
            conexion.cerrar_conexion()
            pass

    def editar_paciente(self,rut_p): # menu para editar datos de un paciente .

        os.system("cls")

        while True:
            os.system("cls")
            print(f'''
                ==========================================================
                            Menú Edicion de datos paciente                          
                ==========================================================
                1 - Nombre
                2 - Dirección
                3 - Comuna
                4 - Teléfono
                5 - Email
                6 - Salir de edición

            ''')

            opcion=input("Ingrese su opción por favor :") # el usuario ingresa el numero



            while not opcion.isdigit(): # en caso de no ingresar un numero, se le pide al usuario nuevamente ingresar numero

                print("Error: ingrese un número válido.")

                opcion = input("Ingrese nuevamente su opción: ")

            opcion = int(opcion)  # Convertie la opción a entero

            if opcion == 1: # Para cambiar nombre

                conexion = ConexionBD()

                os.system("cls")

                try:
                    print("=================================")
                    print(''' Modificar nombre del paciente ''')
                    print("=================================")
                    
                    nombre = input("Ingrese el nombre del paciente: ").upper() # Solicitar los datos del paciente al usuario


                    respuesta=input("¿ Desea modificar el nombre del paciente ? (si/no)").capitalize() # se le pide al usuario confirmar la operacion

                    print("\n")

                    if respuesta == "Si": #si confirma la operacion"

                        consulta = f"UPDATE paciente set nombre_p= %s where rut_P= %s"   # Consulta SQL para insertar los datos del paciente
                        
                        valores = (nombre,rut_p)   # valores de la consulta sql

                        conexion.ejecutar_actualizacion(consulta, valores)    # Ejecutar la consulta de inserción

                        print("Nombre del paciente modificado correctamente.")

                        print("\n")
                        
                        # se ejecuta la funcion con la variable previamente ingresada y validada

                        consulta_datos_paciente = "SELECT * FROM paciente WHERE rut_P = %s"
                        valores_datos_paciente = (rut_p,)
                        datos_paciente = conexion.ejecutar_consulta(consulta_datos_paciente, valores_datos_paciente)

                        if datos_paciente:
                            paciente_actualizado = datos_paciente[0]  # Obtener la primera fila (única fila) de los datos del paciente

                            # Imprimir los datos actualizados del paciente
                            print("-----------------------------------")
                            print("Datos del paciente actualizados:")
                            print("\n")
                            print("Rut del paciente:", paciente_actualizado[0])
                            print("Nombre del paciente:", paciente_actualizado[1])
                            print("Domicilio:", paciente_actualizado[2])
                            print("Comuna:", paciente_actualizado[3])
                            print("Teléfono:", paciente_actualizado[4])
                            print("Email:", paciente_actualizado[5])
                            print("-----------------------------------")

                            print("\n")

                        input("Presione enter para continuar")

                        os.system("cls")

                    elif respuesta == "No":  # si no la confirma.
                        print("\n")

                        print("La operacion ha sido cancelada")

                        print("\n")

                        input("Presione enter para continuar")

                    else:
                        print("Elija una opción valida")

                        print("\n")

                        input("Presione enter para continuar")

                except pymysql.Error as error:  # para dar error en caso de falla

                    print("Error al insertar los datos del paciente: ", error)

                finally:

                    conexion.cerrar_conexion() # Cerrar la conexión
                    
            elif opcion == 2: # Para cambiar direccion
                    
                    os.system("cls")

                    conexion = ConexionBD()
                    
                    try:
                        print("====================================")
                        print('''Modificar Dirección  del paciente ''')
                        print("===================================")
                        
                        direccion = input("Ingrese el nombre de la dirección: ").upper() # Solicitar los datos del paciente al usuario

                        respuesta=input("¿ Desea modificar la dirección del paciente ? (si/no)").capitalize() # se le pide al usuario confirmar la operacion

                        print("\n")

                        if respuesta == "Si": #si confirma la operacion"

                            consulta = f"UPDATE paciente set direccion_P= %s where rut_P= %s" # Consulta SQL para insertar los datos del paciente

                            valores = (direccion,rut_p)  # valores de la consulta sql

                        
                            conexion.ejecutar_actualizacion(consulta, valores)    # Ejecutar la consulta de inserción de datos

                            print("Dirección del paciente modificado correctamente.")

                            
                            # se ejecuta la funcion con la variable previamente ingresada y validada

                            consulta_datos_paciente = "SELECT * FROM paciente WHERE rut_P = %s"
                            valores_datos_paciente = (rut_p,)
                            datos_paciente = conexion.ejecutar_consulta(consulta_datos_paciente, valores_datos_paciente)

                            if datos_paciente:
                                paciente_actualizado = datos_paciente[0]  # Obtener la primera fila (única fila) de los datos del paciente

                                # Imprimir los datos actualizados del paciente
                                print("-----------------------------------")
                                print("Datos del paciente actualizados:")
                                print("\n")
                                print("Rut del paciente:", paciente_actualizado[0])
                                print("Nombre del paciente:", paciente_actualizado[1])
                                print("Domicilio:", paciente_actualizado[2])
                                print("Comuna:", paciente_actualizado[3])
                                print("Teléfono:", paciente_actualizado[4])
                                print("Email:", paciente_actualizado[5])
                                print("-----------------------------------")

                                print("\n")

                            input("Presione enter para continuar")

                            os.system("cls")

                        elif respuesta == "No":  # si no la confirma.
                            print("\n")

                            print("La operacion ha sido cancelada")
                            
                            print("\n")

                            input("Presione enter para continuar")


                        else:
                            print("Elija una opción valida")

                            print("\n")

                            input("Presione enter para continuar")


                    except pymysql.Error as error: # error base de datos

                        print("Error al insertar los datos del paciente:", error)
                    finally:
                        
                        conexion.cerrar_conexion()
                        
                        pass
                

            elif opcion == 3: # modifica Comuna

                os.system("cls")

                conexion = ConexionBD()

                try:
                    print("====================================")
                    print('''Modificar comuna  del paciente ''')
                    print("===================================")
                    
                    comuna = input("Ingrese el nombre de la comuna: ").upper() # Solicitar los datos del paciente al usuario

                    respuesta=input("¿ Desea modificar la comuna del paciente ? (si/no)").capitalize() # se le pide al usuario confirmar la operacion


                    if respuesta == "Si": #si confirma la operacion"

                            consulta = f"UPDATE paciente set comuna_P= %s where rut_P= %s"     # Consulta SQL para insertar los datos del paciente

                            valores = (comuna,rut_p)

                            conexion.ejecutar_actualizacion(consulta, valores)    # Ejecutar la consulta de inserción
                            
                            print("Comuna del paciente correctamente modificado.")

                            input("Presione enter para continuar")

                            print("\n")

                            
                            # se ejecuta la funcion con la variable previamente ingresada y validada

                            consulta_datos_paciente = "SELECT * FROM paciente WHERE rut_P = %s"
                            valores_datos_paciente = (rut_p,)
                            datos_paciente = conexion.ejecutar_consulta(consulta_datos_paciente, valores_datos_paciente)

                            if datos_paciente:
                                paciente_actualizado = datos_paciente[0]  # Obtener la primera fila (única fila) de los datos del paciente

                                # Imprimir los datos actualizados del paciente
                                print("-----------------------------------")
                                print("Datos del paciente actualizados:")
                                print("\n")
                                print("Rut del paciente:", paciente_actualizado[0])
                                print("Nombre del paciente:", paciente_actualizado[1])
                                print("Domicilio:", paciente_actualizado[2])
                                print("Comuna:", paciente_actualizado[3])
                                print("Teléfono:", paciente_actualizado[4])
                                print("Email:", paciente_actualizado[5])
                                print("-----------------------------------")


                            input("Presione enter para continuar")

                            os.system("cls")

                    elif respuesta == "No":  # si no la confirma.

                        print("\n")

                        print("La operacion ha sido cancelada")
                        
                        print("\n")

                        input("Presione enter para continuar")

                    else:
                        print("Elija una opción valida")

                        print("\n")

                        input("Presione enter para continuar")

                except pymysql.Error as error: # en caso de error de la base de datos
                    
                    print("Error al insertar los datos del paciente:", error)

                    input("presione enter para continuar")

                finally:  # Cerrar la conexión

                    conexion.cerrar_conexion()
                    pass

            elif opcion == 4:  # Telefono

                os.system("cls")

                conexion = ConexionBD()
                try:
                    while True:
                        print("====================================")
                        print('''Modificar teléfono  del paciente ''')
                        print("===================================")
                        
                        telefono = input("Ingrese el número de teléfono del paciente: ") # Solicitar los datos del paciente al usuario

                        respuesta=input("¿ Desea modificar el teléfono del paciente ? (si/no)").capitalize() # se le pide al usuario confirmar la operacion

                        if respuesta == "Si": #si confirma la operacion"

                            telefono = int(telefono)  # Convertir a entero

                            
                            consulta = "UPDATE paciente SET telefono_P = %s WHERE rut_P = %s" # Consulta SQL para insertar los datos del paciente
                            
                            valores = (telefono, rut_p)

                            conexion.ejecutar_actualizacion(consulta, valores)     # Ejecutar la consulta de actualización

                            print("Teléfono del paciente actualizados correctamente.")

                            input("presione enter para continuar")

                            consulta_datos_paciente = "SELECT * FROM paciente WHERE rut_P = %s"
                            valores_datos_paciente = (rut_p,)
                            datos_paciente = conexion.ejecutar_consulta(consulta_datos_paciente, valores_datos_paciente)

                            if datos_paciente:
                                paciente_actualizado = datos_paciente[0]  # Obtener la primera fila (única fila) de los datos del paciente

                                    # Imprimir los datos actualizados del paciente
                                print("-----------------------------------")
                                print("Datos del paciente actualizados:")
                                print("\n")
                                print("Rut del paciente:", paciente_actualizado[0])
                                print("Nombre del paciente:", paciente_actualizado[1])
                                print("Domicilio:", paciente_actualizado[2])
                                print("Comuna:", paciente_actualizado[3])
                                print("Teléfono:", paciente_actualizado[4])
                                print("Email:", paciente_actualizado[5])
                                print("-----------------------------------")


                                input("Presione enter para continuar")

                                os.system("cls")

                                break

                        elif respuesta == "No":  # si no la confirma.
                            print("\n")

                            print("La operacion ha sido cancelada")
                            
                            print("\n")

                            input("Presione enter para continuar")

                            break

                        else:
                            print("Elija una opción valida")

                            print("\n")

                            input("Presione enter para continuar")

                except ValueError: # en caso de que no ingrese numero valido

                        print("Error: Ingrese un número valido de telefono.")

                        input("Presione enter para continuar")

                        os.system("cls")

                except pymysql.Error as error:

                    print("Error al insertar los datos del paciente:", error)

                    os.system("cls")

                finally:
        
                    conexion.cerrar_conexion() # Cierra la conexión


            elif opcion == 5:  # Editar correo
                os.system("cls")

                conexion = ConexionBD()

                try:
                    while True:
                        print("====================================")
                        print('''Modificar email  del paciente ''')
                        print("===================================")
                        email = input("Ingrese el correo electrónico del paciente: ") # Solicitar los datos del paciente al usuario

                        if "@" in email: # Consulta SQL para actualizar el correo del paciente

                            respuesta=input("¿ Desea modificar el teléfono del paciente ? (si/no)").capitalize() # se le pide al usuario confirmar la operacion


                            if respuesta == "Si": #si confirma la operacion"
            
                                
                                    consulta = "UPDATE paciente SET email_P = %s WHERE rut_P = %s"

                                    valores = (email, rut_p)

                                    conexion.ejecutar_actualizacion(consulta, valores)        # Ejecutar la consulta de actualización

                                    print("Correo del paciente modificado correctamente.")

                                    input("Presione enter para continuar.")

                                    consulta_datos_paciente = "SELECT * FROM paciente WHERE rut_P = %s"
                                    valores_datos_paciente = (rut_p,)
                                    datos_paciente = conexion.ejecutar_consulta(consulta_datos_paciente, valores_datos_paciente)

                                    
                                    if datos_paciente:
                                        paciente_actualizado = datos_paciente[0]  # Obtener la primera fila (única fila) de los datos del paciente

                                            # Imprimir los datos actualizados del paciente
                                        print("-----------------------------------")
                                        print("Datos del paciente actualizados:")
                                        print("\n")
                                        print("Rut del paciente:", paciente_actualizado[0])
                                        print("Nombre del paciente:", paciente_actualizado[1])
                                        print("Domicilio:", paciente_actualizado[2])
                                        print("Comuna:", paciente_actualizado[3])
                                        print("Teléfono:", paciente_actualizado[4])
                                        print("Email:", paciente_actualizado[5])
                                        print("-----------------------------------")

                                

                                        input("Presione enter para continuar")

                                        os.system("cls")

                                        break

                            elif respuesta == "No":  # si no la confirma.
                                print("\n")

                                print("La operacion ha sido cancelada")
                                
                                print("\n")

                                input("Presione enter para continuar")

                                break

                            else:
                                print("Elija una opción valida")

                                print("\n")

                                input("Presione enter para continuar")


                        else:  # en caso de que falle el correo

                            print("Error: Ingrese un correo electrónico válido.")

                            input("Presione enter para continuar.")

                            os.system("cls")

                except pymysql.Error as error: # en caso de error 

                    print("Error al actualizar los datos del paciente:", error)

                finally:

                    conexion.cerrar_conexion() # Cerrar la conexión
            
            elif opcion == 6: # opcion para salir del menu

                os.system("cls")

                input("Saliendo del menú edición de datos ... presione enter para volver al menú principal")

                break
            else: # en caso de que la opcion tipeada no sea la correcta

                print("Seleccione una opción valida")
                input("Presione enter para continuar")
                os.system("cls")

    def obtener_citas(self, rut_P):  # funcion para obtener citas

        conexion = ConexionBD() # conecta la base de datos

        consulta = '''SELECT  ci.rut_P, ci.codCit, ci.codBox, tc.nomTc, tr.nombre_T, tr2.nombre_T, ci.hora, ci.fecha
                    FROM cita ci
                    INNER JOIN tipo_cita tc ON ci.codTc = tc.codTc
                    INNER JOIN medico me ON ci.codPm = me.codPm
                    INNER JOIN trabajador tr ON me.codTra = tr.codTra
                    INNER JOIN recepcionista re ON ci.codRep = re.codRep
                    INNER JOIN trabajador tr2 ON re.codTra = tr2.codTra
                    WHERE ci.rut_P = %s'''
        
        valores = (rut_P,) # valores de la consulta

        resultado = conexion.ejecutar_consulta(consulta, valores)

        return resultado  # retorna los resultados de la consulta
    
    def crear_cita(self,rut_P,codRep): # funcion para crear cita de un paciente


        while True:
            conexion = ConexionBD() 
            consulta1 = "SELECT funcion FROM medico"  # consulta SQL

            resultado1 = conexion.ejecutar_consulta(consulta1)  # resultado expresado en una variable

            especialidades = [fila[0].upper() for fila in resultado1]  # obtener las especialidades en una lista

            especialidad_valida = False

            while not especialidad_valida:
                print("=================================")
                print('''   Modulo Agendar citas      ''')
                print("=================================")
                print("\n")
                print("Especialidades disponibles:")
                print("\n")
                for especialidad in especialidades:
                    print(f"Especialidad: {especialidad}")

                caracteres_tildes = ['á', 'é', 'í', 'ó', 'ú', 'Á', 'É', 'Í', 'Ó', 'Ú']
                print("\n")
                especialidad = input("Ingrese la especialidad que desea buscar (Ingresar la especialidad sin tilde y sin números): ").upper()

                if any(caracter in especialidad for caracter in caracteres_tildes) or especialidad.isdigit():

                    print("Error: La especialidad contiene tildes o números.\n")
                    
                    input("Presione enter para continuar")
                elif especialidad not in especialidades:

                    print("Error: La especialidad no está disponible.\n")

                    input("Presione enter para continuar")
                else:
                    especialidad_valida = True

                os.system("cls")

                # Pedir nuevamente la entrada del usuario o realizar alguna otra acción
            else:

                valores2 = (especialidad,)  # valores de la consulta

                consulta2 = "SELECT me.codPm, tr.nombre_T, me.funcion, bx.codBox FROM medico me INNER JOIN trabajador TR ON me.codTra=tr.codTra INNER JOIN box bx ON me.codPm=bx.codPm WHERE me.funcion=%s"  # consulta SQL

                resultado2 = conexion.ejecutar_consulta(consulta2, valores2)  # los resultados

                print("=================================")
                print('''   Modulo Agendar citas      ''')
                print("=================================")

                codigos_validos = []

                 # obtener los códigos de los médicos en una lista

                for fila in resultado2:  # imprime los datos de la consulta
                    codPm, nombre_T, funcion, box = fila
                    codigos_validos.append(str(codPm))

                    print(f"Código del médico: {codPm}")
                    print(f"Nombre del médico: {nombre_T}")
                    print(f"Codigo del box Asignado: {box}")
                    print("------------------------------")

                codPM = input("Ingrese el código del médico: ")  # se le pide al usuario que ingrese el código PM

                while codPM not in codigos_validos  or not codPM.isdigit():
                    if not codPM.isdigit():
                        print("Error: El código del médico no debe contener letras.")
                    else:
                        print("Error: El código del médico no es válido, debe ser uno de los códigos mostrados anteriormente.")
                    codPM = input("Ingrese nuevamente el código del médico: ")

                codPM = int(codPM)  # transforma el input string a entero

                consulta8 = "SELECT codbox FROM `box` WHERE codPm = %s"

                resultado8 = conexion.ejecutar_consulta(consulta8, (codPM,)) #

                for fila in resultado8: # imprime los resultado a traves de un ciclo

                    codBox = fila # asigna los resultados a las variables indicadas 

                os.system("cls")

                print("=================================")
                print('''   Modulo Agendar citas      ''')
                print("=================================")

                consulta3 = "SELECT codTc, nomTC FROM tipo_cita"  # consulta sql para obtener datos de codigo tipo cita y nombre del tipo cita
                resultado3 = conexion.ejecutar_consulta(consulta3)

                codigos_validos2 = []

                for fila in resultado3: # imprime el resultado

                    codTc, nomTC = fila # asigna variables con los datos obtenidos agrupados en una fila

                    codigos_validos2.append(str(codTc))

                    print(f"Código de tipo de cita: {codTc}\tNombre de tipo de cita: {nomTC}") #imprime los resultados en una fila

                print("\n")

                codTc=input("Ingrese el código del tipo procedimiento: ") # ingreso de numero

                while not codTc.isdigit() or codTc not in codigos_validos:
                    if not codTc.isdigit():
                        print("Error: El código del tipo de procedimiento debe ser un número.")
                    else:
                        print("Error: El código del tipo de procedimiento no es válido.")
                    codTc = input("Ingrese nuevamente el código del tipo de procedimiento: ")

                codTc = int(codTc)
                
                os.system("cls")

                print("=================================")
                print('''   Modulo Agendar citas      ''')
                print("=================================")

                print("Turnos del médico elegido, Revise su calendario en sistema ")  

                consulta4 = "SELECT tu.dia_T, tu.hora_iT, tu.hora_fT FROM MEDICO ME INNER JOIN turnos TU ON me.codPm = tu.codPm WHERE tu.codPm = %s" # consulta sql para obtener el dia , hora de inicio del turno y hora final del turno

                resultado4 = conexion.ejecutar_consulta(consulta4, (codPM,)) #

                for fila in resultado4: # imprime los resultado a traves de un ciclo

                    dia_t, hora_iT, hora_fT = fila # asigna los resultados a las variables indicadas 

                    print(f"Día del turno: {dia_t}  Hora de inicio: {hora_iT}   Hora de fin: {hora_fT}") # imprime los resultados

                
                fecha_valida = False

                while not fecha_valida:
                    fecha_str = input("Ingrese la fecha (en formato 'YYYY-MM-DD'): ")

                    try:
                        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
                        fecha_valida = True
                    except ValueError:
                        print("Error: Formato de fecha inválido. Intente nuevamente.")

                print("\n")

                if fecha_valida:
                    print("Horas del médico en los próximos días. Considere 15 minutos de consulta. Si aparece con cirugía, considerar no disponible.")


                consulta5='''SELECT  tc.nomTc, ci.hora, ci.fecha 
                            FROM cita ci
                            INNER JOIN tipo_cita tc ON ci.codTc = tc.codTc
                            INNER JOIN medico me ON ci.codPm = me.codPm
                            INNER JOIN trabajador tr ON me.codTra = tr.codTra
                            INNER JOIN recepcionista re ON ci.codRep = re.codRep
                            INNER JOIN trabajador tr2 ON re.codTra = tr2.codTra
                            WHERE ci.fecha= %s''' # consulta sql
                
                resultado5 = conexion.ejecutar_consulta(consulta5, (fecha)) #resultado sql

                for fila in resultado5: # # imprime el resultado a traves de un ciclo

                    nomTc, hora, fecha = fila # agrupa los resultados en una fila

                    print(f"Nombre del tipo de cita: {nomTc} Hora: {hora} Fecha: {fecha} ")

                consulta7='''select nomTc from tipo_cita where codTc=%s''' # consulta sql para descubrir el tipo de consulta donde el codigo TC sea igual a

                resultado7 = conexion.ejecutar_consulta(consulta7,(codTc)) # resultado de la consulta agrupado a una variable

                nomTc = resultado7[0][0] 
                
                print("\n")

                hora_valida = False
 
                while not hora_valida:  # validacion para la hora, que este dentro de un rango, que no este vacia y que el formato de hora es invalido
                    hora_str = input("Ingrese la hora, considere que los turnos de los medicos estan entre 08:00 a 18:00 (en formato 'HH:MM'): ")

                    if re.match(r'^\d{2}:\d{2}$', hora_str):
                        horas, minutos = map(int, hora_str.split(':'))
                        if 0 <= horas <= 23 and 0 <= minutos <= 59:
                            if 8 <= horas <= 17:
                                hora_valida = True
                            else:
                                print("Error: La hora debe estar dentro del rango de trabajo (8:00 - 17:59).")
                                input("Presione enter para continuar")
                        else:
                            print("Error: Hora fuera de rango. Intente nuevamente.")
                            input("Presione enter para continuar")
                    else:
                        print("Error: Formato de hora inválido. Intente nuevamente.")
                        input("Presione enter para continuar")

                fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date() # hora convertira en fecha para ser ingresada a la consulta sql
                
                hora = datetime.strptime(hora_str, "%H:%M").time()  # fecha convertira en fecha para ser ingresada a la consulta sql

                os.system("cls")

                print("=================================")
                print('''   Modulo Agendar citas      ''')
                print("=================================")

                print(f'''
                    Codigo del box:{box}
                    Codigo del médico:{codPM}\t Nombre del médico:{nombre_T}
                    Codigo de la atencion:{codTc}\t Tipo de Atencion:{nomTc}
                    Hora de la atencion: {hora}
                    Fecha de la atencion: {fecha}
                ''')   # imprime la cita del paciente para poder confirmar los datos


                opcion=input("¿ Desea agendar la cita ? (si/no): ").capitalize() # pregunta para agendar la sida

                if opcion == "Si": # al ingresar si, se realiza la consulta
                    
                    consulta6='''INSERT INTO cita (rut_P, codBox, codTc, codPm, codRep, fecha, hora) VALUES (%s, %s, %s, %s, %s, %s, %s)''' # consulta en 

                    valores = (rut_P,box, codTc, codPm, codRep, fecha, hora)

                    conexion.ejecutar_actualizacion(consulta6, valores)

                    print("Datos ingresados correctamente")

                    input("Presione Enter para continuar")

                    conexion.cerrar_conexion()

                    break

                elif opcion == "No": # la consulta no se realiza

                    print("La cita indicada no ha sido registrada")

                    input("Presione enter para continuar")

                    conexion.cerrar_conexion()

                    break



    
    def eliminar_cita(self,rut_P,codRep): # Para eliminar cita 

        print("=================================")
        print(''' Eliminar Cita de la agenda ''')
        print("=================================")
        
        conexion = ConexionBD()

        codCit=input("Ingrese el código de la cita que desea eliminar por favor: ") # ingresar codigo de cita

        while not codCit.isdigit(): # validacion para que sea numero

            print("Error: el código de la cita debe ser un número.")

            codCit = input("Ingrese nuevamente el código de la cita: ")

        codCit = int(codCit)  # Convertir a entero

        consulta="SELECT rut_p,codCit,codBox,codTc,codPm,codRep,fecha,hora FROM `cita` WHERE codCit= %s and rut_p= %s"

        valores=(codCit,rut_P)

        resultado = conexion.ejecutar_consulta(consulta, valores)

        print("\n")


        if resultado: # si encuentra resultado imprime datos
            for fila in resultado: # por cada resultado encontrado
                rut_P, codCit, codBox, nomTc, nombre_T, nombre_T2, hora, fecha = fila
                print(f"RUT del paciente: {rut_P}")
                print(f"Código de cita: {codCit}")
                print(f"Código de box: {codBox}")
                print(f"Tipo de cita: {nomTc}")
                print(f"Nombre del médico: {nombre_T}")
                print(f"Nombre de la recepcionista: {nombre_T2}")
                print(f"Hora: {str(hora)}")
                print(f"Fecha: {fecha}")
                print("\n")

            opcion2=input("¿ Desea eliminar la cita encontrada ? (si/no): ").capitalize() # se le pregunta al usuario si quiere eliminar la cita encontrada

            if opcion2 == "Si": # si el usuario elige si, se ejecuta la consulta 

                consulta2="DELETE FROM `cita` WHERE codCit= %s "

                valores2=(codCit,)

                conexion.ejecutar_actualizacion(consulta2, valores2) #para ejecutar la consulta

                print("La cita ha sido borrada ")

                input("Presione enter para continuar")

            elif opcion2 == "No": # no hace elimina la fecha
                
                print("Operacion cancelada")

                input("Presione enter para continuar")

            else: # en caso de que ingrese mal la opción

                print("Favor de ingresar si/no por favor")
                
                input("Presione enter para continuar")
    
        else: #en caso de no encontrar el codigo de la cita
            print("No se encontró la cita con el código especificado.")

            input("Presione enter para continuar")

            conexion.cerrar_conexion()
        
        
    def __str__(self): # metodo de string para impresion de sus variables
        return f"Recepcionista:\nCodRep: {self.codRep}\nCodTra: {self.codTra}"

    
    
def menu_recepcionista(recepcionista,codigo_trabajador,nombre_trabajador): # menu recepcionista, que recibe el objeto recepcionista, variable codigo trabajador y el nombre del trabajador
    global fecha_actual # la fecha queda como variable global
    
    while True:

        os.system("cls")
        print(f"""
            =======================================================
                        Menú Recepcionista                           
            \tNombre del Recepcionista:{nombre_trabajador}      
            \tCódigo del Recepcionista:{recepcionista.codRep}   
            \tCódigo trabajador:{codigo_trabajador}             

                Hora: {hora_actual}\tFecha: {fecha_actual}        
            =======================================================
            1 - Revisar datos de un paciente
            2 - Revisar citas de un paciente
            3 - Cambiar password
            4 - Volver al menu principal
            """
            )

        opcion_recep = input("Ingrese la opción deseada: ") # ingreso de 

        if opcion_recep == "1": # menu para funciones paciente
            os.system("cls")
            print(
                    """
            ====================================
                    Menú Pacientes
            ====================================
            1 - Buscar paciente
            2 - volver al menú recepcionista
            """
                )

            op_pte = input("ingrese opción deseada: ") # el usuario debe ingresar opcion

            if op_pte == "1":# buscar paciente 

                os.system("cls")
                print("-----------------------------------")
                print("Módulo de pacientes:")
                print("-----------------------------------")

                rut_P = input("Ingrese el Rut del paciente, utilice solo números y sin guion: ") # el usuario debe ingresar el rut del paciente sin numero ni guion

                while not rut_P.isdigit() or "-" in rut_P:
                    print("Error: el RUT debe contener solo números y sin guion.")
                    rut_P = input("Ingrese nuevamente el RUT del paciente, utilice solo números y sin guion: ")

                ficha_paciente=buscar_paciente(rut_P) # se ejecuta la funcion con la variable previamente ingresada y validada

                if ficha_paciente : # imprime los datos del paciente
                    os.system('cls')
                    print("-----------------------------------")
                    print("Módulo de pacientes:")
                    print("-----------------------------------")
                    print("Ingresando a datos del paciente")
                    input("Presione enter para continuar")
                    os.system('cls')
                    print("-----------------------------------")
                    print("Modulo de pacientes:")
                    print("Datos del paciente:")
                    print("-----------------------------------")
                    for fila in ficha_paciente: # imprime los datos del paciente a traves de un ciclo for
                        print("Rut del paciente:", fila[0])
                        print("Nombre del paciente:", fila[1])
                        print("Domicilio:", fila [2])
                        print("Comuna:", fila[3])
                        print("Teléfono:", fila[4])
                        print("Email:", fila[5])
                        print("-----------------------------------")

                        op2=input("¿Desea modificar los datos del paciente ?(si/no)").capitalize() # consulta de si o no para ver si se modifican los datos del paciente

                        if op2 == "Si" : # al contestar si , da a inicio la funcion de menu editar con el rut del paciente previamente obtenido
                            os.system("cls")
                            recepcionista.editar_paciente(rut_P)

                        elif op2 =="No": # se devuelve al menu principal
                            print("Volviendo al menu prinicpal") 
                            input("Presione enter para continuar")
                        else: # en caso de responder incorrectamente a las opciónes previamente dadas 
                            print("Ingrese una opción valida")
                            input("Presione enter para continuar")
                else:
                    op1=input("No se encontró la ficha del paciente,desea crear un nuevo paciente (si/no)").capitalize() # si el paciente no esta en base de datos, se le preguntara si desea crearlo
                    
                    if op1 == "Si": # en caso de que responda que si, 
                        os.system('cls')
                        print("-----------------------------------")
                        print("Módulo de pacientes:")
                        print("-----------------------------------")
                        print("Ingresando a módulo de ingreso de paciente")
                        input("Presione enter para continuar")
                        os.system('cls')
                        print("-----------------------------------")
                        print("Módulo de pacientes:")
                        print("-----------------------------------")
                        
                        recepcionista.agregar_paciente(rut_P)
                    
            
                    elif op1 == "No": # si el usuario responde que no ,volvera al menu principal

                        print("Saliendo del menú Pacientes... presione enter para volver al menú principal")

                        input("Presione enter para continuar")
                        

                    else: # si responde una opción incorrecta

                        print("Ingrese una opción valida (si/no)")

                        input("Presione enter para continuar")

            elif op_pte == "2": # saldra del menú

                input("Saliendo del menú Pacientes... presione enter para volver al menú principal")
                

            else:
                print("Opción inválida. Por favor, ingrese una opción válida.")

                input("Presione enter para continuar")

        elif opcion_recep == "2": # menu para revisar las citas de un paciente
            os.system("cls")
            print("-----------------------------------")
            print("    Revisar citas de un paciente  ")
            print("-----------------------------------")

            rut_P = input("Ingrese el rut del paciente.(solo números y sin guion.): ")

            while not rut_P.isdigit() or "-" in rut_P: 

                print("Error: el RUT debe contener solo números y sin guion.")

                rut_P = input("Ingrese nuevamente el RUT del paciente, utilice solo números y sin guion: ")

            rut_P=int(rut_P)

            resultado_citas = recepcionista.obtener_citas(rut_P) # al ingresar bien el rut, activara la funcion obtener citas.

            if resultado_citas:

                fecha_actual = datetime.now().date()  # Obtener la fecha actual

                citas_activas = []  # Lista para almacenar las citas activas

                for fila in resultado_citas: # ajustara cada resultado en una fila
                    rut_P, codCit, codBox, nomTc, nombre_T, nombre_T2, hora, fecha = fila

                    if fecha >= fecha_actual: # si la fecha de la cita supera a la fecha actual, la agregara a una lista llamada cita activas 

                        citas_activas.append(fila) #almacena todos los resultados en citas_activas

                if citas_activas:  # si tiene citas agendadas imprimira todos los datos de las citas

                    for fila in citas_activas: # en un ciclo for imprimira los datos encontrados y se vera el menu 

                        rut_P, codCit, codBox, nomTc, nombre_T, nombre_T2, hora, fecha = fila
                        print(f"RUT del paciente: {rut_P}")
                        print(f"Código de cita: {codCit}")
                        print(f"Código de box: {codBox}")
                        print(f"Tipo de cita: {nomTc}")
                        print(f"Nombre del médico: {nombre_T}")
                        print(f"Nombre de la recepcionista: {nombre_T2}")
                        print(f"Hora: {str(hora)}")
                        print(f"Fecha: {fecha}")
                        print("\n")
                    input("Presione enter para continuar")

                    print("\n")


                    print("""
                    ====================================
                            Menú Agendar horas
                    ====================================
                    1 - Agregar hora
                    2 - Eliminar hora
                    3 - Salir del menu
                    """)

                    opcion=input("Elija la opción que desea realizar: ") # el usuario debe elgir opcion

                    while not opcion.isdigit(): # valida si es numero 

                        print("la opcion elegida no es valida. Por favor, ingrese un número.")

                        opcion = input("Elija la opción que desea realizar: ")

                    opcion = int(opcion) # convierte la opcion en numero
                    
                    if opcion == 1: # ingresa a menu de agenda

                        os.system("cls")
                    
                        recepcionista.crear_cita(rut_P,recepcionista.codRep) # llama a la funcion de crear cita

                    elif opcion == 2:
                        os.system("cls")

                        recepcionista.eliminar_cita(rut_P,recepcionista.codRep)  # llama a la funcion de eliminar cita
                    
             
                    elif opcion == 3 :  # sale del menu
                        os.system("cls")

                        print("Saliendo del menu...")

                        input("Presione enter para continuar")

                        break

                    else:
                        

                        ("Ingrese una opción valida")

                        input("Presione enter para continuar")

                        os.system("cls")


                    
                else: # en caso de que no se encuentre citas activas del paciente.


                    print("No se encontraron citas activas para el paciente.")

                    print("""
                    ====================================
                            Menú Agendar horas
                    ====================================
                    1 - Agregar hora
                    2 - Eliminar hora
                    3 - Salir del menu
                    """)

                    opcion=input("Elija la opción que desea realizar: ")  # el usuario debe ingresar la opción que desea 

                    while not opcion.isdigit(): # validacion de la opcion 

                        print("Entrada inválida. Por favor, ingrese un número.")

                        opcion = input("Elija la opción que desea realizar: ")

                    opcion=int(opcion)

                    if opcion == 1: # ingresa al menu de agregar hora
                        os.system("cls")
                        recepcionista.crear_cita(rut_P,recepcionista.codRep) # llama a la opción de crear cita

                    elif opcion == 2: # ingresa al menu de eliminar hora
                        os.system("cls")

                        recepcionista.eliminar_cita(rut_P,recepcionista.codRep)
                    
 
                    elif opcion == 3 : # elije salir del menu

                        print("Saliendo del menu...")

                        input("Presione enter para continuar")

                        break

                    else: # en caso de que la opcion sea incorrecta

                        ("Ingrese una opción valida")

                        input("Presione enter para continuar")

            else: # no se encuentra el paciente en la base de datos
                print("No se encontraron citas para el paciente, el paciente no existe en la base de datos")
                input("Presione enter para continuar")
        elif opcion_recep == "3":
            os.system("cls")
            print("=====================")
            print(" Cambio de password  ")
            print("=====================")
            print("\n")
            cambiar_password(recepcionista.codTra)
            
        elif opcion_recep == "4" :
            print("ha cerrado sesion")
            input("Presione enter para continuar")
            break
        else: # en caso de que la opcion no sea la correcta

            print("Opción inválida, ingrese una opción válida por favor,")

            input("Presione enter para continuar")

