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
        self.a = []
        self.n = []
        self.s = []

    def Suposicion(self, p):
        return self.sigmoidal(np.dot(p, self.w))
        
    def sigmoidal(self, x, derivative=False):
        if derivative == True:
            return x * (1 - x)
        return 1 / (1 + np.exp(-x))

    def ObtenerSalida(self, p):
        self.y = self.Suposicion(p)
    
    def forward_propagate(self, inputs):
        self.a = []
        self.n = []
        activation_values = inputs
        for w in self.weights:
            activation_values = np.insert(activation_values, 0, -1)            
            activation_values = activation_values.reshape((activation_values.shape[0], 1))
            self.a.append(activation_values)
            net_inputs = np.dot(w, activation_values)
            self.n.append(net_inputs)
            activation_values = self.sigmoidal(net_inputs)
        self.a.append(activation_values)
        return activation_values
    
    def update(self):#calula el promedido de los gradientes y actualiza pesos
        cont=self.cont
        for a in self.batch:
            for i in range(len(a)):
                a[i]=a[i]/cont
        for i in range(len(self.batch)):       
            self.weights[i] = self.batch[i]
        #print("cont:"+str(self.cont))

    def Jacobiana(self, error):#calcula las jacobianas
        self.s = []
        self.derivatives = []
        num_layers = len(self.a)
        output_layer = num_layers - 1
        for i in reversed(range(1, num_layers)):
            is_output_layer = i == output_layer
            a = self.a[i] if is_output_layer else np.delete(self.a[i], 0, 0)
            d = self.sigmoidal(a)
            derivatives = np.diag(d.reshape((d.shape[0],)))
            self.derivatives = [derivatives] + self.derivatives
            if is_output_layer:
                s = np.dot(derivatives, error)
                self.s.append(s)
            else:
                weights = np.delete(self.weights[i], 0, 1)
                jacobian_matrix = np.dot(derivatives, weights.T)#conseguimos nuestra matrix
                #print(jacobian_matrix)
                s = np.dot(jacobian_matrix, self.s[0])#sacarle inversa
                self.s = [s] + self.s

    def gradient_descent(self, lr):
        for i in range(len(self.weights)):
            new_w = self.weights[i] + lr * np.dot(self.s[i], self.a[i].T)
            self.weights[i] = new_w

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

def ColorDePunto(output):
    if output == 0:
        return "blue"
    if output == 1:
        return "red"       

class Window:
    def __init__(self, window):
        
        style = Style()
        style.configure('W.TButton', font =('Arial', 15, 'bold'),foreground = 'blue')
        
        self.window = window
        self.window.title("Practica 5")
        self.window.geometry("800x500")
        self.colors = ("blue", "red",)
        self.cmap = ListedColormap(self.colors[: len(np.unique([0, 1]))])

        self.points = np.zeros((0,3))
        self.pointsY = np.zeros(0)

        self.startBtn: Button
        self.pesosBtn: Button
        self.entryLabels = ["No Neuronas: ", "LR: ", "A: "]
        self.entries: Entry = []

        self.figure = None
        self.graph = None
        self.canvas = None
        self.limits = [-5, 5] #limites de grafica

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
       
        self.startBtn = Button(master=lowerFrame,style = 'W.TButton', text="Iniciar", command=self.start, width=8)
        self.startBtn.grid(row=1, column=0)
        self.figure = Figure(figsize=(6, 5), dpi=100,facecolor='#dcdcdc')
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
        neuronas = 10
        error=0.1
        EpocasTotales = 1000
        lr = 0.1
        epocas = 0
        hiddenLayer = np.array([])
        #crear pesos y capa salida
        outputLayer = Adaline(lr=lr, inputs=neuronas + 1, outputLayer=True)
        #crear capa entrada
        for i in range(neuronas):
            hiddenLayer = np.append(hiddenLayer, Adaline(lr=lr))
        #crear matriz identidad 
        grid = np.zeros((neuronas, len(self.inputs)))

        while epocas <= EpocasTotales:
            self.window.update()
            self.ConfigGrafica()
            #m= outputLayer.Jacobiana(error)
            #verificar los puntos de la grafica para hacerlos converger   
            for i in range(len(self.points)):
                [layer.ObtenerSalida(self.points[i]) for layer in hiddenLayer]
                outputLayer.ObtenerSalida(np.array([1] + [n.y for n in hiddenLayer]))
                outputLayer.hessiana(CapaAnteriorY=[1] + [n.y for n in hiddenLayer], PuntoY=self.pointsY[i])   
                [layer.hessiana(CapaAnteriorY=self.points[i], CapaSiguiente=outputLayer) for layer in hiddenLayer]
            # puntos grafica
            for i in range(len(self.points)):
                self.graph.plot(self.points[i][1], self.points[i][2], marker="o", c=ColorDePunto(self.pointsY[i]))
            print("N° de epoca: ", epocas)
            epocas += 1
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
        self.graph.plot(event.xdata,event.ydata,marker="o",c=ColorDePunto(deseado),)
        self.canvas.draw()

window = Tk()
app = Window(window)
window.mainloop()