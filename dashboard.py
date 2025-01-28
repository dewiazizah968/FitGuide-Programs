import tkinter as tk
from tkinter import messagebox, Canvas
from PIL import Image, ImageTk
import csv
import os
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
from datetime import datetime

if getattr(sys, 'frozen', False):  
    base_path = os.path.dirname(sys.executable)
else: 
    base_path = os.path.dirname(__file__)

class DashboardPage:
    def __init__(self, master):
        self.master = master
        self.current_user = self.master.current_user_id
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        # Path dinamis untuk folder dan file
        self.profile_folder = os.path.join(base_path, "users_data")
        self.file_path = os.path.join(self.profile_folder, f"profile_{self.current_user}.csv")
        self.desain_folder = os.path.join(base_path, "Desain AI")

        # Background
        self.background_image_path = os.path.join(self.desain_folder, "dashboardbg.png")
        self.background_image = Image.open(self.background_image_path)
        self.background_image = self.background_image.resize((1366, 720))  
        self.background_image = ImageTk.PhotoImage(self.background_image)

        # Create canvas and set background
        self.canvas = Canvas(self.master, width=1366, height=768, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")
        self.canvas.place(x=0, y=0)

        # Display badges
        self.display_badges()

        # Display last activity
        self.display_last_activity()

        # Bar chart for calories
        self.create_bar_chart()

        # Line chart for distance
        self.create_line_chart()

        self.create_navigation()

    def display_badges(self):
        try:
            with open(self.file_path, mode='r') as file:
                reader = csv.DictReader(file)
                row_count = sum(1 for _ in reader)

            if row_count < 5:
                badge_file = "newbie.png"
            elif 5 <= row_count <= 10:
                badge_file = "consisten.png"
            elif 11 <= row_count <= 20:
                badge_file = "beginner.png"
            elif 21 <= row_count <= 35:
                badge_file = "warrior.png"
            elif 36 <= row_count <= 50:
                badge_file = "champion.png"
            else:  # row_count > 50
                badge_file = "legend.png"

            # Path dinamis untuk badge file
            badge_path = os.path.join(self.desain_folder, badge_file)
            badge_image = Image.open(badge_path)
            badge_image = badge_image.resize((890, 300)) 
            badge_image = ImageTk.PhotoImage(badge_image)

            # Display badge
            self.canvas.create_image(0, 125, image=badge_image, anchor="nw")
            self.badge_image = badge_image
        except FileNotFoundError:
            messagebox.showerror("Error", "Badge file not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error displaying badge: {e}")

    def display_last_activity(self):
        try:
            with open(self.file_path, mode='r') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                if rows:
                    last_activity = rows[-1]
                    text = ""
                    text += f"Tanggal: {last_activity['Tanggal']}\n"
                    text += f"Rekomendasi: {last_activity['Rekomendasi']}\n"
                    text += f"Cuaca: {last_activity['Cuaca']}\n"
                    text += f"Mood: {last_activity['Mood']}\n"
                    text += f"Lokasi: {last_activity['Lokasi']}"
                else:
                    text = "Tidak ada data aktivitas."
        except FileNotFoundError:
            text = "File tidak ditemukan."

        self.canvas.create_text(915, 215, text=text, anchor="nw", font=("Times", 20), fill="#823E3E")

    def create_bar_chart(self):
        try:
            data = self.load_csv_data()

            grouped_data = defaultdict(float)
            for row in data:
                grouped_data[row['Tanggal']] += float(row['Kalori'])

            sorted_data = sorted(grouped_data.items(), key=lambda x: datetime.strptime(x[0], '%Y-%m-%d'), reverse=True)
            limited_data = sorted_data[:6]
            dates, calories = zip(*limited_data)
            short_dates = [datetime.strptime(date, '%Y-%m-%d').strftime('%m-%d') for date in dates]

            fig, ax = plt.subplots(figsize=(6, 2))
            fig.patch.set_facecolor('#FAE9D7')  
            ax.set_facecolor('#FAE9D7')
            ax.bar(short_dates, calories, color='#823E3E')
            ax.set_ylabel("Kalori")
            ax.tick_params(axis='x', rotation=0)

            chart = FigureCanvasTkAgg(fig, self.master)
            chart_widget = chart.get_tk_widget()
            chart_widget.place(x=45, y=470)
        except Exception as e:
            messagebox.showerror("Error", f"Errors when creating calorie charts: {e}")

    def create_line_chart(self):
        try:
            data = self.load_csv_data()

            grouped_data = defaultdict(float)
            for row in data:
                grouped_data[row['Tanggal']] += float(row['Jarak'])

            sorted_data = sorted(grouped_data.items(), key=lambda x: datetime.strptime(x[0], '%Y-%m-%d'), reverse=True)
            limited_data = sorted_data[:6]
            dates, distances = zip(*limited_data)
            short_dates = [datetime.strptime(date, '%Y-%m-%d').strftime('%m-%d') for date in dates]

            fig, ax = plt.subplots(figsize=(6, 2))
            fig.patch.set_facecolor('#FAE9D7')  
            ax.set_facecolor('#FAE9D7')
            ax.plot(short_dates, distances, marker='o', color='#823E3E', linestyle='-')
            ax.set_ylabel("Jarak (km)")
            ax.tick_params(axis='x', rotation=0)

            chart = FigureCanvasTkAgg(fig, self.master)
            chart_widget = chart.get_tk_widget()
            chart_widget.place(x=720, y=470)
        except Exception as e:
            messagebox.showerror("Error", f"Errors when creating distance graphs: {e}")

    def load_csv_data(self):
        with open(self.file_path, mode='r') as file:
            reader = csv.DictReader(file)
            return list(reader)
        
    def create_navigation(self):
        # Dashboard Label
        dashboard_label = tk.Label(
            self.master,
            text="Dashboard",
            font=("Times", 20, "bold"),
            fg="#823E3E",
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

    def on_close(self):
            self.master.quit() 