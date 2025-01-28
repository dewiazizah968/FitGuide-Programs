import tkinter as tk
from tkinter import messagebox, filedialog, Canvas, Toplevel, ttk  
from PIL import Image, ImageTk
import csv
import os
import sys

if getattr(sys, 'frozen', False):  
    base_path = os.path.dirname(sys.executable)
else: 
    base_path = os.path.dirname(__file__)

class ProfilePage:
    def __init__(self, master):
        self.master = master
        self.current_user_id = self.master.current_user_id

        self.data_file = os.path.join(base_path, "users_data.csv")

        # Default and background image paths
        self.default_image_path = os.path.join(base_path, "Desain AI", "defaultfoto.png")
        self.background_image = Image.open(os.path.join(base_path, "Desain AI", "profilebg.png"))
        self.background_image = self.background_image.resize((1366, 720))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        # Create canvas and set background
        self.canvas = Canvas(self.master, width=1366, height=768, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")
        self.canvas.place(x=0, y=0)

        self.ensure_pict_column()

        self.create_navigation()

        self.display_user_data()

        # Load profile picture
        self.profile_image_path = self.get_profile_image_path()
        self.load_profile_picture()

        # Add buttons
        self.change_button = tk.Button(self.master, text="Change Photo", font=("Arial", 15), bg="#823E3E", fg="white", command=self.change_photo)
        self.change_button.place(x=90, y=550)

        self.delete_button = tk.Button(self.master, text="Delete Photo", font=("Arial", 15), bg="#823E3E", fg="white", command=self.delete_photo)
        self.delete_button.place(x=250, y=550)

    def ensure_pict_column(self):
        if not os.path.exists(self.data_file):
            return
        with open(self.data_file, mode="r") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            if 'pict' not in fieldnames:
                fieldnames.append('pict')
                rows = list(reader)
                with open(self.data_file, mode="w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    for row in rows:
                        row['pict'] = ''
                        writer.writerow(row)

    def get_profile_image_path(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['ID'] == self.current_user_id:
                        return row.get('pict', self.default_image_path).replace('\\', '\\')
        return self.default_image_path

    def load_profile_picture(self):
        try:
            image = Image.open(self.profile_image_path)
        except (FileNotFoundError, OSError):
            image = Image.open(self.default_image_path)

        image = image.resize((320, 320))
        self.profile_image = ImageTk.PhotoImage(image)
        self.profile_image_canvas = self.canvas.create_image(70, 180, image=self.profile_image, anchor="nw")

    def update_csv(self, key, value):
        if not os.path.exists(self.data_file):
            return
        updated_rows = []
        with open(self.data_file, mode="r") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            for row in reader:
                if row['ID'] == self.current_user_id:
                    row[key] = value
                updated_rows.append(row)
        with open(self.data_file, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_rows)

    def change_photo(self):
        # Allow user to select a new photo
        file_path = filedialog.askopenfilename(
            title="Select Profile Photo",
            filetypes=(
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("All files", "*.*")
            )
        )
        if file_path:
            try:
                image = Image.open(file_path)
                image = image.resize((320, 320))
                self.profile_image = ImageTk.PhotoImage(image)
                self.canvas.itemconfig(self.profile_image_canvas, image=self.profile_image)
                self.profile_image_path = file_path
                self.update_csv('pict', file_path.replace('\\', '\\\\'))
            except OSError:
                messagebox.showerror("Error", "Invalid image file.")

    def delete_photo(self):
        response = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the photo?")
        if response: 
            # Reset ke default photo
            self.profile_image_path = self.default_image_path
            self.update_csv('pict', '')
            self.load_profile_picture()
            messagebox.showinfo("Photo Deleted", "The photo has been successfully deleted.")
        else:
            messagebox.showinfo("Deletion Canceled", "The photo was not deleted.")

    def display_user_data(self):
        if not os.path.exists(self.data_file):
            messagebox.showerror("Error", "Data file not found.")
            return
        with open(self.data_file, mode="r") as file:
            reader = csv.DictReader(file)
            print(reader.fieldnames)  
            for row in reader:
                if row['ID'] == self.current_user_id:
                    print(row)
                    user_data = {
                        "ID": row.get("ID", ""),
                        "Nama": row.get("Nama", ""),
                        "Username": row.get("Username", ""),
                        "Email": row.get("Email", ""),
                        "Password": row.get("Password", ""),
                        "Usia": row.get("Usia", ""),
                        "Jenis Kelamin": row.get("Jenis Kelamin", ""),
                        "Tujuan": row.get("Tujuan", "")
                    }
                    break
            else:
                messagebox.showerror("Error", "User data not found.")
                return

        positions = {
            "ID": (710, 130),
            "Nama": (470, 200),
            "Username": (920, 200),
            "Email": (470, 300),
            "Password": (920, 300),
            "Usia": (470, 400),
            "Jenis Kelamin": (920, 400),
            "Tujuan": (470, 500)
        }

        for label, value in user_data.items():
            if label != "ID": 
                x_label, y_label = positions[label]
                tk.Label(self.master, text=label, font=("Times", 20, "bold"), bg="#FFD8B0", anchor="w").place(x=x_label, y=y_label)

                x_entry, y_entry = x_label, y_label + 35
            else:
                x_entry, y_entry = positions[label]

            if label == "Password":
                value = "*" * len(value) 

            label_box = tk.Label(self.master, text=value, font=("Times", 20), 
                                 bg="#823E3E", fg="white", relief="solid", bd=2)
            label_box.place(x=x_entry, y=y_entry, width=350, height=35)

            setting_button = tk.Button(self.master, text="Setting Profile", font=("Arial", 15), bg="#823E3E", fg="white", command=self.open_profile_settings)
            setting_button.place(x=1170, y=600)

    def open_profile_settings(self):
        settings_window = Toplevel(self.master)
        settings_window.title("Edit Profile")
        settings_window.configure(background="#FAE9D7") 

        fields = ["Nama", "Username", "Email", "Password", "Usia", "Jenis Kelamin", "Tujuan"]
        entries = {}

        def show_password():
            if password_entry.cget("show") == "*":
                password_entry.config(show="")
                show_password_button.config(text="Hide")
            else:
                password_entry.config(show="*")
                show_password_button.config(text="Show")

        for idx, field in enumerate(fields):
            tk.Label(settings_window, text=field, font=("Times", 10),bg="#FAE9D7").grid(row=idx, column=0, pady=5, padx=10, sticky="w")

            if field == "Jenis Kelamin" or field == "Tujuan":
                if field == "Jenis Kelamin":
                    options = ["Laki-laki", "Perempuan"]
                elif field == "Tujuan":
                    options = ["Meningkatkan kekuatan otot", "Meningkatkan fleksibilitas", 
                         "Meningkatkan kesehatan jantung", "Membakar kalori", 
                         "Mengurangi stres", "Melatih keseimbangan", 
                         "Meningkatkan stamina", "Memperbaiki mood", 
                         "Meningkatkan daya tahan fisik", "Lainnya"]

                combo = ttk.Combobox(settings_window, values=options, font=("Times", 10))
                combo.grid(row=idx, column=1, pady=5, padx=10)
                entries[field] = combo
            else:
                entry = tk.Entry(settings_window, font=("Times", 10))
                entry.grid(row=idx, column=1, pady=5, padx=10)
                entries[field] = entry

        with open(self.data_file, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['ID'] == self.current_user_id:
                    entries["Nama"].insert(0, row.get("Nama", ""))
                    entries["Username"].insert(0, row.get("Username", ""))
                    entries["Email"].insert(0, row.get("Email", ""))
                    entries["Password"].insert(0, row.get("Password", ""))
                    entries["Usia"].insert(0, row.get("Usia", ""))
                    entries["Jenis Kelamin"].set(row.get("Jenis Kelamin", "")) 
                    entries["Tujuan"].set(row.get("Tujuan", "")) 
                    break
        
        password_entry = entries["Password"]
        password_entry.config(show="*")  

        # Show/Hide password button
        show_password_button = tk.Button(settings_window, text="Show", bg="#823E3E", fg="white", font=("Times", 10), command=show_password)
        show_password_button.grid(row=3, column=2, pady=5)

        # Back Button
        def close_settings():
            settings_window.destroy()

        back_button = tk.Button(settings_window, text="Back", bg="#823E3E", fg="white", font=("Times", 10), command=close_settings)
        back_button.grid(row=len(fields), column=0, pady=10)

        # Save Button
        def save_profile():
            # Ambil data yang ada di form
            updated_data = {field: entries[field].get() for field in fields}
            updated_data["ID"] = self.current_user_id 

            rows = []
            with open(self.data_file, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['ID'] == self.current_user_id:
                        for field in fields:
                            if updated_data[field] != row.get(field):
                                row[field] = updated_data[field]
                        rows.append(row)  
                    else:
                        rows.append(row)

            with open(self.data_file, mode="w", newline="") as file:
                fieldnames = reader.fieldnames
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            messagebox.showinfo("Success", "Profile updated successfully.")

            self.display_user_data()  
            settings_window.destroy()

        save_button = tk.Button(settings_window, text="Save", bg="#823E3E", fg="white", font=("Times", 10), command=save_profile)
        save_button.grid(row=len(fields), column=1, pady=10)

    def create_navigation(self):
        # Dashboard Label
        dashboard_label = tk.Label(
            self.master,
            text="Dashboard",
            font=("Times", 20, "bold"),
            fg="#000",
            bg="#ECD9C5",
            cursor="hand2"
        )
        dashboard_label.place(x=620, y=55)  
        dashboard_label.bind("<Button-1>", lambda event: self.master.show_dashboard_page())

        # Input Label
        input_label = tk.Label(
            self.master,
            text="Input Form",
            font=("Times", 20, "bold"),
            fg="#000",
            bg="#ECD9C5",
            cursor="hand2"
        )
        input_label.place(x=790, y=55)  
        input_label.bind("<Button-1>", lambda event: self.master.show_input_page())

        # History Label
        history_label = tk.Label(
            self.master,
            text="History",
            font=("Times", 20, "bold"),
            fg="#000",
            bg="#ECD9C5",
            cursor="hand2"
        )
        history_label.place(x=970, y=55)  
        history_label.bind("<Button-1>", lambda event: self.master.show_history_page())

        # Profile Label
        profile_label = tk.Label(
            self.master,
            text="Profile",
            font=("Times", 20, "bold"),
            fg="#823E3E",
            bg="#ECD9C5",
            cursor="hand2"
        )
        profile_label.place(x=1100, y=55)  
        profile_label.bind("<Button-1>", lambda event: self.master.show_profile_page())

        # Logout Button
        logout_button = tk.Button(
            self.master,
            text="Logout",
            font=("Times", 20, "bold"),
            fg="#fff",
            bg="#823E3E",
            activebackground="#823E3E",
            activeforeground="white",
            command=self.confirm_logout  
        )
        logout_button.place(x=1220, y=50, width=100, height=40) 

    def confirm_logout(self):
        """Menampilkan pesan konfirmasi sebelum logout."""
        response = messagebox.askyesno("Logout Confirmation", "Are you sure you want to logout?")
        if response:  
            self.master.show_login_page()