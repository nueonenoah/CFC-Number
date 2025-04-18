import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ttkthemes import ThemedTk
import os
from pathlib import Path
import datetime
import re
import asyncio
import threading

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

file_dipilih = []
output_dir = Path("output")
cancel_process = False
preview_content = []

def is_valid_link(line):
    """Validate if the line is a valid alphanumeric string for links."""
    return bool(re.match(r'^[a-zA-Z0-9_-]+$', line.strip()))

def proses_injeksi(nama_ikon, ikon_emoji, format_pilihan, files, jumlah_bagi, progress_bar, status_label, preview_text):
    global cancel_process
    try:
        if not files:
            raise ValueError("No file selected")
        
        format_link = '+' if format_pilihan == 'A' else 't.me/+'
        prefix_format = 'A_' if format_pilihan == 'A' else 'B_'
        tanggal = datetime.datetime.now().strftime("%d_%m_%y")
        ukuran_bagi = int(jumlah_bagi)

        total_files = len(files)
        progress_per_file = 100 / total_files if total_files > 0 else 100

        for file_idx, file_txt in enumerate(files):
            if cancel_process:
                raise ValueError("Process cancelled by user")

            progress_bar["value"] = file_idx * progress_per_file
            status_label.config(text=f"Processing file {file_idx + 1}/{total_files}...", foreground=COLORS["text"])
            root.update()

            baris = []
            with open(file_txt, "r", encoding="utf-8") as f:
                for line in f:  # Stream reading
                    if cancel_process:
                        raise ValueError("Process cancelled by user")
                    line = line.strip()
                    if line and is_valid_link(line):
                        baris.append(line)
                    elif line and not is_valid_link(line):
                        messagebox.showwarning("Warning", f"Invalid line in {file_txt}: {line}")
            
            if not baris:
                raise ValueError(f"Empty or invalid file: {file_txt}")

            progress_bar["value"] += progress_per_file * 0.4
            root.update()

            kelompok = [baris[i:i + ukuran_bagi] for i in range(0, len(baris), ukuran_bagi)]
            status_label.config(text="Grouping links...", foreground=COLORS["text"])
            progress_bar["value"] += progress_per_file * 0.2
            root.update()

            output_dir.mkdir(exist_ok=True)
            nama_file = Path(file_txt).name
            cocok = re.search(r'_Part_(\d+)', nama_file)
            nomor_bagian = cocok.group(1) if cocok else f"{file_idx + 1}"

            path_output = output_dir / f"{prefix_format}{nama_ikon}_{tanggal}_Part_{nomor_bagian}.txt"
            with open(path_output, "w", encoding="utf-8") as f:
                for grup in kelompok:
                    if cancel_process:
                        raise ValueError("Process cancelled by user")
                    for line in grup:
                        f.write(f"{format_link}{line} {ikon_emoji} Part_{nomor_bagian}\n")
                    f.write("\n")

            # Update preview
            if file_idx == 0:  # Show preview for first file only
                preview_content.clear()
                with open(path_output, "r", encoding="utf-8") as f:
                    preview_content.extend(f.readlines()[:10])  # Show first 10 lines
                preview_text.delete("1.0", tk.END)
                preview_text.insert(tk.END, "".join(preview_content))

            progress_bar["value"] += progress_per_file * 0.3
            status_label.config(text=f"Saving {path_output}...", foreground=COLORS["text"])
            root.update()

        progress_bar["value"] = 100
        status_label.config(text=f"Success: Saved to {output_dir}", foreground=COLORS["success"])
        cancel_process = False
    except Exception as e:
        messagebox.showerror("Error", f"Failed: {e}")
        progress_bar["value"] = 0
        status_label.config(text="Status: Failed", foreground=COLORS["accent"])
        cancel_process = False

def pilih_file():
    global file_dipilih
    files = filedialog.askopenfilenames(filetypes=[("Text Files", "*.txt")])
    if files:
        file_dipilih = list(files)
        nama_file = Path(files[0]).name if len(files) == 1 else f"{len(files)} files selected"
        if len(nama_file) > 20:
            nama_file = f"{nama_file[:15]}..."
        btn_pilih_file.config(text=f"File: {nama_file}")
    return file_dipilih

