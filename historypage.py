import tkinter as tk
from tkinter import ttk, Canvas, messagebox
from PIL import Image, ImageTk
from tkinter.font import Font
import csv
import os
import sys

if getattr(sys, 'frozen', False):  
    base_path = os.path.dirname(sys.executable)
else: 
    base_path = os.path.dirname(__file__)

class HistoryPage:
    def __init__(self, master):
        self.master = master
        self.current_user_id = self.master.current_user_id 

        # File path menyimpan data
        self.profile_folder = os.path.join(base_path, "users_data")
        self.file_path = os.path.join(self.profile_folder, f"profile_{self.current_user_id}.csv")

        # Background Image
        background_image_path = os.path.join(base_path, "Desain AI", "historybg.png")
        self.background_image = Image.open(background_image_path)
        self.background_image = self.background_image.resize((1366, 720))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        # Create canvas and set background
        self.canvas = Canvas(self.master, width=1366, height=720, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")
        self.canvas.place(x=0, y=0)

        self.create_table()

        self.create_navigation()

    def create_table(self):
        # Frame untuk tabel dan scrollbar
        frame = tk.Frame(self.master, bg="#FAE9D7")
        frame.place(x=50, y=150, width=1266, height=500)

        # Scrollbar Vertikal
        scrollbar_y = tk.Scrollbar(frame, orient="vertical")
        scrollbar_y.pack(side="right", fill="y")

        # Scrollbar Horizontal
        scrollbar_x = tk.Scrollbar(frame, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")

        # Treeview untuk tabel
        self.tree = ttk.Treeview(
            frame,
            columns=("No", "Tanggal", "Rekomendasi", "Kalori", "Jarak", "Durasi", "Lama Tidur", "Detak Jantung", "Cuaca", "Mood", "Lokasi"),
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            show="headings", height=15,
        )

        # Konfigurasi scrollbar
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)

        # Definisi heading dan kolom tabel
        headers = ["No", "Tanggal", "Rekomendasi", "Kalori", "Jarak", "Durasi", "Lama Tidur", "Detak Jantung", "Cuaca", "Mood", "Lokasi"]

        # header_font = Font(family="Times", size=20, weight="bold")
        cell_font = Font(family="Times", size=15)

        for header in headers:
            self.tree.heading(header, text=header)
            self.tree.column(header, anchor="center", width=80)

        # Menambahkan tabel ke frame
        self.tree.pack(fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview", 
                        font=cell_font,  # Font untuk isi tabel
                        rowheight=25,    # Tinggi baris
                        background="#FAE9D7",  # Warna latar belakang baris biasa
                        fieldbackground="#FAE9D7") 
        style.configure("Treeview.Heading",
                        font=("Times", 15, "bold"),  # Font header
                        background="#FAE9D7",       # Warna latar header
                        foreground="#823E3E")        
        style.map("Treeview",
                  background=[("selected", "#823E3E")],  # Warna saat baris dipilih
                  foreground=[("selected", "#FFFFFF")])

        # Load data dari CSV
        self.load_history_data()

    def load_history_data(self):
        # Cek apakah file CSV ada
        if not os.path.exists(self.file_path):
            print(f"File {self.file_path} not found.")
            return

        # Membaca file CSV
        with open(self.file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for idx, row in enumerate(reader, start=1):
                self.tree.insert("", "end", values=(
                    idx,
                    row.get("Tanggal", "-"),
                    row.get("Rekomendasi", "-"),
                    row.get("Kalori", "-"),
                    row.get("Jarak", "-"),
                    row.get("Durasi", "-"),
                    row.get("Lama Tidur", "-"),
                    row.get("Detak jantung", "-"),
                    row.get("Cuaca", "-"),
                    row.get("Mood", "-"),
                    row.get("Lokasi", "-"),
                ))

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
            fg="#823E3E",
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
            fg="#000",
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