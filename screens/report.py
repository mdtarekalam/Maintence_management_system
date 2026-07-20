import customtkinter as ctk
from db import get_buildings, get_rooms, get_computers, get_devices, submit_complaint


def show_report_screen(container, navigate, role, user_data):
    # State to track selections across steps
    state = {
        "building_id": None,
        "building_name": "",
        "room_id": None,
        "room_number": "",
        "computer_id": None,
        "computer_number": "",
        "device_id": None,
        "device_name": "",
    }

    def show_step1():
        for w in container.winfo_children():
            w.destroy()

        ctk.CTkLabel(container, text="Step 1 of 4", font=("Segoe UI", 10),
                     text_color="gray").pack(pady=(20, 4))
        ctk.CTkLabel(container, text="Select a Building",
                     font=("Segoe UI", 18, "bold")).pack(pady=(0, 20))

        buildings = get_buildings()
        for b_id, b_name in buildings:
            btn = ctk.CTkButton(container, text=b_name, height=38, corner_radius=8,
                                font=("Segoe UI", 13),
                                command=lambda i=b_id, n=b_name: pick_building(i, n))
            btn.pack(fill="x", padx=35, pady=5)

        ctk.CTkLabel(container, text="← Back", font=("Segoe UI", 10),
                     text_color="#3B8ED0", cursor="hand2").pack(pady=(15, 0))
        container.winfo_children()[-1].bind("<Button-1>", lambda e: navigate("home", role, user_data))

    def pick_building(b_id, b_name):
        state["building_id"] = b_id
        state["building_name"] = b_name
        show_step2()

    def show_step2():
        for w in container.winfo_children():
            w.destroy()

        ctk.CTkLabel(container, text="Step 2 of 4", font=("Segoe UI", 10),
                     text_color="gray").pack(pady=(20, 4))
        ctk.CTkLabel(container, text=f"Select a Room",
                     font=("Segoe UI", 18, "bold")).pack(pady=(0, 4))
        ctk.CTkLabel(container, text=state["building_name"],
                     font=("Segoe UI", 11), text_color="gray").pack(pady=(0, 16))

        rooms = get_rooms(state["building_id"])
        for r_id, r_num, r_type in rooms:
            btn = ctk.CTkButton(container, text=f"Room {r_num}  ·  {r_type}",
                                height=38, corner_radius=8, font=("Segoe UI", 13),
                                command=lambda i=r_id, n=r_num: pick_room(i, n))
            btn.pack(fill="x", padx=35, pady=4)

        ctk.CTkLabel(container, text="← Back", font=("Segoe UI", 10),
                     text_color="#3B8ED0", cursor="hand2").pack(pady=(15, 0))
        container.winfo_children()[-1].bind("<Button-1>", lambda e: show_step1())

    def pick_room(r_id, r_num):
        state["room_id"] = r_id
        state["room_number"] = r_num
        show_step3()

    def show_step3():
        for w in container.winfo_children():
            w.destroy()

        ctk.CTkLabel(container, text="Step 3 of 4", font=("Segoe UI", 10),
                     text_color="gray").pack(pady=(20, 4))
        ctk.CTkLabel(container, text="Select a Computer",
                     font=("Segoe UI", 18, "bold")).pack(pady=(0, 4))
        ctk.CTkLabel(container, text=f"{state['building_name']} · Room {state['room_number']}",
                     font=("Segoe UI", 11), text_color="gray").pack(pady=(0, 12))

        scroll = ctk.CTkScrollableFrame(container, height=280, corner_radius=8)
        scroll.pack(fill="x", padx=35, pady=(0, 10))

        computers = get_computers(state["room_id"])
        for c_id, c_num in computers:
            btn = ctk.CTkButton(scroll, text=f"Computer {c_num}", height=34,
                                corner_radius=8, font=("Segoe UI", 12),
                                command=lambda i=c_id, n=c_num: pick_computer(i, n))
            btn.pack(fill="x", pady=3)

        ctk.CTkLabel(container, text="← Back", font=("Segoe UI", 10),
                     text_color="#3B8ED0", cursor="hand2").pack(pady=(5, 0))
        container.winfo_children()[-1].bind("<Button-1>", lambda e: show_step2())

    def pick_computer(c_id, c_num):
        state["computer_id"] = c_id
        state["computer_number"] = c_num
        show_step4()

    def show_step4():
        for w in container.winfo_children():
            w.destroy()

        ctk.CTkLabel(container, text="Step 4 of 4", font=("Segoe UI", 10),
                     text_color="gray").pack(pady=(15, 4))
        ctk.CTkLabel(container, text="Report the Issue",
                     font=("Segoe UI", 18, "bold")).pack(pady=(0, 4))
        ctk.CTkLabel(container, text=f"{state['building_name']} · Room {state['room_number']} · Computer {state['computer_number']}",
                     font=("Segoe UI", 10), text_color="gray").pack(pady=(0, 12))

        ctk.CTkLabel(container, text="Select device", font=("Segoe UI", 11),
                     anchor="w").pack(fill="x", padx=35)

        device_var = ctk.StringVar(value="")
        devices = get_devices()
        device_map = {}
        device_menu = ctk.CTkOptionMenu(container, variable=device_var,
                                        values=[d[1] for d in devices],
                                        height=36, corner_radius=8)
        device_menu.pack(fill="x", padx=35, pady=(4, 12))
        for d_id, d_name in devices:
            device_map[d_name] = d_id

        ctk.CTkLabel(container, text="Description", font=("Segoe UI", 11),
                     anchor="w").pack(fill="x", padx=35)
        desc_entry = ctk.CTkTextbox(container, height=80, corner_radius=8)
        desc_entry.pack(fill="x", padx=35, pady=(4, 12))

        err_label = ctk.CTkLabel(container, text="", font=("Segoe UI", 11),
                                  text_color="#e74c3c")
        err_label.pack()

        def do_submit():
            device_name = device_var.get()
            description = desc_entry.get("1.0", "end").strip()
            if not device_name:
                err_label.configure(text="Please select a device")
                return
            device_id = device_map.get(device_name)
            success, message = submit_complaint(
                user_data["id"], state["computer_id"], device_id, description
            )
            if success:
                show_success()
            else:
                err_label.configure(text=message)

        ctk.CTkButton(container, text="Submit Complaint", height=38, corner_radius=8,
                      font=("Segoe UI", 13, "bold"), command=do_submit).pack(fill="x", padx=35)

        ctk.CTkLabel(container, text="← Back", font=("Segoe UI", 10),
                     text_color="#3B8ED0", cursor="hand2").pack(pady=(10, 0))
        container.winfo_children()[-1].bind("<Button-1>", lambda e: show_step3())

    def show_success():
        for w in container.winfo_children():
            w.destroy()

        ctk.CTkLabel(container, text="✅", font=("Segoe UI", 40)).pack(pady=(50, 10))
        ctk.CTkLabel(container, text="Complaint Submitted!",
                     font=("Segoe UI", 18, "bold")).pack(pady=(0, 8))
        ctk.CTkLabel(container, text="Your complaint has been sent to the admin.\nYou can track its status from your home screen.",
                     font=("Segoe UI", 11), text_color="gray", justify="center").pack(pady=(0, 24))
        ctk.CTkButton(container, text="Back to Home", height=38, corner_radius=8,
                      font=("Segoe UI", 13, "bold"),
                      command=lambda: navigate("home", role, user_data)).pack(fill="x", padx=35)

    show_step1()