def pilih_output_dir():
    global output_dir
    directory = filedialog.askdirectory()
    if directory:
        output_dir = Path(directory)
        btn_output_dir.config(text=f"Output: {output_dir.name}")

def open_output_folder():
    if output_dir.exists():
        if os.name == 'nt':  # Windows
            os.startfile(output_dir)
        else:  # Linux/macOS
            os.system(f"open {output_dir}" if os.name == 'darwin' else f"xdg-open {output_dir}")
    else:
        messagebox.showwarning("Warning", "Output directory does not exist")

def cancel_processing():
    global cancel_process
    cancel_process = True
    status_label.config(text="Cancelling...", foreground=COLORS["accent"])

def info_aplikasi():
    messagebox.showinfo("About", (
        "Icon Injector NOAH - CFC Number v2.0\n\n"
        "Features:\n"
        "- Select or input custom icon\n"
        "- Import single or multiple .txt files\n"
        "- Choose link format (+ or t.me/+)\n"
        "- Auto-split into groups (3, 6, 8, or 10)\n"
        "- Preview output before saving\n"
        "- Custom output directory\n"
        "- Batch processing and cancel option\n"
        "- Open output folder directly\n\n"
        "Perfect for beautifying and managing Telegram link lists."
    ))

def show_tooltip(widget, text):
    def enter(event):
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 25
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()
        widget.tooltip = tooltip
    def leave(event):
        if hasattr(widget, 'tooltip'):
            widget.tooltip.destroy()
    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)

# Setup GUI
root = ThemedTk(theme="arc")
root.title("CFC Number v2.0")
root.geometry("600x900")
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

header_label = tk.Label(
    header_frame,
    text="NOAH THE KINDEST PERSON IN THE WORLD",
    font=("Arial", 14, "bold"),
    foreground=COLORS["primary"],
    background=COLORS["background"]
)
header_label.pack()
show_tooltip(header_label, "You're awesome, Noah!")

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
    "• Select or input custom icon\n"
    "• Import single or multiple .txt files\n"
    "• Choose link format (+ or t.me/+)\n"
    "• Auto-split into groups (3, 6, 8, or 10)\n"
    "• Preview output and cancel processing\n"
    "• Custom output directory and open folder\n"
)

features_label = tk.Label(
    features_frame,
    text=features_text,
    font=("Arial", 10),
    foreground=COLORS["text"],
    background=COLORS["background"],
    justify="left",
    anchor="w"
)
features_label.pack(anchor="w")
show_tooltip(features_label, "All the cool things this app can do!")

# 1. Choose Icon
icon_frame = ttk.Frame(main_frame)
icon_frame.pack(fill="x", pady=(0, 15))

icon_label = tk.Label(
    icon_frame,
    text="1. Choose an icon:",
    font=("Arial", 11, "bold"),
    foreground=COLORS["primary"],
    background=COLORS["background"]
)
icon_label.pack(anchor="w", pady=(0, 5))
show_tooltip(icon_label, "Select a preset icon or enter a custom emoji")

var_ikon = tk.StringVar(value="Panda")
var_custom_icon = tk.StringVar(value="")
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

custom_icon_frame = ttk.Frame(icon_frame)
custom_icon_frame.pack(fill="x", pady=5)
ttk.Radiobutton(
    custom_icon_frame,
    text="Custom Icon:",
    variable=var_ikon,
    value="Custom"
).pack(side="left", padx=5)
custom_icon_entry = ttk.Entry(custom_icon_frame, textvariable=var_custom_icon, width=10)
custom_icon_entry.pack(side="left", padx=5)
show_tooltip(custom_icon_entry, "Enter a custom emoji (e.g., 😎)")

# 2. Format Links
format_frame = ttk.Frame(main_frame)
format_frame.pack(fill="x", pady=(0, 15))

format_label = tk.Label(
    format_frame,
    text="2. Format links:",
    font=("Arial", 11, "bold"),
    foreground=COLORS["primary"],
    background=COLORS["background"]
)
format_label.pack(anchor="w", pady=(0, 5))
show_tooltip(format_label, "Choose how links are prefixed: + for short, t.me/+ for full Telegram URL")

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

