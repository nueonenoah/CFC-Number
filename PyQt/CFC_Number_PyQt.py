from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QFileDialog, QRadioButton, QVBoxLayout, QWidget
import os
import datetime
import re

icons = {
    "Panda": "🐼", "Nasi": "🍚", "Ninja": "🥷", "Kadal": "🦎",
    "Baterai": "🔋", "Api": "🔥", "Polisi": "👮", "Mobil": "🚗", "Bintang": "✨"
}

class CFCMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CFC Number v1.0")
        self.setGeometry(100, 100, 500, 450)
        self.selected_file = None

        layout = QVBoxLayout()
        layout.addWidget(QLabel("CFC Number v1.0 - NOAH"))
        self.icon_combo = QComboBox()
        self.icon_combo.addItems(icons.keys())
        layout.addWidget(QLabel("Pilih Ikon:"))
        layout.addWidget(self.icon_combo)

        self.format_a = QRadioButton("+")
        self.format_b = QRadioButton("t.me/+")
        self.format_a.setChecked(True)
        layout.addWidget(QLabel("Format Tautan:"))
        layout.addWidget(self.format_a)
        layout.addWidget(self.format_b)

        self.split_3 = QRadioButton("3")
        self.split_6 = QRadioButton("6")
        self.split_8 = QRadioButton("8")
        self.split_10 = QRadioButton("10")
        self.split_8.setChecked(True)
        layout.addWidget(QLabel("Bagi per Grup:"))
        layout.addWidget(self.split_3)
        layout.addWidget(self.split_6)
        layout.addWidget(self.split_8)
        layout.addWidget(self.split_10)

        self.file_label = QLabel("File: Belum dipilih")
        layout.addWidget(self.file_label)
        file_button = QPushButton("Pilih File")
        file_button.clicked.connect(self.pilih_file)
        layout.addWidget(file_button)

        proses_button = QPushButton("Proses")
        proses_button.clicked.connect(self.proses)
        layout.addWidget(proses_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def pilih_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Pilih File .txt", "", "Text Files (*.txt)")
        if file:
            self.selected_file = file
            self.file_label.setText(f"File: {os.path.basename(file)}")

    def proses(self):
        if not self.selected_file:
            return
        link_format = '+' if self.format_a.isChecked() else 't.me/+'
        format_prefix = 'A_' if self.format_a.isChecked() else 'B_'
        tanggal = datetime.datetime.now().strftime("%d_%m_%y")
        split_size = 3 if self.split_3.isChecked() else 6 if self.split_6.isChecked() else 8 if self.split_8.isChecked() else 10

        with open(self.selected_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        if not lines:
            return

        chunks = [lines[i:i + split_size] for i in range(0, len(lines), split_size)]
        os.makedirs("output", exist_ok=True)
        filename = os.path.basename(self.selected_file)
        part_match = re.search(r'_Part_(\d+)', filename)
        part_number = part_match.group(1) if part_match else "unknown"

        output_path = os.path.join("output", f"{format_prefix}{self.icon_combo.currentText()}_{tanggal}_Part_{part_number}.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            for chunk in chunks:
                for line in chunk:
                    f.write(f"{link_format}{line} {icons[self.icon_combo.currentText()]} Part_{part_number}\n")
                f.write("\n")

app = QApplication([])
window = CFCMainWindow()
window.show()
app.exec_()