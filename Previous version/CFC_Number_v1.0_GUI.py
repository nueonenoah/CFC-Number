import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ttkthemes import ThemedTk
import os
import datetime
import re

# Color scheme
COLORS = {
    "primary": "#3498db",       # Main blue
    "secondary": "#2980b9",    # Darker blue
    "accent": "#e74c3c",       # Red for accents
    "background": "#ecf0f1",   # Light gray background
    "text": "#2c3e50",         # Dark text
    "highlight": "#f39c12",    # Orange for highlights
    "success": "#27ae60",      # Green for success messages
    "widget_bg": "#ffffff",    # White for widgets
}

ikon = {
    "Panda": "🐼", "Nasi": "🍚", "Ninja": "🥷", "Kadal": "🦎",
    "Baterai": "🔋", "Api": "🔥", "Polisi": "👮", "Mobil": "🚗", "Bintang": "✨"
}

file_dipilih = None

def proses_injeksi(nama_ikon, format_pilihan, file_txt, jumlah_bagi, progress_bar, status_label):
    try:
        format_link = '+' if format_pilihan == 'A' else 't.me/+'
        prefix_format = 'A_' if format_pilihan == 'A' else 'B_'
        tanggal = datetime.datetime.now().strftime("%d_%m_%y")

        progress_bar["value"] = 0
        status_label.config(text="Loading data...", foreground=COLORS["text"])
        root.update()

        with open(file_txt, "r", encoding="utf-8") as f:
            baris = [line.strip() for line in f if line.strip()]
        if not baris:
            raise ValueError("Empty file")
        progress_bar["value"] = 20
        root.update()

        ukuran_bagi = int(jumlah_bagi)
        kelompok = [baris[i:i + ukuran_bagi] for i in range(0, len(baris), ukuran_bagi)]
        progress_bar["value"] = 40
        status_label.config(text="Grouping links...", foreground=COLORS["text"])
        root.update()

        if not os.path.exists("output"):
            os.makedirs("output")
        progress_bar["value"] = 60
        root.update()

        nama_file = os.path.basename(file_txt)
        cocok = re.search(r'_Part_(\d+)', nama_file)
        nomor_bagian = cocok.group(1) if cocok else "unknown"

        path_output = os.path.join("output", f"{prefix_format}{nama_ikon}_{tanggal}_Part_{nomor_bagian}.txt")
        with open(path_output, "w", encoding="utf-8") as f:
            for grup in kelompok:
                for line in grup:
                    f.write(f"{format_link}{line} {ikon[nama_ikon]} Part_{nomor_bagian}\n")
                f.write("\n")

        progress_bar["value"] = 80
        status_label.config(text="Saving results...", foreground=COLORS["text"])
        root.update()

        progress_bar["value"] = 100
        status_label.config(text=f"Success: {path_output}", foreground=COLORS["success"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed: {e}")
        progress_bar["value"] = 0
        status_label.config(text="Status: Failed", foreground=COLORS["accent"])

def pilih_file():
    global file_dipilih
    file = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file:
        file_dipilih = file
        nama_file = os.path.basename(file)
        if len(nama_file) > 20:
            nama_file = f"{nama_file[:15]}..."
        btn_pilih_file.config(text=f"File: {nama_file}")
    return file_dipilih

def info_aplikasi():
    messagebox.showinfo("About", (
        "Icon Injector NOAH - CFC Number v1.0\n\n"
        "Features:\n"
        "- Select icon from preset list\n"
        "- Import links from .txt file\n"
        "- Choose link format (+ or t.me/+)\n"
        "- Auto-split into groups (3, 6, 8, or 10)\n"
        "- Save results with icon and date stamps\n\n"
        "Perfect for beautifying and managing Telegram link lists."
    ))

# Setup GUI
root = ThemedTk(theme="arc")
root.title("CFC Number v1.0")
root.geometry("500x700")
root.resizable(False, False)
root.configure(bg=COLORS["background"])

# Style configuration
style = ttk.Style()
style.configure("TFrame", background=COLORS["background"])
style.configure("TLabel", background=COLORS["background"], foreground=COLORS["text"])
style.configure("TRadiobutton", background=COLORS["background"], foreground=COLORS["text"])
style.configure("TProgressbar", troughcolor=COLORS["widget_bg"], background=COLORS["primary"])
style.configure("TButton", background=COLORS["primary"], foreground="white", borderwidth=1)
style.map("TButton", 
          background=[("active", COLORS["secondary"]), ("pressed", COLORS["secondary"])])

# Main container
main_frame = ttk.Frame(root)
main_frame.pack(pady=20, padx=20, fill="both", expand=True)

# Header
header_frame = ttk.Frame(main_frame)
header_frame.pack(fill="x", pady=(0, 20))

tk.Label(
    header_frame,
    text="NOAH THE KINDEST PERSON IN THE WORLD",
    font=("Arial", 14, "bold"),
    foreground=COLORS["primary"],
    background=COLORS["background"]
).pack()

# Features section
features_frame = ttk.Frame(main_frame)
features_frame.pack(fill="x", pady=(0, 20))

tk.Label(
    features_frame,
    text="Features:",
    font=("Arial", 12, "bold"),
    foreground=COLORS["primary"],
    background=COLORS["background"]
).pack(anchor="w")

features_text = (
    "• Select an icon from the preset list\n"
    "• Import links from a .txt file\n"
    "• Choose link format (+ or t.me/+)\n"
    "• Auto-split into groups (3, 6, 8, or 10)\n"
    "• Save results with icon and date stamps"
)

tk.Label(
    features_frame,
    text=features_text,
    font=("Arial", 10),
    foreground=COLORS["text"],
    background=COLORS["background"],
    justify="left",
    anchor="w"
).pack(anchor="w")

# 1. Choose Icon
icon_frame = ttk.Frame(main_frame)
icon_frame.pack(fill="x", pady=(0, 15))

tk.Label(
    icon_frame,
    text="1. Choose an icon:",
    font=("Arial", 11, "bold"),
    foreground=COLORS["primary"],
    background=COLORS["background"]
).pack(anchor="w", pady=(0, 5))

var_ikon = tk.StringVar(value="Panda")
icon_grid = ttk.Frame(icon_frame)
icon_grid.pack()

for idx, (nama, emoji) in enumerate(ikon.items()):
    row = idx // 3
    col = idx % 3
    ttk.Radiobutton(
        icon_grid,
        text=f"{emoji} {nama.upper()}",
        variable=var_ikon,
        value=nama
    ).grid(row=row, column=col, padx=10, pady=5, sticky="w")

# 2. Format Links
format_frame = ttk.Frame(main_frame)
format_frame.pack(fill="x", pady=(0, 15))

tk.Label(
    format_frame,
    text="2. Format links:",
    font=("Arial", 11, "bold"),
    foreground=COLORS["primary"],
    background=COLORS["background"]
).pack(anchor="w", pady=(0, 5))

var_format = tk.StringVar(value="A")
format_options = ttk.Frame(format_frame)
format_options.pack()

ttk.Radiobutton(
    format_options,
    text="Add + prefix",
    variable=var_format,
    value="A"
).pack(side="left", padx=10)

ttk.Radiobutton(
    format_options,
    text="Add t.me/+ prefix",
    variable=var_format,
    value="B"
).pack(side="left", padx=10)

# 3. Group Size
group_frame = ttk.Frame(main_frame)
group_frame.pack(fill="x", pady=(0, 15))

tk.Label(
    group_frame,
    text="3. Group size:",
    font=("Arial", 11, "bold"),
    foreground=COLORS["primary"],
    background=COLORS["background"]
).pack(anchor="w", pady=(0, 5))

var_bagi = tk.StringVar(value="8")
group_options = ttk.Frame(group_frame)
group_options.pack()

for val in ["3", "6", "8", "10"]:
    ttk.Radiobutton(
        group_options,
        text=val,
        variable=var_bagi,
        value=val
    ).pack(side="left", padx=10)

# 4. Upload File
upload_frame = ttk.Frame(main_frame)
upload_frame.pack(fill="x", pady=(0, 20))

tk.Label(
    upload_frame,
    text="4. Upload your .txt file with links/numbers:",
    font=("Arial", 11, "bold"),
    foreground=COLORS["primary"],
    background=COLORS["background"]
).pack(anchor="w", pady=(0, 5))

btn_pilih_file = tk.Button(
    upload_frame,
    text="Choose File: No file chosen",
    font=("Arial", 10),
    bg=COLORS["primary"],
    fg="white",
    activebackground=COLORS["secondary"],
    activeforeground="white",
    command=pilih_file,
    width=40,
    relief="flat"
)
btn_pilih_file.pack(pady=5)

# Process Button
process_frame = ttk.Frame(main_frame)
process_frame.pack(fill="x", pady=(10, 5))

btn_proses = tk.Button(
    process_frame,
    text="Process File",
    font=("Arial", 12, "bold"),
    bg=COLORS["primary"],
    fg="white",
    activebackground=COLORS["secondary"],
    activeforeground="white",
    command=lambda: proses_injeksi(
        var_ikon.get(),
        var_format.get(),
        file_dipilih,
        var_bagi.get(),
        progress_bar,
        status_label
    ),
    width=20,
    relief="flat"
)
btn_proses.pack()

# Progress and Status
progress_frame = ttk.Frame(main_frame)
progress_frame.pack(fill="x", pady=(5, 20))

progress_bar = ttk.Progressbar(progress_frame, length=400, mode="determinate")
progress_bar.pack(pady=5)

status_label = ttk.Label(
    progress_frame,
    text="Status: Idle",
    font=("Arial", 10),
    foreground=COLORS["text"]
)
status_label.pack()

# Help Menu
menu_bar = tk.Menu(root)
menu_help = tk.Menu(menu_bar, tearoff=0)
menu_help.add_command(label="About", command=info_aplikasi)
menu_bar.add_cascade(label="Help", menu=menu_help)
root.config(menu=menu_bar)

root.mainloop()