import pandas as pd
import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import filedialog
from PIL import Image, ImageTk
from guess import predict_image

def open_image(prediction_dict):
    # Open file dialog and get the selected file path
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[('Image Files', '*.png *.jpg *.jpeg *.gif *.bmp')]
    )
    
    if file_path:
        img = Image.open(file_path)
        img = img.resize((190, 200))
        tk_img = ImageTk.PhotoImage(img)
        image_label.config(image=tk_img)
        image_label.image = tk_img # Keep reference to avoid garbage collection
        # Update prediction dictionary with the new path
        prediction_dict['path'] = file_path

def run_prediction(prediction_dict):
    predict_image(prediction_dict)
    if prediction_dict.get('name'):
        prediction_label.config(
            text=f'Predicted: {prediction_dict["name"]}\nConfidence: {prediction_dict["confidence"]}%'
        )
    else:
        prediction_label.config(text='Predicted: None\n(Click Predict to classify)')

def show_message(prediction_dict):
    name = prediction_dict.get('name')
    match = poke_data[poke_data['name'].str.lower() == name.lower()]

    if match.empty:
        msgbox.showwarning("No encontrado", f"No se encontró información para '{name}'.")
        return

    japanese_name = match['japanese_name'].values[0]
    get_entry = match['pokedex_number'].values[0]
    get_type = match['type1'].values[0]
    get_weight = match['weight_kg'].values[0]
    get_generation = match['generation'].values[0]

    message = (
        f"Nombre original: {japanese_name}\n"
        f"Pokédex #: {get_entry}\n"
        f"Tipo: {get_type}\n"
        f"Peso: {get_weight} kg\n"
        f"Generación: {get_generation}"
    )

    msgbox.showinfo("Detalles del Pokémon", message)


# Set globals
prediction_dict = {}
geometry = "400x500"
geometry_size = geometry.split('x')
geometry_size = (int(geometry_size[0]), int(geometry_size[1]))
poke_data = pd.read_csv('pokemon_data.csv')

# Set up GUI
root = tk.Tk()
root.title('Poke Guess!')
root.geometry(geometry)

bg_img = Image.open('background.png')
bg_img = bg_img.resize(geometry_size)
bg_photo = ImageTk.PhotoImage(bg_img)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.image = bg_photo  # Keep reference

image_label = tk.Label(root)
image_label.place(relx=0.54, rely=0.325, anchor="center")

prediction_label = tk.Label(root, text='Predicted: None')
prediction_label.place(relx=0.5, rely=0.7, anchor="center")

info_button = tk.Button(root, text='Info', command=lambda: show_message(prediction_dict))
info_button.place(relx=0.05, rely=0.4, anchor="w")

load_button = tk.Button(root, text='Load Image', command=lambda: open_image(prediction_dict))
load_button.place(relx=0.5, rely=0.8, anchor="center")

predict_button = tk.Button(root, text='Predict', command=lambda: run_prediction(prediction_dict))
predict_button.place(relx=0.5, rely=0.9, anchor="center")

# Default placeholders
if not prediction_dict.get('name'):
    prediction_label.config(text='Predicted: None\n(Click Predict to classify)')
else:
    prediction_label.config(text=f'Predicted: {prediction_dict["name"]}\nConfidence: {prediction_dict["confidence"]}%')
if not prediction_dict.get('path'):
    img = Image.open('./placeholder.png')
    img = img.resize((190, 200))
    tk_img = ImageTk.PhotoImage(img)
    image_label.config(image=tk_img)
    image_label.image = tk_img # Keep reference to avoid garbage collection

root.mainloop()