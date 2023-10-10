import matplotlib.pyplot as plt 
import pickle 
import os 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
from tkinter import *

X = []

def plot_point(event):
    ix, iy = event.xdata, event.ydata
    X.append((ix, iy))
    ax.plot(ix,iy,'Pk', linewidth=2, markersize=5)
    canvas.draw() 

def plot_backup_point():
    for point in X:
        ax.plot(point[0],point[1],'Pk', linewidth=2, markersize=5)
    canvas.draw()

def clean():
    global X
    ax.cla()  
    ejeX = [-3,3] 
    ejeY = [-3,3]
    ceros = [0,0] 
    plt.plot(ejeX, ceros, 'black') 
    plt.plot(ceros, ejeY, 'black') 
    plt.grid(axis='x', color='0.95')
    plt.grid(axis='y', color='0.95')
    canvas.draw()
    X = []

def Perceptron():
    w1 = float(W1.get())
    w2 = float(W2.get())
    bias = float(Bias_str.get())
    m = -w1/w2
    b = bias/w2
    ax.cla()
    ejeX = [-3,3]  
    ejeY = [-3,3]
    ceros = [0,0] 
    plt.plot(ejeX, ceros, 'black') 
    plt.plot(ceros, ejeY, 'black') 
    plt.grid(axis='x', color='0.95')
    plt.grid(axis='y', color='0.95')

    for i in range(len(X)):
        if X[i][0]*w1 + X[i][1]*w2 - bias >=0: 
            plt.plot(X[i][0],X[i][1],'Pb', linewidth=2, markersize=5)
        else:
            plt.plot(X[i][0],X[i][1],'Pr', linewidth=2, markersize=5)
    plt.axline((X[0][0], (X[0][0]*m)+b), slope=m, color='green') 

    canvas.draw()

def on_closing():
    if messagebox.askokcancel("Salir", "Esta seguro que desea salir?"):
        if len(X) != 0:
            if messagebox.askokcancel("Guardar", "Desea guardar sus cambios?"):
                with open("backup.pickle", "wb") as outfile:
                    pickle.dump(X, outfile)
        else:
            if os.path.exists('./backup.pickle'):
                if messagebox.askokcancel("Borrar", "No hay datos, desea eliminar el archivo de respaldo?"):
                    os.remove('./backup.pickle')
        mainwindow.destroy()

def check_backup():
    if os.path.exists('./backup.pickle'):
        if messagebox.askokcancel("Recuperar", "Desea reestablecer valores?"):
            global X
            with open("backup.pickle", "rb") as infile:
                X = pickle.load(infile)
            plot_backup_point()
        else:
            if messagebox.askokcancel("Borrar", "Desea borrar el respaldo?"):
                os.remove('./backup.pickle')

# Definir ventana
mainwindow = Tk()
mainwindow.geometry('600x640')
mainwindow.wm_title('Palma Garcia - Practica 1')
mainwindow.configure(bg='#34495E')

# Definir plano interactivo 
fig, ax = plt.subplots(facecolor='#66A999')
fig.canvas.mpl_connect('button_press_event', plot_point)
plt.xlim(-3,3)
plt.ylim(-3,3)

ejeX = [-3,3] 
ejeY = [-3,3]
ceros = [0,0] 
plt.plot(ejeX, ceros, 'black') 
plt.plot(ceros, ejeY, 'black') 
plt.grid(axis='x', color='0.95')
plt.grid(axis='y', color='0.95')

canvas = FigureCanvasTkAgg(fig, master = mainwindow)
canvas.get_tk_widget().place(x=10, y=45, width=580, height=580) 

# Definir Peso 1
W1_label = Label(mainwindow, text = "Peso 1: ")
W1_label.place(x=10, y=10) 
W1 = StringVar(mainwindow)
W1_entry = Entry(mainwindow, textvariable=W1, width='15')
W1_entry.place(x=55, y=10) 

# Definir Peso 2
W2_label = Label(mainwindow, text = "Peso 2: ")
W2_label.place(x=153, y=10) 
W2 = StringVar(mainwindow)
W2_entry = Entry(mainwindow, textvariable=W2, width='15')
W2_entry.place(x=200, y=10) 

# Definir Sesgo
Bias_label = Label(mainwindow, text = "Sesgo: ")
Bias_label.place(x=303, y=10) 
Bias_str = StringVar(mainwindow)
Bias_entry = Entry(mainwindow, textvariable=Bias_str, width='10')
Bias_entry.place(x=347, y=10) 

# Definir Boton de Calculo
start_button = Button(mainwindow, text="Calcular", command=Perceptron)
start_button.place(x=450, y=8)

# Definir Boton de Limpieza
start_button = Button(mainwindow, text="Limpiar", command=clean)
start_button.place(x=530, y=8)

# Ciclo principal
mainwindow.protocol("WM_DELETE_WINDOW", on_closing)
mainwindow.after_idle(check_backup)
mainwindow.mainloop()
