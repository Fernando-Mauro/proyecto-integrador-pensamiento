from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import font

app = Tk()
app.title('Menu Memorama')
# asignamos valores por si los queremos cambiar
w = 800
h = 800
app.geometry(f"{w}x{h}")

frame = LabelFrame(
    app
)

# imagen de fondo
image = Image.open('photos/nubes.jpg')
image = image.resize((800, 800))
bg_image = ImageTk.PhotoImage(image)

bg_label = Label(frame, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
# configurar columnas
for i in range(3): 
    frame.columnconfigure(i, weight=1)

# configurar rows
frame.rowconfigure(0, weight = 3)
frame.rowconfigure(1, weight = 1)
frame.rowconfigure(2, weight = 1)
frame.rowconfigure(3, weight = 1)
frame.rowconfigure(4, weight=1)


        
frame.pack(
    expand=True, 
    fill=BOTH, 
)

# asignamos en variables los paddings internos de los botones
bipady = 10
bipadx = 100

label = Label(
    frame, 
    text = "Compurama!", 
    font=("Lato", 40)
)

label.grid(
    column = 1, 
    row = 0, 
    ipady=25, 
    pady=(0, 35),
    sticky='sew'
)

empezar = Button(
    frame, 
    text="Empezar", 
)

empezar.grid(
    column = 1, 
    row = 1, 
    ipady = bipady, 
    ipadx = bipadx,
    sticky='nswe', 
    pady = 20, 
    
)

puntajes = Button(
    frame, 
    text="Puntajes maximos", 
)

puntajes.grid(
    column = 1, 
    row = 2, 
    ipady = bipady, 
    ipadx = bipadx, 
    sticky='nswe', 
    pady = 20, 

)

salir = Button(
    frame, 
    text="Salir", 
)

salir.grid(
    column = 1, 
    row = 3, 
    ipady = bipady, 
    ipadx = bipadx, 
    sticky='nswe', 
    pady = 20, 


)

# declaramos fuentes
fuente = font.Font(family='Lato', size=12)
botones = [empezar, puntajes, salir]
for boton in botones: 
    boton.config(font=fuente)


app.mainloop()

