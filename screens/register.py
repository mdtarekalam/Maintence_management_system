import customtkinter as ctk
from db import register_user


def show_register_screen(container, navigate, role):
    for widget in container.winfo_children():
        widget.destroy()

    icon = ctk.CTkLabel(container, text="🔧", font=("Segoe UI", 28))
    icon.pack(pady=(15, 3))

    title = ctk.CTkLabel(container, text=f"{role} Registration", font=("Segoe UI", 18, "bold"))
    title.pack(pady=(0, 10))

    error_label = ctk.CTkLabel(container, text="", font=("Segoe UI", 11), text_color="#e74c3c",
                                wraplength=280)
    error_label.pack(pady=(0, 5))

    name_entry = ctk.CTkEntry(container, placeholder_text="Full Name", height=34, corner_radius=8)
    name_entry.pack(fill="x", padx=35, pady=4)

    id_entry = ctk.CTkEntry(container, placeholder_text=f"{role} ID", height=34, corner_radius=8)
    id_entry.pack(fill="x", padx=35, pady=4)

    email_entry = ctk.CTkEntry(container, placeholder_text="Email", height=34, corner_radius=8)
    email_entry.pack(fill="x", padx=35, pady=4)

    dept_entry = ctk.CTkEntry(container, placeholder_text="Department", height=34, corner_radius=8)
    dept_entry.pack(fill="x", padx=35, pady=4)

    pass_entry = ctk.CTkEntry(container, placeholder_text="Password", show="*", height=34, corner_radius=8)
    pass_entry.pack(fill="x", padx=35, pady=4)

    def attempt_register():
        name = name_entry.get().strip()
        student_id = id_entry.get().strip()
        email = email_entry.get().strip()
        department = dept_entry.get().strip()
        password = pass_entry.get().strip()

        if not all([name, student_id, email, department, password]):
            error_label.configure(text_color="#e74c3c", text="Please fill in all fields")
            return

        success, message = register_user(name, student_id, email, password, department, role)

        if success:
            error_label.configure(text_color="#2ecc71", text="Registered! Redirecting to login...")
            container.after(1500, lambda: navigate("login", role))
        else:
            error_label.configure(text_color="#e74c3c", text=message)

    register_btn = ctk.CTkButton(container, text="Register", height=36, corner_radius=8,
                                  font=("Segoe UI", 13, "bold"), command=attempt_register)
    register_btn.pack(fill="x", padx=35, pady=(12, 8))

    back_label = ctk.CTkLabel(container, text="Already have an account? Login",
                               font=("Segoe UI", 10), text_color="#3B8ED0", cursor="hand2")
    back_label.pack(pady=(0, 10))
    back_label.bind("<Button-1>", lambda e: navigate("login", role))