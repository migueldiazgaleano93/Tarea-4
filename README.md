# Tarea-4

 ## 1) Crear un esquema de modulación BPSK para los bits presentados. Esto implica asignar una forma de onda sinusoidal normalizada (amplitud unitaria) para cada bit y luego una concatenación de todas estas formas de onda.
 
 Primeramente la modulación es una alteración sistemática de una onda portadora de acuerdo con el mensaje de la señal modulada y puede ser también una codificación
 por ejemplo las señales de banda producidas por diferentes fuentes de información que no son siempre adecuadas para la transmición directa através de un canal dado.
 Una modulación BPSK, es una forma de modulación cuadrada de la portadora suprimida de una señal de onda continua. Es decir, con la transmición por desplazamiento de fase 
 binaria (BPSK), son posibles dos fases de salida para una sola frecuencia de la portadora. Una fase de salida representada con 1 lógico y la otra a un 0 lógico. La modulación (BPSK) se utiliza para transmisores de bajo costo que no requieren altas velocidadedes.
En la figura de abajo se muestra la "Forma de onda senosoidal normalizada"

![Screenshot](ondaportadora.png)

## 2)  Calcular la potencia promedio de la señal modulada generada.

Lo que primero que se hizo es encontrara la potencia instantanea de la señal modulada.Posteriormente se realizó la potencia promedio a partir de la potencia instantanea.
El resultado obtenido en pycharm es de 0.49500049500049487, este resultado se puede verificar en el código.

## 3)  Simular un canal ruidoso del tipo AWGN (ruido aditivo blanco gaussiano) con una relación señal a ruido (SNR) desde -2 hasta 3 dB.

Dado que en la realidad cuando se transmite una señal por un medio ya sea por el espacio como las ondas de radio o por un medio como un cable, la señal transmitida no tendrá una forma definida debido al ruido ocacionado por el medio por la que la señal es transmitida. A un canal ruidoso del tipo (AWGN) también conocido como ruido blanco gaussiano por lo que exite una relación de señal a ruido (SNR)

![Screenshot](Señalrecibida1dB.png)
![Screenshot](Señalrecibida2dB.png)
![Screenshot](Señalrecibida-2-3dB.png)
