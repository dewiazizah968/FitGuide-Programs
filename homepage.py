from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import os
import sys

if getattr(sys, 'frozen', False):  
    base_path = os.path.dirname(sys.executable)
else: 
    base_path = os.path.dirname(__file__)

class HomePage(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # Canvas untuk scroll
        self.canvas = tk.Canvas(self)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.bg_image1 = Image.open(os.path.join(base_path, "Desain AI", "21.png")).resize((1366, 768))
        self.bg_image2 = Image.open(os.path.join(base_path, "Desain AI", "22.png")).resize((1366, 768))
        self.bg_image3 = Image.open(os.path.join(base_path, "Desain AI", "21.png")).resize((1920, 1080))

        self.bg_image1 = ImageTk.PhotoImage(self.bg_image1)
        self.bg_image2 = ImageTk.PhotoImage(self.bg_image2)
        self.bg_image3 = ImageTk.PhotoImage(self.bg_image3)

        self.canvas.create_image(0, 0, image=self.bg_image1, anchor="nw")
        self.canvas.create_image(0, 768, image=self.bg_image2, anchor="nw")
        self.canvas.create_image(0, 1536, image=self.bg_image3, anchor="nw")
        
        # Navbar logo
        self.logo_image = Image.open(os.path.join(base_path, "Desain AI", "logonavbar.png")).resize((400, 150))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.canvas.create_image(8, 10, image=self.logo_image, anchor="nw")

        # Welcome image
        self.welcome_image = tk.PhotoImage(file=os.path.join(base_path, "Desain AI", "welcome.png"))
        self.canvas.create_image(250, 155, image=self.welcome_image, anchor="nw")

        # About Us section
        self.about_us_image = tk.PhotoImage(file=os.path.join(base_path, "Desain AI", "about_us.png"))
        self.about_uss_image = Image.open(os.path.join(base_path, "Desain AI", "about_uss.png")).resize((550, 550))
        self.about_uss_image = ImageTk.PhotoImage(self.about_uss_image)
        self.canvas.create_image(200, 800, image=self.about_us_image, anchor="nw")
        self.canvas.create_image(800, 920, image=self.about_uss_image, anchor="nw")
        self.canvas.create_text(
            465, 1100,  
            text="FitGuide adalah aplikasi inovatif yang dirancang untuk membantu Anda mencapai tujuan kebugaran dengan cara yang lebih mudah, efisien, dan personal. Kami percaya bahwa setiap individu memiliki kebutuhan unik, dan itulah mengapa kami mengembangkan sistem rekomendasi workout berbasis data yang sepenuhnya disesuaikan dengan Anda.", 
            font=("Times", 20),
            fill="#FFF",
            width=650, 
            justify="center" 
        )

        mission_text = (
            "Misi Kami:\n"
            "• Meningkatkan kualitas hidup melalui kebugaran.\n"
            "• Memberikan dukungan personal dengan rekomendasi yang relevan dan efektif.\n"
            "• Membantu pengguna mencapai tujuan kebugaran mereka tanpa tekanan atau kebingungan."
        )
        
        self.canvas.create_text(
            50, 1250, 
            text=mission_text, 
            font=("Times", 20),
            fill="#FFF",
            width=650, 
            anchor="nw" 
        )

        self.meet_image = tk.PhotoImage(file=os.path.join(base_path, "Desain AI", "meet.png"))
        self.canvas.create_image(280, 1600, image=self.meet_image, anchor="nw")

        self.dev1_photo = Image.open(os.path.join(base_path, "Desain AI", "shei.png")).resize((350, 350))
        self.dev2_photo = Image.open(os.path.join(base_path, "Desain AI", "dew.png")).resize((350, 350))
        self.dev3_photo = Image.open(os.path.join(base_path, "Desain AI", "ime.png")).resize((350, 350))

        self.dev1_photo = ImageTk.PhotoImage(self.dev1_photo)
        self.dev2_photo = ImageTk.PhotoImage(self.dev2_photo)
        self.dev3_photo = ImageTk.PhotoImage(self.dev3_photo)

        self.canvas.create_image(50, 1800, image=self.dev1_photo, anchor="nw")
        self.canvas.create_text(225, 2100, text="Name: Sheila Edistya Salsabilla\nNIM: 23031554056", font=("Times", 19), fill="#FFF")

        self.canvas.create_image(500, 1800, image=self.dev2_photo, anchor="nw")
        self.canvas.create_text(675, 2100, text="Name: Dewi Isarotul Azizah\nNIM: 23031554069", font=("Times", 20), fill="#FFF")

        self.canvas.create_image(950, 1800, image=self.dev3_photo, anchor="nw")
        self.canvas.create_text(1115, 2100, text="Name: Fatimah Azzaroh A\nNIM: 23031554202", font=("Times", 20), fill="#FFF")

        self.footer = Image.open(os.path.join(base_path, "Desain AI", "logonavbar.png")).resize((431, 151))
        self.footer = ImageTk.PhotoImage(self.footer)
        self.canvas.create_image(450, 2350, image=self.footer, anchor="nw")
        
        # Buttons
        signup_image_raw = Image.open(os.path.join(base_path, "Desain AI", "signupbutton.png"))
        signup_image_resized = signup_image_raw.resize((200, 70))  
        signup_image = ImageTk.PhotoImage(signup_image_resized)

        login_image_raw = Image.open(os.path.join(base_path, "Desain AI", "loginbutton.png"))
        login_image_resized = login_image_raw.resize((750, 80))  
        login_image = ImageTk.PhotoImage(login_image_resized)

        # Login button
        self.login_button = tk.Button(
            self,
            image=login_image,  
            bg="#FFD8B0",
            activebackground="#FFD8B0",
            borderwidth=0,
            command=self.login_action
        )
        self.login_button.image = login_image  
        self.canvas.create_window(285, 620, anchor="nw", window=self.login_button)

        # Signup button
        self.signup_button = tk.Button(
            self,
            image=signup_image,  
            bg="#FFD8B0",
            activebackground="#FFD8B0",
            borderwidth=0,
            command=self.signup_action
        )
        self.signup_button.image = signup_image 
        self.canvas.create_window(1120, 26, anchor="nw", window=self.signup_button)

    def login_action(self):
        self.master.show_login_page()

    def signup_action(self):
        self.master.show_signup_page()
