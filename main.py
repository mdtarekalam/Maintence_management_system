import customtkinter as ctk
import tkinter as tk
from screens.welcome import show_welcome_screen
from screens.login import show_login_screen
from screens.home import show_home_screen
from screens.register import show_register_screen
from screens.report import show_report_screen
from screens.suggestion import show_suggestion_screen
from screens.status import show_status_screen
from screens.admin import show_admin_screen

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("MMS - ULAB")
app.geometry("900x650")
app.minsize(420, 600)

bg_canvas = tk.Canvas(app, bg="#1a1a2e", highlightthickness=0)
bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)


def draw_background(event=None):
    bg_canvas.delete("all")
    w = bg_canvas.winfo_width()
    h = bg_canvas.winfo_height()

    bg_canvas.create_oval(-w*0.15, -h*0.12, w*0.30, h*0.25, fill="#16213e", outline="")
    bg_canvas.create_oval(w*0.70, -h*0.10, w*1.15, h*0.25, fill="#0f3460", outline="")
    bg_canvas.create_oval(-w*0.15, h*0.75, w*0.25, h*1.15, fill="#0f3460", outline="")
    bg_canvas.create_oval(w*0.70, h*0.78, w*1.15, h*1.15, fill="#16213e", outline="")


bg_canvas.bind("<Configure>", draw_background)

container = ctk.CTkFrame(app, corner_radius=20, fg_color="#22223b", width=340, height=480)
container.place(relx=0.5, rely=0.5, anchor="center")
container.pack_propagate(False)


def resize_container(event=None):
    w = app.winfo_width()
    h = app.winfo_height()
    card_w = max(340, min(480, int(w * 0.4)))
    card_h = max(480, min(620, int(h * 0.85)))
    container.configure(width=card_w, height=card_h)
    container.place(relx=0.5, rely=0.5, anchor="center")


app.bind("<Configure>", resize_container)


def navigate(screen_name, *args):
    print(f"DEBUG navigate called: {screen_name}")
    if screen_name == "welcome":
        show_welcome_screen(container, navigate)
    elif screen_name == "login":
        show_login_screen(container, navigate, *args)
    elif screen_name == "home":
        show_home_screen(container, navigate, *args)
    elif screen_name == "register":
        show_register_screen(container, navigate, *args)
    elif screen_name == "report":
        show_report_screen(container, navigate, *args)
    elif screen_name == "suggestion":
        show_suggestion_screen(container, navigate, *args)
    elif screen_name == "status":
        show_status_screen(container, navigate, *args)
    elif screen_name == "admin":
        show_admin_screen(container, navigate, *args)


navigate("welcome")
app.mainloop()