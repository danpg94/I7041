from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import ListedColormap
from matplotlib.figure import Figure
from tkinter.ttk import *
import numpy as np

class Adaline: # clase adaline 
    def __init__(self, lr, inputs=3, outputLayer=False): # constructor
        self.lr = lr
        self.inputs = inputs
        self.outputLayer = outputLayer
        self.w = np.zeros(inputs)
        for i in range(self.inputs):
            self.w[i] = np.random.uniform(-1, 1)
        self.y = np.zeros(0)
        self.GradienteLocal = 0
        self.derivatives = []

    def Suposicion(self, p):
        return self.sigmoidal(np.dot(p, self.w))
        
    def sigmoidal(self, x, derivative=False):
        if derivative == True:
            return x * (1 - x)
        return 1 / (1 + np.exp(-x))

    def ObtenerSalida(self, p):
        self.y = self.Suposicion(p)

    def GradienteLocalFunc(self, PuntoY, CapaSiguiente=None):
        sigmoidal = self.sigmoidal(self.y, True)
        if self.outputLayer == True:
            error = PuntoY - self.y
            return sigmoidal * error
        wSum = sum(CapaSiguiente.w)
        return sigmoidal * wSum * CapaSiguiente.GradienteLocal

    def hessiana(self, CapaAnteriorY=None, CapaSiguiente=None, PuntoY=None):
        if self.outputLayer == True:
            self.GradienteLocal = self.GradienteLocalFunc(PuntoY=PuntoY)
        else:
            self.GradienteLocal = self.GradienteLocalFunc(
                PuntoY=PuntoY, CapaSiguiente=CapaSiguiente
            )
        for i in range(self.inputs):
            self.w[i] += self.GradienteLocal * CapaAnteriorY[i] * self.lr      

