import os
import unicodedata
import cv2
import subprocess
import sys
from tkinter import messagebox
import speech_recognition as sr
import winsound
import tkinter as tk
from PIL import Image, ImageTk
# Directorio de videos
VIDEO_FOLDER = os.path.join(os.path.dirname(__file__), 'videos')

# FUNCIONES DEL APARTADO DE TEXTO A SEÑAS


def reproducir_video_bienvenida(root, callback=None):
    video_path = os.path.join(VIDEO_FOLDER, 'bienvenida.mp4')
    if not os.path.exists(video_path):
        messagebox.showerror("Error", "No se encontró el video de bienvenida.")
        return

    cap = cv2.VideoCapture(video_path)

    video_label = tk.Label(root, bg="black")
    video_label.pack(fill="both", expand=True)

    def mostrar_frame():
        ret, frame = cap.read()
        if not ret:
            cap.release()
            video_label.destroy()
            if callback:
                callback()
            return

        # Obtener el tamaño actual de la ventana
        ancho_ventana = root.winfo_width()
        alto_ventana = root.winfo_height()

        # Redimensionar el frame al tamaño actual de la ventana
        frame = cv2.resize(frame, (ancho_ventana, alto_ventana))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

        root.after(1, mostrar_frame)

    # Asegura que se obtenga el tamaño real después de que la ventana haya sido inicializada
    root.update_idletasks()
    mostrar_frame()


def centrar_ventana(ventana, ancho, alto):
    """ Centra la ventana en la pantalla """
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    posicion_x = (pantalla_ancho // 2) - (ancho // 2)
    posicion_y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f'{ancho}x{alto}+{posicion_x}+{posicion_y}')


def traducir(entrada_texto):
    """ Procesa el texto ingresado y reproduce los videos correspondientes """
    texto = entrada_texto.get().strip().lower()
    if not texto:
        messagebox.showwarning("Aviso", "Por favor, ingresa un texto.")
        return

    texto = quitar_tildes(texto)
    fragmentos = encontrar_fragmentos(texto)
    videos_a_reproducir = []

    for fragmento in fragmentos:
        ruta_video = os.path.join(VIDEO_FOLDER, fragmento + '.mp4')
        if os.path.exists(ruta_video):
            videos_a_reproducir.append(ruta_video)
        else:
            for letra in fragmento:
                ruta_letra = os.path.join(VIDEO_FOLDER, letra + '.mp4')
                if os.path.exists(ruta_letra):
                    videos_a_reproducir.append(ruta_letra)
                else:
                    messagebox.showerror("Error", f"No se encontró el video para la letra: {letra}")

    if videos_a_reproducir:
        reproducir_videos(videos_a_reproducir)


def encontrar_fragmentos(texto):
    texto = ' '.join(texto.split())  # Elimina espacios extra
    palabras = texto.split()
    i = 0
    fragmentos = []

    while i < len(palabras):
        for j in range(len(palabras), i, -1):  # Busca la frase más larga posible
            frase = "_".join(palabras[i:j])  # Ejemplo: "buenos dias" → "buenos_dias"
            ruta_video = os.path.join(VIDEO_FOLDER, frase + '.mp4')
            if os.path.exists(ruta_video):
                fragmentos.append(frase)
                i = j
                break
        else:
            fragmentos.append(palabras[i])
            i += 1

    return fragmentos


def reproducir_videos(lista_videos):
    cv2.namedWindow('TRADUCCION', cv2.WINDOW_AUTOSIZE)
    video_width, video_height = 640, 640
    TARGET_FPS = 60

    for ruta_video in lista_videos:
        cap = cv2.VideoCapture(ruta_video)
        fps_video = cap.get(cv2.CAP_PROP_FPS)
        fps_video = fps_video if fps_video > 0 else 30
        delay = max(1, int(1000 / TARGET_FPS))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_resized = cv2.resize(frame, (video_width, video_height))
            cv2.imshow('TRADUCCION', frame_resized)
            if cv2.waitKey(delay) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return

        cap.release()

    cv2.destroyAllWindows()


def escuchar_microfono(BotonMicrofono, entrada_texto, root):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        BotonMicrofono.config(bg="red")
        root.update()
        winsound.Beep(1000, 300)

        try:
            audio = recognizer.listen(source, timeout=5)
            BotonMicrofono.config(bg="SystemButtonFace")
            root.update()
            texto = recognizer.recognize_google(audio, language='es-ES')
            entrada_texto.delete(0, tk.END)
            entrada_texto.insert(0, texto)
        except sr.WaitTimeoutError:
            messagebox.showerror("Tiempo agotado", "No detecté ningún sonido.")
        except sr.UnknownValueError:
            messagebox.showerror("Error", "No entendí lo que dijiste.")
        except sr.RequestError as e:
            messagebox.showerror("Error", f"No se pudo conectar al servicio de reconocimiento: {e}")
        finally:
            BotonMicrofono.config(bg="white")
            root.update()


def quitar_tildes(texto):
    """ Normaliza el texto eliminando las tildes """
    return ''.join(c for c in unicodedata.normalize('NFKD', texto) if not unicodedata.combining(c))


def validar_entrada(event):
    """ Permite solo letras, números, espacio, backspace y teclas direccionales """
    if event.keysym in ["BackSpace", "Left", "Right", "Up", "Down"]:
        return  # Permite navegación y Backspace
    if not event.char.isalnum() and event.char != ' ':
        return "break"  # Bloquea caracteres especiales



# FUNCION PARA EJECUTAR LA DETECION DE SENÑAS
def ejecutar_final_pred():
    """ Ejecuta el script final_pred.py en un proceso separado """
    subprocess.run([sys.executable, "final_pred.py"])