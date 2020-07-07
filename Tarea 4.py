import numpy as np
from scipy import stats
from scipy import signal
from scipy import integrate
import matplotlib.pyplot as plt



doc = []
with open('bits10k.csv') as archivo:
    lectura = archivo.read().splitlines()
    for fila in lectura:
        doc.append((fila))

bits10k = [doc]
print('Creación de vector de bits del documento dado',bits10k)

 #Número de bits por generar
N =  len(doc) #len(doc) #La cantidad de bits del bits.csv  son 10000
print('Cantidad de Bits del documento',N)



# Variable aleatoria binaria
X = stats.bernoulli(0.5) #Forma equiprobable


# Generar bits para "transmitir"
bits = X.rvs(N) #Forma aleatoria
print('Creación de un vector de bits de manera aleatoria',bits)
'''
1. Crear un esquema de modulación BPSK para los bits presentados. Esto implica asignar una forma de onda sinusoidal
 normalizada (amplitud unitaria) para cada bit y luego una concatenación de todas estas formas de onda.
'''
print('\n--- 1 ---\n')

# Frecuencia de operación dada por el ejercicio para la portadora
frecuencia = 5000 #  5KHz


# Duración del período de cada onda
T = 1/frecuencia # 5 ms

# Número de puntos de muestreo por período
p = 100

# Puntos de muestreo para cada período (Creación de un vector de tiempo)
tp = np.linspace(0, T, p)

# Creación de la forma de onda senosoidal según el número de muestreo por cada período
seno = np.sin(2*np.pi * frecuencia * tp)

# Visualización de la forma de onda de la portadora
plt.plot(tp, seno)
plt.xlabel('Tiempo / s')
plt.title('Forma de onda de la portadora')
plt.ylabel('Amplitud')
plt.savefig('ondaportadora.png')

# Frecuencia de muestreo
fs = p/T # 500KHz
#print(fs)


# Creación de la línea temporal para toda la señal Tx
t = np.linspace(0, N*T, N*p)
#print(N*T)
#print(N*p)
senal_modulada = np.zeros(N*p)


# Creación de la señal modulada BPSK
for k,b in enumerate(bits):
    if b==1:
        senal_modulada[k*p:(k+1)*p] = seno
    else:
        senal_modulada[k * p:(k + 1) * p] = -seno


# Visualización de los primeros bits modulados
pb = 20
plt.figure()
plt.plot(senal_modulada[0:pb*p])
plt.xlabel('Frecuencia Hz')
plt.ylabel('Amplitud')
plt.title('Señal Modulada')
plt.savefig('modulada.png')



'''
2. Calcular la potencia promedio de la señal modulada generada.
'''
# Potencia instantánea de la señal modulada
P_instantanea = senal_modulada**2
print('La potencia instantanea de la señal modulada es=',P_instantanea)

# Potencia promedio a partir de la potencia instantánea (W)
P_promedio = integrate.trapz(P_instantanea, t) / (N * T)
print('La potencia promedio de la señal instantenea es=',P_promedio)


'''
3. Simular un canal ruidoso del tipo AWGN (ruido aditivo blanco gaussiano) 
con una relación señal a ruido (SNR) desde -2 hasta 3 dB.
'''
# Relación señal-a-ruido deseada para -2dB,3dB y de (-2 hasta 3)
SNR = np.linspace(-2,3,N*p)
SNR1 = -2
SNR2 = 3

# Potencia del ruido para SNR y potencia de la señal dadas
P_ruido1 = P_promedio / (10**(SNR1 / 10)) #Para 1dB
P_ruido2 = P_promedio / (10**(SNR2 / 10)) #Para 2dB
P_ruido3 = P_promedio / (10**(SNR / 10)) #Para -2 hasta 3 dB

# Desviación estándar del ruido para cada uno de los ruidos según los dBs
sigma1 = np.sqrt(P_ruido1)
sigma2 = np.sqrt(P_ruido2)
sigma3 = np.sqrt(P_ruido3)
# Creación de ruido
ruido1 = np.random.normal(0, sigma1, senal_modulada.shape)
ruido2 = np.random.normal(0, sigma2, senal_modulada.shape)
ruido3 = np.random.normal(0, sigma3, senal_modulada.shape)

# Simular "el canal": señal recibida
senal_recibida1 = senal_modulada + ruido1
senal_recibida2 = senal_modulada + ruido2
senal_recibida3 = senal_modulada + ruido3

# Visualización de los primeros bits recibidos

#Número de Bits
pb = 25

#Gráfica de la señal para SRN=1dB
plt.figure()
plt.plot(senal_recibida1[0:pb*p])
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud')
plt.title('Canal ruidoso para SRN=-2dB')
plt.savefig('Señalrecibida-2dB.png')

#Gráfica de la señal para SRN=2dB
plt.figure()
plt.plot(senal_recibida2[0:pb*p])
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud')
plt.title('Canal ruidoso para SRN=3dB')
plt.savefig('Señalrecibida3dB.png')

#Gráfica de la señal para SRN de -2 hasta 3 dB
plt.figure()
plt.plot(senal_recibida3[0:pb*p])
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud')
plt.title('Canal ruidoso realizando el recorrido de -2 a 3 dB')
plt.savefig('Señalrecibida-2-3dB.png')


