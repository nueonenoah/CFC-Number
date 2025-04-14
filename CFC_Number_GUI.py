import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ttkthemes import ThemedTk
import os
import datetime
import re

icons = {
    "Panda": "🐼", "Nasi": "🍚", "Ninja": "🥷", "Kadal": "🦎",
    "Baterai": "🔋", "Api": "🔥", "Polisi": "👮", "Mobil": "🚗", "Bintang": "✨"
}

selected_file = None

def proses_injeksi(icon_name, format_choice, txt_file, split_choice, progress_bar, status_label):
    try:
        link_format = '+' if format_choice == 'A' else 't.me/+'
        format_prefix = 'A_' if format_choice == 'A' else 'B_'
        tanggal = datetime.datetime.now().strftime("%d_%m_%y")

        progress_bar["value"] = 0
        status_label.config(text="Memuat data...")
        root.update()

        with open(txt_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        if not lines:
            raise ValueError("File kosong")
        progress_bar["value"] = 20
        root.update()

        split_size = int(split_choice)
        chunks = [lines[i:i + split_size] for i in range(0, len(lines), split_size)]
        progress_bar["value"] = 40
        status_label.config(text="Mengelompokkan tautan...")
        root.update()

        if not os.path.exists("output"):
            os.makedirs("output")
        progress_bar["value"] = 60
        root.update()

        # Ambil part dari nama file asli
        filename = os.path.basename(txt_file)
        part_match = re.search(r'_Part_(\d+)', filename)
        part_number = part_match.group(1) if part_match else "unknown"

        # Simpan ke satu file
        output_path = os.path.join("output", f"{format_prefix}{icon_name}_{tanggal}_Part_{part_number}.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            for chunk in chunks:
                for line in chunk:
                    f.write(f"{link_format}{line} {icons[icon_name]} Part_{part_number}\n")
                f.write("\n")  # Baris kosong antar grup

        progress_bar["value"] = 80
        status_label.config(text="Menyimpan hasil...")
        root.update()

        progress_bar["value"] = 100
        status_label.config(text=f"Berhasil: {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal: {e}")
        progress_bar["value"] = 0
        status_label.config(text="Status: Gagal")

def pilih_file():
    global selected_file
    file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file:
        selected_file = file
        file_label.config(text=f"File: {os.path.basename(file)}")
    return selected_file

def tampilkan_info():
    messagebox.showinfo("Info Aplikasi", (
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
    ))

root = ThemedTk(theme="arc")
root.title("CFC Number v1.0")
root.geometry("500x450")
root.resizable(False, False)

header_label = tk.Label(root, text="CFC Number v1.0 - NOAH", font=("Arial", 18, "bold"), fg="#00FFFF")
header_label.pack(pady=10)

input_frame = ttk.Frame(root)
input_frame.pack(pady=10, padx=10, fill="x")

ttk.Label(input_frame, text="Pilih Ikon:").grid(row=0, column=0, sticky="w", padx=5)
icon_var = tk.StringVar(value="Panda")
icon_menu = ttk.Combobox(input_frame, textvariable=icon_var, values=list(icons.keys()), state="readonly", width=15)
icon_menu.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Format Tautan:").grid(row=1, column=0, sticky="w", padx=5)
format_var = tk.StringVar(value="A")
ttk.Radiobutton(input_frame, text="+", variable=format_var, value="A").grid(row=1, column=1, sticky="w")
ttk.Radiobutton(input_frame, text="t.me/+", variable=format_var, value="B").grid(row=1, column=2, sticky="w")

ttk.Label(input_frame, text="Bagi per Grup:").grid(row=2, column=0, sticky="w", padx=5)
split_var = tk.StringVar(value="8")
ttk.Radiobutton(input_frame, text="3", variable=split_var, value="3").grid(row=2, column=1, sticky="w")
ttk.Radiobutton(input_frame, text="6", variable=split_var, value="6").grid(row=2, column=2, sticky="w")
ttk.Radiobutton(input_frame, text="8", variable=split_var, value="8").grid(row=3, column=1, sticky="w")
ttk.Radiobutton(input_frame, text="10", variable=split_var, value="10").grid(row=3, column=2, sticky="w")

file_label = ttk.Label(input_frame, text="File: Belum dipilih")
file_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=5, pady=5)
ttk.Button(input_frame, text="Pilih File", command=pilih_file).grid(row=4, column=2, padx=5, pady=5)

progress_bar = ttk.Progressbar(root, length=400, mode="determinate")
progress_bar.pack(pady=10)

button_frame = ttk.Frame(root)
button_frame.pack(pady=10)
ttk.Button(button_frame, text="Proses", command=lambda: proses_injeksi(icon_var.get(), format_var.get(), selected_file, split_var.get(), progress_bar, status_label)).pack(side="left", padx=5)
ttk.Button(button_frame, text="Info", command=tampilkan_info).pack(side="left", padx=5)
ttk.Button(button_frame, text="Keluar", command=root.quit).pack(side="left", padx=5)

status_label = ttk.Label(root, text="Status: Idle", font=("Arial", 10))
status_label.pack(pady=10)

root.mainloop()