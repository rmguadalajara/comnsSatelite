import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import math
import functions as func
import pandas as pd
import math


def toggle_trace():
        if trace_var.get() == 1:
            for label_widget in trace_labels:
                label_widget.grid()
            for entry in trace_entries:
                entry.grid()
        else:
            for label_widget in trace_labels:
                label_widget.grid_remove()
            for entry in trace_entries:
                entry.grid_remove()

def calculate():
    try:
        # Realiza tus cálculos aquí
        # Por ahora, solo recopilamos los valores ingresados
        values = [float(entry.get().replace(',', '.')) for entry in entries]
        values.append(modulation_var.get())
        #messagebox.showinfo("Valores ingresados", f"Los valores ingresados son {values}")

        # Calcular elevación y azimut de ambas estaciones terrenas con respecto a la posición del satélite

        sat_long = math.radians(values[31])
        est1_long = math.radians(values[0])
        est1_lat = math.radians(values[1])
        est2_long = math.radians(values[3])
        est2_lat = math.radians(values[4])

        # Cálculo de la elevación
        elev_est1 = func.calculate_elevation(est1_lat, est1_long, sat_long, sat_long)
        elev_est2 = func.calculate_elevation(est2_lat, est2_long, sat_long, sat_long)

        # Cálculo del azimut
        azimut_est1 = func.calculate_azimuth(est1_lat, est1_long, sat_long, sat_long)
        azimut_est2 = func.calculate_azimuth(est2_lat, est2_long, sat_long, sat_long)
        
        pot_saturacion_ascendente = values[14]
        perdidas_antena_ascendente = values[15]
        Xmtr_pow_ascendente = func.Xmtr_pow(pot_saturacion_ascendente, perdidas_antena_ascendente)

        # revisar indices values
        diametro_antena_ascendente = values[12]
        frec_ascendente_ascendente = values[6]

        Xmtr_gain_ascendente = func.calculate_Xmtr_gain(pot_saturacion_ascendente, diametro_antena_ascendente, frec_ascendente_ascendente)

        backout_ascendente= values[15]
        pire_ascendente = func.calculate_pire(Xmtr_pow_ascendente, Xmtr_gain_ascendente, backout_ascendente)

       # messagebox.showinfo("Resultados", f"Elevación Estación 1: {elev_est1}\nAzimut Estación 1: {azimut_est1}\nElevación Estación 2: {elev_est2}\nAzimut Estación 2: {azimut_est2}\nXmtr_pow: {Xmtr_pow_ascendente}")

        # Calcular traza del satélite
        ground_station = {
            "latitude": est1_lat,
            "longitude": est1_long,
            "altitude": values[5]
        }
        # satellite = {satellite['semimajor_axis'], satellite['eccentricity'], satellite['inclination'], satellite['RAAN'], satellite['argument_of_perigee'], satellite['true_anomaly'], i)
        satellite = {
            "semimajor_axis": values[8],
            "eccentricity": values[9],
            "inclination": values[10],
            "RAAN": values[11],
            "argument_of_perigee": values[12],
            "true_anomaly": values[13]
        }
        
        #crea la ventana de resultados
        result_window = tk.Toplevel(root)
        
        # Crea los frames para cada grupo de resultados
        frame1 = tk.Frame(result_window)
        frame2 = tk.Frame(result_window)
        frame3 = tk.Frame(result_window)

        # Coloca los frames en la ventana de resultados
        frame1.pack(side="left", fill="both", expand=True)
        frame2.pack(side="left", fill="both", expand=True)
        frame3.pack(side="left", fill="both", expand=True)

        # Crea los Treeviews en cada frame
        tree1 = ttk.Treeview(frame1)
        tree2 = ttk.Treeview(frame2)
        tree3 = ttk.Treeview(frame3)

        # Configura los Treeviews
        for tree in [tree1, tree2, tree3]:
            tree["columns"] = ("value")
            tree.column("#0", width=150, minwidth=150)
            tree.column("value", width=150, minwidth=150)
            tree.heading("#0", text="Parámetro")
            tree.heading("value", text="Valor")
            tree.pack(fill="both", expand=True)
       

        # Agregar los parámetros calculados al Treeview
        tree1.insert("", "end", text="Elevación Estación 1", values=(elev_est1,))
        tree1.insert("", "end", text="Azimut Estación 1", values=(azimut_est1,))
        tree1.insert("", "end", text="Elevación Estación 2", values=(elev_est2,))
        tree1.insert("", "end", text="Azimut Estación 2", values=(azimut_est2,))
        tree1.insert("", "end", text="Xmtr_pow", values=(Xmtr_pow_ascendente,))

        #alinea el tree a la izquierda
        tree1.pack(side="left", fill="both", expand=True)
        #dale un titulo al tree view
        result_window.title("Resultados")
        #fale una anchura y altura al tree view
        result_window.geometry("400x400")
       # satellite_Trace = trc.calculate_satellite_trace(ground_station, satellite)
        #trc.plot_satellite_trace(ground_station, satellite_Trace)
    except ValueError as e:
        messagebox.showerror("Error", f"Entrada inválida: {str(e)}")

root = tk.Tk()
root.title("Formulario de entrada")
#maximiza la ventana root
root.state('zoomed')
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

