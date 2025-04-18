from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
import os
import datetime
import re

icons = {
    "Panda": "🐼", "Nasi": "🍚", "Ninja": "🥷", "Kadal": "🦎",
    "Baterai": "🔋", "Api": "🔥", "Polisi": "👮", "Mobil": "🚗", "Bintang": "✨"
}

class CFCNumberLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=10, **kwargs)
        self.selected_file = None

        self.add_widget(Label(text="CFC Number v1.0 - NOAH", font_size=24, color=(0, 1, 1, 1)))
        self.icon_spinner = Spinner(text="Panda", values=list(icons.keys()))
        self.add_widget(Label(text="Pilih Ikon:"))
        self.add_widget(self.icon_spinner)

        self.format_var = "A"
        format_layout = BoxLayout(size_hint_y=None, height=30)
        format_layout.add_widget(Button(text="+", on_press=lambda x: setattr(self, "format_var", "A")))
        format_layout.add_widget(Button(text="t.me/+", on_press=lambda x: setattr(self, "format_var", "B")))
        self.add_widget(Label(text="Format Tautan:"))
        self.add_widget(format_layout)

        self.split_var = "8"
        split_layout = BoxLayout(size_hint_y=None, height=30)
        for size in ["3", "6", "8", "10"]:
            split_layout.add_widget(Button(text=size, on_press=lambda x, s=size: setattr(self, "split_var", s)))
        self.add_widget(Label(text="Bagi per Grup:"))
        self.add_widget(split_layout)

        self.file_label = Label(text="File: Belum dipilih")
        self.add_widget(self.file_label)
        self.add_widget(Button(text="Pilih File", on_press=self.pilih_file))

        self.progress_bar = ProgressBar(max=100)
        self.add_widget(self.progress_bar)
        self.status_label = Label(text="Status: Idle")
        self.add_widget(self.status_label)

        button_layout = BoxLayout(size_hint_y=None, height=50)
        button_layout.add_widget(Button(text="Proses", on_press=self.proses))
        button_layout.add_widget(Button(text="Info", on_press=self.tampilkan_info))
        button_layout.add_widget(Button(text="Keluar", on_press=App.get_running_app().stop))
        self.add_widget(button_layout)

    def pilih_file(self, instance):
        self.selected_file = os.path.join(os.getcwd(), "SILUP_Part_53.txt")  # Ganti saat build
        self.file_label.text = f"File: {os.path.basename(self.selected_file)}"

    def proses(self, instance):
        if not self.selected_file:
            popup = Popup(title="Peringatan", content=Label(text="Pilih file dulu!"), size_hint=(0.5, 0.5))
            popup.open()
            return

        try:
            link_format = '+' if self.format_var == 'A' else 't.me/+'
            format_prefix = 'A_' if self.format_var == 'A' else 'B_'
            tanggal = datetime.datetime.now().strftime("%d_%m_%y")

            self.progress_bar.value = 0
            self.status_label.text = "Memuat data..."

            with open(self.selected_file, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
            if not lines:
                raise ValueError("File kosong")
            self.progress_bar.value = 20

            split_size = int(self.split_var)
            chunks = [lines[i:i + split_size] for i in range(0, len(lines), split_size)]
            self.progress_bar.value = 40
            self.status_label.text = "Mengelompokkan tautan..."

            os.makedirs("output", exist_ok=True)
            self.progress_bar.value = 60

            filename = os.path.basename(self.selected_file)
            part_match = re.search(r'_Part_(\d+)', filename)
            part_number = part_match.group(1) if part_match else "unknown"

            output_path = os.path.join("output", f"{format_prefix}{self.icon_spinner.text}_{tanggal}_Part_{part_number}.txt")
            with open(output_path, "w", encoding="utf-8") as f:
                for chunk in chunks:
                    for line in chunk:
                        f.write(f"{link_format}{line} {icons[self.icon_spinner.text]} Part_{part_number}\n")
                    f.write("\n")
            self.progress_bar.value = 80
            self.status_label.text = "Menyimpan hasil..."

            self.progress_bar.value = 100
            self.status_label.text = f"Berhasil: {output_path}"
        except Exception as e:
            popup = Popup(title="Error", content=Label(text=f"Gagal: {e}"), size_hint=(0.5, 0.5))
            popup.open()
            self.progress_bar.value = 0
            self.status_label.text = "Status: Gagal"

    def tampilkan_info(self, instance):
        popup = Popup(title="Info Aplikasi", content=Label(text=(
            "Icon Injector NOAH - CFC Number v1.0\n\n"
            "Tujuan:\n"
            "Skrip ini mengotomatiskan penambahan ikon ke daftar tautan Telegram.\n\n"
            "Fungsi:\n"
            "- Memilih ikon dari daftar.\n"
            "- Menggabungkan tautan dari file .txt.\n"
            "- Membagi tautan sesuai pilihan (3, 6, 8, 10).\n"
            "- Menyimpan hasil dengan ikon dan tanggal.\n\n"
            "Penggunaan:\n"
            "Cocok untuk mengatur dan mempercantik daftar tautan Telegram."
        )), size_hint=(0.8, 0.8))
        popup.open()

class CFCNumberApp(App):
    def build(self):
        return CFCNumberLayout()

if __name__ == "__main__":
    CFCNumberApp().run()