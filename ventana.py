from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk


app = Tk()
app.title('Memorama')
# asignamos valores por si los queremos cambiar
w = 800
h = 800
app.geometry(f"{w}x{h}")

frame = LabelFrame(
    app,
)

frame.pack(expand=True, fill=BOTH)

# inicializar lista de botones, para accesarlos despues
buttons = []

# numero de tamano del cuadro
num = 3

# esta variable determina si alguna carta esta clickeada
last_click = ''


def preparar_imagen(path):
    # funcion utilizada para preparar la foto para ser puesta en un boton

    # calcular tamano de foto para el boton
    cell_w = w // num - 50
    cell_h = h // num - 50
    iphoto = Image.open(path)
    img_resized = iphoto.resize((cell_w, cell_h))
    photo = ImageTk.PhotoImage(img_resized)
    return photo


def cambiar_imagen(index):
    print("click ")
    if last_click == '':
        last_click = index
    else:
        print(index)
    # funcion utilizada para cambiar la imagen del boton (la carta), cuando es clickeada
    for i in range(len(buttons)):
        if i != index:
            # si no es la imagen que fue clickeada, regresamos a photo original
            buttons[i].config(image=front_img)
            buttons[i].image = front_img

    buttons[index].config(image=back_img)
    buttons[index].image = back_img


# inicializar imagenes
# frente es la imagen con la que comenzamos, mientras que back es la que se revela

back_img = preparar_imagen('./ImagenesPython/2.png')
front_img = preparar_imagen('./ImagenesPython/1.png')


count = 0
for i in range(num):
    frame.rowconfigure(i, weight=1)
    for j in range(num):
        frame.columnconfigure(j, weight=1)

        b = Button(
            frame,
            image=front_img,
        )
        b.image = front_img
        # configuramos para agregar commando, tiene que ser una vez que la carta esta creada
        b.config(command=lambda index=count: cambiar_imagen(index))
        # agregamos uno a la variable count
        b.grid(row=i, column=j, sticky='nswe',
               padx=20, pady=20, ipadx=10, ipady=10)
        buttons.append(b)
        count += 1


# def resize_images(event):
#     print(event.width, event.height)
#     width = event.width // num - 40
#     height = event.height // num - 40
#     for id, button in enumerate(buttons):
#         # cambiar tamano
#         img_resized = photo_ejemplo.resize((width, height))
#         # convertir en Tk
#         photo = ImageTk.PhotoImage(img_resized)
#         # agregar foto a boton
#         button.config(image=photo)
#         button.image = photo  # keep reference

# para que las imagenes se adapten al tamano
# frame.bind('<Configure>', resize_images)

app.mainloop()
