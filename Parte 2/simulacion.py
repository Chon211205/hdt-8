#bibliotecas importadas
import random
import matplotlib.pyplot as plt
import simpy

#Configuracion de seed de la simulacion
random.seed(10)

#Clase paciente
#simula al paciente con sus caracteristicas como el nombre o la severidad.
class Paciente:
    #Constructor
    #Constructor del paciente.
    def __init__(Paciente, Nombre, Severidad):
        Paciente.Nombre = Nombre
        Paciente.Severidad = Severidad

    #Metodos
    #Metodo para evaluar la severidad.
    def __lt__(Paciente, severidad_menor):
        return Paciente.Severidad <= severidad_menor.Severidad
    
    #Metodo para comparar la severidad de varios pacientes y ordenarlos.
    def __str__(Paciente):
        return f"{Paciente.Nombre}, Severidad {Paciente.Severidad}"
    
#Listas de almacenamiento de tiempos de espera en las tres etapas
Clasificacion_severidad = []
Tiempo_doctorGeneral = []
Tiempo_doctorEspecial = []
Tiempo_rayosX = []

#Funcion de simulacion del hospital
def Hospital(ambiente):
    
    #Definicion de recursos del hospital
    enfermera = simpy.Resource(ambiente, capacity = 2)
    doctorGeneral = simpy.PriorityResource(ambiente, capacity = 2)
    doctorEspecial = simpy.PriorityResource(ambiente, capacity = 1)
    rayosX = simpy.PriorityResource(ambiente, capacity = 2)

    #Pacientes que se debe atender
    pacientes = ["Arturo", "Jimena", "Luis", "Carlo", "Arodi"]
    #Ciclo para generar los datos de los pacientes.
    for i in range (5):
        #Elige un nombre de la lista de pacientes
        Nombre = random.choice(pacientes)
        #Eleccion aleatoria de la severidad del paciente
        Severidad = random.randint(1, 5)
        #Recopila los datos generados anteriormente y los guarda
        paciente = Paciente(Nombre, Severidad)
        ambiente.process(paciente_procesado(ambiente, paciente, enfermera, doctorGeneral, doctorEspecial, rayosX))
        #Tiempo de llegada de los pacientes
        yield ambiente.timeout(3)

#Funcion de simulacion de los procesos de un paciente en urgencias
def paciente_procesado(entrada, paciente, enfermera, doctorGeneral, doctorEspecial, rayosX):

    #Ingreso del paciente a urgencias
    ingreso_paciente = entrada.now
    #Espera a la enfermera
    with enfermera.request() as solicitud:
        yield solicitud
        Sala_espera = entrada.now - ingreso_paciente
        #Llevan al paciente para clasificar su severidad y agregarloa la lista.
        Clasificacion_severidad.append(max(Sala_espera, 0.1))
        print(f"{entrada.now}: {paciente} ingreso del paciente a la sala de urgencias")
        #Tiempo de tardanza de evaluacion del paciente.
        yield entrada.timeout(5)

    #Clasificar si el paciente necesita un doctor general o un especialista.
    ingreso_doctor = entrada.now
    #Evalua el nivel de severidad del paciente.
    #Si es en una escala de 1 y 2, se considera como urgente y lo atiende un especialista.
    #Si es una escala de 3 a 5, se considera como no tan urgente y lo atiende un doctor general.
    if paciente.Severidad <= 2:
        with doctorEspecial.request(priority = paciente.Severidad) as solicitud:
            #Espera para el doctor especialista.
            yield solicitud
            Sala_espera = entrada.now - ingreso_doctor
            #El doctor especialista revisa al paciente y se agrega a la lista de pacientes
            Tiempo_doctorEspecial.append(Sala_espera)
            print(f"{entrada.now}: {paciente} esta siendo atendido por un doctor especialista")
            #Tiempo que se tardo la revision por el doctor especialista.
            yield entrada.timeout(10)
    else:
        with doctorGeneral.request(priority = paciente.Severidad) as solicitud:
            #Espera para el doctor general.
            yield solicitud
            Sala_espera = entrada.now - ingreso_doctor
            #El doctor general revisa al paciente y se agrega a la lista de pacientes
            Tiempo_doctorGeneral.append(Sala_espera)
            print(f"{entrada.now}: {paciente} esta siendo atendido por un doctor general")
            #Tiempo que se tardo la revision por el doctor general.
            yield entrada.timeout(12)
    
    #Si es necesario, el paciente pasa por rayos X.
    ingreso_rayosX = entrada.now
    with rayosX.request(priority = paciente.Severidad) as solicitud:
        #Espera para los rayos X.
        yield solicitud
        Sala_espera = entrada.now - ingreso_rayosX
        #El paciente pasa porla maquina de rayos X.
        Tiempo_rayosX.append(Sala_espera)
        print(f"{entrada.now}: {paciente} se encuentra en la maquina de rayos X")
        #Tiempo que se tarda el paciente en pasar por los rayos X.
        yield entrada.timeout(15)
    print(f"{entrada.now}: {paciente} fue terminado de atender")

#Creacion del ambiente de simulacion
if __name__ == "__main__":
    #inico del ambiente de simulacion
    Ambiente = simpy.Environment()
    Ambiente.process(Hospital(Ambiente))
    Ambiente.run()

    #Graficar tiempos de espera

    #Recopilacion de los datos apartir de las listas de cada rol.
    Fases = ["Clasificacion", "Doctor general", "Doctor Especial", "Rayos X"]
    Recopilacion_tiempoPromedio = [
        sum(Clasificacion_severidad) / len(Clasificacion_severidad) if Clasificacion_severidad else 0.1,
        sum(Tiempo_doctorGeneral) / len(Tiempo_doctorGeneral) if Tiempo_doctorGeneral else 0,
        sum(Tiempo_doctorEspecial) / len(Tiempo_doctorEspecial) if Tiempo_doctorEspecial else 0,
        sum(Tiempo_rayosX) / len(Tiempo_rayosX) if Tiempo_rayosX else 0
    ]

    #Crear grafica apartir de los datos recopilados
    plt.figure(figsize=(8, 5))
    plt.bar(Fases, Recopilacion_tiempoPromedio, color = ["blue", "green", "red", "purple"])
    plt.xlabel("Fases")
    plt.ylabel("Tiempo promedio en minutos")
    plt.title("Tiempos promedio de espera en cada fase")
    plt.show()
