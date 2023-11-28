import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import math


def calculate():
    try:
        # Realiza tus cálculos aquí
        # Por ahora, solo recopilamos los valores ingresados
        values = [float(entry.get()) for entry in entries]
        values.append(modulation_var.get())
        messagebox.showinfo("Valores ingresados", f"Los valores ingresados son {values}")

        # Calcular elevación y azimut de ambas estaciones terrenas con respecto a la posición del satélite
        sat_long = values[1]
        est1_long = values[3]
        est1_lat = values[4]
        est2_long = values[6]
        est2_lat = values[7]

        # Cálculo de la elevación
        elev_est1 = math.degrees(math.asin(math.sin(est1_lat) * math.sin(sat_long - est1_long) + math.cos(est1_lat) * math.cos(sat_long - est1_long) * math.cos(est1_long - sat_long)))
        elev_est2 = math.degrees(math.asin(math.sin(est2_lat) * math.sin(sat_long - est2_long) + math.cos(est2_lat) * math.cos(sat_long - est2_long) * math.cos(est2_long - sat_long)))

        # Cálculo del azimut
        azimut_est1 = math.degrees(math.atan2(math.sin(est1_long - sat_long) * math.cos(est1_lat), math.cos(sat_long) * math.cos(est1_lat) * math.sin(est1_long - sat_long) - math.sin(sat_long) * math.cos(est1_lat)))
        azimut_est2 = math.degrees(math.atan2(math.sin(est2_long - sat_long) * math.cos(est2_lat), math.cos(sat_long) * math.cos(est2_lat) * math.sin(est2_long - sat_long) - math.sin(sat_long) * math.cos(est2_lat)))

        messagebox.showinfo("Resultados", f"Elevación Estación 1: {elev_est1}\nAzimut Estación 1: {azimut_est1}\nElevación Estación 2: {elev_est2}\nAzimut Estación 2: {azimut_est2}")
    except ValueError as e:
        messagebox.showerror("Error", f"Entrada inválida: {str(e)}")

root = tk.Tk()
root.title("Formulario de entrada")

# Crear un frame para el contenido del formulario
frame = ttk.Frame(root)
frame.pack(fill="both", expand=True)

# Crear un canvas con scrollbar
canvas = tk.Canvas(frame)
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

labels = [
    "SATÉLITE",
    "Longitud (rad)",
    "ESTACIÓN TERRENA 1",
    "Longitud (rad)",
    "Latitud (rad)",
    "Altura (Km)",
    "ESTACIÓN TERRENA 2",
    "Longitud (rad)",
    "Latitud (rad)",
    "Altura (Km)",
    "PARÁMETROS DE ENLACE",
    "F.asc (↑) (GHz)",
    "F.desc (↓) (GHz)",
    "Rb (Mbps)",
    "Modulación",
    "Roll-Off",
    "rs (Km)",
    "rt (Km)",
]
labels_2 = [
    "ENLACE ASCENDENTE",
    "Diametro Antena (m)",
    "Eficiencia",
    "Pot.Saturacion de HPA (W)",
    "Pérdidas tx (dB)",
    "G/T (dB/K)",
    "Figura de ruido(dB)",
    "ENLACE DESCENDENTE",
    "Diametro Antena (m)",
    "Eficiencia",
    "Pot.Saturacion de HPA (W)",
    "Pérdidas tx (dB)",
    "G/T (dB/K)",
    "Figura de ruido(dB)"
]
entries = []
modulation_var = tk.StringVar(root)
modulation_var.set("BPSK")  # valor por defecto

for i, label in enumerate(labels):
    if label in ["SATÉLITE", "ESTACIÓN TERRENA 1", "ESTACIÓN TERRENA 2", "PARÁMETROS DE ENLACE", "ENLACE ASCENDENTE", "ENLACE DESCENDENTE"]:
        label_widget = tk.Label(scrollable_frame, text=label, font=("Arial", 14), bg="lightblue")
        label_widget.grid(row=i, column=0, padx=10, pady=5, sticky="w")
    else:
        label_widget = tk.Label(scrollable_frame, text=label, font=("Arial", 12))
        label_widget.grid(row=i, column=0, padx=10, pady=5, sticky="w")

    if label == "Modulación":
        option_menu = tk.OptionMenu(scrollable_frame, modulation_var, "BPSK", "QPSK", "16-QAM")
        option_menu.grid(row=i, column=1, padx=10, pady=5, sticky="w")
    elif label not in ["SATÉLITE", "ESTACIÓN TERRENA 1", "ESTACIÓN TERRENA 2", "PARÁMETROS DE ENLACE", "ENLACE ASCENDENTE", "ENLACE DESCENDENTE"]:
        entry = tk.Entry(scrollable_frame)
        entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
        entries.append(entry)

for i, label in enumerate(labels_2):
    if label in ["ENLACE ASCENDENTE", "ENLACE DESCENDENTE"]:
        label_widget = tk.Label(scrollable_frame, text=label, font=("Arial", 14), bg="lightblue")
        label_widget.grid(row=i, column=2, padx=10, pady=5, sticky="w")
    else:
        label_widget = tk.Label(scrollable_frame, text=label, font=("Arial", 12))
        label_widget.grid(row=i, column=2, padx=10, pady=5, sticky="w")

    if label not in ["ENLACE ASCENDENTE", "ENLACE DESCENDENTE"]:
        entry = tk.Entry(scrollable_frame)
        entry.grid(row=i, column=3, padx=10, pady=5, sticky="w")
        entries.append(entry)

button = tk.Button(root, text="Calcular", command=calculate, font=("Arial", 12), bg="lightgreen")
button.pack(pady=10)

root.mainloop()