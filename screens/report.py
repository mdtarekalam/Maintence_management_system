import customtkinter as ctk
from db import get_buildings, get_rooms, get_computers, get_devices, submit_complaint, ensure_computer_exists, ensure_device_exists


def show_report_screen(container, navigate, role, user_data):
    # State to track selections across steps
    print("DEBUG: report screen loaded")
    state = {
        "building_id": None,
        "building_name": "",
        "room_id": None,
        "room_number": "",
        "room_type": "",
        "computer_id": None,
        "computer_number": "",
        "device_id": None,
        "device_name": "",
        "preset_device_name": None,
    }

    def show_step1():
        for w in container.winfo_children():
            w.destroy()

        ctk.CTkLabel(container, text="Step 1 of 4", font=("Segoe UI", 10),
                     text_color="gray").pack(pady=(20, 4))
        ctk.CTkLabel(container, text="Select a Building",
                     font=("Segoe UI", 18, "bold")).pack(pady=(0, 20))

        buildings = get_buildings()
        scroll = ctk.CTkScrollableFrame(container, height=260, corner_radius=8)
        scroll.pack(fill="x", padx=35, pady=(0, 10))
        for b_id, b_name in buildings:
            btn = ctk.CTkButton(scroll, text=b_name, height=38, corner_radius=8,
                                font=("Segoe UI", 13),
                                command=lambda i=b_id, n=b_name: pick_building(i, n))
            btn.pack(fill="x", pady=5)

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
        scroll = ctk.CTkScrollableFrame(container, height=260, corner_radius=8)
        scroll.pack(fill="x", padx=35, pady=(0, 10))
        for r_id, r_num, r_type in rooms:
            btn = ctk.CTkButton(scroll, text=f"Room {r_num}  ·  {r_type}",
                                height=38, corner_radius=8, font=("Segoe UI", 13),
                                command=lambda i=r_id, n=r_num, t=r_type: pick_room(i, n, t))
            btn.pack(fill="x", pady=4)

        ctk.CTkLabel(container, text="← Back", font=("Segoe UI", 10),
                     text_color="#3B8ED0", cursor="hand2").pack(pady=(15, 0))
        container.winfo_children()[-1].bind("<Button-1>", lambda e: show_step1())

    def pick_room(r_id, r_num, r_type):
        state["room_id"] = r_id
        state["room_number"] = r_num
        state["room_type"] = r_type
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
        def comp_label(cnum):
            if str(cnum).lower() in ("faculty computer", "faculty", "0"):
                return "Faculty Computer"
            return f"Computer {cnum}"

        seen = set()
        for c_id, c_num in computers:
            label = comp_label(c_num)
            # Skip numeric '1' entries for classrooms (user requested only faculty computer)
            if label == "Computer 1" and state.get("room_type") and "classroom" in state.get("room_type", "").lower():
                continue
            # Skip listing Faculty Computer here for lab/classroom rooms to avoid duplicate
            if label == "Faculty Computer" and state.get("room_type") and ("lab" in state.get("room_type", "").lower() or "classroom" in state.get("room_type", "").lower()):
                continue
            # Deduplicate labels (keep first occurrence)
            if label in seen:
                continue
            seen.add(label)
            btn = ctk.CTkButton(scroll, text=label, height=34,
                                corner_radius=8, font=("Segoe UI", 12),
                                command=lambda i=c_id, n=c_num: pick_computer(i, n))
            btn.pack(fill="x", pady=3)

        # Offer a faculty computer option for lab or classroom rooms
        if state.get("room_type") and ("lab" in state.get("room_type", "").lower() or "classroom" in state.get("room_type", "").lower()):
            def pick_faculty():
                comp_id = ensure_computer_exists(state["room_id"], "Faculty Computer")
                pick_computer(comp_id, "Faculty Computer")

            # place faculty button and device quick-buttons in one horizontal row
            row_frame = ctk.CTkFrame(scroll, corner_radius=6)
            row_frame.pack(fill="x", pady=(8, 3), padx=6)

            faculty_btn = ctk.CTkButton(row_frame, text="Faculty Computer", width=160, height=34,
                                        corner_radius=8, font=("Segoe UI", 12),
                                        command=pick_faculty)
            faculty_btn.pack(side="left", padx=(6, 12), pady=6)

            # Add quick device buttons for classrooms to report AC/Fan/Speaker issues
            def pick_device_in_classroom(dev_name):
                comp_id = ensure_computer_exists(state["room_id"], "Faculty Computer")
                ensure_device_exists(dev_name)
                state["computer_id"] = comp_id
                state["computer_number"] = "Faculty Computer"
                state["preset_device_name"] = dev_name
                show_step4()

            ctk.CTkButton(row_frame, text="AC", width=100, height=30, corner_radius=6,
                          command=lambda: pick_device_in_classroom("AC")).pack(side="left", padx=6, pady=6)
            ctk.CTkButton(row_frame, text="Speaker", width=100, height=30, corner_radius=6,
                          command=lambda: pick_device_in_classroom("Speaker")).pack(side="left", padx=6, pady=6)
            ctk.CTkButton(row_frame, text="Projector", width=100, height=30, corner_radius=6,
                          command=lambda: pick_device_in_classroom("Projector")).pack(side="left", padx=6, pady=6)
            ctk.CTkButton(row_frame, text="Fans", width=100, height=30, corner_radius=6,
                          command=lambda: pick_device_in_classroom("Fan")).pack(side="left", padx=6, pady=6)

        ctk.CTkLabel(container, text="← Back", font=("Segoe UI", 10),
                     text_color="#3B8ED0", cursor="hand2").pack(pady=(5, 0))
        container.winfo_children()[-1].bind("<Button-1>", lambda e: show_step2())

    def pick_computer(c_id, c_num):
        state["computer_id"] = c_id
        # normalize display value for faculty computer when numeric DB uses 0
        if str(c_num).lower() in ("faculty computer", "faculty", "0"):
            state["computer_number"] = "Faculty Computer"
        else:
            state["computer_number"] = c_num
        show_step4()

    def show_step4():
        for w in container.winfo_children():
            w.destroy()

        ctk.CTkLabel(container, text="Step 4 of 4", font=("Segoe UI", 10),
                     text_color="gray").pack(pady=(15, 4))
        ctk.CTkLabel(container, text="Report the Issue",
                     font=("Segoe UI", 18, "bold")).pack(pady=(0, 4))
        display_comp = state['computer_number']
        ctk.CTkLabel(container, text=f"{state['building_name']} · Room {state['room_number']} · Computer {display_comp}",
                     font=("Segoe UI", 10), text_color="gray").pack(pady=(0, 12))

        ctk.CTkLabel(container, text="Select device", font=("Segoe UI", 11),
                     anchor="w").pack(fill="x", padx=35)

        # If a device was preset (from classroom quick buttons), prefill it here
        device_var = ctk.StringVar(value=state.get("preset_device_name") or "")
        # Ensure common devices exist for labs and classrooms, then fetch devices
        if state.get("room_type") and ("lab" in state.get("room_type", "").lower() or "classroom" in state.get("room_type", "").lower()):
            for dn in ["AC", "Projector", "Fan", "Speaker", "Faculty Computer"]:
                ensure_device_exists(dn)
        devices = get_devices()
        device_map = {}
        device_menu = ctk.CTkOptionMenu(container, variable=device_var,
                                        values=[d[1] for d in devices],
                                        height=36, corner_radius=8)
        device_menu.pack(fill="x", padx=35, pady=(4, 12))
        for d_id, d_name in devices:
            device_map[d_name] = d_id

        # If preset was used, set the option menu selection and then clear the preset
        if state.get("preset_device_name"):
            # set variable explicitly to match one of the available devices
            if state["preset_device_name"] in device_map:
                device_var.set(state["preset_device_name"])
            state["preset_device_name"] = None

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