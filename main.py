import tkinter as tk
import os
import sys
from homepage import HomePage
from login_signup import LoginSignupPage 
from dashboard import DashboardPage
from input import InputPage
from hasil import HasilPage
from historypage import HistoryPage
from profilepage import ProfilePage

if getattr(sys, 'frozen', False):  
    base_path = os.path.dirname(sys.executable)
else:  
    base_path = os.path.dirname(__file__)

# Path ke file yang dibutuhkan aplikasi
dataset_path = os.path.join(base_path, 'dataset_cleaned.csv')
users_data_path = os.path.join(base_path, 'users_data.csv')
model_path = os.path.join(base_path, 'random_forest_model.pkl')
desain_folder = os.path.join(base_path, 'Desain AI')
users_data_folder = os.path.join(base_path, 'users_data')

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.current_user_id = None 

        self.title("FitGuide")
        self.geometry("1366x768")
        
        # Halaman Pertama
        self.home_page = HomePage(self)
        self.home_page.pack(fill="both", expand=True)

    def show_login_page(self):
        self.home_page.pack_forget()
        login_signup_page = LoginSignupPage(self)
        login_signup_page.show_login_page()

    def show_signup_page(self):
        self.home_page.pack_forget()
        login_signup_page = LoginSignupPage(self)
        login_signup_page.show_signup_page()

    def show_dashboard_page(self):
        self.home_page.pack_forget()
        dashboard_page = DashboardPage(self)
    
    def show_input_page(self):
        self.home_page.pack_forget()
        input_page = InputPage(self)

    def show_hasil_page(self):
        self.home_page.pack_forget()
        hasil_page = HasilPage(self)

    def show_history_page(self):
        self.home_page.pack_forget()
        history_page = HistoryPage(self)

    def show_profile_page(self):
        self.home_page.pack_forget()
        profile_page = ProfilePage(self)

if __name__ == "__main__":
    app = App()
    app.mainloop()