'''
4. Graficar la densidad espectral de potencia de la señal con el método de Welch (SciPy), antes y después del canal ruidoso.
'''

#Visualización de la densidad espectral de potencia de la señal antes y depués del canal ruidoso para SRN=1dB

# Antes del canal ruidoso
fw, PSD = signal.welch(senal_modulada, fs, nperseg=1024)
plt.figure()
plt.semilogy(fw, PSD)
plt.xlabel('Frecuencia / Hz')
plt.ylabel('Densidad espectral de potencia / V**2/Hz')
plt.title('Densidad espectral de potencia antes del canal ruidoso')
plt.savefig('PDEantescanalruidoso')

#Visualización de la densidad espectral de potencia de la señal depués del canal ruidoso para SRN=-2dB
fw, PSD = signal.welch(senal_recibida1, fs, nperseg=1024)
plt.figure()
plt.semilogy(fw, PSD)
plt.xlabel('Frecuencia / Hz')
plt.ylabel('Densidad espectral de potencia / V**2/Hz')
plt.title('Densidad espectral de potencia después del canal ruidoso para SNR=-2dB')
plt.savefig('PDEdespuescanalruidosoSRN=-2dB')

#Visualización de la densidad espectral de potencia de la señal depués del canal ruidoso para SRN=3dB
fw, PSD = signal.welch(senal_recibida2, fs, nperseg=1024)
plt.figure()
plt.semilogy(fw, PSD)
plt.xlabel('Frecuencia / Hz')
plt.ylabel('Densidad espectral de potencia / V**2/Hz')
plt.title('Densidad espectral de potencia después del canal ruidoso para SNR=3dB')
plt.savefig('PDEdespuescanalruidosoSRN=3dB')

#Visualización de la densidad espectral de potencia de la señal depués del canal ruidoso para SRN=-2 a 3 dB
fw, PSD = signal.welch(senal_recibida3, fs, nperseg=1024)
plt.figure()
plt.semilogy(fw, PSD)
plt.xlabel('Frecuencia / Hz')
plt.ylabel('Densidad espectral de potencia / V**2/Hz')
plt.title('Densidad espectral de potencia después del canal ruidoso para rango de -2 a 3 dB')
plt.savefig('PDEdespuescanalruidosoSRN=-2dBa3dB')



'''
5. Demodular y decodificar la señal y hacer un conteo de la tasa de error de bits (BER, bit error rate) para cada nivel SNR.
'''

# Supuesto de energía de la onda original
E_pesuedo = np.sum(seno**2)
print('Pseudo de energía de la onda original es =',E_pesuedo)

#Creación de un vector de la señal de bits recibidos para SNR=1dB y para SNR=2dB
bits_senalrecibida1 = np.zeros(bits.shape)
bits_senalrecibida2 = np.zeros(bits.shape)
bits_senalrecibida3 = np.zeros(bits.shape)

#Decodificación de la señal por detección de energía para SNR=-2dB
for k, b in enumerate(bits):
    Energy1 = np.sum(senal_recibida1[k*p:(k+1)*p] * seno )
    if Energy1 > E_pesuedo/2:
        bits_senalrecibida1[k] = 1
    else:
        bits_senalrecibida1[k] = 0

#Decodificación de la señal por detección de energía para SNR=3dB
for k, b in enumerate(bits):
    Energy2 = np.sum(senal_recibida2[k*p:(k+1)*p] * seno )
    if Energy2 > E_pesuedo/2:
        bits_senalrecibida2[k] = 1
    else:
        bits_senalrecibida2[k] = 0

#Decodificación de la señal por detección de energía para SNR=-2 a 3 dB
for k, b in enumerate(bits):
    Energy2 = np.sum(senal_recibida3[k*p:(k+1)*p] * seno )
    if Energy2 > E_pesuedo/2:
        bits_senalrecibida3[k] = 1
    else:
        bits_senalrecibida3[k] = 0


#Obtención de errores para cada una de las señales
err1 = np.sum(np.abs(bits - bits_senalrecibida1))
err2 = np.sum(np.abs(bits - bits_senalrecibida2))
err3 = np.sum(np.abs(bits - bits_senalrecibida3))

#Tasa de error de bits de las señales
BER1 = err1/N
print('Tasa de error para la señal SRN=-2dB',BER1)
BER2 = err2/N
print('Tasa de error para la señal SRN=3dB =',BER2)
BER3 = err3/N
print('Tasa de error para la señal SRN=-2 a 3 dB =',BER3)

'''
6. Graficar BER versus SNR.
'''
#Creación de vectores para la tasa de error
Vector_Ber1 = np.linspace(0, BER1, N*p)
Vector_Ber2 = np.linspace(0, BER2, N*p)
Vector_Ber3 = np.linspace(0, BER3, N*p)

plt.subplot(3, 1, 1)
plt.plot(Vector_Ber1, senal_recibida1)
plt.subplot(3, 1, 2)
plt.plot(Vector_Ber2, senal_recibida2)
plt.subplot(3, 1, 3)
plt.plot(Vector_Ber3, senal_recibida3)
plt.savefig('BerVsSRN')

