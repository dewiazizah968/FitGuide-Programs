import tkinter as tk
from tkinter import messagebox, Canvas
from PIL import Image, ImageTk
import csv
import os
import sys

if getattr(sys, 'frozen', False):  
    base_path = os.path.dirname(sys.executable)
else: 
    base_path = os.path.dirname(__file__)

class HasilPage:
    def __init__(self, master):
        self.master = master
        self.current_user = self.master.current_user_id

        self.profile_folder = os.path.join(base_path, "users_data")
        self.file_path = os.path.join(self.profile_folder, f"profile_{self.current_user}.csv")

        # Background
        background_image_path = os.path.join(base_path, "Desain AI", "hasilbg.png")
        self.background_image = Image.open(background_image_path)
        self.background_image = self.background_image.resize((1366, 720))  
        self.background_image = ImageTk.PhotoImage(self.background_image)

        # Create canvas and set background
        self.canvas = Canvas(self.master, width=1366, height=768, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")
        self.canvas.place(x=0, y=0)

        self.create_navigation()

        # Kolom Data
        self.data_labels = {}

        # Definisikan font untuk semua label
        label_font = ("Times", 20, "bold")  # Font untuk label utama
        data_font = ("Times", 15)           # Font untuk data teks

        # Fungsi untuk membuat kotak data dengan teks rata tengah
        def create_data_label(master, text, x, y, width, height):
            data_label = tk.Label(
                master, 
                text=text, 
                font=data_font, 
                bg="#7F3535", 
                fg="white", 
                width=width, 
                height=height, 
                anchor="center", 
                relief="solid", 
                borderwidth=0
            )
            data_label.place(x=x, y=y)
            return data_label

        # Label dan data: "Rekomendasi"
        label_rekomendasi = tk.Label(self.master, text="Rekomendasi:", font=label_font, bg="#FAE9D7", fg="#7F3535")
        label_rekomendasi.place(x=920, y=150)  # Koordinat untuk label
        self.data_labels["Rekomendasi"] = create_data_label(self.master, "Still Empty", 780, 200, 40, 2)

        # Label dan data: "Tanggal"
        label_tanggal = tk.Label(self.master, text="Tanggal:", font=label_font, bg="#FAE9D7", fg="#7F3535")
        label_tanggal.place(x=700, y=300)  # Koordinat untuk label
        self.data_labels["Tanggal"] = create_data_label(self.master, "Still Empty", 700, 350, 25, 2)

        # Label dan data: "Jarak (km)"
        label_jarak = tk.Label(self.master, text="Jarak (km):", font=label_font, bg="#FAE9D7", fg="#7F3535")
        label_jarak.place(x=1050, y=300)  # Koordinat untuk label
        self.data_labels["Jarak (km)"] = create_data_label(self.master, "Still Empty", 1050, 350, 25, 2)

        # Label dan data: "Waktu (menit)"
        label_waktu = tk.Label(self.master, text="Waktu (menit):", font=label_font, bg="#FAE9D7", fg="#7F3535")
        label_waktu.place(x=700, y=450)  # Koordinat untuk label
        self.data_labels["Waktu (menit)"] = create_data_label(self.master, "Still Empty", 700, 500, 25, 2)

        # Label dan data: "Lokasi"
        label_lokasi = tk.Label(self.master, text="Lokasi:", font=label_font, bg="#FAE9D7", fg="#7F3535")
        label_lokasi.place(x=1050, y=450)  # Koordinat untuk label
        self.data_labels["Lokasi"] = create_data_label(self.master, "Still Empty", 1050, 500, 25, 2)

        # Tombol
        tk.Button(self.master, text="Repeat", command=self.repeat_and_clear, font=("Times", 20, "bold"), bg="#7F3535", fg="white").place(x=740, y=610, width=200, height=40)
        tk.Button(self.master, text="Save", command=self.save_data, font=("Times", 20, "bold"), bg="#7F3535", fg="white").place(x=1090, y=610, width=200, height=40)

        # Load data dari file CSV
        self.load_data()

    def repeat_and_clear(self):
        """Hapus data terbaru dari file CSV dan navigasi ke halaman input."""
        if os.path.exists(self.file_path):
            # Membaca semua data dari file CSV
            with open(self.file_path, mode="r") as file:
                reader = list(csv.DictReader(file))  # Baca semua data sebagai list
            if reader:
                # Menghapus baris terakhir (data terbaru)
                reader = reader[:-1]

                # Menulis ulang file CSV tanpa baris terakhir
                with open(self.file_path, mode="w", newline="") as file:
                    writer = csv.DictWriter(file, fieldnames=reader[0].keys())
                    writer.writeheader() 
                    writer.writerows(reader)  

                messagebox.showinfo("Info", "Are you sure you want to repeat?")
            else:
                messagebox.showinfo("Info", "No data to delete.")
        else:
            messagebox.showerror("Error", "CSV file not found.")
        
        # Setelah data dihapus, navigasi ke halaman input
        self.master.show_input_page()

    def save_data(self):
        """Simpan data dengan popup notifikasi."""
        messagebox.showinfo("Success", "Data saved successfully!")

    def load_data(self):
        """Memuat data terbaru pengguna dari file CSV dan menampilkan gambar berdasarkan rekomendasi."""
        if os.path.exists(self.file_path):
            with open(self.file_path, mode="r") as file:
                reader = list(csv.DictReader(file)) 
                if reader:  # Jika ada data
                    latest_data = reader[-1] 
                    rekomendasi = latest_data.get("Rekomendasi", "Still Empty")
                    
                    # Update label dengan rekomendasi
                    self.data_labels["Rekomendasi"].config(text=rekomendasi)

                    images_folder = os.path.join(base_path, "Desain AI")

                    # Tentukan gambar berdasarkan rekomendasi
                    image_path = ""
                    if rekomendasi == "Swimming":
                        image_path = os.path.join(images_folder, "swimming.png")
                    elif rekomendasi == "Cycling":
                        image_path = os.path.join(images_folder, "cycling.png")
                    elif rekomendasi == "Running":
                        image_path = os.path.join(images_folder, "running.png")
                    elif rekomendasi == "Walking":
                        image_path = os.path.join(images_folder, "walking.png")
                    elif rekomendasi == "Yoga":
                        image_path = os.path.join(images_folder, "yoga.png")
                    elif rekomendasi == "Gym Workout":
                        image_path = os.path.join(images_folder, "gym.png")

                    # Load dan tampilkan gambar
                    if image_path and os.path.exists(image_path):  
                        image = Image.open(image_path)
                        image = image.resize((450, 450))  
                        self.image_tk = ImageTk.PhotoImage(image)

                        if hasattr(self, 'image_label'):
                            self.image_label.destroy()

                        # Tempatkan gambar di canvas
                        self.image_label = tk.Label(self.master, image=self.image_tk, bg="#FFD8B0")
                        self.image_label.place(x=100, y=180)  
                    else:
                        messagebox.showerror("Error", f"Image not found: {image_path}")

                    # Update data lainnya
                    self.data_labels["Tanggal"].config(text=latest_data.get("Tanggal", "Still Empty"))
                    self.data_labels["Jarak (km)"].config(text=latest_data.get("Jarak", "Still Empty"))
                    self.data_labels["Waktu (menit)"].config(text=latest_data.get("Durasi", "Still Empty"))
                    self.data_labels["Lokasi"].config(text=latest_data.get("Lokasi", "Still Empty"))
                else:  # Jika CSV kosong
                    for label in self.data_labels.values():
                        label.config(text="Still Empty")
                    if hasattr(self, 'image_label'):
                        self.image_label.destroy()
        else:
            for label in self.data_labels.values():
                label.config(text="Still Empty")
            if hasattr(self, 'image_label'):
                self.image_label.destroy()

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
            fg="#823E3E",
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