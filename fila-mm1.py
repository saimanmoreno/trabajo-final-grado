import random
import simpy
import numpy as np
import scipy.stats as st

nClients = 5
arrivalFee = 1.0 / 6.0      # inverse of the average interval between arrivals in minutes = lambda
attendFee = 1.0 / 5.0       # inverse of the average service time in minutes = mu
timesInQueue = []

def arrivals(env):
    """ Generates customer arrivals in the system """
    for i in range(nClients):
        yield env.timeout(random.expovariate(arrivalFee))
        name = 'Client %d' % (i+1)
        env.process(attendence(env, name))

def attendence(env, name):
    """ Simulates customer service on server 1 """
    arrival = env.now                   # guarda la hora de llegada del cliente
    print('%7.2f\t Arrival\t %s' % (env.now, name))
    
    atendReq = Servidor1.request()      # solicita el recurso del servidor1
    yield atendReq                      # espera en la cola hasta la liberación del recurso para sólo entonces ocuparlo

    timeInQueue = env.now - arrival     # calcula el tiempo de espera
    timesInQueue.append(timeInQueue)    # crea una lista con el tiempo de espera de cada cliente

    print('%7.2f\t Atendence\t %s\t Time in Queue: %7.2f' % (env.now, name, timeInQueue))

    yield env.timeout(random.expovariate(attendFee))    # espera un tiempo de servicio distribuido exponencialmente
    Servidor1.release(atendReq)                         # libera el recurso del servidor1

    print('%7.2f\t Departure\t %s\t Clients in Queue: %d' % (env.now, name, len(Servidor1.queue)))

""" Main block """
print('\nM/M/1\n')
print('Time\t', 'Event\t\t', 'Client\n')

random.seed(27)
env = simpy.Environment()
Servidor1 = simpy.Resource(env, capacity=1)
env.process(arrivals(env))
env.run()

# Calcular el tiempo medio de espera en la cola
print('\n\nTIEMPO MEDIO DE ESPERA EN LA COLA >> %7.2f minutos' % (sum(timesInQueue)/len(timesInQueue)))

# Calcular teóricamente el tiempo medio de espera en una cola
averageWaitTime = arrivalFee / (attendFee * (attendFee - arrivalFee))
print('TIEMPO MEDIO DE ESPERA EN LA COLA TEORICAMENTE >> %7.2f minutos\n\n' % (averageWaitTime))

# Calcule el intervalo de confianza del 95%.
confidence_interval = st.t.interval(alpha=0.95, df=len(timesInQueue)-1,
              loc=np.mean(timesInQueue), scale=st.sem(timesInQueue))

# redondear los intervalos a tres decimales
confidence_interval = [round(num, 3) for num in confidence_interval]

print('INTERVALO DE CONFIANCA A 95%: ')
print(confidence_interval)


# OUTPUT: 

# PS C:\Users\pc\Desktop\defensa> & python.exe fila-mm1.py
# M/M/1
# Time     Event           Client
#    6.27  Arrival         Client 1
#    6.27  Atendence       Client 1        Time in Queue:    0.00
#   13.52  Arrival         Client 2
#   14.84  Arrival         Client 3
#   15.24  Arrival         Client 4
#   22.01  Departure       Client 1        Clients in Queue: 3   
#   22.01  Atendence       Client 2        Time in Queue:    8.49
#   24.04  Departure       Client 2        Clients in Queue: 2   
#   24.04  Atendence       Client 3        Time in Queue:    9.20
#   25.67  Arrival         Client 5
#   26.37  Departure       Client 3        Clients in Queue: 2
#   26.37  Atendence       Client 4        Time in Queue:   11.12
#   34.80  Departure       Client 4        Clients in Queue: 1
#   34.80  Atendence       Client 5        Time in Queue:    9.12
#   35.81  Departure       Client 5        Clients in Queue: 0   

# TIEMPO MEDIO DE ESPERA EN LA COLA >>    7.59 minutos
# TIEMPO MEDIO DE ESPERA EN LA COLA TEORICAMENTE >>   25.00 minutos

# INTERVALO DE CONFIANCA A 95%: 
# [2.18, 12.994]