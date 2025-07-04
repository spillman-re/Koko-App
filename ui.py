import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from app import (
    validar_entrada,
    traducir,
    ejecutar_final_pred,
    escuchar_microfono,
    reproducir_video_bienvenida,
    abrir_info
)

# ----- VENTANA PRINCIPAL -----
root = tk.Tk()
# root.resizable(False, False)
root.title("Koko App")
root.geometry("1000x600")  # Tamaño base más amplio
root.minsize(800,600)
root.configure(bg="white")
root.resizable(False, False)  # Permitir redimensionar
root.state('zoomed')  # Abrir en pantalla completa

# ----- FUNCIÓN PARA CARGAR INTERFAZ UNA VEZ FINALIZA EL VIDEO -----
def iniciar_ui():
    frame = tk.Frame(root, bg="white")
    frame.pack(expand=True, fill="both", padx=10, pady=10)

    # ----- Icono de la ventana -----
    icon_path = os.path.join(os.path.dirname(__file__), 'imagenes', 'icono.png')
    icon = Image.open(icon_path).resize((128, 128))
    icon = ImageTk.PhotoImage(icon)
    root.wm_iconphoto(True, icon)

    # ----- Logo de la aplicación -----
    logo_path = os.path.join(os.path.dirname(__file__), 'imagenes', 'logo.png')
    logo = Image.open(logo_path).resize((560, 160))
    logo_final = ImageTk.PhotoImage(logo)
    imagen = tk.Label(frame, image=logo_final, bg="white")
    imagen.image = logo_final
    imagen.pack(pady=(0, 0))

    # ----- CONTENEDOR PRINCIPAL -----
    contenedor_principal = tk.Frame(frame, bg="white")
    contenedor_principal.pack(expand=True, fill="both", pady=(0,0))

    contenedor_principal.columnconfigure(0, weight=1)
    contenedor_principal.columnconfigure(1, weight=1)
    contenedor_principal.rowconfigure(0, weight=1)

    color_cuadro = "#D9D9D9"

    # Estilo de los contenedores
    estilo_contenedor = {
        "bg": color_cuadro,
        "relief": "ridge",
        "borderwidth": 5,
        "width": 700,
        "height": 300
    }

    # ----- TEXTO A SEÑAS -----
    contenedor_izq = tk.Frame(contenedor_principal, **estilo_contenedor)
    contenedor_izq.grid(row=0, column=0, padx=20, pady=1)
    contenedor_izq.pack_propagate(False)

    TextoIndicador1 = tk.Label(contenedor_izq, text="Traduzca su mensaje de TEXTO a SEÑAS", font=("Arial", 20, "bold"), bg=color_cuadro)
    TextoIndicador1.pack(pady=(10))

    # Frame interno para Entry y botón de micrófono
    frame_input = tk.Frame(contenedor_izq, bg=color_cuadro)
    frame_input.pack(pady=5)
    entrada_texto = tk.Entry(frame_input, width=30, font=("Arial", 20, "italic"))
    entrada_texto.pack(side="left", padx=5)
    entrada_texto.bind("<KeyPress>", validar_entrada)

    # ----- Botón Micrófono -----
    microfono_path = os.path.join(os.path.dirname(__file__), 'imagenes', 'microfono.png')
    microfono = Image.open(microfono_path).resize((50, 50))
    microfono_final = ImageTk.PhotoImage(microfono)

    def on_hover(event):
        BotonMicrofono.config(cursor="hand2")
        BotonInfo.config(cursor="hand2")
        BotonEnviarSena.config(cursor="hand2")
        BotonEnviarTexto.config(cursor="hand2")
    def on_leave(event):
        BotonMicrofono.config(cursor="")
        BotonInfo.config(cursor="")
        BotonEnviarSena.config(cursor="")
        BotonEnviarTexto.config(cursor="")

    BotonMicrofono = tk.Button(
        frame_input,
        image=microfono_final,
        bg="white",
        activebackground="#A9A9A9",
        command=lambda: escuchar_microfono(BotonMicrofono, entrada_texto, root)
    )
    BotonMicrofono.pack(side="left", padx=1)
    BotonMicrofono.bind("<Enter>", on_hover)
    BotonMicrofono.bind("<Leave>", on_leave)
    BotonMicrofono.image = microfono_final

    # ----- Botón para traducir -----
    BotonEnviarTexto = tk.Button(
        contenedor_izq,
        text="Traducir",
        font=("Arial", 20, "bold"),
        width=20,
        height=2,
        bg="#00C853",
        fg="white",
        command=lambda: traducir(entrada_texto, root)
    )
    BotonEnviarTexto.pack(pady=10)
    BotonEnviarTexto.bind("<Enter>", on_hover)
    BotonEnviarTexto.bind("<Leave>", on_leave)

    # ----- SEÑAS A TEXTO -----
    contenedor_der = tk.Frame(contenedor_principal, **estilo_contenedor)
    contenedor_der.grid(row=0, column=1, padx=20, pady=1)
    contenedor_der.pack_propagate(False)

    TextoIndicador2 = tk.Label(contenedor_der, text="Traduzca su mensaje de SEÑAS a TEXTO", font=("Arial", 20, "bold"), bg=color_cuadro)
    TextoIndicador2.pack(pady=(30, 10))

    BotonEnviarSena = tk.Button(
        contenedor_der,
        text="Detectar",
        font=("Arial", 20, "bold"),
        width=20,
        height=2,
        bg="#2196F3",
        fg="white",
        command=lambda: ejecutar_final_pred(root)
    )
    BotonEnviarSena.pack(pady=10)
    BotonEnviarSena.bind("<Enter>", on_hover)
    BotonEnviarSena.bind("<Leave>", on_leave)

    # ----- Pie de ventana -----
    TextoTestApp = tk.Label(frame, text="DevU", font=("Arial", 16, "italic"), fg="gray", bg="white")
    TextoTestApp.place(relx=1, rely=1, anchor="se", x=-10, y=-10)
    
    libro_path = os.path.join(os.path.dirname(__file__), 'imagenes', 'libro_info.png')
    libro = Image.open(libro_path).resize((70, 70))
    libro_info = ImageTk.PhotoImage(libro)
    BotonInfo = tk.Button(
        root,
        image=libro_info,
        bg="white",
        activebackground="#A9A9A9",
        command=abrir_info
    )
    BotonInfo.pack(padx=5)
    BotonInfo.bind("<Enter>", on_hover)
    BotonInfo.bind("<Leave>", on_leave)
    BotonInfo.image = libro_info
    BotonInfo.place(relx=0.5, rely=0.90, anchor="center")

# ----- Reproducir video de bienvenida dentro de la ventana -----
reproducir_video_bienvenida(root, callback=iniciar_ui)

# ----- Iniciar loop principal -----
root.mainloop()