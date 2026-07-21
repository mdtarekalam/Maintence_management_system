import customtkinter as ctk
from db import get_user_complaints


def show_home_screen(container, navigate, role, user_data):
    for widget in container.winfo_children():
        widget.destroy()

    name = user_data.get("full_name", "User")

    # Welcome label
    welcome = ctk.CTkLabel(container, text=f"Welcome, {name}! 👋",
                            font=("Segoe UI", 18, "bold"))
    welcome.pack(pady=(30, 4))

    role_label = ctk.CTkLabel(container, text=f"Logged in as: {role}",
                               font=("Segoe UI", 11), text_color="gray")
    role_label.pack(pady=(0, 20))

    if role != "Admin":
        # Report button
        def go_report():
            print("DEBUG: going to report screen")
            print("DEBUG user_data:", user_data)
            navigate("report", role, user_data)

        report_btn = ctk.CTkButton(container, text="+ Report an issue",
                                    height=38, corner_radius=8,
                                    font=("Segoe UI", 13, "bold"),
                                    command=go_report)
        report_btn.pack(fill="x", padx=35, pady=(0, 10))

        # Suggestion button
        suggestion_btn = ctk.CTkButton(container, text="+ Give a suggestion",
                                        height=38, corner_radius=8,
                                        font=("Segoe UI", 13, "bold"),
                                        fg_color="#4b7bec",
                                        hover_color="#3c6ef2",
                                        command=lambda: navigate("suggestion", role, user_data))
        suggestion_btn.pack(fill="x", padx=35, pady=(0, 10))

        # Status tracker button
        status_btn = ctk.CTkButton(container, text="Track my issues",
                                    height=38, corner_radius=8,
                                    font=("Segoe UI", 13, "bold"),
                                    fg_color="#2ecc71",
                                    hover_color="#28b463",
                                    command=lambda: navigate("status", role, user_data))
        status_btn.pack(fill="x", padx=35, pady=(0, 16))

        # My complaints label
        complaints_label = ctk.CTkLabel(container, text="My complaints",
                                         font=("Segoe UI", 11),
                                         text_color="gray", anchor="w")
        complaints_label.pack(fill="x", padx=35)

        # Fetch and show complaints
        complaints = get_user_complaints(user_data["id"])

        if not complaints:
            empty = ctk.CTkLabel(container, text="No complaints yet.",
                                  font=("Segoe UI", 11), text_color="gray")
            empty.pack(pady=10)
        else:
            scroll = ctk.CTkScrollableFrame(container, height=180, corner_radius=8)
            scroll.pack(fill="x", padx=35, pady=(6, 10))
            for c in complaints:
                if c["status"] == "Resolved":
                    color = "#2ecc71"
                elif c["status"] == "In Progress":
                    color = "#3B8ED0"
                else:
                    color = "#EF9F27"
                row = ctk.CTkFrame(scroll, corner_radius=8, fg_color="#2d2d4e")
                row.pack(fill="x", pady=3)
                info = ctk.CTkLabel(row,
                                     text=f"{c['building_name']} · Room {c['room_number']} · {c['device_name']}",
                                     font=("Segoe UI", 11), anchor="w")
                info.pack(side="left", padx=10, pady=6)
                status = ctk.CTkLabel(row, text=c["status"],
                                       font=("Segoe UI", 10), text_color=color)
                status.pack(side="right", padx=10)
    else:
        admin_note = ctk.CTkLabel(container, text="Admin dashboard access is available below.",
                                  font=("Segoe UI", 12), text_color="gray")
        admin_note.pack(pady=(0, 16))

        admin_btn = ctk.CTkButton(container, text="Open Admin Dashboard",
                                  height=38, corner_radius=8,
                                  font=("Segoe UI", 13, "bold"),
                                  fg_color="#6a5acd",
                                  hover_color="#5b4cb6",
                                  command=lambda: navigate("admin", role, user_data))
        admin_btn.pack(fill="x", padx=35, pady=(0, 12))

    # Logout button
    logout_btn = ctk.CTkButton(container, text="Logout",
                                height=36, corner_radius=8,
                                font=("Segoe UI", 12),
                                fg_color="transparent",
                                border_width=1,
                                border_color="#555",
                                text_color="#aaa",
                                command=lambda: navigate("welcome"))
    logout_btn.pack(fill="x", padx=35, pady=(8, 10))