import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import *
from sklearn.base import BaseEstimator
import random
import threading

class Perceptron(BaseEstimator):
    def fit(self, x, y):
        pass
    def predict(self, x):
        result = []
        for i in range(len(X)):
            if X[i] == d[i]:
                result.append(1)
            else:
                result.append(0)
        return np.array(result)
    
perceptron = Perceptron()

X = []
d = [] #arreglo de deseados
resultados_flag = True

def result_good():
    global resultados_flag
    resultados_flag = True

def result_bad():
    global resultados_flag
    resultados_flag = False

def plot_point(event):
    ix, iy = event.xdata, event.ydata
    print("{:.2f}".format(ix) + "/" + "{:.2f}".format(iy))
    X.append((ix, iy))
    if resultados_flag:
        d.append(1)
        ax.plot(ix,iy, 'Dg')
    else:
        d.append(0)
        ax.plot(ix,iy, 'Db')
    canvas.draw()

def clean():
    global X
    global d
    ax.cla()
    
    ejeX = [-10,10] #marcar las rectas del plano cartesiano 
    ejeY = [-10,10]
    ceros = [0,0] 
    plt.plot(ejeX, ceros, 'k') #se grafica una linea en el eje x
    plt.plot(ceros, ejeY, 'k') #se grafica una linea en el eje y

    canvas.draw()
    X = []
    d = []

def Perceptron():
    global W1, W2, Theta, Eta, Epocas_str, X, d
    Epocas = int(Epocas_str.get())
    error = True
    while Epocas and error:
        e = [] #arreglo de errores 
        for i in range(len(X)):
            Y = np.dot(X[i],[W1,W2]) - Theta >=0
            e.append(d[i]-Y)
            W1 = W1 + (float(Eta.get())*e[-1]*X[i][0])
            W2 = W2 + (float(Eta.get())*e[-1]*X[i][1])
            Theta = Theta - (float(Eta.get())*e[-1]*1)
        
        W = [W1,W2]

        #Generamos los valores para la funcion de la recta 
        m = -W[0]/W[1] #pendiente 
        b = Theta/W[1] #altura en la que se coloca el punto 

        ax.cla()

        #Imprimir plano cartesiano    
        ejeX = [-10,10] #marcar las rectas del plano cartesiano 
        ejeY = [-10,10]
        ceros = [0,0] 
        plt.plot(ejeX, ceros, 'k') #se grafica una linea en el eje x
        plt.plot(ceros, ejeY, 'k') #se grafica una linea en el eje y

        #Recorrer la matriz y graficar los puntos correspondientes 
        for i in range(len(X)):
            if X[i][0]*W[0] + X[i][1]*W[1] - Theta >=0: #Si es mayor o igual a cero pasa 
                plt.plot(X[i][0],X[i][1],'Dg')
            else:
                plt.plot(X[i][0],X[i][1],'Db')
        plt.axline((X[0][0], (X[0][0]*m)+b), slope=m, color='y') #Dibujar la recta 

        canvas.draw()
        W1_label.config(text = "Valor de W1: {:.2f}".format(W1))
        W2_label.config(text = "Valor de W2: {:.2f}".format(W2))
        Theta_label.config(text = "Valor de Theta: {:.2f}".format(Theta))

        if not(1 in e) and not(-1 in e):
            error = False

        Epocas = Epocas - 1
        

#Inicializar la grafica con mathplotlib
fig, ax = plt.subplots(facecolor='#FFFFFF')
fig.canvas.mpl_connect('button_press_event', plot_point)
plt.xlim(-10,10)
plt.ylim(-10,10)

#Imprimir plano cartesiano    
ejeX = [-10,10] #marcar las rectas del plano cartesiano 
ejeY = [-10,10]
ceros = [0,0] 
plt.plot(ejeX, ceros, 'k') #se grafica una linea en el eje x
plt.plot(ceros, ejeY, 'k') #se grafica una linea en el eje y

#Interfaz Grafica 
mainwindow = Tk()
mainwindow.geometry('600x700')
mainwindow.wm_title('Practica 2. Daniel Palma')

#Valores de los pesos
W1 = random.random()
W2 = random.random()
Theta = random.random()
Eta = StringVar(mainwindow)
Epocas_str = StringVar(mainwindow)

#Grafica en la interfaz 
canvas = FigureCanvasTkAgg(fig, master = mainwindow)
canvas.get_tk_widget().place(x=10, y=110, width=580, height=580)  


#Etiquetas
W1_label = Label(mainwindow, text = "Peso 1 (W1): {:.2f}".format(W1))
W1_label.place(x=10, y=20) 

W2_label = Label(mainwindow, text = "Peso 1 (W1): {:.2f}".format(W2))
W2_label.place(x=10, y=50) 

Theta_label = Label(mainwindow, text = "Theta: {:.2f}".format(Theta))
Theta_label.place(x=10, y=80) 

Eta_label = Label(mainwindow, text = "Valor de Eta: ")
Eta_label.place(x=160, y=20) 
Eta_entry = Entry(mainwindow, textvariable=Eta)
Eta_entry.place(x=230, y=20) 

Epocas_label = Label(mainwindow, text = "Epocas: ")
Epocas_label.place(x=160, y=50) 
Epocas_entry = Entry(mainwindow, textvariable=Epocas_str)
Epocas_entry.place(x=210, y=50) 


#button
start_button = Button(mainwindow, text="Graficar", command=lambda:threading.Thread(target=Perceptron).start())
start_button.place(x=400, y=20)

clean_button = Button(mainwindow, text="Limpiar", command=clean)
clean_button.place(x=480, y=20)

color_button = Button(mainwindow, text="Verdes", command=result_good, bg='green')
color_button.place(x=400, y=60)

color_button = Button(mainwindow, text="Azules", command=result_bad, bg='blue')
color_button.place(x=480, y=60)

mainwindow.mainloop()
