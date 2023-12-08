import pymysql
import getpass
import re
import os
import sys


class ConexionBD:
    def __init__(self):   # Inicia la conexion automatico
        self.conexion = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="centro medico",
            port=3306
        )
        self.cursor = self.conexion.cursor()
    
    def ejecutar_consulta(self, consulta, valores=None):   # metodo para ejecutat la consulta
        self.cursor.execute(consulta, valores)
        resultado = self.cursor.fetchall()
        return resultado

    def ejecutar_actualizacion(self, consulta, valores): # metodo ejecturar una actualizacion
        self.cursor.execute(consulta, valores)
        self.conexion.commit()

    def cerrar_conexion(self): #metodo para cerrar conexion.
        self.cursor.close()
        self.conexion.close()

def verificar_inicio_sesion():
    conexion = ConexionBD()

    usuario = input("Ingrese el nombre de usuario (solo números): ")

    # Validar que el usuario solo contenga números
    if not re.match(r"^\d+$", usuario):
        print("El nombre de usuario debe contener solo números.")
        return None,None

    contraseña = getpass.getpass("Ingrese la contraseña: ")

    consulta = "SELECT * FROM USUARIO WHERE codU = %s"
    valores = (usuario,)
    resultado = conexion.ejecutar_consulta(consulta, valores)

    if len(resultado) == 1:
        usuario_bd = resultado[0]
        contraseña_bd = usuario_bd[3]  # Columna pass en la tabla
        if contraseña == contraseña_bd:
            trabajador=usuario_bd[1]
            perfil = usuario_bd[2]
            # Columna codPer en la tabla
            return perfil,trabajador

    return None,None

def obtener_nombre_trabajador(cod_trabajador):
    conexion = ConexionBD()
    consulta = "SELECT nombre_t FROM TRABAJADOR WHERE codTra = %s "
    valores = (cod_trabajador,)
    resultado = conexion.ejecutar_consulta(consulta, valores)

    if len(resultado) == 1:
        nombre = resultado[0][0]  # Primer registro, primera columna (nombre)
        return f"{nombre}"
    return None

def obtener_codigo_trabajador(cod_trabajador):
    conexion = ConexionBD()

    consulta = "SELECT codTra FROM TRABAJADOR WHERE codTra = %s "
    valores = (cod_trabajador,)
    resultado = conexion.ejecutar_consulta(consulta, valores)

    if len(resultado) == 1:
        codigo= resultado[0][0]  # Primer registro, primera columna (nombre)
        return f"{codigo}"
    return None



def buscar_paciente(rut_P):  
        conexion = ConexionBD()
        # Validar que el usuario solo contenga números
        if not re.match(r"^\d+$", rut_P):
            print("El nombre de usuario debe contener solo números.")
            return None

        
        consulta = "SELECT * FROM PACIENTE WHERE rut_P = %s"
        valores = (rut_P,)
        resultado = conexion.ejecutar_consulta(consulta, valores)
        
        if len(resultado) > 0:
            return resultado  # Retorna todas las filas que corresponden al Rut

        return None
    
        return None

def cambiar_password(codTra):
    conexion=ConexionBD()

    consulta= "select * from usuario where codtra=%s"
    valores=codTra

    resultado=conexion.ejecutar_consulta(consulta, valores)

    for fila in resultado:
        # Asignar variables a cada columna de la fila
        columna1, columna2, columna3, columna4 = fila[0], fila[1], fila[2], fila[3]

        columna4 = "*" * len(columna4) # ocultara la contraseña con astericos
        
        # Imprimir los valores asignados a las variables
        print("tus datos de usuario son los siguientes:")

        print("Usuario :", columna1)
        print("Codigo de trabajador:", columna2)
        print("Codigo del perfil", columna3)
        print("Password:", columna4)
        print("---------------------------")

        respuesta=input("Desea cambiar el password (si/no): ").capitalize()

        if respuesta == "Si":
            pass_nuevo=getpass.getpass("Ingrese su nuevo password: ")
            pass_nuevo2=getpass.getpass("Ingrese su nuevo password nuevamente:  ")

            if pass_nuevo == pass_nuevo2:
                consulta="UPDATE USUARIO SET pass =%s where codTra = %s"
                valores=pass_nuevo,codTra
            
                resultado=conexion.ejecutar_actualizacion(consulta,valores)

                print("El password ha sido cambiado")

                input("Presione enter para continuar")
            
            else: 
                print("El password no ha sido cambiado porque los passwords ingresados no coinciden")

                input("Presione enter para continuar")

        elif respuesta == "No":
            input("Presione enter para continuar")
            break
        else:
            print("Ingrese una opcion valida por favor")

            input("Presione enter para continuar")

