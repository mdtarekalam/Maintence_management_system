import customtkinter as ctk
from db import check_user_login, check_admin_login


def show_login_screen(container, navigate, role):
    for widget in container.winfo_children():
        widget.destroy()

    icon = ctk.CTkLabel(container, text="🔧", font=("Segoe UI", 32))
    icon.pack(pady=(25, 5))

    title = ctk.CTkLabel(container, text=f"{role} Login", font=("Segoe UI", 20, "bold"))
    title.pack(pady=(0, 3))

    subtitle = ctk.CTkLabel(container, text="University of Liberal Arts Bangladesh",
                             font=("Segoe UI", 11), text_color="gray")
    subtitle.pack(pady=(0, 15))

    error_label = ctk.CTkLabel(container, text="", font=("Segoe UI", 11), text_color="#e74c3c")
    error_label.pack(pady=(0, 5))

    id_text = "Username" if role == "Admin" else f"{role} ID"
    id_label = ctk.CTkLabel(container, text=id_text, font=("Segoe UI", 11), anchor="w")
    id_label.pack(fill="x", padx=35)

    id_entry = ctk.CTkEntry(container, placeholder_text=f"Enter your {id_text.lower()}",
                             height=36, corner_radius=8)
    id_entry.pack(fill="x", padx=35, pady=(4, 12))

    pass_label = ctk.CTkLabel(container, text="Password", font=("Segoe UI", 11), anchor="w")
    pass_label.pack(fill="x", padx=35)

    pass_entry = ctk.CTkEntry(container, placeholder_text="Enter your password", show="*",
                               height=36, corner_radius=8)
    pass_entry.pack(fill="x", padx=35, pady=(4, 18))

    def attempt_login():
        entered_id = id_entry.get().strip()
        entered_pass = pass_entry.get().strip()

        if not entered_id or not entered_pass:
            error_label.configure(text="Please fill in both fields")
            return

        if role == "Admin":
            result = check_admin_login(entered_id, entered_pass)
        else:
            result = check_user_login(entered_id, entered_pass, role)

        if result:
            error_label.configure(text="")
            navigate("home", role, result)
        else:
            error_label.configure(text="Invalid ID or password")

    login_btn = ctk.CTkButton(container, text="Login", height=38, corner_radius=8,
                               font=("Segoe UI", 13, "bold"), command=attempt_login)
    login_btn.pack(fill="x", padx=35, pady=(0, 10))

    back_label = ctk.CTkLabel(container, text="← Back", font=("Segoe UI", 10),
                               text_color="#3B8ED0", cursor="hand2")
    back_label.pack(pady=(0, 6))
    back_label.bind("<Button-1>", lambda e: navigate("welcome"))

    if role != "Admin":
        register_label = ctk.CTkLabel(container, text="Don't have an account? Register here",
                                       font=("Segoe UI", 10), text_color="#3B8ED0", cursor="hand2")
        register_label.pack(pady=(0, 10))
        register_label.bind("<Button-1>", lambda e: navigate("register", role))