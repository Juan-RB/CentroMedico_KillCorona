import os
from conexion import *
import re
from datetime import datetime

hora_actual = datetime.now().strftime("%H:%M")
fecha_actual = datetime.now().strftime("%d - %m - %Y")

class Administrador:
    def __init__(self, codU, codTra):
        self.codU = codU
        self.codTra = codTra

    def modificar_funcion_med():
        conexion = ConexionBD()
        os.system("cls")
        consulta_tc = '''
                        SELECT med.codPm, tr.nombre_T from medico med 
                        inner join trabajador tr on med.codTra= tr.codTra
        ''' # Muestra todos los médicos para que el usuario elija el codigo del médico que desea modificar
        resultado_tc = conexion.ejecutar_consulta(consulta_tc)

        print("MÉDICOS: ")
        print("-----------------------------------------------------------------")
        for fila in resultado_tc:
            print("Código del médico:", fila[0])
            print("Nombre:", fila[1])
            print("-----------------------------------------------------------------")

        codPm = input("Ingrese el código del médico al que desea modificar su función: ").upper()
        consulta_tc = "SELECT * FROM medico WHERE codPm = %s"  # Verifica si el codPm existe en la base de datos
        valores_tc = (codPm,)
        resultado_tc = conexion.ejecutar_consulta(consulta_tc, valores_tc)

        if len(resultado_tc) == 0:
            os.system('cls')
            print("Error: El código del médico no existe.")
            input("Presione ENTER para continuar")
            return

        funcion = input("Ingrese la nueva función del médico (sin tildes): ").upper()
        while not re.match(r'^[a-zA-Z\s]+$',funcion): 
            os.system('cls')
            print("Error: La función debe contener solo letras.")
            input("Presione ENTER para volver a intentar.")
            print("-----------------------------------------------------------------")
            funcion = input("Ingrese nuevamente la función: ").upper()
            os.system('cls')

        while True:
            confirmacion = input("¿Está seguro que desea modificar los datos? (s/n): ")
            if confirmacion.lower() not in ['s', 'n']:
                os.system('cls')
                print("Opción inválida. Por favor, ingrese 's' para confirmar o 'n' para cancelar.")
                input("Presione ENTER para continuar.")
            elif confirmacion == "s":
                valores = (funcion,codPm,)
                consulta = "UPDATE medico SET funcion = %s WHERE codPm = %s"
                conexion.ejecutar_consulta(consulta, valores)
                
                os.system("cls")
                print("Los datos han sido modificados exitosamente.")
                input("Presione ENTER para continuar.")
                break
            else: 
                os.system("cls")
                print("No se han modificado los datos.")
                input("Presione ENTER para continuar.")
                break
        conexion.cerrar_conexion()                      # Cerrar la conexión

    def obtener_disponibilidad_medicos():
        conexion = ConexionBD()
        os.system("cls")
        consulta_tc = '''
                        SELECT med.codPm, tr.nombre_T from medico med 
                        inner join trabajador tr on med.codTra= tr.codTra
        ''' # Muestra todos los médicos para que el usuario elija el codigo del médico que desea modificar
        resultado_tc = conexion.ejecutar_consulta(consulta_tc)

        print("MÉDICOS: ")
        print("-----------------------------------------------------------------")
        for fila in resultado_tc:
            print("Código del médico:", fila[0])
            print("Nombre:", fila[1])
            print("-----------------------------------------------------------------")
        
        codPm = input("Ingrese el código del médico que desea ver su disponibilidad: ")
        consulta = "SELECT tu.codPm, dia_T, hora_iT, hora_fT, funcion, nombre_T, nombre FROM turnos tu INNER JOIN medico med ON tu.codPm = med.codPm INNER JOIN trabajador tr ON med.codTra = tr.codTra INNER JOIN tipo_especialidad te ON med.codPm = te.codPm INNER JOIN especialidad esp ON te.codEsp = esp.codEsp WHERE tu.codPm = %s"
        valores = (codPm,)
        resultado = conexion.ejecutar_consulta(consulta,valores)

        if len(resultado_tc) == 0:
            os.system('cls')
            print("Error: El código del médico no existe.")
            input("Presione ENTER para continuar")
            return
        
        if resultado:
            os.system('cls')
            print("Disponibilidad del médico:")
            print("-----------------------------------")
            for fila in resultado:
                print("Código del médico:", fila[0])
                print("Día:", fila[1])
                print("Hora inicio:", fila[2])
                print("Hora término:", fila[3])
                print("Función:", fila[4])
                print("Nombre médico:", fila[5])
                print("Especialidad:", fila[6])
                print("-----------------------------------")
            input("Presione ENTER para volver al menú")
        else:
            print("No se encontró el horario de este médico.")
            input("Presione ENTER para volver al menú")

        conexion.cerrar_conexion()                      # Cerrar la conexión
    
        
    def agregar_especialidad():
        conexion = ConexionBD()  # Crear una instancia de la clase ConexionBD
        os.system('cls')
        consulta_tc = '''
                        SELECT med.codPm, tr.nombre_T from medico med 
                        inner join trabajador tr on med.codTra= tr.codTra
        ''' # Muestra todos los médicos para que el usuario elija el codigo del médico que desea modificar
        resultado_tc = conexion.ejecutar_consulta(consulta_tc)

        print("MÉDICOS: ")
        print("-----------------------------------------------------------------")
        for fila in resultado_tc:
            print("Código del médico:", fila[0])
            print("Nombre:", fila[1])
            print("-----------------------------------------------------------------")

        codPm = input("Ingrese el código del médico al que desea añadir la especialidad: ")

        consulta_medico = "SELECT * FROM medico WHERE codPm = %s" # Verifica si el médico existe en la base de datos
        valores_medico = (codPm,)
        resultado_medico = conexion.ejecutar_consulta(consulta_medico, valores_medico)

        if len(resultado_medico) == 0:
            os.system('cls')
            print("Error: Código de médico no válido.")
            input("Presione ENTER para continuar")
            return
        
        consulta_espe = "SELECT * FROM especialidad" # Verifica si el médico existe en la base de datos
        resultado_espe = conexion.ejecutar_consulta(consulta_espe)

        print ("ESPECIALIDADES")
        print ("---------------------------")
        for fila in resultado_espe:
            print ("Código de la especialidad: ", fila[0])
            print ("Nombre de la especialidad: ", fila[1])
            print ("---------------------------")


        codEsp = input("Ingrese el código de especialidad que desea agregar al médico: ")

        consulta_esp = "SELECT * FROM especialidad WHERE codEsp = %s" # Verifica si la especialidad existe en la base de datos
        valores_esp = (codEsp,)
        resultado_esp = conexion.ejecutar_consulta(consulta_esp, valores_esp)

        if len(resultado_esp) == 0:
            os.system('cls')
            print("Error: Código de especialidad no válido.")
            input("Presione ENTER para continuar")
            return

        consulta_asignacion = "SELECT * FROM tipo_especialidad WHERE codPm = %s AND codEsp = %s" # Verifica si la especialidad ya está asignada al médico
        valores_asignacion = (codPm, codEsp)
        resultado_asignacion = conexion.ejecutar_consulta(consulta_asignacion, valores_asignacion)

        if len(resultado_asignacion) > 0:
            os.system('cls')
            print("La especialidad ya está asignada al médico.")
            input("Presione ENTER para continuar")
            return

        consulta_insertar = "INSERT INTO tipo_especialidad (codEsp, codPm) VALUES (%s, %s)" # Agregar la especialidad al médico
        valores_insertar = (codEsp, codPm)
        conexion.ejecutar_actualizacion(consulta_insertar, valores_insertar)

        os.system('cls')
        print("La especialidad se ha agregado correctamente.")
        input("Presione ENTER para continuar")

        conexion.cerrar_conexion()  
 

    def actualizar_nombre_med():
        conexion = ConexionBD()
        os.system('cls')
        consulta_tc = '''
                        SELECT med.codPm, tr.nombre_T from medico med 
                        inner join trabajador tr on med.codTra= tr.codTra
        ''' # Muestra todos los médicos para que el usuario elija el codigo del médico que desea modificar
        resultado_tc = conexion.ejecutar_consulta(consulta_tc)

        print("MÉDICOS: ")
        print("-----------------------------------------------------------------")
        for fila in resultado_tc:
            print("Código del médico:", fila[0])
            print("Nombre:", fila[1])
            print("-----------------------------------------------------------------")

        codPm = input("Ingrese el código del médico al que desea actualizar su nombre (sin tildes): ")
        consulta_medico = "SELECT * FROM medico WHERE codPm = %s"  # Verifica si el médico existe en la base de datos
        valores_medico = (codPm,)
        resultado_medico = conexion.ejecutar_consulta(consulta_medico, valores_medico)

        if len(resultado_medico) == 0:
            os.system('cls')
            print("Error: Código de médico no válido.")
            input("Presione ENTER para continuar")
            return

        nombre_T = input("Ingrese el nuevo nombre para el médico (sin tildes):  ").upper()

        if re.match(r'^[a-zA-Z\s]+$', nombre_T):
            os.system('cls')
            print("¿Está seguro de guardar los cambios? (S/N)")
            opcion = input("> ")

            if opcion.upper() == "S":
                consulta_nombre = "UPDATE trabajador AS t JOIN medico AS m ON t.codTra = m.codTra SET t.nombre_T = %s WHERE m.codPm = %s"
                valores_nombre = (nombre_T, codPm)
                conexion.ejecutar_consulta(consulta_nombre, valores_nombre)

                print("La actualización se ha guardado correctamente.")
                input("Presione ENTER para continuar")
            else:
                print("Se canceló la actualización.")
                input("Presione ENTER para continuar")
        else:
            os.system("cls")
            print("El nombre debe contener solo letras y espacios.")
            input("Presione ENTER para continuar")

        conexion.cerrar_conexion()                      # Cerrar la conexión
        
    def actualizar_direccion_med():
        conexion = ConexionBD()
        os.system("cls")
        consulta_tc = '''
                        SELECT med.codPm, tr.nombre_T from medico med 
                        inner join trabajador tr on med.codTra= tr.codTra
        ''' # Muestra todos los médicos para que el usuario elija el codigo del médico que desea modificar
        resultado_tc = conexion.ejecutar_consulta(consulta_tc)

        print("MÉDICOS: ")
        print("-----------------------------------------------------------------")
        for fila in resultado_tc:
            print("Código del médico:", fila[0])
            print("Nombre:", fila[1])
            print("-----------------------------------------------------------------")
        codPm = input("Ingrese el código del médico al que desea actualizar su dirección: ")
        consulta_medico = "SELECT * FROM medico WHERE codPm = %s"  # Verifica si el médico existe en la base de datos
        valores_medico = (codPm,)
        resultado_medico = conexion.ejecutar_consulta(consulta_medico, valores_medico)

        if len(resultado_medico) == 0:
            os.system('cls')
            print("Error: Código de médico no válido.")
            input("Presione ENTER para continuar")
            return

        dir_T = input("Ingrese la nueva dirección del médico: ").upper()

        if not dir_T.strip():
            os.system('cls')
            print("La dirección no puede quedar vacía. Intente nuevamente")
            input("Presione ENTER para continuar")
        else:
            os.system('cls')
            print("¿Está seguro de guardar los cambios? (S/N)")
            opcion = input("> ")

            if opcion.upper() == "S":
                consulta_dir = "UPDATE trabajador AS t JOIN medico AS m ON t.codTra = m.codTra SET t.direccion_T = %s WHERE m.codPm = %s"
                valores_dir = (dir_T, codPm)
                conexion.ejecutar_consulta(consulta_dir, valores_dir)

                print("La actualización se ha guardado correctamente.")
                input("Presione ENTER para continuar")
            else:
                print("Se canceló la actualización.")
                input("Presione ENTER para continuar")

        conexion.cerrar_conexion()                      # Cerrar la conexión

    def actualizar_telefono_med():
        conexion = ConexionBD()
        os.system("cls")
        consulta_tc = '''
                        SELECT med.codPm, tr.nombre_T from medico med 
                        inner join trabajador tr on med.codTra= tr.codTra
        ''' # Muestra todos los médicos para que el usuario elija el codigo del médico que desea modificar
        resultado_tc = conexion.ejecutar_consulta(consulta_tc)

        print("MÉDICOS: ")
        print("-----------------------------------------------------------------")
        for fila in resultado_tc:
            print("Código del médico:", fila[0])
            print("Nombre:", fila[1])
            print("-----------------------------------------------------------------")
        codPm = input("Ingrese el código del médico al que desea actualizar su teléfono: ")
        consulta_medico = "SELECT * FROM medico WHERE codPm = %s"  # Verifica si el médico existe en la base de datos
        valores_medico = (codPm,)
        resultado_medico = conexion.ejecutar_consulta(consulta_medico, valores_medico)

        if len(resultado_medico) == 0:
            os.system('cls')
            print("Error: Código de médico no válido.")
            input("Presione ENTER para continuar")
            return

        tel_T = input("Ingrese el nuevo teléfono para el médico: ")

        try:
            if re.match(r'^\d+$', tel_T):  # VERIFICA QUE EL TELEFONO SOLO TENGA CARACTERES NUMERICOS
                os.system('cls')
                print("¿Está seguro de guardar los cambios? (S/N)")
                opcion = input("> ")

                if opcion.upper() == "S":
                    consulta_tel = "UPDATE trabajador AS t JOIN medico AS m ON t.codTra = m.codTra SET t.telefono_T = %s WHERE m.codPm = %s"
                    valores_tel = (tel_T, codPm)
                    conexion.ejecutar_consulta(consulta_tel, valores_tel)

                    print("La actualización se ha guardado correctamente.")
                    input("Presione ENTER para continuar")
                else:
                    print("Se canceló la actualización.")
                    input("Presione ENTER para continuar")
            else:  # EN CASO DE TENER LETRAS, LANZA ESTE MENSAJE DE ERROR.
                os.system("cls")
                print("El teléfono debe contener solo números.")
                input("Presione ENTER para continuar")

        except Exception as e:
            print("Error", e)
            input("Presione ENTER para continuar")

        conexion.cerrar_conexion()                      # Cerrar la conexión
 

    def actualizar_email_med():
        conexion = ConexionBD()
        os.system("cls")
        consulta_tc = '''
                        SELECT med.codPm, tr.nombre_T from medico med 
                        inner join trabajador tr on med.codTra= tr.codTra
        ''' # Muestra todos los médicos para que el usuario elija el codigo del médico que desea modificar
        resultado_tc = conexion.ejecutar_consulta(consulta_tc)

        print("MÉDICOS: ")
        print("-----------------------------------------------------------------")
        for fila in resultado_tc:
            print("Código del médico:", fila[0])
            print("Nombre:", fila[1])
            print("-----------------------------------------------------------------")
        codPm = input("Ingrese el código del médico al que desea actualizar su email: ")
        consulta_medico = "SELECT * FROM medico WHERE codPm = %s"  # Verifica si el médico existe en la base de datos
        valores_medico = (codPm,)
        resultado_medico = conexion.ejecutar_consulta(consulta_medico, valores_medico)

        if len(resultado_medico) == 0:
            os.system('cls')
            print("Error: Código de médico no válido.")
            input("Presione ENTER para continuar")
            return

        email_T = input("Ingrese el nuevo email para el médico: ").lower()

        try:
            if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email_T):  # VERIFICA QUE EL EMAIL TENGA UN FORMATO VÁLIDO
                os.system('cls')
                print("¿Está seguro de guardar los cambios? (S/N)")
                opcion = input("> ")

                if opcion.upper() == "S":
                    consulta_email = "UPDATE trabajador AS t JOIN medico AS m ON t.codTra = m.codTra SET t.email_T = %s WHERE m.codPm = %s"
                    valores_email = (email_T, codPm)
                    conexion.ejecutar_consulta(consulta_email, valores_email)

                    print("La actualización se ha guardado correctamente.")
                    input("Presione ENTER para continuar")
                else:
                    print("Se canceló la actualización.")
                    input("Presione ENTER para continuar")
            else:  # EN CASO DE TENER UN FORMATO INVÁLIDO, LANZA ESTE MENSAJE DE ERROR.
                os.system("cls")
                print("El email ingresado contiene un formato inválido. Intente nuevamente")
                input("Presione ENTER para continuar")

        except Exception as e:
            print("Error", e)
            input("Presione ENTER para continuar")

        conexion.cerrar_conexion()                      # Cerrar la conexión

    def listar_planilla_tr():
        conexion = ConexionBD()
        os.system('cls')
        print("Ingresando a planilla de trabajadores...")
        input("Presione ENTER para continuar")
        os.system('cls')
        consulta_planilla = "SELECT tr.codTra, pr.nombre_Perfil, tr.rut_T, tr.nombre_T, tr.direccion_T, tr.telefono_T, tr.email_T FROM trabajador tr inner join usuario us on tr.codTra = us.codTra inner join perfil pr on us.codPer = pr.codPer WHERE pr.codPer < 5" 
        resultado_planilla = conexion.ejecutar_consulta(consulta_planilla)

        if len(resultado_planilla) > 0:
            return resultado_planilla
        else:
            conexion.cerrar_conexion()                      # Cerrar la conexión
            return None
        
        
    def despedir_tr(codTra):
        conexion = ConexionBD()
        os.system("cls")
        
        consulta_trabajador = "SELECT * FROM USUARIO WHERE codTra = %s and codPer < 5"  # Valida que el usuario este activo y tenga un perfil anterioramente.
        # HACER DELETE INDICANDO EL CODTRA DEL RECEPCIONISTA Y LUEGO MOVERLO A LA TABLA DEL MEDICO CON SU CODIGO Y SU FUNCION
        valores_trabajador = (codTra,)
        resultado_trabajador = conexion.ejecutar_consulta(consulta_trabajador, valores_trabajador)

        if len(resultado_trabajador) == 0:
            print("Error: Código de trabajador no válido. Este trabajador no existe o no tiene un perfil activo.")
            input("Presione ENTER para continuar.")
            return
        else:
            respuesta = input("¿Estás seguro de guardar los cambios? (s/n): ").lower()
            if respuesta == 's':
                # Realizar la actualización en la base de datos
                consulta = "UPDATE USUARIO SET codPer = 5 WHERE codTra = %s"
                valores = (codTra)
                conexion.ejecutar_consulta(consulta, valores)
                print("Rol de trabajador cambiado exitosamente. Ahora el trabajador no tendrá acceso al sistema.")
                input("Presione ENTER para continuar.")
            elif respuesta == 'n':
                print("Cambios no guardados.")
                input("Presione ENTER para continuar.")      
            else:
                print("Respuesta inválida. Por favor, ingrese 's' para sí o 'n' para no.")
                input("Presione ENTER para continuar.")

        conexion.cerrar_conexion()                      # Cerrar la conexión


    def actualizar_nombre_tr():
        conexion = ConexionBD()
        os.system('cls')

        codTra = input("Ingrese el código del trabajador al que desea actualizar su nombre: ")
        consulta_medico = "SELECT * FROM trabajador WHERE codTra = %s"  # Verifica si el trabajador existe en la base de datos
        valores_medico = (codTra,)
        resultado_medico = conexion.ejecutar_consulta(consulta_medico, valores_medico)

        if len(resultado_medico) == 0:
            os.system('cls')
            print("Error: Código de trabajador no válido.")
            input("Presione ENTER para continuar")
            return

        nombre_T = input("Ingrese el nuevo nombre para el trabajador: ").upper()

        try:
            if re.match(r'^[a-zA-Z\s]+$', nombre_T):  # VERIFICA QUE EL NOMBRE SOLAMENTE TENGA CARACTERES DE TEXTO
                os.system('cls')
                print("¿Está seguro de guardar los cambios? (S/N)")
                opcion = input("> ")

                if opcion.upper() == "S":
                    consulta_nombre = "UPDATE trabajador SET nombre_T = %s WHERE codTra = %s"
                    valores_nombre = (nombre_T, codTra)
                    conexion.ejecutar_consulta(consulta_nombre, valores_nombre)

                    print("La actualización se ha guardado correctamente.")
                    input("Presione ENTER para continuar")
                else:
                    print("Se canceló la actualización.")
                    input("Presione ENTER para continuar")
            else:  # EN CASO DE TENER NUMEROS, LANZA ESTE MENSAJE DE ERROR.
                os.system("cls")
                print("El nombre debe contener solo letras y espacios.")
                input("Presione ENTER para continuar")

        except Exception as e:
            print("Error", e)
            input("Presione ENTER para continuar")

        conexion.cerrar_conexion()                      # Cerrar la conexión

        
        
    def actualizar_direccion_tr():
        conexion = ConexionBD()
        os.system("cls")
        codTra = input("Ingrese el código del trabajador al que desea actualizar su dirección: ")
        consulta_trabajador = "SELECT * FROM trabajador WHERE codTra = %s"  # Verifica si el trabajador existe en la base de datos
        valores_trabajador = (codTra,)
        resultado_trabajador = conexion.ejecutar_consulta(consulta_trabajador, valores_trabajador)

        if len(resultado_trabajador) == 0:
            os.system('cls')
            print("Error: Código de trabajador no válido.")
            input("Presione ENTER para continuar")
            return

        dir_T = input("Ingrese la nueva dirección del trabajador: ").upper()

        if not dir_T.strip():
            print("La dirección no puede quedar vacía. Intente nuevamente")
            input("Presione ENTER para continuar")
        else:
            os.system('cls')
            print("¿Está seguro de guardar los cambios? (S/N)")
            opcion = input("> ")

            if opcion.upper() == "S":
                consulta_dir = "UPDATE trabajador SET direccion_T = %s WHERE codTra = %s"
                valores_dir = (dir_T, codTra)
                conexion.ejecutar_consulta(consulta_dir, valores_dir)
                print("La actualización se ha guardado correctamente.")
                input("Presione ENTER para continuar")
            else:
                print("Se canceló la actualización.")
                input("Presione ENTER para continuar")

        conexion.cerrar_conexion()                      # Cerrar la conexión

    def actualizar_telefono_tr():
        conexion = ConexionBD()
        os.system("cls")
        codTra = input("Ingrese el código del trabajador al que desea actualizar su teléfono: ")
        consulta_trabajador = "SELECT * FROM trabajador WHERE codTra = %s"  # Verifica si el trabajador existe en la base de datos
        valores_trabajador = (codTra,)
        resultado_trabajador = conexion.ejecutar_consulta(consulta_trabajador, valores_trabajador)

        if len(resultado_trabajador) == 0:
            os.system('cls')
            print("Error: Código de trabajador no válido.")
            input("Presione ENTER para continuar")
            return

        tel_T = input("Ingrese el nuevo teléfono para el trabajador: ")

        if re.match(r'^\d+$', tel_T):
            os.system('cls')
            print("¿Está seguro de guardar los cambios? (S/N)")
            opcion = input("> ")

            if opcion.upper() == "S":
                consulta_tel = "UPDATE trabajador SET telefono_T = %s WHERE codTra = %s"
                valores_tel = (tel_T, codTra)
                conexion.ejecutar_consulta(consulta_tel, valores_tel)
                print("La actualización se ha guardado correctamente.")
                input("Presione ENTER para continuar")
            else:
                print("Se canceló la actualización.")
                input("Presione ENTER para continuar")
        else:
            os.system("cls")
            print("El teléfono debe contener solo números.")
            input("Presione ENTER para continuar")

        conexion.cerrar_conexion()                      # Cerrar la conexión


    def actualizar_email_tr():
        conexion = ConexionBD()
        os.system("cls")
        codTra = input("Ingrese el código del trabajador al que desea actualizar su email: ")
        consulta_trabajador = "SELECT * FROM trabajador WHERE codTra = %s"  # Verifica si el trabajador existe en la base de datos
        valores_trabajador = (codTra,)
        resultado_trabajador = conexion.ejecutar_consulta(consulta_trabajador, valores_trabajador)

        if len(resultado_trabajador) == 0:
            os.system('cls')
            print("Error: Código de trabajador no válido.")
            input("Presione ENTER para continuar")
            return

        email_T = input("Ingrese el nuevo email para el trabajador: ").lower() 

        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email_T):
            os.system('cls')
            print("¿Está seguro de guardar los cambios? (S/N)")
            opcion = input("> ")

            if opcion.upper() == "S":
                consulta_email = "UPDATE trabajador SET email_T = %s WHERE codTra = %s"
                valores_email = (email_T, codTra)
                conexion.ejecutar_consulta(consulta_email, valores_email)
                print("La actualización se ha guardado correctamente.")
                input("Presione ENTER para continuar")
            else:
                print("Se canceló la actualización.")
                input("Presione ENTER para continuar")
        else:
            os.system("cls")
            print("El email ingresado contiene un formato inválido. Intente nuevamente.")
            input("Presione ENTER para continuar")

        conexion.cerrar_conexion()                      # Cerrar la conexión

    def ingresar_tr():
        conexion = ConexionBD()  # Crear una instancia de la clase ConexionBD
        os.system('cls')

        rut_tr = input("Ingrese el rut del trabajador que desea agregar: ").upper()
        
        while not rut_tr.isdigit():
            os.system('cls')
            print("Error: El rut debe contener solo números.")
            input("Presione ENTER para continuar.")
            print("-----------------------------------------------------------------")
            rut_tr = input("Ingrese nuevamente el rut del trabajador que desea agregar: ").upper()
            os.system('cls')

        nombre_tr = input("Ingrese el nombre (sin tildes): ").upper()

        while not re.match(r'^[a-zA-Z\s]+$',nombre_tr):
            os.system('cls')
            print("Error: El nombre debe contener solo letras.")
            input("Presione ENTER para continuar.")
            print("-----------------------------------------------------------------")
            nombre_tr = input("Ingrese nuevamente el nombre (sin tildes): ").upper()
            os.system('cls')

        direccion_tr = input("Ingrese la dirección: ").upper()
        while not direccion_tr.strip(): # Verificar que las variable dirección no este vacia.
                os.system('cls')
                print("Error: La dirección no puede estar vacía.")
                input("Presione ENTER para continuar.")
                print("-----------------------------------------------------------------")
                direccion_tr = input("Ingrese nuevamente la dirección: ").upper()
                os.system('cls')

        telefono_tr = input("Ingrese el teléfono: ")
        while not telefono_tr.isdigit():
            os.system('cls')
            print("Error: El teléfono debe contener solo números.")
            input("Presione ENTER para continuar.")
            print("-----------------------------------------------------------------")
            telefono_tr = input("Ingrese nuevamente el teléfono del trabajador: ").upper()
            os.system('cls')

        email_tr = input("Ingrese el email ( con @ ): ").lower()
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$' #Validacion para formato de email 
        while not re.match(pattern, email_tr):
            os.system('cls')
            print("Error: El email ingresado no tiene un formato válido, le falta @")
            input("Presione ENTER para continuar.")
            print("-----------------------------------------------------------------")
            email_tr = input("Ingrese nuevamente el email: ").lower()
            os.system('cls')

        os.system('cls')
        print("Los datos ingresados son los siguientes:")
        print("Rut:", rut_tr)
        print("Nombre:", nombre_tr)
        print("Dirección:", direccion_tr)
        print("Teléfono:", telefono_tr)
        print("Email:", email_tr)
        print("-----------------------------------")

        respuesta = input("¿Está seguro de guardar estos datos? (s/n): ")
        while respuesta.lower() not in ['s', 'n']:
            os.system('cls')
            print("Error: Respuesta inválida. Por favor, ingrese 's' para sí o 'n' para no.")
            input("Presione ENTER para continuar.")
            respuesta = input("¿Está seguro de guardar estos datos? (s/n): ")
            

        if respuesta.lower() == 's':
            # Realizar la operación de guardado en la base de datos o realizar cualquier acción necesaria
            print("Los datos han sido guardados correctamente.")
        else:
            print("Los datos no han sido guardados.")
            input("Presione ENTER para continuar.")
            os.system('cls')
            return
    
            
           
           
        consulta_tr = "INSERT INTO TRABAJADOR (rut_t, nombre_t, direccion_t, telefono_t, email_t) VALUES (%s, %s, %s, %s, %s)" # Verifica si el médico existe en la base de datos
        valores_tr = (rut_tr, nombre_tr, direccion_tr,telefono_tr,email_tr)
        conexion.ejecutar_actualizacion(consulta_tr, valores_tr)

        consulta_codtra = '''
                            SELECT *
                            FROM trabajador
                            WHERE codTra = (SELECT MAX(codTra) FROM trabajador);
         ''' # Muestra todos los datos del trabajador recien ingresado
        resultado_codtra = conexion.ejecutar_consulta(consulta_codtra)
        os.system("cls")
        for fila in resultado_codtra: #HACER UN SELECT QUE ME MUESTRE EL ULTIMO CODIGO DE TRABAJADOR, OSEA EL MAYOR.
            print("Código del trabajador:", fila[0])
            print("Rut:", fila[1])
            print("Nombre:", fila [2])
            print("Dirección:", fila[3])
            print("Teléfono:", fila[4])
            print("Email:", fila[5])
            print("-----------------------------------")
        print("El trabajador se ha ingresado correctamente a la planilla de trabajadores.")
        input("Presione ENTER para continuar...")
        
        os.system("cls")
        opcion_valida = False
        while not opcion_valida:
            print("-----------------------------------------")
            print("Menú ingreso de trabajador")
            print("Código del trabajador:", fila[0])
            print('''
                    1- Ingresar trabajador a medicos
                    2- Ingresar trabajador a recepcionistas
                    3- Ingresar trabajador a farmaceuticos
                ''')
            print("-----------------------------------------")
            respuesta = input("Ingrese su opción ")
            
            if respuesta == "1": #Opcion ingreso médicos
                conexion = ConexionBD()
                funcion = input("Ingrese la función que tendrá el médico: ")
                valores = (fila[0],funcion)
                consulta = "INSERT INTO MEDICO (codTra,funcion) VALUES (%s, %s)"
                conexion.ejecutar_consulta(consulta, valores)

                consulta_med = '''
                                SELECT *
                                FROM medico
                                WHERE codTra = (SELECT MAX(codTra) FROM trabajador);
                ''' 
                resultado_med = conexion.ejecutar_consulta(consulta_med)

                for fila in resultado_med: # Muestra todos los datos del médico recien ingresado
                    os.system("cls")
                    print("Código del médico: ", fila[0])
                    print("Código del trabajador: ", fila[1])
                    print("Función del médico: ", fila[2])

                print("Rol asignado exitosamente.")    
                input("Presione ENTER para continuar.")    

                codTra = fila[1]
                codU = rut_tr 
                codPer = 2 #codigo perfil médico
                os.system("cls")
                password = input("Ingrese el password para el trabajador: ")

                valores = (codU, codTra, codPer, password)
                consulta = "INSERT INTO USUARIO (codU, codTra, codPer, pass) VALUES (%s, %s, %s, %s)"
                conexion.ejecutar_consulta(consulta,valores)

                consulta_u = '''
                                SELECT *
                                FROM usuario
                                WHERE codTra = (SELECT MAX(codTra) FROM trabajador);
                ''' # Muestra todos los datos del trabajador recien ingresado
                resultado_u = conexion.ejecutar_consulta(consulta_u)

                for fila in resultado_u:
                    os.system('cls')
                    print("Código del usuario:", fila[0])
                    print("Código del trabajador:", fila[1])
                    print("Código del perfil", fila[2])
                    print("Password:", fila[3])
                    print("-----------------------------------------------------------------")
                print("Usuario, perfil, y contraseña asignadas exitosamente.")
                print("Recuerde que para añadir una especialidad a un médico debe realizarlo desde el menú de mantenedor de médicos.")
                input("Presione ENTER para continuar.") 

                opcion_valida = True
                
            elif respuesta == "2": #Opcion ingreso recepcionistas
                conexion = ConexionBD()
                valores = (fila[0],)
                consulta = "INSERT INTO RECEPCIONISTA (codTra) VALUES (%s)"
                conexion.ejecutar_consulta(consulta, valores)

                consulta_rep = '''
                                SELECT *
                                FROM recepcionista
                                WHERE codTra = (SELECT MAX(codTra) FROM trabajador);
                ''' # Muestra todos los datos del trabajador recien ingresado
                resultado_rep = conexion.ejecutar_consulta(consulta_rep)

                for fila in resultado_rep:
                    os.system("cls")
                    print("Código del recepcionista:", fila[0])
                    print("Código del trabajador:", fila[1])
                
                print("Rol asignado exitosamente.")    
                input("Presione ENTER para continuar.")    

                codTra = fila[1]
                codU = rut_tr 
                codPer = 3 #codigo perfil recepcionista
                os.system("cls")
                password = input("Ingrese el password para el trabajador: ")

                valores = (codU, codTra, codPer, password)
                consulta = "INSERT INTO USUARIO (codU, codTra, codPer, pass) VALUES (%s, %s, %s, %s)"
                conexion.ejecutar_consulta(consulta,valores)

                consulta_u = '''
                                SELECT *
                                FROM usuario
                                WHERE codTra = (SELECT MAX(codTra) FROM trabajador);
                ''' # Muestra todos los datos del trabajador recien ingresado
                resultado_u = conexion.ejecutar_consulta(consulta_u)

                for fila in resultado_u:
                    os.system('cls')
                    print("Código del usuario:", fila[0])
                    print("Código del trabajador:", fila[1])
                    print("Codigo del perfil", fila[2])
                    print("Password:", fila[3])
                    print("-----------------------------------------------------------------")
                print("Usuario, perfil, y contraseña asignadas exitosamente.")
                print("El trabajador ha sido ingresado completamente al sistema.")
                input("Presione ENTER para continuar.")    
                
                opcion_valida = True
            
            elif respuesta == "3": #Opcion ingreso farmaceuticos
                conexion = ConexionBD()
                valores = (fila[0],)
                consulta = "INSERT INTO FARMACEUTICO (codTra) VALUES (%s)"
                conexion.ejecutar_consulta(consulta, valores)

                consulta_far = '''
                                SELECT *
                                FROM farmaceutico
                                WHERE codTra = (SELECT MAX(codTra) FROM trabajador);
            '''                                                                        
                resultado_far = conexion.ejecutar_consulta(consulta_far)

                for fila in resultado_far:# Muestra el codigo del farmaceutico y trabajador recien ingresado
                    os.system("cls")
                    print("Código del farmaceutico:", fila[0])
                    print("Código del trabajador:", fila[1])
                
                print("Rol asignado exitosamente.")
                input("Presione ENTER para continuar.")    

                codTra = fila[1]
                codU = rut_tr 
                codPer = 4 #codigo perfil farmaceutico
                os.system("cls")
                password = input("Ingrese el password para el trabajador: ")

                valores = (codU, codTra, codPer, password)
                consulta = "INSERT INTO USUARIO (codU, codTra, codPer, pass) VALUES (%s, %s, %s, %s)"
                conexion.ejecutar_consulta(consulta,valores)

                consulta_u = '''
                                SELECT *
                                FROM usuario
                                WHERE codTra = (SELECT MAX(codTra) FROM trabajador);
             ''' # Muestra todos los datos del trabajador recien ingresado
                resultado_u = conexion.ejecutar_consulta(consulta_u)

                for fila in resultado_u:
                    os.system('cls')
                    print("Código del usuario:", fila[0])
                    print("Código del trabajador:", fila[1])
                    print("Código del perfil", fila[2])
                    print("Password:", fila[3])
                    print("-----------------------------------------------------------------")

                print("Usuario, perfil, y contraseña asignadas exitosamente.")
                print("El trabajador ha sido ingresado completamente al sistema.")
                input("Presione ENTER para continuar.")    

                opcion_valida = True

            else:
                os.system("cls")
                print("Ingrese una opción valida por favor.")
                input("Presione ENTER para continuar.")
                os.system("cls")


        conexion.cerrar_conexion()                      # Cerrar la conexión
    
    def listar_tc():
        conexion = ConexionBD()
        os.system("cls")
        
        
        consulta = '''
                        SELECT *
                        FROM tipo_cita;
                       
        ''' # Muestra todos los tipos de cita
        resultado = conexion.ejecutar_consulta(consulta)
        os.system('cls')
        print("Tipos de cita existentes: ")
        print("-----------------------------------------------------------------")
        for fila in resultado:
            print("Código tipo cita:", fila[0])
            print("Nombre:", fila[1])
            print("-----------------------------------------------------------------")

        input("Presione ENTER para volver al menú de administrar tipos de cita.")

        conexion.cerrar_conexion()                      # Cerrar la conexión

    def agregar_tc():
        conexion = ConexionBD()
        os.system("cls")
        nomTc = input("Ingrese el nuevo tipo de cita que desea ingresar (sin tildes): ").upper()
        while not re.match(r'^[a-zA-Z\s]+$',nomTc):
            os.system('cls')
            print("Error: El nombre del tipo de cita debe contener solo letras.")
            input("Presione ENTER para volver a intentar.")
            print("-----------------------------------------------------------------")
            nomTc = input("Ingrese nuevamente el nombre (sin tildes): ").upper()
            os.system('cls')

        while True:
            confirmacion = input("¿Está seguro de agregar los datos? (s/n): ").lower()

            if confirmacion.lower() not in ['s', 'n']:
                os.system('cls')
                print("Opción inválida. Por favor, ingrese 's' para confirmar o 'n' para cancelar.")
                input("Presione ENTER para continuar.")
            elif confirmacion == "s":
                valores = (nomTc,)
                consulta = "INSERT INTO tipo_cita (nomTc) VALUES (%s)"
                conexion.ejecutar_consulta(consulta, valores)
                
                consulta_tc = '''
                                SELECT *
                                FROM tipo_cita
                                WHERE codTc = (SELECT MAX(codTc) FROM tipo_cita);
                ''' # Muestra el tipo de cita recién ingresado
                resultado_tc = conexion.ejecutar_consulta(consulta_tc)
                
                print("Datos agregados: ")
                print("-----------------------------------------------------------------")
                for fila in resultado_tc:
                    print("Código tipo cita:", fila[0])
                    print("Nombre:", fila[1])
                    print("-----------------------------------------------------------------")

                print("Los datos han sido agregados exitosamente.")
                input("Presione ENTER para continuar.")
                break
            else:
                os.system('cls')
                print("No se han guardado los datos.")
                input("Presione ENTER para continuar.")
                break

        conexion.cerrar_conexion()                      # Cerrar la conexión
        
    def actualizar_tc():
        conexion = ConexionBD()
        os.system("cls")
        consulta_tc = '''
                        SELECT *
                        FROM tipo_cita
        ''' # Muestra todos los tipos de cita para que el usuario elija el codigo del tipo de cita que desea modificar
        resultado_tc = conexion.ejecutar_consulta(consulta_tc)

        print("Tipos de cita: ")
        print("-----------------------------------------------------------------")
        for fila in resultado_tc:
            print("Código tipo cita:", fila[0])
            print("Nombre:", fila[1])
            print("-----------------------------------------------------------------")

        codTc = input("Ingrese el código del tipo de cita que desea modificar: ").upper()
        consulta_tc = "SELECT * FROM tipo_cita WHERE codTc = %s"  # Verifica si el codTc existe en la base de datos
        valores_tc = (codTc,)
        resultado_tc = conexion.ejecutar_consulta(consulta_tc, valores_tc)

        if len(resultado_tc) == 0:
            os.system('cls')
            print("Error: El código del tipo de cita no existe.")
            input("Presione ENTER para continuar")
            return

        nomTc = input("Ingrese el nuevo nombre del tipo de cita (sin tildes): ").upper()
        while not re.match(r'^[a-zA-Z\s]+$',nomTc):
            os.system('cls')
            print("Error: El nombre del tipo de cita debe contener solo letras.")
            input("Presione ENTER para volver a intentar.")
            print("-----------------------------------------------------------------")
            nomTc = input("Ingrese nuevamente el nombre (sin tildes): ").upper()
            os.system('cls')

        while True:
            confirmacion = input("¿Está seguro que desea modificar los datos? (s/n): ").lower()
            if confirmacion.lower() not in ['s', 'n']:
                os.system('cls')
                print("Opción inválida. Por favor, ingrese 's' para confirmar o 'n' para cancelar.")
                input("Presione ENTER para continuar.")
            elif confirmacion == "s":
                valores = (nomTc, codTc,)
                consulta = "UPDATE tipo_cita SET nomTc = %s WHERE codTc = %s"
                conexion.ejecutar_consulta(consulta, valores)
                
                os.system("cls")
                print("Los datos han sido modificados exitosamente.")
                input("Presione ENTER para continuar.")
                break
            else: 
                os.system("cls")
                print("No se han modificado los datos.")
                input("Presione ENTER para continuar.")
                break

        conexion.cerrar_conexion()                      # Cerrar la conexión


    def eliminar_tc():
        conexion = ConexionBD()
        os.system("cls")
        consulta_tc = '''
                        SELECT *
                        FROM tipo_cita
        ''' # Muestra todos los tipos de cita para que el usuario elija el codigo del tipo de cita que desea eliminar
        resultado_tc = conexion.ejecutar_consulta(consulta_tc)

        print("Tipos de cita: ")
        print("-----------------------------------------------------------------")
        for fila in resultado_tc:
            print("Código tipo cita:", fila[0])
            print("Nombre:", fila[1])
            print("-----------------------------------------------------------------")

        codTc = input("Ingrese el código del tipo de cita que desea eliminar: ").upper()
        consulta_tc = "SELECT * FROM tipo_cita WHERE codTc = %s"  # Verifica si el codTc existe en la base de datos
        valores_tc = (codTc,)
        resultado_tc = conexion.ejecutar_consulta(consulta_tc, valores_tc)

        if len(resultado_tc) == 0:
            os.system('cls')
            print("Error: El código del tipo de cita no existe.")
            input("Presione ENTER para continuar")
            return

        while True:
            confirmacion = input("¿Está seguro que desea eliminar los datos? (s/n): ").lower()
            if confirmacion.lower() not in ['s', 'n']:
                os.system('cls')
                print("Opción inválida. Por favor, ingrese 's' para confirmar o 'n' para cancelar.")
                input("Presione ENTER para continuar.")
            elif confirmacion == "s" :
                valores = (codTc,)
                consulta = "DELETE FROM tipo_cita WHERE codTc = %s"
                conexion.ejecutar_consulta(consulta, valores)
                os.system("cls")
                print("Los datos han sido eliminados exitosamente.")
                input("Presione ENTER para continuar.")
                break
            else: 
                os.system("cls")
                print("No se han eliminado los datos.")
                input("Presione ENTER para continuar.")
                break

        conexion.cerrar_conexion()                      # Cerrar la conexión

    def modificar_funcion_med():
        conexion = ConexionBD()
        os.system("cls")
        consulta_tc = '''
                        SELECT med.codPm, tr.nombre_T from medico med 
                        inner join trabajador tr on med.codTra= tr.codTra
        ''' # Muestra todos los médicos para que el usuario elija el codigo del médico que desea modificar
        resultado_tc = conexion.ejecutar_consulta(consulta_tc)

        print("MÉDICOS: ")
        print("-----------------------------------------------------------------")
        for fila in resultado_tc:
            print("Código del médico:", fila[0])
            print("Nombre:", fila[1])
            print("-----------------------------------------------------------------")

        codPm = input("Ingrese el código del médico al que desea modificar su función: ").upper()
        consulta_tc = "SELECT * FROM medico WHERE codPm = %s"  # Verifica si el codPm existe en la base de datos
        valores_tc = (codPm,)
        resultado_tc = conexion.ejecutar_consulta(consulta_tc, valores_tc)

        if len(resultado_tc) == 0:
            os.system('cls')
            print("Error: El código del médico no existe.")
            input("Presione ENTER para continuar")
            return

        funcion = input("Ingrese la nueva función del médico (sin tildes): ").upper()
        while not re.match(r'^[a-zA-Z\s]+$',funcion): 
            os.system('cls')
            print("Error: La función debe contener solo letras.")
            input("Presione ENTER para volver a intentar.")
            print("-----------------------------------------------------------------")
            funcion = input("Ingrese nuevamente la función: ").upper()
            os.system('cls')

        while True:
            confirmacion = input("¿Está seguro que desea modificar los datos? (s/n): ").lower()
            if confirmacion.lower() not in ['s', 'n']:
                os.system('cls')
                print("Opción inválida. Por favor, ingrese 's' para confirmar o 'n' para cancelar.")
                input("Presione ENTER para continuar.")
            elif confirmacion == "s":
                valores = (funcion,codPm,)
                consulta = "UPDATE medico SET funcion = %s WHERE codPm = %s"
                conexion.ejecutar_consulta(consulta, valores)
                
                os.system("cls")
                print("Los datos han sido modificados exitosamente.")
                input("Presione ENTER para continuar.")
                break
            else: 
                os.system("cls")
                print("No se han modificado los datos.")
                input("Presione ENTER para continuar.")
                break

        conexion.cerrar_conexion()                      # Cerrar la conexión
    

    def modificar_password():
        conexion = ConexionBD()
        os.system("cls")
        consulta_tc = '''
                        SELECT tr.codTra, tr.nombre_T from trabajador tr 
                        inner join usuario us on tr.codTra = us.codTra WHERE us.codPer < 5;
        ''' # Muestra todos los trabajadores para que el usuario elija el codigo del trabajador que desea modificar.
        resultado_tc = conexion.ejecutar_consulta(consulta_tc)

        print("TRABAJADORES CON PERFIL ACTIVO: ")
        print("-----------------------------------------------------------------")
        for fila in resultado_tc:
            print("Código del trabajador:", fila[0])
            print("Nombre:", fila[1])
            print("-----------------------------------------------------------------")

        codTra = input("Ingrese el código del trabajador al que desea modificar su contraseña: ").lower()
        consulta_tc = '''SELECT tr.codTra, tr.nombre_T from trabajador tr 
                       inner join usuario us on tr.codTra = us.codTra 
                       WHERE us.codPer < 5 and tr.codTra = %s ''' # Verifica si el codTra existe en la base de datos
        valores_tc = (codTra,)
        resultado_tc = conexion.ejecutar_consulta(consulta_tc, valores_tc)

        if len(resultado_tc) == 0:
            os.system('cls')
            print("Error: El trabajador no tiene un perfil al cual modificar la contraseña.")
            input("Presione ENTER para continuar")
            return

        password= input("Ingrese la nueva contraseña del trabajador: ")

        while True:
            confirmacion = input("¿Está seguro que desea modificar la contraseña? (s/n): ").lower()
            if confirmacion.lower() not in ['s', 'n']:
                os.system('cls')
                print("Opción inválida. Por favor, ingrese 's' para confirmar o 'n' para cancelar.")
                input("Presione ENTER para continuar.")
            elif confirmacion == "s":
                valores = (password, codTra)
                consulta = "UPDATE usuario SET pass = %s WHERE codTra = %s"
                conexion.ejecutar_consulta(consulta, valores)
                
                os.system("cls")
                print("La contraseña se ha modificado exitosamente.")
                input("Presione ENTER para continuar.")
                break
            else: 
                os.system("cls")
                print("No se ha modificado la contraseña.")
                input("Presione ENTER para continuar.")
                break
        conexion.cerrar_conexion()                      # Cerrar la conexión
    
    def listar_insumos():                              # Función para listar por tipo de insumo
        
        conexion = ConexionBD()                             # Establecer la conexión a la base de datos
        try:
            
            query_tipos = "SELECT * FROM TIPO_INSUMO"       # Consultar los tipos de insumo disponibles
            tipos_insumo = conexion.ejecutar_consulta(query_tipos)

            while True:   
                os.system("cls")                                  # Comienza un buble while donde imprime primero los tipos de insumo 
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
                            print(
                            f" - Código: {codIns}, Nombre: {nombre}, Stock: {stock}")
                        input("Presione ENTER para volver al menú")
                    else:
                        print(f"No se encontraron insumos del tipo {cod_tipo_elegido}.") # En caso de no encontrar datos en la base de datos
                        input("Presione ENTER para volver al menú") 
                except ValueError:
                    print("Error: Ingrese un número válido.")           # En caso de ingresar mal los datos
                except pymysql.Error as error:
                    print("Error al ejecutar la consulta:", error)      # En caso de que se ejecute mal la consulta 
        finally:
        
            conexion.cerrar_conexion()                                  # Cerrar la conexión



