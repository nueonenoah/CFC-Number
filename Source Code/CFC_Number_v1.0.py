from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.prompt import Prompt
from rich.progress import Progress, BarColumn, TextColumn
import os
import datetime
import time
import re

console = Console(width=80)

def tampilkan_header():
    console.print(Rule(style="bright_cyan"))
    console.print(Panel(
        "[bold magenta]      __    __   ______    ______   __    __ \n"
        "[bold magenta]     /  \\  /  | /      \\  /      \\ /  |  /  |\n"
        "[bold magenta]     $$  \\ $$ |/$$$$$$  |/$$$$$$  |$$ |  $$ |\n"
        "[bold magenta]     $$$  \\$$ |$$ |  $$ |$$ |__$$ |$$|__$$  |\n"
        "[bold magenta]     $$$$  $$ |$$ |  $$ |$$    $$ |$$    $$ |\n"
        "[bold magenta]     $$ $$ $$ |$$ |  $$ |$$$$$$$$ |$$$$$$$$ |\n"
        "[bold magenta]     $$ |$$$$ |$$ \\__$$ |$$ |  $$ |$$ |  $$ |\n"
        "[bold magenta]     $$ | $$$ |$$    $$/ $$ |  $$ |$$ |  $$ |\n"
        "[bold magenta]     $$/   $$/  $$$$$$/  $$/   $$/ $$/   $$/ \n"
        "                                             [/]\n"
        "[bold bright_yellow]CFC Number v1.0 - NOAH MANUSIA PALING BAIK DI BUMI[/]",
        style="white", border_style="bright_cyan", width=80
    ))
    console.print(Rule(style="bright_cyan"))

icons = {
    "1": ("🐼", "PANDA"),
    "2": ("🍚", "NASI"),
    "3": ("🥷", "NINJA"),
    "4": ("🦎", "KADAL"),
    "5": ("🔋", "BATERAI"),
    "6": ("🔥", "API"),
    "7": ("👮", "POLISI"),
    "8": ("🚗", "MOBIL"),
    "9": ("✨", "BINTANG")
}

def tampilkan_menu_icon():
    os.system("cls" if os.name == "nt" else "clear")
    tampilkan_header()
    console.print("[bright_cyan]>> [PROSES] Sesi Injeksi Ikon Dimulai ⚡[/bright_cyan]")
    console.print("[bold cyan]INGIN MENAMBAHKAN TANDA???[/bold cyan]\n")

    menu_text = (
        "[white]1. 🐼 PANDA    6. 🔥 API\n"
        "2. 🍚 NASI     7. 👮 POLISI\n"
        "3. 🥷 NINJA    8. 🚗 MOBIL\n"
        "4. 🦎 KADAL    9. ✨ BINTANG\n"
        "5. 🔋 BATERAI  0. ❌ KELUAR[/white]"
    )

    console.print(Panel(
        menu_text,
        style="white", border_style="bright_cyan", width=80
    ))
    console.print(Panel(
        "[bright_yellow]INFO[/bright_yellow]   - Ketik \"info\" untuk melihat informasi aplikasi",
        style="white", border_style="bright_cyan", width=80
    ))
    console.print("[bright_cyan]>> [MASUKAN] Pilih salah satu (0-9) atau ketik info:[/bright_cyan]")

def tampilkan_menu_format():
    os.system("cls" if os.name == "nt" else "clear")
    tampilkan_header()
    console.print("[bright_cyan]>> [PROSES] Pilih Format Tautan ⚡[/bright_cyan]")
    console.print("[bold cyan]PILIH FORMAT TAUTAN:[/bold cyan]\n")

    menu_text = (
        "[white]A. Tambahkan (+)\n"
        "B. Tambahkan (t.me/+)[/white]"
    )

    console.print(Panel(
        menu_text,
        style="white", border_style="bright_cyan", width=80
    ))
    console.print("[bright_cyan]>> [MASUKAN] Pilih salah satu (A/B):[/bright_cyan]")

def tampilkan_menu_split():
    os.system("cls" if os.name == "nt" else "clear")
    tampilkan_header()
    console.print("[bright_cyan]>> [PROSES] Pilih Pembagian Grup ⚡[/bright_cyan]")
    console.print("[bold cyan]BAGI PER GRUP:[/bold cyan]\n")

    menu_text = (
        "[white]1. 3 tautan\n"
        "2. 6 tautan\n"
        "3. 8 tautan\n"
        "4. 10 tautan[/white]"
    )

    console.print(Panel(
        menu_text,
        style="white", border_style="bright_cyan", width=80
    ))
    console.print("[bright_cyan]>> [MASUKAN] Pilih salah satu (1-4):[/bright_cyan]")

def pilih_file():
    os.system("cls" if os.name == "nt" else "clear")
    tampilkan_header()
    console.print("[bright_cyan]>> [PROSES] Pilih File .txt ⚡[/bright_cyan]")
    console.print("[bold cyan]MASUKKAN NAMA FILE (contoh: SILUP_Part_53.txt):[/bold cyan]")
    file_name = Prompt.ask("> ").strip()
    file_path = os.path.join(os.getcwd(), file_name)
    if not os.path.isfile(file_path):
        console.print("[red]>> [KESALAHAN] File tidak ditemukan[/red]")
        return None
    return file_path