class Window:
    def __init__(self, window):
        
        style = Style()
        style.configure('W.TButton', font =('Arial', 15, 'bold'),foreground = 'blue')
        
        self.window = window
        self.window.title("Practica 5&6")
        self.window.geometry("1000x500")
        self.colors = ("blue", "red")
        self.cmap = ListedColormap(self.colors[: len(np.unique([0, 1]))])

        self.points = np.zeros((0,3))
        self.pointsY = np.zeros(0)

        self.startBtn: Button
        self.clear: Button
        
        self.eta_str = StringVar(self.window)
        self.epochs_str = StringVar(self.window)
        self.neurons_str = StringVar(self.window)    

        self.figure = None
        self.graph = None
        self.canvas = None
        self.limits = [-10, 10] #limites de grafica

        self.x = np.linspace(self.limits[0], self.limits[1], 50)
        self.y = np.linspace(self.limits[0], self.limits[1], 50)
        self.xx, self.yy = np.meshgrid(self.x, self.y)
        self.inputs = np.array([np.ones(len(self.xx.ravel())), self.xx.ravel(), self.yy.ravel()]).T
        self.outputs = np.zeros(len(self.inputs))
        self.startUI()

    def startUI(self):
        actionFrame = Frame(self.window)
        actionFrame.grid(row=0, column=0, padx=20, ipady=10)
        upperFrame = Frame(actionFrame)
        upperFrame.grid(row=1, column=0)
        middleFrame = Frame(actionFrame)
        middleFrame.grid(row=0, column=0)
        lowerFrame = Frame(actionFrame)
        lowerFrame.grid(row=2, column=0)
       
        self.n_neurons_lbl = Label(master=lowerFrame, text="Numero de Neuronas:")
        self.n_neurons_lbl.grid(row=0, column=0)
        self.n_neurons = Entry(master=lowerFrame, textvariable=self.neurons_str, width=10)
        self.n_neurons.grid(row=0, column=1)
        
        self.eta_lbl = Label(master=lowerFrame, text="Tasa de aprendizaje:")
        self.eta_lbl.grid(row=1, column=0)
        self.eta_entry = Entry(master=lowerFrame, textvariable=self.eta_str, width=10)
        self.eta_entry.grid(row=1, column=1)
        
        self.epochs_lbl = Label(master=lowerFrame, text="Epocas:")
        self.epochs_lbl.grid(row=2, column=0)
        self.epochs_entry = Entry(master=lowerFrame, textvariable=self.epochs_str, width=10)
        self.epochs_entry.grid(row=2, column=1)
        
        self.startBtn = Button(master=lowerFrame,style = 'W.TButton', text="Iniciar", command=self.start, width=8)
        self.startBtn.grid(row=3, column=0)
        
        self.figure = Figure(figsize=(6, 5), dpi=100,facecolor='#acacac')
        self.graph = self.figure.add_subplot(111)
        self.ConfigGrafica()

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.window)
        self.canvas.get_tk_widget().grid(row=0, column=2)

        cid = self.figure.canvas.mpl_connect('button_press_event', self.onClick)

    def ConfigGrafica(self):
        self.graph.cla()
        self.graph.set_xlim([self.limits[0], self.limits[1]])
        self.graph.set_ylim([self.limits[0], self.limits[1]])
        self.graph.grid(color='r', linestyle='--', linewidth=.3)
        self.graph.axhline(y=0, color="k",linewidth=.6)
        self.graph.axvline(x=0, color="k",linewidth=.6)

    def start(self): # Obtener valores
        neuronas = int(self.neurons_str.get())
        epocas = int(self.epochs_entry.get())
        lr = float(self.eta_entry.get())
        hiddenLayer = np.array([])
        #crear pesos y capa salida
        outputLayer = Adaline(lr=lr, inputs=neuronas + 1, outputLayer=True)
        #crear capa entrada
        for i in range(neuronas):
            hiddenLayer = np.append(hiddenLayer, Adaline(lr=lr))
        #crear matriz identidad 
        grid = np.zeros((neuronas, len(self.inputs)))

        while epocas:
            self.window.update()
            self.ConfigGrafica()
            #verificar los puntos de la grafica para hacerlos converger   
            for i in range(len(self.points)):
                [layer.ObtenerSalida(self.points[i]) for layer in hiddenLayer]
                outputLayer.ObtenerSalida(np.array([1] + [n.y for n in hiddenLayer]))
                outputLayer.hessiana(CapaAnteriorY=[1] + [n.y for n in hiddenLayer], PuntoY=self.pointsY[i])   
                [layer.hessiana(CapaAnteriorY=self.points[i], CapaSiguiente=outputLayer) for layer in hiddenLayer]
            # puntos grafica
            for i in range(len(self.points)):
                self.graph.plot(self.points[i][1], self.points[i][2], marker="o", c=self.ColorDePunto(self.pointsY[i]))
            print("N° de epocas restantes: ", epocas)
            epocas -= 1
            #imprimir funcion contorno
            for j in range(neuronas):
                grid[j] = hiddenLayer[j].Suposicion(self.inputs)
            self.outputs = [outputLayer.Suposicion(np.concatenate((np.array([1]), [g]), axis=None)) for g in grid.T]
            self.outputs = np.array(self.outputs)
            self.graph.contourf(self.xx, self.yy, self.outputs.reshape(self.xx.shape), cmap="seismic")
            self.canvas.draw()

    def onClick(self, event: Event):
        deseado: int
        if event.button == 1:
            deseado = 0
        elif event.button == 3:
            deseado = 1
        self.points = np.append(self.points, [[1, float(event.xdata), float(event.ydata)]], axis=0)
        self.pointsY = np.append(self.pointsY, [deseado])
        self.graph.plot(event.xdata,event.ydata,marker="o",c=self.ColorDePunto(deseado),)
        self.canvas.draw()

    def ColorDePunto(self, output):
        if output == 0:
            return self.colors[0]
        if output == 1:
            return self.colors[1] 

window = Tk()
app = Window(window)
window.mainloop()