def terminos_condiciones():

    conexion=ConexionBD()
    consulta= "select * from ACEPTACION"

    resultado=conexion.ejecutar_consulta(consulta)


    for fila in resultado:
        columna1 = fila[0]

    if columna1 == "NO":

        os.system("cls")
        print("ANTES DE USAR EL PROGRAMA FAVOR DE LEER LOS TERMINOS Y CONDICIONES.")
        print("\n")

        print('''Términos y Condiciones Generales

            Aceptación de los Términos y Condiciones
                
            Al utilizar nuestro software de gestión de fichas de pacientes y agendamiento de horas,
            usted acepta estos Términos y Condiciones.
                
            Lea detenidamente este documento antes de utilizar el software. Si no está de acuerdo con 
            estos términos, por favor, no utilice el software. ''')
        print("\n")
        input("Presione enter para continuar")
        print("\n")
        print('''
            1-Propósito del Software
              
            El software proporciona herramientas para la gestión de fichas de pacientes y el 
            agendamiento de horas médicas. Su uso está destinado únicamente a profesionales 
            de la salud y establecimientos médicos autorizados.''')
        print("\n") 
        input("Presione enter para continuar")
        print("\n")

        print('''
            2- Confidencialidad y Protección de Datos
                
            Nos comprometemos a proteger la confidencialidad y privacidad de los datos personales de 
            los pacientes ingresados en el software. Todos los datos personales recopilados serán 
            tratados de acuerdo con las leyes y regulaciones de protección de datos personales de Chile.
            No divulgaremos ni compartiremos los datos personales de los pacientes con terceros sin su 
            consentimiento previo, excepto cuando sea requerido por ley.
            ''')
        print("\n") 
        input("Presione enter para continuar")
        print("\n")

        print('''
                    
            3-Responsabilidad del Usuario
            El usuario es responsable de la veracidad y precisión de los datos ingresados en el software. 
            Además, es responsable de garantizar que cumple con todas las leyes y regulaciones aplicables, 
            incluyendo las relacionadas con la protección de datos personales y la confidencialidad 
            de la información médica.
            ''')
        print("\n") 
        input("Presione enter para continuar")
        print("\n")

        print('''
            4-Propiedad Intelectual
                
            El software, incluyendo todos los derechos de propiedad intelectual asociados, pertenece a JJM. 
            Queda prohibida la reproducción, distribución, modificación o cualquier otro uso no autorizado del 
            software sin nuestro consentimiento previo por escrito.
            ''')
        print("\n") 
        input("Presione enter para continuar")            
        print("\n")

        print('''
                
            5-Limitación de Responsabilidad
            
            En ningún caso seremos responsables de cualquier daño directo, indirecto, incidental, especial o 
            consecuencial derivado del uso o la imposibilidad de uso del software. Asimismo, no nos hacemos 
            responsables de los errores u omisiones en la información contenida en el software.
            ''')
        print("\n") 
        input("Presione enter para continuar")
        print("\n")

        print('''
                
            6-Modificaciones de los Términos y Condiciones
                
            Nos reservamos el derecho de modificar estos Términos y Condiciones en cualquier momento.
            Cualquier modificación se publicará en el software y entrará en vigencia a partir de su publicación. 
            Le recomendamos revisar periódicamente los Términos y Condiciones actualizados.
            ''')


        print("\n") 
        input("Presione enter para continuar")
        print("\n")

        print('''
            7-Ley Aplicable y Jurisdicción
            
            Estos Términos y Condiciones se regirán e interpretarán de acuerdo con las leyes de la República de
            Chile. Cualquier disputa relacionada con el uso del software se someterá a la jurisdicción de 
            los tribunales competentes de Chile.

            ''')
        
        print("\n") 
        input("Presione enter para continuar")
        print("\n")

        print('''
            8-Protección de Datos Personales
        
            Los datos personales recopilados y tratados a través del software se realizarán de acuerdo con las leyes y
            regulaciones de protección de datos personales de Chile. Nos comprometemos a implementar las medidas de seguridad
            y protección necesarias para garantizar la confidencialidad y seguridad de los datos personales.
            ''')
        print("\n")

            

        while True:
            
            respuesta=input("Esta de acuerdo con los terminos y condiciones del programa ( si/no)").upper()

            if respuesta == "SI":
                consulta="UPDATE ACEPTACION SET RESPUESTA =%s"
                valores=("SI",)
                
                resultado=conexion.ejecutar_actualizacion(consulta,valores)

                print("Gracias por aceptar los terminos, ahora ingresara al programa")

                input("Presione enter para continuar")
                break

            elif respuesta == "NO":
                print("No se aceptaron los términos y condiciones. El programa se cerrará.")
                sys.exit()

            else:
                print("Ingrese una opcion valida por favor")
                continue
    else:
        pass


