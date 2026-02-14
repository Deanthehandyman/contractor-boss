from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.properties import StringProperty


# ────────────────────────────────────────────────
#                  Backend Logic
# ────────────────────────────────────────────────
class JobStatusEngine:
    def __init__(self):
        self.jobs = {
            "Starlink Install - Site A": "Completed",
            "RV Pad Electrical Rough-in": "In Progress",
            "Generator Install - Johnson": "Pending",
        }

    def add_job(self, job_name: str) → str:
        job_name = job_name.strip()
        if not job_name:
            return "Error: Job name cannot be empty."
        if job_name in self.jobs:
            return f"Error: Job '{job_name}' already exists."
        self.jobs[job_name] = "Pending"
        return f"Added job: {job_name}"

    def update_status(self, job_name: str, status: str) → str:
        job_name = job_name.strip()
        status = status.strip()
        if not job_name or not status:
            return "Error: Both job name and status are required."
        if job_name not in self.jobs:
            return f"Error: Job '{job_name}' not found."
        self.jobs[job_name] = status
        return f"Updated '{job_name}' → {status}"

    def get_all_jobs(self) -> list[tuple[str, str]]:
        return list(self.jobs.items())


def perform_ocr(image_path: str) -> str:
    # Placeholder — replace with pytesseract / easyocr / Google Vision later
    print(f"OCR simulation on: {image_path}")
    return (
        "Extracted Invoice Data:\n"
        "• Materials: $450.00\n"
        "• Labor: $200.00\n"
        "• Tax: $38.25\n"
        "Total: $688.25"
    )


# ────────────────────────────────────────────────
#                   UI Components
# ────────────────────────────────────────────────
class DashboardTab(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = dp(20)
        self.spacing = dp(12)

        self.add_widget(
            Label(
                text="Profit & Loss Overview",
                font_size="26sp",
                bold=True,
                size_hint_y=None,
                height=dp(60),
            )
        )

        stats = [
            ("Gross Income", "$12,500", (0.2, 0.8, 0.2, 1)),
            ("Materials & Expenses", "$4,200", (0.9, 0.3, 0.2, 1)),
            ("Net Profit", "$8,300", (0.1, 0.6, 0.9, 1), "24sp", True),
        ]

        for label, value, color, *extra in stats:
            row = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(48))
            row.add_widget(Label(text=label, halign="left", valign="middle"))
            val_label = Label(
                text=value,
                color=color,
                bold=extra[-1] if extra else False,
                font_size=extra[0] if extra else "18sp",
            )
            val_label.bind(size=val_label.setter("text_size"))
            row.add_widget(val_label)
            self.add_widget(row)


