import tkinter as tk
from tkinter import Canvas, Label, Entry, StringVar, OptionMenu, Button, messagebox, Tk, PhotoImage
from PIL import Image, ImageTk
import csv
import os
import sys
from datetime import datetime 
import pandas as pd
import numpy as np
import joblib  

if getattr(sys, 'frozen', False):  
    base_path = os.path.dirname(sys.executable)
else: 
    base_path = os.path.dirname(__file__)

class InputPage:
    def __init__(self, master):
        self.master = master
        self.current_user_id = self.master.current_user_id 

        # File path menyimpan data
        self.profile_folder = os.path.join(base_path, "users_data")
        self.file_path = os.path.join(self.profile_folder, f"profile_{self.current_user_id}.csv")

        # Background Image
        background_image_path = os.path.join(base_path, "Desain AI", "inputbg.png")
        self.background_image = Image.open(background_image_path)
        self.background_image = self.background_image.resize((1366, 720))
        self.background_image = ImageTk.PhotoImage(self.background_image)

        # Create canvas and set background
        self.canvas = Canvas(self.master, width=1366, height=768, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")
        self.canvas.place(x=0, y=0)

        self.create_navigation()

        # Font style
        font_style = ("Times", 20, "bold")

        # Calories Input
        Label(self.master, text="Calories", font=font_style, bg="#FAE9D7", fg="#7F3535").place(x=250, y=150)
        self.entry_calories = Entry(self.master, font=("Arial", 15), fg="white", bg="#7F3535", justify="center")
        self.entry_calories.insert(0, "Enter calories to burn")
        self.entry_calories.place(x=250, y=200, width=350, height=50)

        # Heart Rate Input
        Label(self.master, text="Heart Rate", font=font_style, bg="#FAE9D7", fg="#7F3535").place(x=250, y=280)
        self.entry_heart_rate = Entry(self.master, font=("Arial", 15), fg="white", bg="#7F3535", justify="center")
        self.entry_heart_rate.insert(0, "Enter heart rate")
        self.entry_heart_rate.place(x=250, y=330, width=350, height=50)

        # Sleep Hours Input
        Label(self.master, text="Sleep Hours", font=font_style, bg="#FAE9D7", fg="#7F3535").place(x=750, y=280)
        self.entry_sleep = Entry(self.master, font=("Arial", 15), fg="white", bg="#7F3535", justify="center")
        self.entry_sleep.insert(0, "Enter sleep hours")
        self.entry_sleep.place(x=750, y=330, width=350, height=50)

        # clear and restore
        def clear_entry(event, entry_field, placeholder_text):
            if entry_field.get() == placeholder_text:
                entry_field.delete(0, 'end')

        def restore_placeholder(entry_field, placeholder_text):
            if entry_field.get() == "":
                entry_field.insert(0, placeholder_text)

        self.entry_calories.bind("<FocusIn>", lambda event: clear_entry(event, self.entry_calories, "Enter calories to burn"))
        self.entry_heart_rate.bind("<FocusIn>", lambda event: clear_entry(event, self.entry_heart_rate, "Enter heart rate"))
        self.entry_sleep.bind("<FocusIn>", lambda event: clear_entry(event, self.entry_sleep, "Enter sleep hours"))

        self.entry_calories.bind("<FocusOut>", lambda event: restore_placeholder(self.entry_calories, "Enter calories to burn"))
        self.entry_heart_rate.bind("<FocusOut>", lambda event: restore_placeholder(self.entry_heart_rate, "Enter heart rate"))
        self.entry_sleep.bind("<FocusOut>", lambda event: restore_placeholder(self.entry_sleep, "Enter sleep hours"))

        # Weather Dropdown
        Label(self.master, text="Weather", font=font_style, bg="#FAE9D7", fg="#7F3535").place(x=250, y=430)
        self.weather_var = StringVar(value="Select Weather")
        weather_options = ["Clear", "Fog", "Rain", "Snow"]
        weather_menu = OptionMenu(self.master, self.weather_var, *weather_options)
        weather_menu.place(x=250, y=480, width=350, height=50)
        weather_menu.config(bg="#7F3535", fg="white", font=("Arial", 15))

        # Mood Dropdown
        Label(self.master, text="Mood", font=font_style, bg="#FAE9D7", fg="#7F3535").place(x=750, y=430)
        self.mood_var = StringVar(value="Select Mood")
        mood_options = ["Happy", "Neutral", "Stressed", "Tired"]
        mood_menu = OptionMenu(self.master, self.mood_var, *mood_options)
        mood_menu.place(x=750, y=480, width=350, height=50)
        mood_menu.config(bg="#7F3535", fg="white", font=("Arial", 15))

        submit_image_path = os.path.join(base_path, "Desain AI", "submit.png")
        original_image = Image.open(submit_image_path)
        resized_image = original_image.resize((850, 100)) 
        self.submit_image = ImageTk.PhotoImage(resized_image)
        Button(self.master, image=self.submit_image, command=self.submit_action, bg="#FAE9D7", activebackground="#FAE9D7", borderwidth=0).place(x=250, y=570)

        # Muat model random forest
        model_path = os.path.join(base_path, "random_forest_model.pkl")
        self.forest = joblib.load(model_path)
        print("Model has been loaded successfully.")

    def submit_action(self):
        # Ambil data input
        calories = self.entry_calories.get()
        heart_rate = self.entry_heart_rate.get()
        sleep_hours = self.entry_sleep.get()
        weather = self.weather_var.get()
        mood = self.mood_var.get()
        date_time = datetime.now().strftime("%Y-%m-%d") 

        # Validasi input
        def is_number(value):
            """Periksa apakah input adalah angka (integer atau float)."""
            try:
                float(value)  
                return True
            except ValueError:
                return False

        # Validasi input untuk angka
        if not is_number(calories) or not is_number(heart_rate) or not is_number(sleep_hours):
            messagebox.showerror("Error", "Calories, Heart Rate, and Sleep Hours must be valid numbers!")
            return

        if weather == "Select Weather" or mood == "Select Mood":
            messagebox.showerror("Error", "Weather and Mood must be selected!")
            return

        # Normalisasi input berdasarkan asumsi min dan max
        calories_burned_normalized = self.normalize(float(calories), 1500.17, 3999.47)  
        sleep_hours_normalized = self.normalize(float(sleep_hours), 0, 12)  
        heart_rate_normalized = self.normalize(float(heart_rate), 60, 179) 
        weather_encoded = ["Clear", "Fog", "Rain", "Snow"].index(weather)
        mood_encoded = ["Happy", "Neutral", "Stressed", "Tired"].index(mood)

        # Buat sample data untuk prediksi
        sample = [
            calories_burned_normalized,
            sleep_hours_normalized,
            heart_rate_normalized,
            weather_encoded,
            mood_encoded,
        ]

        # Prediksi jenis workout
        predicted_workout = self.predict_forest(self.forest, sample)

        # Map hasil prediksi ke jenis workout
        workout_mapping = {
            0: "Cycling",
            1: "Gym Workout",
            2: "Running",
            3: "Swimming",
            4: "Walking",
            5: "Yoga",
        }

        # Tentukan rekomendasi berdasarkan prediksi model
        recommended_workout = workout_mapping.get(predicted_workout, "Unknown")

        # Load dataset untuk mencari jarak, durasi, dan lokasi
        dataset_path = os.path.join(base_path, "dataset_cleaned.csv")
        dataset_cleaned = pd.read_csv(dataset_path)
        
        # Fungsi untuk menghitung jarak Euclidean antara dua vektor
        def calculate_distance(row, sample):
            return np.sqrt(
                (row['calories_burned_normalized'] - sample[0]) ** 2 +
                (row['sleep_hours_normalized'] - sample[1]) ** 2 +
                (row['heart_rate_avg_normalized'] - sample[2]) ** 2 +
                (row['weather_conditions_encoded'] - sample[3]) ** 2 +
                (row['mood_encoded'] - sample[4]) ** 2
            )

        # Hitung jarak setiap baris di dataset dengan input sample
        dataset_cleaned['distance'] = dataset_cleaned.apply(lambda row: calculate_distance(row, sample), axis=1)

        # Ambil baris dengan jarak terkecil
        closest_row = dataset_cleaned.loc[dataset_cleaned['distance'].idxmin()]

        # Ambil informasi distance_km, active_minutes, dan location
        distance_km = closest_row['distance_km']
        active_minutes = closest_row['active_minutes']
        location = closest_row['location']

        # Simpan data ke file CSV pengguna
        file_exists = os.path.exists(self.file_path)
        with open(self.file_path, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["Tanggal", "Rekomendasi", "Kalori", "Jarak", "Durasi", "Lama Tidur", "Detak jantung", "Cuaca", "Mood", "Lokasi"])
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                "Tanggal": date_time,
                "Rekomendasi": recommended_workout, 
                "Kalori": calories,
                "Jarak": distance_km, 
                "Durasi": active_minutes,  
                "Lama Tidur": sleep_hours,
                "Detak jantung": heart_rate,
                "Cuaca": weather,
                "Mood": mood,
                "Lokasi": location, 
            })

        # Navigasi ke halaman hasil
        self.master.show_hasil_page()

    def normalize(self, value, min_value, max_value):
        """Fungsi untuk normalisasi input berdasarkan asumsi min-max scaling"""
        return (value - min_value) / (max_value - min_value)

    def predict_tree(self, tree, sample):
        """Fungsi untuk prediksi dengan satu decision tree"""
        if isinstance(tree, dict):  
            feature = tree["feature"]
            threshold = tree["threshold"]
            if sample[feature] <= threshold:
                return self.predict_tree(tree["left"], sample)
            else:
                return self.predict_tree(tree["right"], sample)
        else:  
            return tree

    def predict_forest(self, forest, sample):
        """Fungsi untuk prediksi dengan random forest"""
        predictions = [self.predict_tree(tree, sample) for tree in forest]
        return max(set(predictions), key=predictions.count)

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