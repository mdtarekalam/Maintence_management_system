import customtkinter as ctk


def show_home_screen(container, navigate, role, user_data):
    for widget in container.winfo_children():
        widget.destroy()

    name = user_data.get("full_name") if role != "Admin" else user_data.get("full_name", "Admin")

    welcome_label = ctk.CTkLabel(container, text=f"Welcome, {name}! 👋",
                                  font=("Segoe UI", 20, "bold"))
    welcome_label.pack(pady=(40, 10))

    role_label = ctk.CTkLabel(container, text=f"Logged in as: {role}",
                               font=("Segoe UI", 13), text_color="gray")
    role_label.pack(pady=(0, 30))

    info_label = ctk.CTkLabel(container, text="Home screen coming soon...",
                               font=("Segoe UI", 12))
    info_label.pack(pady=(0, 30))

    logout_btn = ctk.CTkButton(container, text="Logout", height=38, corner_radius=8,
                                font=("Segoe UI", 13, "bold"),
                                command=lambda: navigate("welcome"))
    logout_btn.pack(fill="x", padx=35, pady=(0, 10))