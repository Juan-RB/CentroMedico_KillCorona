import os
os.system('cls')
from conexion import *
from datetime import datetime
import calendar
import locale
import re
from datetime import date

hora_actual = datetime.now().strftime("%H:%M")
fecha_actual = datetime.now().strftime("%d - %m - %Y")

class Medico:
    def __init__(self, codPm, codTra, funcion):
        self.codPm = codPm
        self.codTra = codTra
        self.funcion = funcion

    def asignar_medico(cod_trabajador): # crear objeto medico, parte de funcion exclusiva de medico
        conexion = ConexionBD()
        consulta_medico = """
            SELECT me.codPm, me.codTra, me.funcion
            FROM usuario us
            INNER JOIN trabajador tr ON us.codTra = tr.codTra
            INNER JOIN medico me ON tr.codTra = me.codTra
            WHERE us.codTra = %s
        """
        valores_medico = (cod_trabajador,)
        resultado_medico = conexion.ejecutar_consulta(consulta_medico, valores_medico)

        if len(resultado_medico) == 1:
            cod_pm, codTra, funcion = resultado_medico[0]

            medico = Medico(cod_pm, codTra, funcion)
            return medico

        conexion.cerrar_conexion()                      # Cerrar la conexión
        return None
        
    
    def obtener_ficha_paciente(self,rut_P): #funcion exclusiva medico 
        conexion = ConexionBD()
        consulta = "SELECT ATENCION.codPm, codAte, nombre_T, rut_P, tratamiento, receta, descripcion, diagnostico, fecha_a FROM ATENCION INNER JOIN MEDICO ON ATENCION.codPm = MEDICO.codPm INNER JOIN TRABAJADOR ON MEDICO.codTra = TRABAJADOR.codTra WHERE ATENCION.rut_P = %s"
        valores = (rut_P,)
        resultado = conexion.ejecutar_consulta(consulta, valores)

        if len(resultado) > 0:
            return resultado  # Retorna todas las filas que corresponden al Rut
        
        conexion.cerrar_conexion()                      # Cerrar la conexión
        return None

    def obtener_atenciones(self,codPm):  # CONSULTA SQL PARA BUSCAR TODAS LAS ATENCIONES, FUNCION EXCLUSIVA MEDICO
        conexion = ConexionBD() # SELECT codAte, rut_P, tratamiento, receta, descripcion, diagnostico, fecha_a FROM ATENCION WHERE codPm = 1 AND MONTH(fecha_a) = 5;
        consulta = "SELECT ATENCION.codPm, codAte, nombre_T, rut_P, tratamiento, receta, descripcion, diagnostico, fecha_a FROM ATENCION INNER JOIN MEDICO ON ATENCION.codPm = MEDICO.codPm INNER JOIN TRABAJADOR ON MEDICO.codTra = TRABAJADOR.codTra WHERE ATENCION.codPm = %s"
        valores = (codPm,)
        resultado = conexion.ejecutar_consulta(consulta, valores)

        if len(resultado) > 0:
            return resultado  # Retorna todas las filas que corresponden al Rut
        conexion.cerrar_conexion()                      # Cerrar la conexión
        return None


    def obtener_atenciones_mes(self,codPm, mes):  # CONSULTA SQL PARA BUSCAR POR MES, FUNCION EXCLUSIVA MEDICO
        conexion = ConexionBD()
        consulta = "SELECT ATENCION.codPm, codAte, nombre_T, rut_P, tratamiento, receta, descripcion, diagnostico, fecha_a FROM ATENCION INNER JOIN MEDICO ON ATENCION.codPm = MEDICO.codPm INNER JOIN TRABAJADOR ON MEDICO.codTra = TRABAJADOR.codTra WHERE ATENCION.codPm = %s AND MONTH(fecha_a) = %s"
        valores = (codPm, mes)
        resultado = conexion.ejecutar_consulta(consulta, valores)

        if len(resultado) > 0:
            return resultado
        else:
            conexion.cerrar_conexion()                      # Cerrar la conexión
            return None
        


    def obtener_atenciones_dia(self,codPm, dia):  # CONSULTA SQL PARA BUSCAR POR DIA, FUNCION EXCLUSIVA MEDICO
        conexion = ConexionBD()
        consulta = "SELECT ATENCION.codPm, codAte, nombre_T, rut_P, tratamiento, receta, descripcion, diagnostico, fecha_a FROM ATENCION INNER JOIN MEDICO ON ATENCION.codPm = MEDICO.codPm INNER JOIN TRABAJADOR ON MEDICO.codTra = TRABAJADOR.codTra WHERE ATENCION.codPm = %s AND fecha_a = %s"
        valores = (codPm, dia)
        resultado = conexion.ejecutar_consulta(consulta, valores)

        if len(resultado) > 0:
            return resultado
        else:
            conexion.cerrar_conexion()                      # Cerrar la conexión
            return None
            

    def crear_anamnesis(self, codPm, rut_P):

        fecha_actual = date.today()
        fecha_actual_str = fecha_actual.strftime("%Y-%m-%d")

        conexion = ConexionBD()
        os.system('cls')

        print("Creación de Nueva Anamnesis")
        print("-----------------------------------")
        codPm = codPm
        rut_P = rut_P
        tratamiento = input("Ingrese el tratamiento: ")
        receta = input("Ingrese la receta: ")
        descripcion = input("Ingrese la descripción: ")
        diagnostico = input("Ingrese el diagnóstico: ")
        fecha_a = fecha_actual_str

        # Validar los datos ingresados
        if not codPm or not rut_P or not tratamiento or not receta or not descripcion or not diagnostico or not fecha_a:
            os.system('cls')
            print("Por favor, complete todos los campos.")
            input("Presione cualquier ENTER para continuar")
            return

        # Confirmar si se está seguro de crear la anamnesis
        respuesta = input("¿Está seguro de crear esta anamnesis? (s/n): ")
        if respuesta.lower() == "s":
            # Realizar la inserción en la base de datos
            consulta = "INSERT INTO ATENCION (codPm, rut_P, tratamiento, receta, descripcion, diagnostico, fecha_a) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            valores = (codPm, rut_P, tratamiento, receta, descripcion, diagnostico, fecha_a)

            try:
                conexion.ejecutar_actualizacion(consulta, valores)
                os.system('cls')
                print("La anamnesis se ha creado correctamente.")
            except:
                os.system('cls')
                print("Ocurrió un error al crear la anamnesis. Intente nuevamente.")
        else:
            os.system('cls')
            print("La creación de anamnesis ha sido cancelada.")

        input("Presione ENTER para continuar")
        os.system('cls')
        conexion.cerrar_conexion()                      # Cerrar la conexión


    
    

