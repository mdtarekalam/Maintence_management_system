import customtkinter as ctk

from db import get_all_complaints, update_complaint, get_device_complaint_stats, get_status_summary, get_priority_summary


def show_admin_screen(container, navigate, role, user_data):
    for widget in container.winfo_children():
        widget.destroy()

    header = ctk.CTkLabel(container, text="Admin Dashboard", font=("Segoe UI", 20, "bold"))
    header.pack(pady=(20, 8))

    subtitle = ctk.CTkLabel(container, text="Review complaints, update status, and view issue analytics",
                             font=("Segoe UI", 11), text_color="gray")
    subtitle.pack(pady=(0, 18))

    summary_frame = ctk.CTkFrame(container, fg_color="#292d3e", corner_radius=12)
    summary_frame.pack(fill="x", padx=25, pady=(0, 14))

    status_summary = get_status_summary()
    priority_summary = get_priority_summary()
    device_stats = get_device_complaint_stats()

    summary_row = ctk.CTkFrame(summary_frame, fg_color="#1f2433", corner_radius=12)
    summary_row.pack(fill="x", padx=10, pady=10)

    status_card = ctk.CTkFrame(summary_row, fg_color="#262b3f", corner_radius=10)
    status_card.pack(side="left", expand=True, fill="both", padx=(0, 5), pady=5)
    ctk.CTkLabel(status_card, text="Status Summary", font=("Segoe UI", 12, "bold")).pack(pady=(12, 8))
    for status, count in status_summary:
        ctk.CTkLabel(status_card, text=f"{status}: {count}", font=("Segoe UI", 11), anchor="w").pack(fill="x", padx=12, pady=2)

    priority_card = ctk.CTkFrame(summary_row, fg_color="#262b3f", corner_radius=10)
    priority_card.pack(side="left", expand=True, fill="both", padx=(5, 0), pady=5)
    ctk.CTkLabel(priority_card, text="Priority Summary", font=("Segoe UI", 12, "bold")).pack(pady=(12, 8))
    for priority, count in priority_summary:
        ctk.CTkLabel(priority_card, text=f"{priority}: {count}", font=("Segoe UI", 11), anchor="w").pack(fill="x", padx=12, pady=2)

    device_card = ctk.CTkFrame(summary_frame, fg_color="#262b3f", corner_radius=10)
    device_card.pack(fill="x", padx=10, pady=(0, 10))
    ctk.CTkLabel(device_card, text="Top Devices by Complaints", font=("Segoe UI", 12, "bold")).pack(pady=(12, 8))
    for device_name, count in device_stats:
        ctk.CTkLabel(device_card, text=f"{device_name}: {count}", font=("Segoe UI", 11), anchor="w").pack(fill="x", padx=12, pady=2)

    complaint_label = ctk.CTkLabel(container, text="Complaint Queue", font=("Segoe UI", 14, "bold"))
    complaint_label.pack(pady=(0, 8), anchor="w", padx=25)

    complaints = get_all_complaints()
    complaints_frame = ctk.CTkScrollableFrame(container, height=320, corner_radius=12)
    complaints_frame.pack(fill="both", padx=25, pady=(0, 10), expand=True)

    if not complaints:
        ctk.CTkLabel(complaints_frame, text="No complaints available.", font=("Segoe UI", 12), text_color="gray").pack(pady=20)
    else:
        for complaint in complaints:
            row = ctk.CTkFrame(complaints_frame, fg_color="#1f2433", corner_radius=12)
            row.pack(fill="x", pady=8, padx=5)

            heading = ctk.CTkLabel(row, text=f"#{complaint['id']}  {complaint['building_name']} · Room {complaint['room_number']} · {complaint['device_name']}",
                                   font=("Segoe UI", 12, "bold"), anchor="w")
            heading.pack(fill="x", padx=12, pady=(12, 4))

            meta = ctk.CTkLabel(row, text=f"Reporter: {complaint['reporter_name']} ({complaint['reporter_id']}) · Status: {complaint['status']} · Priority: {complaint['priority']}",
                                font=("Segoe UI", 10), text_color="#a3a3a3", anchor="w")
            meta.pack(fill="x", padx=12)

            desc = ctk.CTkLabel(row, text=complaint['description'], font=("Segoe UI", 11), wraplength=560, justify="left", anchor="w")
            desc.pack(fill="x", padx=12, pady=(6, 8))

            action_row = ctk.CTkFrame(row, fg_color="#252a3e", corner_radius=10)
            action_row.pack(fill="x", padx=12, pady=(0, 12))

            status_var = ctk.StringVar(value=complaint['status'])
            priority_var = ctk.StringVar(value=complaint['priority'])
            note_entry = ctk.CTkTextbox(action_row, height=80, corner_radius=10)
            note_entry.insert("1.0", complaint.get('admin_note') or "")
            note_entry.pack(fill="x", padx=10, pady=8)

            control_frame = ctk.CTkFrame(action_row, fg_color="transparent")
            control_frame.pack(fill="x", padx=10, pady=(0, 8))

            ctk.CTkLabel(control_frame, text="Status:", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w")
            ctk.CTkOptionMenu(control_frame, variable=status_var, values=["Pending", "In Progress", "Resolved"], width=140).grid(row=0, column=1, padx=10, pady=4)
            ctk.CTkLabel(control_frame, text="Priority:", font=("Segoe UI", 11)).grid(row=0, column=2, sticky="w", padx=(20, 0))
            ctk.CTkOptionMenu(control_frame, variable=priority_var, values=["Low", "Medium", "High"], width=140).grid(row=0, column=3, padx=10, pady=4)

            def make_update(complaint_id, status_var, priority_var, note_entry):
                def callback():
                    message = note_entry.get("1.0", "end").strip()
                    success, msg = update_complaint(complaint_id, status_var.get(), priority_var.get(), message)
                    if success:
                        navigate("admin", role, user_data)
                    else:
                        ctk.CTkLabel(row, text=msg, font=("Segoe UI", 10), text_color="#e74c3c").pack(pady=(4, 8))
                return callback

            update_btn = ctk.CTkButton(action_row, text="Update", command=make_update(complaint['id'], status_var, priority_var, note_entry), width=100)
            update_btn.pack(anchor="e", padx=10, pady=(0, 8))

    ctk.CTkButton(container, text="Back to Home", height=38, corner_radius=8,
                  font=("Segoe UI", 13, "bold"), command=lambda: navigate("home", role, user_data)).pack(fill="x", padx=25, pady=(0, 14))