class JobManagerTab(BoxLayout):
    message = StringProperty("Ready.")

    def __init__(self, engine: JobStatusEngine, **kwargs):
        super().__init__(**kwargs)
        self.engine = engine
        self.orientation = "vertical"
        self.padding = dp(20)
        self.spacing = dp(15)

        # Header
        self.add_widget(
            Label(
                text="Job Status Manager",
                font_size="26sp",
                bold=True,
                size_hint_y=None,
                height=dp(60),
            )
        )

        # Add new job
        add_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(48))
        add_layout.add_widget(Label(text="New Job:", size_hint_x=0.3))
        self.new_job_input = TextInput(multiline=False, hint_text="e.g. Heat Pump Install")
        add_layout.add_widget(self.new_job_input)
        self.add_widget(add_layout)

        add_btn = Button(text="Add Job", size_hint_y=None, height=dp(52))
        add_btn.bind(on_press=self.add_job)
        self.add_widget(add_btn)

        # Status update section
        update_grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(48))
        update_grid.add_widget(Label(text="Job:", size_hint_x=0.3))
        self.job_name_input = TextInput(multiline=False, hint_text="Exact job name")
        update_grid.add_widget(self.job_name_input)

        self.add_widget(update_grid)

        status_grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(48))
        status_grid.add_widget(Label(text="Set Status:", size_hint_x=0.3))
        self.status_input = TextInput(
            multiline=False, hint_text="e.g. Completed, In Progress, Cancelled"
        )
        status_grid.add_widget(self.status_input)
        self.add_widget(status_grid)

        update_btn = Button(text="Update Status", size_hint_y=None, height=dp(52))
        update_btn.bind(on_press=self.update_status)
        self.add_widget(update_btn)

        # Feedback label
        self.feedback_lbl = Label(
            text=self.message,
            color=(0.9, 0.9, 0.4, 1),
            size_hint_y=None,
            height=dp(60),
            halign="center",
            valign="middle",
        )
        self.feedback_lbl.bind(size=self.feedback_lbl.setter("text_size"))
        self.add_widget(self.feedback_lbl)

        # Current jobs list
        self.add_widget(Label(text="Current Jobs:", font_size="18sp", bold=True))

        scroll = ScrollView(size_hint=(1, None), height=dp(220))
        self.jobs_container = BoxLayout(orientation="vertical", size_hint_y=None)
        self.jobs_container.bind(minimum_height=self.jobs_container.setter("height"))
        scroll.add_widget(self.jobs_container)
        self.add_widget(scroll)

        self.refresh_jobs_list()

    def set_message(self, text: str, color=(0.9, 0.9, 0.4, 1)):
        self.message = text
        self.feedback_lbl.text = text
        self.feedback_lbl.color = color

    def add_job(self, instance):
        result = self.engine.add_job(self.new_job_input.text)
        if result.startswith("Error"):
            self.set_message(result, (0.9, 0.3, 0.2, 1))
        else:
            self.set_message(result, (0.3, 0.9, 0.4, 1))
            self.new_job_input.text = ""
            self.refresh_jobs_list()

    def update_status(self, instance):
        result = self.engine.update_status(self.job_name_input.text, self.status_input.text)
        if result.startswith("Error"):
            self.set_message(result, (0.9, 0.3, 0.2, 1))
        else:
            self.set_message(result, (0.3, 0.9, 0.4, 1))
            self.refresh_jobs_list()

    def refresh_jobs_list(self):
        self.jobs_container.clear_widgets()
        for job, status in self.engine.get_all_jobs():
            row = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(42))
            row.add_widget(Label(text=job, halign="left", valign="middle"))
            status_color = {
                "Completed": (0.2, 0.8, 0.2, 1),
                "In Progress": (0.9, 0.6, 0.1, 1),
                "Pending": (0.6, 0.6, 0.9, 1),
            }.get(status, (0.7, 0.7, 0.7, 1))
            lbl = Label(text=status, color=status_color, bold=True)
            row.add_widget(lbl)
            self.jobs_container.add_widget(row)


class OCRScannerTab(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = dp(20)
        self.spacing = dp(15)

        self.add_widget(
            Label(
                text="Receipt / Invoice Scanner",
                font_size="26sp",
                bold=True,
                size_hint_y=None,
                height=dp(60),
            )
        )

        self.result_label = Label(
            text="Awaiting scan...\n\n(press button to simulate)",
            halign="center",
            valign="middle",
            markup=True,
            text_size=(None, None),
        )
        self.add_widget(self.result_label)

        scan_btn = Button(
            text="Simulate Camera / Upload Scan", size_hint_y=None, height=dp(60)
        )
        scan_btn.bind(on_press=self.run_ocr)
        self.add_widget(scan_btn)

    def run_ocr(self, instance):
        # In real app: open camera / file chooser → get path
        fake_path = "uploads/invoice_2026-02-13.jpg"
        result = perform_ocr(fake_path)
        self.result_label.text = f"[b]OCR Result:[/b]\n\n{result}"


# ────────────────────────────────────────────────
#                     Main App
# ────────────────────────────────────────────────
class HandymanApp(App):
    def build(self):
        engine = JobStatusEngine()  # could be global or passed around

        tabs = TabbedPanel(do_default_tab=False, tab_width=dp(180))

        # Dashboard
        dashboard_tab = TabbedPanelItem(text="Dashboard")
        dashboard_tab.add_widget(DashboardTab())
        tabs.add_widget(dashboard_tab)

        # Jobs
        jobs_tab = TabbedPanelItem(text="Jobs")
        jobs_tab.add_widget(JobManagerTab(engine))
        tabs.add_widget(jobs_tab)

        # Scanner
        scanner_tab = TabbedPanelItem(text="Scanner")
        scanner_tab.add_widget(OCRScannerTab())
        tabs.add_widget(scanner_tab)

        return tabs


if __name__ == "__main__":
    HandymanApp().run()
