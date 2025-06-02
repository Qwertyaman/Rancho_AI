import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext, ttk
from PIL import Image, ImageTk
import openai
import pyttsx3
import random
import threading
import math
import time

# ==== OpenAI & TTS Setup ====
OPENAI_API_KEY="Key"
client = openai.OpenAI(api_key=OPENAI_API_KEY)
engine = pyttsx3.init()
engine.setProperty('rate', 170)

# ==== Global Variables ====
stars = 0
conversation = []
class_level = 1

# ==== TTS ====
def speak(text):
    engine.say(text)
    engine.runAndWait()

# ==== Canvas Animations ====
def run_splash_animation():
    canvas.delete("all")
    radius = 40
    center_x, center_y = 150, 150
    num_points = 12
    angle_offset = 0

    def animate():
        nonlocal angle_offset
        canvas.delete("anim")
        for i in range(num_points):
            angle = math.radians(i * (360 / num_points) + angle_offset)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            canvas.create_oval(x-5, y-5, x+5, y+5, fill="gold", tags="anim")
        angle_offset += 10
        if angle_offset < 360:
            root.after(100, animate)
        else:
            canvas.delete("anim")

    animate()

def run_thinking_animation():
    canvas.delete("all")
    steps = 0
    colors = ["purple", "blue", "cyan", "green"]

    def animate():
        nonlocal steps
        canvas.delete("anim")
        for i in range(4):
            x = 80 + i * 40
            canvas.create_oval(x, 140, x+20, 160, fill=colors[i % len(colors)], tags="anim")
        steps += 1
        if steps < 10:
            root.after(200, animate)
        else:
            canvas.delete("anim")

    animate()

# ==== Conversation Initialization ====
def init_conversation(level):
    return [
        {
            "role": "system",
            "content": (
                f"You are AI Rancho 🤖, an AI tutor that strictly helps students from Nursery to Class 12 "
                f"with CBSE NCERT subjects and age-appropriate basics. You are now helping a student from Class {level}. "
                "Only answer questions from this curriculum scope. If something is out of syllabus, reply: "
                "'Sorry, that’s out of my galaxy! 😢'. Keep things cheerful, simple, and use emojis a lot! 🎉📚"
            )
        }
    ]

# ==== Chat with OpenAI ====
def chat_with_openai(user_input):
    global conversation
    chat_area.insert(tk.END, f"\nYou: {user_input}\n")
    conversation.append({"role": "user", "content": user_input})
    chat_area.insert(tk.END, "AI Rancho 🤖 is thinking...\n")
    chat_area.see(tk.END)
    run_thinking_animation()

    def ask():
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation,
                temperature=0.7
            )
            bot_reply = response.choices[0].message.content
            conversation.append({"role": "assistant", "content": bot_reply})
            chat_area.insert(tk.END, f"AI Rancho 🤖: {bot_reply}\n\n")
            chat_area.see(tk.END)
            speak(bot_reply)
        except Exception as e:
            chat_area.insert(tk.END, f"Error: {e}\n")
            speak("Oops! Something went wrong!")

    threading.Thread(target=ask).start()

# ==== Quiz Mode ====
def quiz_mode():
    global stars
    questions = [
        ("What is the capital of India?", "New Delhi"),
        ("What planet do we live on?", "Earth"),
        ("Solve: 6 + 3 x 2", "12"),
    ]
    q, a = random.choice(questions)
    user_ans = simpledialog.askstring("Quiz Time! 🧠", f"❓ {q}")
    if user_ans:
        if user_ans.strip().lower() == a.lower():
            stars += 1
            msg = "✅ Correct! 🌟 You earned a star!"
        else:
            msg = f"❌ Oops! The correct answer was: {a}"
        star_label.config(text=f"🌟 Stars: {stars}")
        chat_area.insert(tk.END, f"\n{msg}\n\n")
        speak(msg)

# ==== Class Selection ====
def on_class_selected(event):
    global class_level, conversation
    class_level = class_var.get()
    conversation = init_conversation(class_level)
    chat_area.insert(tk.END, f"\n🤖 Starting help for Class {class_level}. Ask me anything!\n\n")
    speak(f"Hello! I'm your AI Rancho for Class {class_level}!")

# ==== Send Button ====
def on_send():
    user_input = user_entry.get()
    if user_input.strip() != "":
        user_entry.delete(0, tk.END)
        chat_with_openai(user_input)

# ==== GUI ====
root = tk.Tk()
root.title("AI Rancho 🤖")
root.geometry("600x700")

# ==== Blinking Background ====
img1 = ImageTk.PhotoImage(Image.open(r"D:\New folder\Screenshot 2025-04-16 153359.png").resize((600, 700)))
img2 = ImageTk.PhotoImage(Image.open(r"D:\New folder\anime.png").resize((600, 700)))
bg_label = tk.Label(root)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

current_img = [1]

def blink_background():
    if current_img[0] == 1:
        bg_label.config(image=img1)
        current_img[0] = 2
    else:
        bg_label.config(image=img2)
        current_img[0] = 1
    root.after(700, blink_background)

blink_background()

# ==== Interface Widgets ====
title = tk.Label(root, text="🤖 AI Rancho", font=("Helvetica", 20, "bold"), bg="#ffffff")
title.place(relx=0.5, y=20, anchor="center")

class_frame = tk.Frame(root, bg="#ffffff")
class_frame.place(relx=0.5, y=60, anchor="center")
tk.Label(class_frame, text="Select Class:", bg="#ffffff").pack(side=tk.LEFT, padx=5)
class_var = tk.IntVar(value=1)
class_dropdown = ttk.Combobox(class_frame, textvariable=class_var, values=list(range(0, 13)), width=5)
class_dropdown.pack(side=tk.LEFT)
class_dropdown.bind("<<ComboboxSelected>>", on_class_selected)

star_label = tk.Label(root, text="🌟 Stars: 0", font=("Arial", 12), bg="#ffffff")
star_label.place(relx=0.9, y=60, anchor="center")

canvas = tk.Canvas(root, width=300, height=300, bg="white", highlightthickness=1, highlightbackground="gray")
canvas.place(relx=0.5, y=200, anchor="center")

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, font=("Arial", 12))
chat_area.place(x=20, y=360, width=560, height=180)
chat_area.insert(tk.END, "🎉 Welcome! Select your class to begin. 🎒\n")
chat_area.config(state=tk.NORMAL)

entry_frame = tk.Frame(root)
entry_frame.place(x=20, y=550, width=560)

user_entry = tk.Entry(entry_frame, font=("Arial", 12))
user_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

send_btn = tk.Button(entry_frame, text="Send", command=on_send, width=10)
send_btn.pack(side=tk.LEFT)

quiz_btn = tk.Button(root, text="🧠 Quiz Time!", command=quiz_mode, bg="#FFD966", font=("Arial", 12, "bold"))
quiz_btn.place(relx=0.5, y=620, anchor="center")

# ==== Run splash animation on load ====
root.after(1000, run_splash_animation)

# ==== Start Interface ====
root.mainloop()