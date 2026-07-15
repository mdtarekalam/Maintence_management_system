import customtkinter as ctk


def show_welcome_screen(container, navigate):
    for widget in container.winfo_children():
        widget.destroy()

    icon = ctk.CTkLabel(container, text="🔧", font=("Segoe UI", 40))
    icon.pack(pady=(30, 5))

    title = ctk.CTkLabel(container, text="Maintenance\nManagement System",
                          font=("Segoe UI", 20, "bold"), justify="center")
    title.pack(pady=(0, 5))

    subtitle = ctk.CTkLabel(container, text="University of Liberal Arts Bangladesh",
                             font=("Segoe UI", 11), text_color="gray")
    subtitle.pack(pady=(0, 15))

    instruction = ctk.CTkLabel(container, text="Continue as", font=("Segoe UI", 12))
    instruction.pack(pady=(10, 12))

    roles = ["Student", "Faculty", "Staff", "Admin"]
    for role in roles:
        btn = ctk.CTkButton(container, text=role, height=38, corner_radius=8,
                             font=("Segoe UI", 13, "bold"),
                             command=lambda r=role: navigate("login", r))
        btn.pack(fill="x", padx=35, pady=5)