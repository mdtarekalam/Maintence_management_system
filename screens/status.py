import customtkinter as ctk
from db import get_user_complaints


def show_status_screen(container, navigate, role, user_data):
    for widget in container.winfo_children():
        widget.destroy()

    ctk.CTkLabel(container, text="Issue Tracker", font=("Segoe UI", 18, "bold")).pack(pady=(25, 6))
    ctk.CTkLabel(container, text="Track the status of your reported issues",
                 font=("Segoe UI", 11), text_color="gray").pack(pady=(0, 14))

    complaints = get_user_complaints(user_data["id"])
    if not complaints:
        ctk.CTkLabel(container, text="No issues reported yet.", font=("Segoe UI", 12), text_color="gray").pack(pady=20)
    else:
        scroll = ctk.CTkScrollableFrame(container, height=320, corner_radius=8)
        scroll.pack(fill="x", padx=35, pady=(0, 10))
        for c in complaints:
            frame = ctk.CTkFrame(scroll, corner_radius=8, fg_color="#2d2d4e")
            frame.pack(fill="x", pady=6)
            title = ctk.CTkLabel(frame, text=f"{c['building_name']} · Room {c['room_number']} · {c['device_name']}",
                                 font=("Segoe UI", 12, "bold"), anchor="w")
            title.pack(fill="x", padx=10, pady=(8, 0))

            status_color = "#EF9F27"
            if c["status"] == "Resolved":
                status_color = "#2ecc71"
            elif c["status"] == "In Progress":
                status_color = "#3B8ED0"
            status = ctk.CTkLabel(frame, text=f"Status: {c['status']}",
                                 font=("Segoe UI", 11), text_color=status_color, anchor="w")
            status.pack(fill="x", padx=10, pady=(4, 0))

            priority = ctk.CTkLabel(frame, text=f"Priority: {c['priority']}",
                                   font=("Segoe UI", 11), text_color="#a5d6a7", anchor="w")
            priority.pack(fill="x", padx=10, pady=(2, 0))

            desc = ctk.CTkLabel(frame, text=f"{c['description']}",
                                font=("Segoe UI", 11), wraplength=300, justify="left", anchor="w")
            desc.pack(fill="x", padx=10, pady=(4, 10))

    ctk.CTkButton(container, text="Back to Home", height=38, corner_radius=8,
                  font=("Segoe UI", 13, "bold"),
                  command=lambda: navigate("home", role, user_data)).pack(fill="x", padx=35, pady=(10, 0))