labels_terrain_stations = {
    "ESTACIÓN TERRENA 1": [],
    "Longitud (rad) Est1": [-3.94],
    "Latitud (rad) Est1": [40.475],
    "Altura (Km) Est1": [0.6],
    "ESTACIÓN TERRENA 2": [""],
    "Longitud (rad) Est2": [-15.42],
    "Latitud (rad) Est2": [28.12],
    "Altura (Km) Est2": [0],
    "PARÁMETROS DE ENLACE": [],
    "F.asc (↑) (GHz)": [14.5],
    "F.desc (↓) (GHz)": [11],
    "Rb (Mbps)": [16000],
    "Modulación": ["BPSK"],
    "Roll-Off": [0.5],
    "rs (Km)": [42378],
    "rt (Km)": [6378],

}
labels_links = {
    "ENLACE ASCENDENTE": [],
    "Diametro Antena (m)_asc": [3],
    "Eficiencia _asc": [65],
    "Pot.Saturacion de HPA (W)": [100],
    "Pérdidas tx (dB)": [2],
    "G/T (dB/K)": [10],
    "Figura de ruido(dB)": [5],
    "BACKIN_asc(IB0)":[4],
    "BACKOUT_Asc(OB0)":[6],
    "ENLACE DESCENDENTE": [],
    "Diametro Antena (m)_desc": [2.6],
    "Eficiencia_desc": [85],
    "Pire (dBW)": [50],
    "Pérdidas rx (dB)": [1],
    "Fn (dB)": [4.5],
    "Tcielo (K)": [20],
    "Tsuelo (K)": [20],
    "pw":[10],
    "BACKIN_desc(IB0)":[4],
    "BACKOUT_desc(OB0)":[6],
    "Pérdidas tx_desc (dB)": [2]
}

labels_satelite = {
    "SATÉLITE": [],
    "Longitud (rad)": [-31],
    "semimajor_axis (Km)": [0],
    "eccentricity": [0],
    "inclination (rad)": [0],
    "RAAN (rad)": [0],
    "argument_of_perigee (rad)": [0],
    "true_anomaly (rad)": [0]
}
df_terrain_stations = pd.DataFrame.from_dict(labels_terrain_stations, orient="index")
df_links= pd.DataFrame.from_dict(labels_links, orient="index")
df_satelite = pd.DataFrame.from_dict(labels_satelite, orient="index")
entries = []
modulation_var = tk.StringVar(root)
modulation_var.set("BPSK")  # valor por defecto

for i, label in enumerate(labels_terrain_stations):
    if label in ["SATÉLITE", "ESTACIÓN TERRENA 1", "ESTACIÓN TERRENA 2", "PARÁMETROS DE ENLACE", "ENLACE ASCENDENTE", "ENLACE DESCENDENTE"]:
        label_widget = tk.Label(scrollable_frame, text=label, font=("Arial", 14), bg="lightblue")
        label_widget.grid(row=i, column=0, padx=10, pady=5, sticky="w")
    else:
        label_widget = tk.Label(scrollable_frame, text=label, font=("Arial", 12))
        label_widget.grid(row=i, column=0, padx=10, pady=5, sticky="w")

    if label == "Modulación":
        option_menu = tk.OptionMenu(scrollable_frame, modulation_var, *labels_terrain_stations[label])
        option_menu.grid(row=i, column=1, padx=10, pady=5, sticky="w")
    elif label not in ["SATÉLITE", "ESTACIÓN TERRENA 1", "ESTACIÓN TERRENA 2", "PARÁMETROS DE ENLACE", "ENLACE ASCENDENTE", "ENLACE DESCENDENTE"]:
        entry = tk.Entry(scrollable_frame)
        entry.insert(0, labels_terrain_stations[label][0])
        entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
        entries.append(entry)

for i, label in enumerate(labels_links):
    if label in ["ENLACE ASCENDENTE", "ENLACE DESCENDENTE"]:
        label_widget = tk.Label(scrollable_frame, text=label, font=("Arial", 14), bg="lightblue")
        label_widget.grid(row=i, column=2, padx=10, pady=5, sticky="w")
    else:
        label_widget = tk.Label(scrollable_frame, text=label, font=("Arial", 12))
        label_widget.grid(row=i, column=2, padx=10, pady=5, sticky="w")

    if label not in ["ENLACE ASCENDENTE", "ENLACE DESCENDENTE"]:
        entry = tk.Entry(scrollable_frame)
        entry.insert(0, labels_links[label][0])
        entry.grid(row=i, column=3, padx=10, pady=5, sticky="w")
        entries.append(entry)

trace_labels = []  # Define trace_labels list
trace_entries = []  # Define trace_entries list

for i, label in enumerate(labels_satelite):

    if label == "SATÉLITE":
        label_widget = tk.Label(scrollable_frame, text=label, font=("Arial", 14), bg="lightblue")
        label_widget.grid(row=i, column=4, padx=10, pady=5, sticky="w")
    else:
        label_widget = tk.Label(scrollable_frame, text=label, font=("Arial", 12))
        label_widget.grid(row=i, column=4, padx=10, pady=5, sticky="w")

        entry = tk.Entry(scrollable_frame)
        if len(labels_satelite[label]) > 0:
            entry.insert(0, labels_satelite[label][0])
        entry.grid(row=i, column=5, padx=10, pady=5, sticky="w")
        entries.append(entry)
        if label != "Longitud (rad)":
            # Add labels and entries to trace lists
            trace_labels.append(label_widget)
            trace_entries.append(entry)
        toggle_trace()
    trace_var = tk.IntVar()
    trace_checkbox = tk.Checkbutton(scrollable_frame, text="Calcular traza", variable=trace_var, font=("Arial", 12))
    trace_checkbox.grid(row=len(labels_terrain_stations), column=4, padx=10, pady=5, sticky="w")

    trace_checkbox.config(command=toggle_trace)

button = tk.Button(root, text="Calcular", command=calculate, font=("Arial", 12), bg="lightgreen")
button.pack(pady=10)


root.mainloop()

