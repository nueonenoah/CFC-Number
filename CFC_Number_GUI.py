import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import datetime

icons = {
    "Panda": "🐼", "Nasi": "🍚", "Ninja": "🥷", "Kadal": "🦎",
    "Baterai": "🔋", "Api": "🔥", "Polisi": "👮", "Mobil": "🚗", "Bintang": "✨"
}

# Variabel global untuk menyimpan path file
selected_file = None

def proses_injeksi(icon_name, format_choice, txt_file):
    try:
        link_format = '+' if format_choice == 'A' else 't.me/+'
        format_prefix = 'A_' if format_choice == 'A' else 'B_'
        tanggal = datetime.datetime.now().strftime("%d_%m_%y")

        with open(txt_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        if not lines:
            raise ValueError("File kosong")

        chunks = [lines[i:i + 8] for i in range(0, len(lines), 8)]
        if not os.path.exists("output"):
            os.makedirs("output")

        output_path = os.path.join("output", f"{format_prefix}{icon_name}_{tanggal}.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            for idx, group in enumerate(chunks, start=1):
                f.write(f"==== Group {idx} ====\n")
                for i, line in enumerate(group, start=1):
                    f.write(f"{link_format}{line} {icons[icon_name]} {i}\n")
                f.write("\n")

        status_label.config(text=f"Berhasil: {output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal: {e}")

def pilih_file():
    global selected_file
    file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file:
        selected_file = file
        file_label.config(text=f"File: {os.path.basename(file)}")
    return selected_file

def tampilkan_info():
    messagebox.showinfo("Info", "CFC Number v1.0\nTambah ikon ke tautan Telegram.")

root = tk.Tk()
root.title("CFC Number v1.0")
root.geometry("400x300")

tk.Label(root, text="Pilih Ikon:").pack()
icon_var = tk.StringVar(value="Panda")
ttk.Combobox(root, textvariable=icon_var, values=list(icons.keys()), state="readonly").pack()

tk.Label(root, text="Format:").pack()
format_var = tk.StringVar(value="A")
tk.Radiobutton(root, text="+", variable=format_var, value="A").pack()
tk.Radiobutton(root, text="t.me/+", variable=format_var, value="B").pack()

file_label = tk.Label(root, text="File: Belum dipilih")
file_label.pack()
tk.Button(root, text="Pilih File", command=pilih_file).pack()

def jalankan_proses():
    if not selected_file:
        messagebox.showwarning("Peringatan", "Pilih file .txt terlebih dahulu!")
        return
    proses_injeksi(icon_var.get(), format_var.get(), selected_file)

tk.Button(root, text="Proses", command=jalankan_proses).pack()
tk.Button(root, text="Info", command=tampilkan_info).pack()
tk.Button(root, text="Keluar", command=root.quit).pack()

status_label = tk.Label(root, text="Status: Idle")
status_label.pack()

root.mainloop()