def menu_administrador():
    while True:
        os.system("cls")
        print(f'''
        ===========================================
                    Menú Administrador
              
        Hora: {hora_actual} \tFecha: {fecha_actual} 
        ===========================================
        1 - Administrar personal
        2 - Realizar mantenimiento planilla médicos
        3 - Administrar tipos de citas 
        4 - Modificar función de un médico
        5 - Modificar contraseña de trabajadores
        6 - Listar insumos de bodega
        7 - Volver al menú principal
        ''')
        opcion_admin = input("Ingrese la opción deseada: ")

        if opcion_admin == "1":
            while True:
                os.system("cls")
                print(
                    """
                ====================================
                        Administrar personal
                ====================================
                        1 - Listar planilla de trabajadores con usuarios activos en sistema
                        2 - Añadir un nuevo trabajador
                        3 - Despedir un trabajador
                        4 - Actualizar datos de trabajadores
                        5 - Volver al menú de administrador           
                    """
                )
                op_adm = input("Ingrese la opción deseada: ")

                if op_adm == "1":
                    os.system('cls')
                    planilla = Administrador.listar_planilla_tr()
                    print("=========================================")
                    print("      PLANILLA DE TRABAJADORES")
                    print("=========================================")
                    for fila in planilla:
                        print("Código del trabajador:", fila[0])
                        print("Rol:", fila[1])
                        print("Rut:", fila[2])
                        print("Nombre del trabajador:", fila[3])
                        print("Dirección:", fila[4])
                        print("Teléfono:", fila[5])
                        print("Email:", fila[6])
                        print("-----------------------------------")

                    input("Presione ENTER para volver al submenú anterior...")

                elif op_adm == "2":
                    os.system("cls")
                    Administrador.ingresar_tr()

                elif op_adm == "3":
                    os.system("cls")
                    codTra = input("Ingrese el código del trabajador que desea despedir: ")
                    Administrador.despedir_tr(codTra)

                elif op_adm == "4":
                    os.system("cls")
                    while True:
                        print(
                            """
                        =================================================
                                Actualización datos de trabajadores
                        =================================================
                                1 - Actualizar nombre
                                2 - Actualizar dirección
                                3 - Actualizar teléfono
                                4 - Actualizar email
                                5 - Volver al submenú anterior         
                            """
                        )
                        op_act = input("Ingrese la opción deseada: ")

                        if op_act == "1":
                            os.system("cls")
                            Administrador.actualizar_nombre_tr()
                        elif op_act == "2":
                            os.system("cls")
                            Administrador.actualizar_direccion_tr()
                        elif op_act == "3":
                            os.system("cls")
                            Administrador.actualizar_telefono_tr()
                        elif op_act == "4":
                            os.system("cls")
                            Administrador.actualizar_email_tr()
                        elif op_act == "5":
                            break
                        else:
                            os.system("cls")
                            print("Opción inválida. Por favor, ingrese un número del 1 al 5.")
                            input("Presione ENTER para continuar")
                            os.system("cls")


                elif op_adm == "5":
                    break

                else:
                    print("Opción inválida. Por favor, ingrese un número del 1 al 5.")
                    input("Presione ENTER para continuar")

        elif opcion_admin == "2":
            os.system("cls")
            while True:
                os.system("cls")
                print(
                    """
                ====================================
                        Mantenimiento médicos
                ====================================
                        1 - Visualizar horario de médicos
                        2 - Añadir especialidad a médico
                        3 - Actualizar datos de médico
                        4 - Volver al menú de administrador           
                    """
                )
                op_admin = input("Ingrese la opción deseada: ")

                if op_admin == "1":
                    os.system('cls')
                    Administrador.obtener_disponibilidad_medicos()

                elif op_admin == "2":
                    os.system('cls')
                    Administrador.agregar_especialidad()

                elif op_admin == "3":
                    while True:
                        os.system("cls")
                        print(
                            """
                        =================================================
                                Actualización datos de médicos
                        =================================================
                                1 - Actualizar nombre
                                2 - Actualizar dirección
                                3 - Actualizar teléfono
                                4 - Actualizar email
                                5 - Volver al submenú mantenimiento de médicos         
                            """
                        )
                        op_act = input("Ingrese la opción deseada: ")

                        if op_act == "1":
                            os.system("cls")
                            Administrador.actualizar_nombre_med()
                        elif op_act == "2":
                            os.system("cls")
                            Administrador.actualizar_direccion_med()
                        elif op_act == "3":
                            os.system("cls")
                            Administrador.actualizar_telefono_med()
                        elif op_act == "4":
                            os.system("cls")
                            Administrador.actualizar_email_med()
                        elif op_act == "5":
                            break
                        else:
                            os.system("cls")
                            print("Opción inválida. Por favor, ingrese un número del 1 al 5.")
                            input("Presione ENTER para continuar")
                            os.system("cls")

                elif op_admin == "4":
                    break
                else:
                    os.system("cls")
                    print("Opción inválida. Por favor, ingrese un número del 1 al 4.")
                    input("Presione ENTER para continuar")
                    os.system("cls")

        elif opcion_admin == "3":
            while True:
                os.system("cls")
                print(
                    """
                ======================================
                    Administrar tipos de citas
                ======================================
                        1 - Listar tipos de citas
                        2 - Agregar un nuevo tipo de cita
                        3 - Modificar un tipo de cita
                        4 - Eliminar un tipo de cita
                        5 - Volver al menú de administrador        
                    """
                )
                op_tc = input("Ingrese la opción deseada: ")
                os.system("cls")
                if op_tc == "1":
                    os.system("cls")
                    Administrador.listar_tc()

                elif op_tc == "2":
                    os.system("cls")
                    Administrador.agregar_tc()

                elif op_tc == "3":
                    os.system("cls")
                    Administrador.actualizar_tc()

                elif op_tc == "4":
                    os.system("cls")
                    Administrador.eliminar_tc()
                elif op_tc == "5":
                    break
                else:
                    os.system("cls")
                    print("Opción inválida. Por favor, ingrese un número del 1 al 5.")
                    input("Presione ENTER para continuar")
                    os.system("cls")

        elif opcion_admin == "4":
            os.system("cls")
            Administrador.modificar_funcion_med()

        elif opcion_admin == "5":
            os.system("cls")
            Administrador.modificar_password()
        elif opcion_admin == "6":
            os.system("cls")
            Administrador.listar_insumos()

        elif opcion_admin == "7":
            os.system("cls")
            input("Saliendo del menú administrador... Presione ENTER para volver al menú principal")
            break
        else:
            print("Opción inválida. Por favor, ingrese un número del 1 al 7.")
            input("Presione ENTER para continuar")
