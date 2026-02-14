import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import sqlite3
import datetime

# Expert OCR Logic Placeholder (Requires Tesseract)
try:
    import pytesseract
    from PIL import Image
except ImportError:
    pytesseract = None

class ContractorBOSS(App):
    def build(self):
        self.title = "Contractor BOSS - Enterprise"
        self.conn = sqlite3.connect("vault.db")
        self.create_tables()
        self.root = BoxLayout(orientation='vertical')
        
        # Dashboard
        self.dashboard = BoxLayout(orientation='vertical', size_hint=(1, 0.3))
        self.lbl_profit = Label(text="NET PROFIT: $0.00", font_size='30sp', color=(0,1,0,1))
        self.dashboard.add_widget(self.lbl_profit)
        self.root.add_widget(self.dashboard)
        
        # Actions
        btn_scan = Button(text="📷 SCAN RECEIPT", font_size='24sp', on_release=self.scan_receipt)
        self.root.add_widget(btn_scan)
        
        self.update_dashboard()
        return self.root

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, cost REAL, date TEXT)")
        self.conn.commit()

    def update_dashboard(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT SUM(cost) FROM expenses")
        exp = cursor.fetchone()[0] or 0.0
        self.lbl_profit.text = f"NET PROFIT: -${exp:,.2f}"

    def scan_receipt(self, instance):
        if not pytesseract:
            self.show_popup("Error", "OCR Libraries Missing")
            return
        # Simulation
        self.show_popup("Scan", "Simulating OCR Scan...")
        self.log_expense(50.00)

    def log_expense(self, amount):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO expenses (cost, date) VALUES (?, ?)", (amount, str(datetime.date.today())))
        self.conn.commit()
        self.update_dashboard()

    def show_popup(self, title, msg):
        popup = Popup(title=title, content=Label(text=msg), size_hint=(0.8, 0.3))
        popup.open()

if __name__ == '__main__':
    ContractorBOSS().run()
