from dotenv import load_dotenv
import os
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import filedialog
from tkinter.colorchooser import askcolor
from PIL import ImageTk, Image
import openai

load_dotenv()

openai.api_key = os.environ.get("API_KEY")

# Définition des widgets en tant que variables globales
window = None
bg_label = None
chat_box = None
input_box = None

def send_message():
    message = input_box.get()

    if message.lower() == "clear":
        chat_box.delete(1.0, tk.END)
    else:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )

        reply = response["choices"][0]["message"]["content"]

        chat_box.insert(tk.END, "You: " + message + "\n\n")
        chat_box.insert(tk.END, "IA: " + reply + "\n\n")

    input_box.delete(0, tk.END)

def quitter():
    window.destroy()

def change_text_color():
    color = askcolor(color="#00ffff")[1]  # Couleur de départ définie sur cyan
    chat_box.configure(fg=color)

def change_background_image():
    file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg;*.gif')])
    if file_path:
        image = Image.open(file_path)
        image = image.resize((1080, 720), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        chat_box.configure(bg="#003333", highlightbackground="#00ffff", highlightcolor="#00ffff", highlightthickness=1)
        bg_label.configure(image=photo)
        bg_label.image = photo
    else:
        chat_box.configure(bg="#003333", highlightbackground="#00ffff", highlightcolor="#00ffff", highlightthickness=1)
        bg_label.configure(image="")
        bg_label.image = None

def main():
    global window, bg_label, chat_box, input_box

    window = tk.Tk()
    window.title("Chat Gamer")
    window.geometry("1080x720")
    window.configure(bg="#003333")

    bg_label = tk.Label(window, bg="#003333")
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    chat_box = scrolledtext.ScrolledText(window, width=80, height=30, bg="#000000", fg="#00ffff", insertbackground="#00ffff", highlightbackground="#00ffff", highlightcolor="#00ffff", highlightthickness=1)
    chat_box.pack(pady=10)

    input_box = tk.Entry(window, width=70, bg="#000000", fg="#00ffff", insertbackground="#00ffff", font=("Arial", 14))
    input_box.pack(pady=10)

    button_frame = ttk.Frame(window)
    button_frame.pack(pady=(0, 10))

    send_button = tk.Button(button_frame, text="Envoyer", command=send_message, bg="#009999", font=("Arial", 14, "bold"))
    send_button.pack(side=tk.LEFT, padx=5)

    quitter_button = tk.Button(button_frame, text="Quitter", command=quitter, bg="#009999", font=("Arial", 14, "bold"),)
    quitter_button.pack(side=tk.LEFT, padx=5)

    color_button = ttk.Button(window, text="Couleur du texte", command=change_text_color, style="Cyan.TButton")
    color_button.pack(pady=(0, 10))

    bg_image_button = ttk.Button(window, text="Changer Background", command=change_background_image, style="Cyan.TButton")
    bg_image_button.pack()

    style = ttk.Style()
    style.configure("Cyan.TButton", background="#00ffff", foreground="#000000", font=("Arial", 12, "bold"), width=20, padding=8)

    window.bind('<Return>', lambda event: send_message())

    window.mainloop()

if __name__ == "__main__":
    main()
