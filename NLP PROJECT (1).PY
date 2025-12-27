import tkinter as tk
from tkinter import ttk
import pyttsx3
import speech_recognition as sr
import webbrowser
import threading
from datetime import datetime

root = tk.Tk()
root.title("NLP Project – NOVA ASSISTANT ")
root.geometry("1000x600")
root.configure(bg="#1E1E2D")

current_mode = tk.StringVar(value="Text to Speech")
status = tk.StringVar(value="Ready")
speech_rate = tk.IntVar(value=165)

def speak(text):
    def run():
        try:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            if len(voices) > 1:
                engine.setProperty('voice', voices[1].id)

            engine.setProperty('rate', speech_rate.get())
            root.after(0, lambda: status.set("🔊 Speaking..."))

            engine.say(text)
            engine.runAndWait()
            engine.stop()

            root.after(0, lambda: status.set(" Ready"))

        except Exception:
            root.after(0, lambda: status.set(" TTS failed"))

    threading.Thread(target=run, daemon=True).start()

def stop_speaking():
    status.set("⏹ Stopped")

def listen(process_command=False):
    r = sr.Recognizer()
    root.after(0, lambda: status.set(" Speak now..."))

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=7)
        except:
            status.set(" No speech detected")
            return

    root.after(0, lambda: status.set("Processing..."))

    try:
        text = r.recognize_google(audio)

        root.after(0, lambda: (
            output.delete(1.0, tk.END),
            output.insert(tk.END, text)
        ))

        if process_command:
            handle_command(text.lower())
        else:
            root.after(0, lambda: status.set("Speech converted"))

    except sr.UnknownValueError:
        status.set("Speech not understood")
    except sr.RequestError:
        status.set("Network error")

def handle_command(cmd):
    if "youtube" in cmd:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "whatsapp" in cmd:
        speak("Opening WhatsApp")
        webbrowser.open("https://web.whatsapp.com")

    elif "time" in cmd:
        now = datetime.now().strftime("%I:%M %p")
        speak(f"Current time is {now}")

    else:
        speak("Sorry, I did not understand")

def execute():
    mode = current_mode.get()

    if mode == "Text to Speech":
        text = input_box.get().strip()
        if text:
            speak(text)
            input_box.delete(0, tk.END)

    elif mode == "Rihab Project":
        threading.Thread(target=listen, daemon=True).start()

    elif mode == "nova Voice Command":
        threading.Thread(target=lambda: listen(True), daemon=True).start()

def on_mode_change():
    input_box.delete(0, tk.END)
    output.delete(1.0, tk.END)
    status.set(f"Mode: {current_mode.get()}")
    header.config(text=current_mode.get())

sidebar = tk.Frame(root, bg="#252A38", width=280)
sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

tk.Label(sidebar, text="NLP Project",
         font=("Segoe UI", 28, "bold"),
         fg="#38bdf8", bg="#252A38").pack(pady=20)

tk.Label(sidebar, text="NOVA Voice Assistant",
         fg="#94a3b8", bg="#252A38").pack()

style = ttk.Style()
style.theme_use("default")

style.configure("Custom.TRadiobutton",
                background="#252A38",
                foreground="#94a3b8",
                font=("Segoe UI", 14),
                padding=10)

style.configure("Custom.TButton",
                font=("Segoe UI", 14),
                padding=10)

for m in ["Text to Speech", "Rihab Project", "nova Voice Command"]:
    ttk.Radiobutton(sidebar, text=m,
                    variable=current_mode,
                    value=m,
                    command=on_mode_change,
                    style="Custom.TRadiobutton"
                    ).pack(anchor="w", padx=20, pady=15)

main = tk.Frame(root, bg="#1E1E2D")
main.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)

header = tk.Label(main, text="Text to Speech",
                  font=("Segoe UI", 22, "bold"),
                  fg="#22d3ee", bg="#1E1E2D")
header.pack(pady=15)

input_box = tk.Entry(main, font=("Segoe UI", 15),
                     width=50, bg="#EAEAEA", bd=0)
input_box.pack(pady=10)
input_box.bind("<Return>", lambda e: execute())

tk.Label(main, text="Speech Speed",
         fg="#94a3b8", bg="#1E1E2D",
         font=("Segoe UI", 12)).pack(pady=5)

ttk.Scale(main, from_=100, to=220,
          orient="horizontal",
          variable=speech_rate,
          length=300).pack()

btn_frame = tk.Frame(main, bg="#1E1E2D")
btn_frame.pack(pady=15)

ttk.Button(btn_frame, text="ACTIVATE",
           command=execute,
           width=15).grid(row=0, column=0, padx=10)

ttk.Button(btn_frame, text="STOP",
           command=stop_speaking,
           width=15).grid(row=0, column=1, padx=10)

output = tk.Text(main, height=7, width=70,
                 bg="#252A38", fg="#EAEAEA",
                 font=("Segoe UI", 13), bd=0)
output.pack(pady=15)

tk.Label(main, textvariable=status,
         fg="#94a3b8", bg="#1E1E2D").pack()

root.mainloop()
