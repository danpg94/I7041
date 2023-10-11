import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
import random
import threading

X = []
W = [] 
d = [] 

colores = ['#44ff5c','#faf18e','#ff4040','#0a47e0','#ff9966','#ebf5fe',
            '#a5f99e','#143264','#082d28','#f5f5f5','#faf18e','#a5c0fa',
            '#f5cccc','#000080','#660066','#6d33b4','#AAF35C','#31F8EC',]


def FuncionActivacion (W,X):
    v = np.dot(W,X)
    #logistica
    F_u = 1/(1+np.exp(-(float(1))*v))
    return F_u


def FuncionDerivacion(Y):
    #Logistica
    F_u = float(1)*Y*(1-Y)
    return F_u

def Perceptron():
    global  Eta, Epocas_str, X, d, W
    Epocas = int(Epocas_str.get())
    error = True

    d = np.matrix(d)
    if funcion_evaluar.get() != 0:
        d[d==0]=(-1)

    while Epocas and error:
        error = False 
        errores_matrices = []
        for i in range(len(X)):
            errores = []
            for j in range(len(W)):
                Y = FuncionActivacion(W[j], X[i])
                e = d[i,j]-Y
                errores.append(e)
                y_prima = FuncionDerivacion(Y)
                W[j] = W[j] + (np.dot(float(Eta.get())*e*y_prima,X[i]))
            errores_matrices.append(errores)
        
        ax.cla()

        matrices_cuadradas = np.power(errores_matrices,2)
        average = matrices_cuadradas.mean(0)
        for a in average:
            if a > float(error_minimo.get()):
                error = True

        aceptar_minimo = 0
        if funcion_evaluar.get()==0:
            aceptar_minimo = 0.5

       
        for i in range(len(X)):
            Y = FuncionActivacion(W, X[i]) >= aceptar_minimo
            ax.plot(X[i][1],X[i][2],'D',color=colores[int("".join(str(j) for j in list(map(int, Y))),2)])

        for i in range(len(W)):
            m = -W[i][1]/W[i][2]
            b = -W[i][0]/W[i][2]

            plt.axline((X[0][1], (X[0][1]*m)+b), slope=m, color ='c', linestyle='-')

        ejeX = [-10,10] 
        ejeY = [-10,10]
        ceros = [0,0] 
        plt.plot(ejeX, ceros, 'k', linestyle='--') 
        plt.plot(ceros, ejeY, 'k', linestyle='--') 
        plt.xlim(-10,10)
        plt.ylim(-10,10)

        canvas.draw()
        Epocas = Epocas - 1
        print(f"Epocas restantes: {Epocas}")
    print("terminado")


fig, ax = plt.subplots(facecolor='#ffffff')
plt.xlim(-10,10)
plt.ylim(-10,10)

#Imprimir plano cartesiano    
ejeX = [-10,10] #marcar las rectas del plano cartesiano 
ejeY = [-10,10]
ceros = [0,0] 
plt.plot(ejeX, ceros, 'k', linestyle='--') #se grafica una linea en el eje x
plt.plot(ceros, ejeY, 'k', linestyle='--') #se grafica una linea en el eje y

#Ingresar los archivos 
archivo_d = "archivo_d.txt"
archivo_x = "archivo_x.txt"

#Abrir el archivo de texto
with open(archivo_d) as f:
    lineas = f.readlines()

    for i in range(len(lineas)):
        v = lineas[i].replace('\n', '').split(' ')
        vector = list(map(int, v))
        d.append(vector)

    for i in range(len(d[0])):
        W.append([random.random(), random.random(), random.random()])


#Abrir el archivo de texto
with open(archivo_x) as f:
    lineas = f.readlines()

#Llenar la matriz X con los valores del archivo de texto
for i in range(len(lineas)):
    v = lineas[i].replace('\n', '').split(' ') #Funciones de python para trabajar cadenas 
    vector = list(map(float, v))
    ax.plot(vector[0],vector[1],'D',color=colores[int("".join(str(j) for j in d[i]),2)])
    X.append([1,vector[0],vector[1]])

#Interfaz Grafica 
mainwindow = Tk()
mainwindow.geometry('750x600')
mainwindow.wm_title('Practica 4')

#Valores de los pesos
Eta = StringVar(mainwindow)
Epocas_str = StringVar(mainwindow)
funcion_evaluar = IntVar(mainwindow)
error_minimo = StringVar(mainwindow)
#a = StringVar(mainwindow)

#Grafica en la interfaz 
canvas = FigureCanvasTkAgg(fig, master = mainwindow)
canvas.get_tk_widget().place(x=10, y=10, width=580, height=580) 


#Etiquetas
#a_label = Label(mainwindow, text = "A: ")
#a_label.place(x=600, y=40) 
#a_entry = Entry(mainwindow, textvariable=a)
#a_entry.place(x=600, y=70) 

Eta_label = Label(mainwindow, text = "ETA: ")
Eta_label.place(x=600, y=100) 
Eta_entry = Entry(mainwindow, textvariable=Eta)
Eta_entry.place(x=600, y=130) 

Epocas_label = Label(mainwindow, text = "Epocas: ")
Epocas_label.place(x=600, y=160) 
Epocas_entry = Entry(mainwindow, textvariable=Epocas_str)
Epocas_entry.place(x=600, y=190) 

Error_label = Label(mainwindow, text = "E. Minimo: ")
Error_label.place(x=600, y=220) 
Error_entry = Entry(mainwindow, textvariable=error_minimo)
Error_entry.place(x=600, y=250) 

#button
#logistica_rb = Radiobutton(mainwindow, text="Logistica", variable=funcion_evaluar, value=0)
#logistica_rb.place(x=600, y=280)

#button
start_button = Button(mainwindow, text="Iniciar", command=lambda:threading.Thread(target=Perceptron).start())
start_button.place(x=600, y=370)

mainwindow.mainloop()


