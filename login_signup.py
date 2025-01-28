import tkinter as tk
from tkinter import messagebox, ttk, font
from PIL import Image, ImageTk
import csv
import re
import os
import random
import sys

if getattr(sys, 'frozen', False):  
    base_path = os.path.dirname(sys.executable)
else: 
    base_path = os.path.dirname(__file__)

class LoginSignupPage:
    def __init__(self, master):
        self.master = master
        self.data_file = os.path.join(base_path, "users_data.csv")
        self.profile_folder = os.path.join(base_path, "users_data")

        if not os.path.exists(self.profile_folder):
            os.makedirs(self.profile_folder)

    def show_login_page(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        # Frame login
        self.frame_login = tk.Frame(self.master, bg="#FFDFC4")
        self.frame_login.pack(fill="both", expand=True)

        image = Image.open(os.path.join(base_path, "Desain AI", "loginbg.png"))
        image = image.resize((1366, 768))
        self.bg_image = ImageTk.PhotoImage(image)

        bg_label = tk.Label(self.frame_login, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        sub_font = font.Font(family="Lato", size=20, weight="bold")
        input_font = font.Font(family="Times", size=20)

        # Label input User
        user_label = tk.Label(self.frame_login, text="USERNAME:", bg="#FAE9D7", fg="#823E3E", font=sub_font)
        user_label.place(x=120, y=250)

        # Input field User
        self.user_entry = tk.Entry(self.frame_login, width=35, font=input_font, bg="#D99879", fg="#000000", borderwidth=2)
        self.user_entry.place(x=120, y=290)

        # Label input Password
        password_label = tk.Label(self.frame_login, text="PASSWORD:", bg="#FAE9D7", fg="#823E3E", font=sub_font)
        password_label.place(x=120, y=380)

        # Input field Password
        self.password_entry = tk.Entry(self.frame_login, show="*", width=30, font=input_font, bg="#D99879", fg="#000000", borderwidth=2)
        self.password_entry.place(x=120, y=420)

        # Load ikon mata (terbuka dan tertutup)
        self.eye_closed_image = ImageTk.PhotoImage(Image.open(os.path.join(base_path, "Desain AI", "lihat1.png")).resize((40, 40)))
        self.eye_open_image = ImageTk.PhotoImage(Image.open(os.path.join(base_path, "Desain AI", "lihat2.png")).resize((40, 40)))
        self.show_password = False

        def toggle_password_login():
            """Mengubah tampilan password di halaman login."""
            if self.show_password:
                self.password_entry.config(show="*")
                self.toggle_button.config(image=self.eye_closed_image) 
                self.show_password = False
            else:
                self.password_entry.config(show="")
                self.toggle_button.config(image=self.eye_open_image)
                self.show_password = True

        # Tombol untuk toggle password
        self.toggle_button = tk.Button(
            self.frame_login,
            image=self.eye_closed_image,  
            command=toggle_password_login,
            bg="#FAE9D7",
            borderwidth=0,
            )
        self.toggle_button.place(x=575, y=418)

        # Tombol Sign Up (PNG)
        signup_image = Image.open(os.path.join(base_path, "Desain AI", "signup (1).png"))
        signup_image = signup_image.resize((230, 60))
        self.signup_image = ImageTk.PhotoImage(signup_image)
        signup_button = tk.Button(self.frame_login, image=self.signup_image, bg="#FFE8C2", borderwidth=0, command=self.show_signup_page)
        signup_button.place(x=120, y=550)

        # Tombol Submit Login (PNG)
        submit_image = Image.open(os.path.join(base_path, "Desain AI", "submit_login.png"))
        submit_image = submit_image.resize((230, 60))
        self.submit_image = ImageTk.PhotoImage(submit_image)
        submit_button = tk.Button(self.frame_login, image=self.submit_image, bg="#FFE8C2", borderwidth=0, command=self.validate_login)
        submit_button.place(x=387, y=550)

    def validate_login(self):
        username = self.user_entry.get()
        password = self.password_entry.get()

        # Validasi login
        with open(self.data_file, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Username"] == username and row["Password"] == password:
                    user_id = row["ID"]
                    self.master.current_user_id = user_id 

                    self.master.show_dashboard_page()  
                    return True, user_id  
        messagebox.showerror("Login Failed", "Username or Password is incorrect.")
        return False, None 

    def show_signup_page(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        # Frame signup
        self.frame_signup = tk.Frame(self.master, bg="#FFDFC4")
        self.frame_signup.pack(fill="both", expand=True)

        # Background image
        image = Image.open(os.path.join(base_path, "Desain AI", "signupbg.png"))
        image = image.resize((1366, 768))
        self.bg_image = ImageTk.PhotoImage(image)

        bg_label = tk.Label(self.frame_signup, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Font configuration
        label_font = font.Font(family="Lato", size=15, weight="bold")
        input_font = font.Font(family="Times", size=12)

        # Style for Combobox
        style = ttk.Style()
        style.theme_use("clam")

        style.map(
            "Custom.TCombobox",
            fieldbackground=[("readonly", "#D99879")],
            background=[("readonly", "#D99879")],
            selectbackground=[("!disabled", "#D99879")],
            selectforeground=[("!disabled", "#000000")],
        )

        style.configure(
            "Custom.TCombobox",
            fieldbackground="#D99879",
            background="#D99879",
            foreground="#000000",
            arrowcolor="#823E3E",
            bordercolor="#823E3E"
        )

        self.entries = {}
        fields = [
            ("Nama:", "entry"),
            ("Username:", "entry"),
            ("Email:", "entry"),
            ("Password:", "entry"),
            ("Usia:", "entry"),
            ("Jenis Kelamin:", ["Laki-laki", "Perempuan"]),
            ("Tujuan:", ["Meningkatkan kekuatan otot", "Meningkatkan fleksibilitas", 
                         "Meningkatkan kesehatan jantung", "Membakar kalori", 
                         "Mengurangi stres", "Melatih keseimbangan", 
                         "Meningkatkan stamina", "Memperbaiki mood", 
                         "Meningkatkan daya tahan fisik", "Lainnya"])
        ]

        y_position = 160
        for field, field_type in fields:
            label = tk.Label(self.frame_signup, text=field.upper(), bg="#FAE9D7", fg="#823E3E", font=label_font)
            label.place(x=80, y=y_position)

            if field_type == "entry":
                entry = tk.Entry(self.frame_signup, width=30, font=input_font, bg="#D99879", fg="#000000", borderwidth=2)
                if field == "Password:": 
                    entry.config(show="*")
                    self.password_entry_signup = entry  # Store the password entry for later
                entry.place(x=300, y=y_position)
                self.entries[field] = entry
            elif isinstance(field_type, list):
                self.entries[field] = tk.StringVar()
                combobox = ttk.Combobox(self.frame_signup, textvariable=self.entries[field], values=field_type, state="readonly", style="Custom.TCombobox", width=28, font=input_font )
                combobox.place(x=300, y=y_position)

            y_position += 50

        # Load ikon mata (terbuka dan tertutup) untuk signup
        self.eye_closed_image = ImageTk.PhotoImage(Image.open(os.path.join(base_path, "Desain AI", "lihat1.png")).resize((30, 30)))
        self.eye_open_image = ImageTk.PhotoImage(Image.open(os.path.join(base_path, "Desain AI", "lihat2.png")).resize((30, 30)))
        self.show_password_signup = False

        def toggle_password_signup():
            """Mengubah tampilan password di halaman signup."""
            if self.show_password_signup:
                self.password_entry_signup.config(show="*")
                self.toggle_button_signup.config(image=self.eye_closed_image)
                self.show_password_signup = False
            else:
                self.password_entry_signup.config(show="")
                self.toggle_button_signup.config(image=self.eye_open_image)
                self.show_password_signup = True

        # Tombol untuk toggle password di signup
        self.toggle_button_signup = tk.Button(
            self.frame_signup,
            image=self.eye_closed_image,  
            command=toggle_password_signup,
            bg="#FAE9D7",
            borderwidth=0,
        )
        self.toggle_button_signup.place(x=550, y=305)  # Position the icon near the password entry

        # Tombol Submit Sign-up (PNG)
        submit_image = Image.open(os.path.join(base_path, "Desain AI", "submit_signup.png"))
        submit_image = submit_image.resize((530, 50))
        self.signup_submit_image = ImageTk.PhotoImage(submit_image)
        submit_button = tk.Button(self.frame_signup, image=self.signup_submit_image, bg="#FFE8C2", borderwidth=0, command=self.submit_signup)
        submit_button.place(x=80, y=540)

        # Label "Tidak punya akun?"
        self.label = tk.Label(
            self.frame_signup,
            text="Sudah punya akun?",
            fg="black",
            bg="#FAE9D7",
            font=(input_font)
        )
        self.label.place(x=240, y=620)  

        # Tombol "Login Here"
        login_image = Image.open(os.path.join(base_path, "Desain AI", "login Here.png"))
        login_image = login_image.resize((75, 26))
        self.signup_login_image = ImageTk.PhotoImage(login_image)
        login_button = tk.Button(self.frame_signup, image=self.signup_login_image, bg="#FFE8C2", borderwidth=0, command=self.show_login_page)
        login_button.place(x=376, y=620)

    def submit_signup(self):
        user_data = {field: entry.get() for field, entry in self.entries.items()}

        # Validasi Email menggunakan regex
        email = user_data["Email:"]
        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format!")
            return

        # Validasi Password
        password = user_data["Password:"]
        if len(password) < 6:
            messagebox.showerror("Error", "Password must have a minimum of 6 characters!")
            return

        # Validasi Username unik
        username = user_data["Username:"]
        if self.is_username_taken(username):
            messagebox.showerror("Error", "Username already exists! Please choose another.")
            return
        
        # Generate ID unik
        user_id = f"{random.randint(10000, 99999)}"
        user_data["ID"] = user_id

        # Simpan data ke CSV
        with open(self.data_file, mode="a", newline="") as file:
            fieldnames = ["ID", "Nama:", "Username:", "Email:", "Password:", "Usia:", "Jenis Kelamin:", "Tujuan:"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            if file.tell() == 0:  
                writer.writeheader()
            
            row_data = {k: user_data.get(k, "") for k in fieldnames}
            
            data_line = ",".join(str(row_data[k]) for k in fieldnames) + ",\n"
            file.write(data_line)

        # Buat file profil pengguna
        profile_file = os.path.join(self.profile_folder, f"profile_{user_id}.csv")
        with open(profile_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Tanggal", "Rekomendasi", "Kalori", "Jarak", "Durasi", "Lama Tidur", "Detak jantung", "Cuaca", "Mood", "Lokasi"])

        messagebox.showinfo("Sign Up Successful", f"Account successfully created with ID: {user_id}. Please log in.")
        self.show_login_page()

    def is_username_taken(self, username):
        """Periksa apakah username sudah ada di CSV."""
        try:
            with open(self.data_file, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Username"] == username:
                        return True
        except FileNotFoundError:
            return False
        return False

    def validate_email(self, email):
        """Validasi format email"""
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None