def menu_medico(medico,codigo_trabajador,nombre_trabajador):
    fecha_actual = datetime.now()
    os.system("cls")
    
    while True:
        os.system("cls")
        print(f'''
        ===============================================
                        Menú Médico
              
        Nombre del doctor(a):{nombre_trabajador}
        Código del doctor(a):{medico.codPm}
        Código trabajador:{codigo_trabajador}
        Especialidad: {medico.funcion}

        Hora: {hora_actual}\tFecha: {fecha_actual} 
        ===============================================
        1 - Gestionar ficha de un paciente
        2 - Listar todas mis atenciones
        3 - Listar mis atenciones por mes
        4 - Listar mis atenciones por día especifico
        5 - Volver al menú principal
        6 - Cambiar password
        ''')
        opcion_medico = input("Ingrese la opción deseada: ")

        if opcion_medico == "1":
            os.system('cls')
            # Lógica para acceder a la ficha de un paciente
            rut_P = input("Ingrese el Rut del paciente (sin puntos ni guión): ")
            primera_entrada = True
            if re.match(r'^\d+$', rut_P):
                while True:
                    os.system('cls')
                    if primera_entrada: # Muestra el mensaje solo cuando ingreso la primera vez
                        ficha_paciente = medico.obtener_ficha_paciente(rut_P)
                        if ficha_paciente:
                            print("Ingresando a la ficha del paciente...")
                            input("Presione ENTER para continuar")
                            os.system('cls')
                        else:
                            print("No se encontró la ficha del paciente")
                            input("Presione ENTER para volver")
                            break
                        primera_entrada = False
                    print(
                        """
                    ====================================
                        Gestión de ficha de paciente
                    ====================================
                            1 - Visualizar ficha del paciente
                            2 - Generar una nueva anamnesis al paciente
                            3 - Volver al menú de médico
                    """
                    )
                    op_med = input("Ingrese la opción deseada: ")
                    if op_med == "1":
                        ficha_paciente = medico.obtener_ficha_paciente(rut_P)
                        if ficha_paciente:
                            os.system('cls')
                            print("Ficha del paciente:")
                            print("-----------------------------------")
                            for fila in ficha_paciente:
                                print("Código del médico:", fila[0])
                                print("Codigo de la atención:", fila[1])
                                print("Nombre del doctor:", fila [2])
                                print("Rut del paciente:", fila[3])
                                print("Tratamiento:", fila[4])
                                print("Receta:", fila[5])
                                print("Descripción:", fila[6])
                                print("Diagnóstico:", fila[7])
                                print("Fecha de atención:", fila[8])
                                print("-----------------------------------")
                        else:
                            print("No se encontró la ficha del paciente")
                        input("Presione ENTER para volver")
                    elif op_med == "2":
                        medico.crear_anamnesis(medico.codPm,rut_P)
                    elif op_med == "3":
                        break  # Salir del bucle y volver al menú principal
                    else:
                        print("Opción inválida. Por favor, ingrese una opción válida.")
                        input("Presione ENTER para continuar")
            else: 
                os.system("cls")
                print("El Rut debe contener solo números.")
                input("Presione ENTER para continuar")
        elif opcion_medico == "2":
            os.system('cls')
                                    
            codPm = medico.codPm #Acceder a todas las atenciones de un medico
            
            
            atenciones_doctor = medico.obtener_atenciones(codPm) 
            if atenciones_doctor:
                os.system('cls')
                print("Ingresando a sus atenciones...")
                input("Presione ENTER para continuar")
                os.system('cls')
                print("-----------------------------------")
                print("Resumen de sus atenciones:")
                print("-----------------------------------")
                for fila in atenciones_doctor:
                    print("Código del médico:", fila[0])
                    print("Codigo de la atención:", fila[1])
                    print("Nombre del doctor:", fila [2])
                    print("Rut del paciente:", fila[3])
                    print("Tratamiento:", fila[4])
                    print("Receta:", fila[5])
                    print("Descripción:", fila[6])
                    print("Diagnóstico:", fila[7])
                    print("Fecha de atención:", fila[8])
                    print("-----------------------------------")
            else:
                os.system('cls')
                print("No se encontraron atenciones")
            input("Presione ENTER para continuar")
        
        elif opcion_medico == "3":
            os.system('cls')
            codPm = medico.codPm

            mes = input("Ingrese el número del mes (1-12): ")
            if mes.isdigit() and int(mes) >= 1 and int(mes) <= 12:
                mes = int(mes)
                # Lógica para obtener las atenciones según el mes indicado
                atenciones_doctor_mes = medico.obtener_atenciones_mes(codPm, mes)

                if atenciones_doctor_mes:
                    os.system('cls')
                    print("--------------------------------------------------------------------")
                    print(f"Resumen de sus atenciones durante 2023/{mes:02d}:")
                    print("--------------------------------------------------------------------")

                    for fila in atenciones_doctor_mes:
                        print("Código del médico:", fila[0])
                        print("Código de la atención:", fila[1])
                        print("Nombre del doctor:", fila[2])
                        print("Rut del paciente:", fila[3])
                        print("Tratamiento:", fila[4])
                        print("Receta:", fila[5])
                        print("Descripción:", fila[6])
                        print("Diagnóstico:", fila[7])
                        print("Fecha de atención:", fila[8])
                        print("-----------------------------------")
                    input("Presione ENTER para continuar")
                else:
                    os.system('cls')
                    print("No se encontraron atenciones en este mes")
                    input("Presione ENTER para continuar")
            else:
                os.system('cls')
                print("El número de mes ingresado es inválido. Por favor, ingrese un número entre 1 y 12.")
                input("Presione ENTER para continuar")

        elif opcion_medico == "4":
            os.system('cls')
            codPm = medico.codPm
            fecha = input("Ingrese la fecha específica en la que desea buscar (YYYY-MM-DD): ")

            # Validación del formato de fecha
            if re.match(r'^\d{4}-\d{2}-\d{2}$', fecha):
                try:
                    datetime.strptime(fecha, '%Y-%m-%d')  # Validación adicional de la fecha
                    # Lógica para obtener atenciones por día en específico
                    atenciones_doctor_dia = medico.obtener_atenciones_dia(codPm, fecha)

                    if atenciones_doctor_dia:
                        os.system('cls')
                        print("Ingresando a sus atenciones...")
                        input("Presione ENTER para continuar")
                        os.system('cls')
                        print("-------------------------------------------------------------")
                        print("Resumen de sus atenciones durante el día "+ fecha +":")
                        print("-------------------------------------------------------------")
                        for fila in atenciones_doctor_dia:
                            print("Código del médico:", fila[0])
                            print("Código de la atención:", fila[1])
                            print("Nombre del doctor:", fila [2])
                            print("Rut del paciente:", fila[3])
                            print("Tratamiento:", fila[4])
                            print("Receta:", fila[5])
                            print("Descripción:", fila[6])
                            print("Diagnóstico:", fila[7])
                            print("Fecha de atención:", fila[8])
                            print("-----------------------------------")
                    else:
                        os.system('cls')
                        print("No se encontraron atenciones en esta fecha")
                except ValueError:
                    os.system('cls')
                    print("La fecha ingresada no es válida. Asegúrese de que siga el formato YYYY-MM-DD.")
            else:
                os.system('cls')
                print("El formato de fecha ingresado no es válido. Asegúrese de que siga el formato YYYY-MM-DD.")
            
            input("Presione ENTER para continuar")

            
        elif opcion_medico == "5":
            input("Saliendo del menu medico... Presione ENTER para volver al menu principal")
            break

        elif opcion_medico == "6":
            os.system("cls")
            cambiar_password(medico.codTra)
        else:
            os.system('cls')
            print("Opción inválida. Por favor, ingrese un número del 1 al 5.")
            input("Presione ENTER para continuar")