group_label = tk.Label(
    group_frame,
    text="3. Group size:",
    font=("Arial", 11, "bold"),
    foreground=COLORS["primary"],
    background=COLORS["background"]
)
group_label.pack(anchor="w", pady=(0, 5))
show_tooltip(group_label, "Number of links per group in the output file")

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

# 4. Output Directory
output_dir_frame = ttk.Frame(main_frame)
output_dir_frame.pack(fill="x", pady=(0, 15))

output_dir_label = tk.Label(
    output_dir_frame,
    text="4. Output directory:",
    font=("Arial", 11, "bold"),
    foreground=COLORS["primary"],
    background=COLORS["background"]
)
output_dir_label.pack(anchor="w", pady=(0, 5))
show_tooltip(output_dir_label, "Choose where to save the output files")

btn_output_dir = tk.Button(
    output_dir_frame,
    text=f"Output: {output_dir.name}",
    font=("Arial", 10),
    bg=COLORS["primary"],
    fg="white",
    activebackground=COLORS["secondary"],
    activeforeground="white",
    command=pilih_output_dir,
    width=40,
    relief="flat"
)
btn_output_dir.pack(pady=5)

# 5. Upload File
upload_frame = ttk.Frame(main_frame)
upload_frame.pack(fill="x", pady=(0, 15))

upload_label = tk.Label(
    upload_frame,
    text="5. Upload your .txt file(s) with links/numbers:",
    font=("Arial", 11, "bold"),
    foreground=COLORS["primary"],
    background=COLORS["background"]
)
upload_label.pack(anchor="w", pady=(0, 5))
show_tooltip(upload_label, "Select one or more .txt files containing links or numbers")

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

# 6. Preview Output
preview_frame = ttk.Frame(main_frame)
preview_frame.pack(fill="x", pady=(0, 15))

preview_label = tk.Label(
    preview_frame,
    text="6. Preview output:",
    font=("Arial", 11, "bold"),
    foreground=COLORS["primary"],
    background=COLORS["background"]
)
preview_label.pack(anchor="w", pady=(0, 5))
show_tooltip(preview_label, "Preview the first 10 lines of the first processed file")

preview_text = tk.Text(
    preview_frame,
    height=5,
    width=50,
    font=("Arial", 10),
    bg=COLORS["widget_bg"],
    fg=COLORS["text"],
    relief="flat",
    borderwidth=1
)
preview_text.pack(pady=5)

# Process and Cancel Buttons
process_frame = ttk.Frame(main_frame)
process_frame.pack(fill="x", pady=(10, 5))

btn_proses = tk.Button(
    process_frame,
    text="Process Files",
    font=("Arial", 12, "bold"),
    bg=COLORS["primary"],
    fg="white",
    activebackground=COLORS["secondary"],
    activeforeground="white",
    command=lambda: threading.Thread(target=proses_injeksi, args=(
        var_ikon.get(),
        var_custom_icon.get() if var_ikon.get() == "Custom" else ikon.get(var_ikon.get(), "🐼"),
        var_format.get(),
        file_dipilih,
        var_bagi.get(),
        progress_bar,
        status_label,
        preview_text
    ), daemon=True).start(),
    width=15,
    relief="flat"
)
btn_proses.pack(side="left", padx=5)

btn_cancel = tk.Button(
    process_frame,
    text="Cancel",
    font=("Arial", 12, "bold"),
    bg=COLORS["accent"],
    fg="white",
    activebackground=COLORS["accent"],
    activeforeground="white",
    command=cancel_processing,
    width=15,
    relief="flat"
)
btn_cancel.pack(side="left", padx=5)

btn_open_folder = tk.Button(
    process_frame,
    text="Open Folder",
    font=("Arial", 12, "bold"),
    bg=COLORS["highlight"],
    fg="white",
    activebackground=COLORS["highlight"],
    activeforeground="white",
    command=open_output_folder,
    width=15,
    relief="flat"
)
btn_open_folder.pack(side="left", padx=5)

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