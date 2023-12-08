import os
from datetime import datetime

os.system("cls")

from conexion import *
from medico import *
from recepcionista import *
from administrador import *
from farmaceutico import *


hora_actual = datetime.now().strftime("%H:%M")
fecha_actual = datetime.now().strftime("%d - %m - %Y")



while True:
    try:
        conexion = ConexionBD()
        terminos_condiciones()
        os.system("cls")
        print("Conexión establecida correctamente.")
        # Resto de tu código aquí

        
        
        
        print(f'''
        ======================================================
        |        Bienvenido a KILLCORONAVIRUS center         |
        |                                                    |
        |       Hora: {hora_actual} Fecha: {fecha_actual}            |
        ======================================================

                    1 - Ingresar al sistema
                    2 - Salir del programa
        ''' )

        opcion = input("Ingrese el número de la opcion que desea ingresar por favor: ")



        if re.match(r'^\d+$', opcion): # validacion para que no ingrese algo distinto a numeros como din
            opcion = int(opcion)
            

            if opcion == 1: #com
                while True :
                    os.system("cls")
                    print(f'''
        ======================================================
        |        Bienvenido a KILLCORONAVIRUS center         |
        |                                                    |
        |       Hora: {hora_actual}\tFecha: {fecha_actual}            |
        ======================================================
                    
                        ''')
                    
                    perfil_usuario, trabajador = verificar_inicio_sesion()  ### arreglar validacion1

                    if perfil_usuario is not None and trabajador is not None: # en caso de que encuentre perfil

                        nombre_trabajador = obtener_nombre_trabajador(trabajador)
                        codigo_trabajador = obtener_codigo_trabajador(trabajador)

                        if perfil_usuario == 1:  # si es el administrador
                            print("Bienvenido Administrador:", nombre_trabajador)
                            input("Presione enter para continuar")
                            menu_administrador()
                
                        elif perfil_usuario == 2: # si es el medico
                            print("Bienvenido Doctor(a):",nombre_trabajador)
                            medico = Medico.asignar_medico(codigo_trabajador)
                            input("Presione enter para continuar")
                            menu_medico(medico,codigo_trabajador,nombre_trabajador)
                        
                        elif perfil_usuario == 3: # si es el recepcionista
                            print("Bienvenido Recepcionista: ", nombre_trabajador)
                            recepcionista = Recepcionista.asignar_recepcionista(codigo_trabajador)
                            input("Presione cualquier tecla")
                            menu_recepcionista(recepcionista,codigo_trabajador,nombre_trabajador)


                        elif perfil_usuario == 4: # si es el farmaceutico                       
                            print("Bienvenido Farmaceutico(a): ", nombre_trabajador)
                            farmaceutico=Farmaceutico.asignar_farmaceutico(codigo_trabajador)
                            input("Presione enter para continuar")
                            menu_farmaceutico(farmaceutico, codigo_trabajador,nombre_trabajador)

                        elif perfil_usuario == 5: # si el perfil inactivo
                            print("Bienvenido ,", nombre_trabajador) 
                            print("su usuario ha sido desactivado, comuniquese con el administrador")
                            input("Presione enter para continuar")

                        else:  # falla en caso de que no tenga asignado el 
                            print("no tiene perfil asignado, comuniquese con el administrador.")
                    else: # falla en caso de no encontrar al usuario 
                        print("Inicio de sesión fallido. Usuario o contraseña estan incorrecto")
                        input("Presione enter para continuar")
                        os.system("cls")
                        break

            elif opcion == 2:
                os.system("cls")
                print("el programa se ha cerrado.")
                conexion.cerrar_conexion()
                input("Presione enter para continuar")
                os.system("cls")
                break

            else:
                os.system("cls")
                print("ingrese un numero valido ,entre 1 y 2")
                input("Presione enter para continuar")

        else:
            os.system("cls")
            print("Ingrese un numero entre 1 y 2 por favor")
            input("Presione enter para continuar")
            os.system("cls")


    except Exception as e:
        print("el programa se cerrara, el programa no se puede conectar a la base de datos")
        input("Presione enter para continuar")
        break
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