def tampilkan_info():
    os.system("cls" if os.name == "nt" else "clear")
    tampilkan_header()
    console.print(Panel(
        "[bold bright_yellow]Icon Injector NOAH - Informasi Aplikasi[/bold bright_yellow]\n\n"
        "[white]Tujuan:\n"
        "Skrip ini mengotomatiskan penambahan ikon ke daftar tautan Telegram.\n\n"
        "Fungsi:\n"
        "- Memilih ikon dari daftar (1-9).\n"
        "- Menggabungkan tautan dari file .txt.\n"
        "- Membagi tautan sesuai pilihan (3, 6, 8, 10).\n"
        "- Menyimpan hasil dengan ikon dan tanggal.\n\n"
        "Penggunaan:\n"
        "Cocok untuk mengatur dan mempercantik daftar tautan Telegram.[/white]",
        style="white", border_style="bright_yellow", width=80
    ))
    input(">> Tekan Enter untuk kembali ke menu:")

def proses_animasi(icon_name):
    os.system("cls" if os.name == "nt" else "clear")
    tampilkan_header()
    console.print(f"[bright_cyan]>> [PROSES] Injeksi Ikon {icon_name} 🚀[/bright_cyan]")
    console.print(Rule(style="bright_cyan"))

    tahapan = [
        "MEMUAT DATA TAUTAN...",
        "MENYUNTIKKAN IKON...",
        "MENGELOMPOKKAN TAUTAN...",
        "MEMFORMAT OUTPUT...",
        "MENYIMPAN HASIL..."
    ]

    with Progress(
        TextColumn("[bright_green][NOAH-INJECT] {task.description}"),
        BarColumn(bar_width=30, style="green", complete_style="bright_green"),
        "[progress.percentage]{task.percentage:>3.0f}%",
        console=console
    ) as progress:
        for tahap in tahapan:
            task = progress.add_task(tahap, total=100)
            for _ in range(100):
                progress.update(task, advance=1)
                time.sleep(0.005)

def main():
    while True:
        tampilkan_menu_icon()
        choice = Prompt.ask("> ").strip().lower()

        if choice == "info":
            tampilkan_info()
            continue

        if choice == "0":
            console.print("[red]>> [KELUAR] Oke keluar, ga jadi nambahin icon[/red]")
            break

        if choice not in icons:
            console.print("[red]>> [KESALAHAN] Pilihan ga valid[/red]")
            continue

        selected_icon, icon_name = icons[choice]

        tampilkan_menu_format()
        format_choice = Prompt.ask("> ").strip().lower()
        if format_choice not in ['a', 'b']:
            console.print("[red]>> [KESALAHAN] Pilihan ga valid[/red]")
            continue
        link_format = '+' if format_choice == 'a' else 't.me/+'
        format_prefix = 'A_' if format_choice == 'a' else 'B_'

        tampilkan_menu_split()
        split_choice = Prompt.ask("> ").strip()
        split_map = {'1': 3, '2': 6, '3': 8, '4': 10}
        if split_choice not in split_map:
            console.print("[red]>> [KESALAHAN] Pilihan ga valid[/red]")
            continue
        split_size = split_map[split_choice]

        txt_file = pilih_file()
        if not txt_file:
            continue

        proses_animasi(icon_name)

        try:
            with open(txt_file, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
            if not lines:
                console.print("[red]>> [KESALAHAN] File kosong[/red]")
                continue

            chunks = [lines[i:i + split_size] for i in range(0, len(lines), split_size)]

            if not os.path.exists("output"):
                os.makedirs("output")

            filename = os.path.basename(txt_file)
            part_match = re.search(r'_Part_(\d+)', filename)
            part_number = part_match.group(1) if part_match else "unknown"

            output_path = os.path.join("output", f"{format_prefix}{icon_name}_{datetime.datetime.now().strftime('%d_%m_%y')}_Part_{part_number}.txt")
            with open(output_path, "w", encoding="utf-8") as f:
                for chunk in chunks:
                    for line in chunk:
                        f.write(f"{link_format}{line} {selected_icon} Part_{part_number}\n")
                    f.write("\n")

            console.print(Rule(style="bright_cyan"))
            console.print(Panel(
                f"[bright_green]Berhasil disimpan ke {output_path}[/bright_green]",
                style="white", border_style="bright_green", width=80
            ))
        except Exception as e:
            console.print(f"[red]>> [KESALAHAN] Gagal: {str(e)[:50]}...[/red]")

        input(">> Tekan Enter untuk kembali ke menu:")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("[red]>> [KELUAR] Dihentikan oleh pengguna[/red]")
    except Exception as e:
        console.print(f"[red]>> [KRITIS] Kesalahan sistem: {str(e)[:50]}...[/red]")