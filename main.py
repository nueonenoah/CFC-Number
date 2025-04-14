import os
import datetime
import re
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from werkzeug.utils import secure_filename
import logging
from number_formatter import ICONS, ICON_NAMES, read_links, split_into_groups, format_groups, extract_part_number

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "defaultsecretkey")

# Configure upload folder and output folder
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)
        
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Available languages
LANGUAGES = {
    'en': 'English',
    'id': 'Bahasa Indonesia'
}

# Translations
TRANSLATIONS = {
    'en': {
        'app_title': 'NOAH THE KINDEST PERSON IN THE WORLD',
        'features': 'Features:',
        'feature_1': 'Select an icon from the preset list',
        'feature_2': 'Import links from a .txt file',
        'feature_3': 'Choose link format (+ or t.me/+)',
        'feature_4': 'Auto-split into groups (3, 6, 8, or 10)',
        'feature_5': 'Save results with icon and date stamps',
        'choose_icon': 'Choose an icon:',
        'format_links': 'Format links:',
        'format_plus': 'Add + prefix',
        'format_tme': 'Add t.me/+ prefix',
        'group_size': 'Group size:',
        'upload_file': 'Upload your .txt file with links/numbers:',
        'only_txt': 'Only .txt files are supported.',
        'process_file': 'Process File',
        'how_to_use': 'How to Use',
        'step_1': 'Select one of the icons from the options above',
        'step_2': 'Choose the link format (+/t.me/+)',
        'step_3': 'Select the group size (3, 6, 8, or 10 links per group)',
        'step_4': 'Upload a .txt file containing your links or numbers (one per line)',
        'step_5': 'Click "Process File" to generate your formatted list',
        'step_6': 'Download the result for use in Telegram',
        'file_tip': 'Tip: Make sure your .txt file has one number or link per line with no empty lines. For best results, name your file with _Part_XX in the name.',
        'processing_complete': 'Processing Complete! ✅',
        'processing_results': 'Processing Results:',
        'total_entries': 'Total entries processed:',
        'split_into': 'Split into groups:',
        'results_saved': 'Results saved to:',
        'download_file': 'Download Formatted File',
        'process_another': 'Process Another File',
        'next_steps': 'Next Steps',
        'how_to_use_result': 'How to use your formatted list in Telegram:',
        'use_step_1': 'Download the formatted file using the button above',
        'use_step_2': 'Open the file in a text editor',
        'use_step_3': 'Copy each group separately when sending messages',
        'use_step_4': 'Paste directly into Telegram messages',
        'use_tip': 'Tip: Each link is formatted with the selected icon and part number, making your lists easily identifiable.',
        'dark_mode': 'Dark Mode',
        'light_mode': 'Light Mode',
        'no_file': 'No file selected',
        'select_icon': 'Please select a valid icon',
        'empty_file': 'The input file is empty',
        'error_processing': 'Error processing file'
    },
    'id': {
        'app_title': 'NOAH MANUSIA PALING BAIK DI DUNIA',
        'features': 'Fitur:',
        'feature_1': 'Pilih ikon dari daftar yang tersedia',
        'feature_2': 'Impor tautan dari file .txt',
        'feature_3': 'Pilih format tautan (+ atau t.me/+)',
        'feature_4': 'Bagi otomatis ke dalam grup (3, 6, 8, atau 10)',
        'feature_5': 'Simpan hasil dengan ikon dan tanggal',
        'choose_icon': 'Pilih ikon:',
        'format_links': 'Format tautan:',
        'format_plus': 'Tambah awalan +',
        'format_tme': 'Tambah awalan t.me/+',
        'group_size': 'Ukuran grup:',
        'upload_file': 'Unggah file .txt dengan tautan/nomor:',
        'only_txt': 'Hanya file .txt yang didukung.',
        'process_file': 'Proses File',
        'how_to_use': 'Cara Penggunaan',
        'step_1': 'Pilih salah satu ikon dari opsi di atas',
        'step_2': 'Pilih format tautan (+/t.me/+)',
        'step_3': 'Pilih ukuran grup (3, 6, 8, atau 10 tautan per grup)',
        'step_4': 'Unggah file .txt yang berisi tautan atau nomor (satu per baris)',
        'step_5': 'Klik "Proses File" untuk menghasilkan daftar yang diformat',
        'step_6': 'Unduh hasilnya untuk digunakan di Telegram',
        'file_tip': 'Tips: Pastikan file .txt Anda memiliki satu nomor atau tautan per baris tanpa baris kosong. Untuk hasil terbaik, beri nama file Anda dengan _Part_XX di namanya.',
        'processing_complete': 'Pemrosesan Selesai! ✅',
        'processing_results': 'Hasil Pemrosesan:',
        'total_entries': 'Total entri diproses:',
        'split_into': 'Dibagi menjadi grup:',
        'results_saved': 'Hasil disimpan ke:',
        'download_file': 'Unduh File yang Diformat',
        'process_another': 'Proses File Lain',
        'next_steps': 'Langkah Selanjutnya',
        'how_to_use_result': 'Cara menggunakan daftar yang diformat di Telegram:',
        'use_step_1': 'Unduh file yang diformat menggunakan tombol di atas',
        'use_step_2': 'Buka file di editor teks',
        'use_step_3': 'Salin setiap grup secara terpisah saat mengirim pesan',
        'use_step_4': 'Tempel langsung ke pesan Telegram',
        'use_tip': 'Tips: Setiap tautan diformat dengan ikon yang dipilih dan nomor bagian, membuat daftar Anda mudah diidentifikasi.',
        'dark_mode': 'Mode Gelap',
        'light_mode': 'Mode Terang',
        'no_file': 'Tidak ada file yang dipilih',
        'select_icon': 'Pilih ikon yang valid',
        'empty_file': 'File kosong',
        'error_processing': 'Kesalahan memproses file'
    }
}

@app.route('/')
def index():
    # Set default language and theme if not in session
    if 'lang' not in session:
        session['lang'] = 'en'
    if 'theme' not in session:
        session['theme'] = 'dark'
        
    # Get translations for current language
    lang = session.get('lang', 'en')
    translations = TRANSLATIONS[lang]
    
    # Combine icons with names for display
    icons_with_names = {}
    for num, icon in ICONS.items():
        icons_with_names[num] = {
            'icon': icon,
            'name': ICON_NAMES.get(num, f"Icon {num}")
        }
    
    return render_template(
        'index.html',
        icons=icons_with_names,
        translations=translations,
        current_lang=lang,
        current_theme=session.get('theme', 'dark'),
        languages=LANGUAGES
    )

@app.route('/set-language/<lang>')
def set_language(lang):
    if lang in LANGUAGES:
        session['lang'] = lang
    return redirect(request.referrer or url_for('index'))

@app.route('/set-theme/<theme>')
def set_theme(theme):
    if theme in ['light', 'dark']:
        session['theme'] = theme
    return redirect(request.referrer or url_for('index'))

@app.route('/process', methods=['POST'])
def process():
    # Get current language
    lang = session.get('lang', 'en')
    translations = TRANSLATIONS[lang]
    
    # Check if file part exists in the request
    if 'file' not in request.files:
        flash(translations['no_file'])
        return redirect(request.url)
    
    file = request.files['file']
    
    # Check if file was selected
    if file.filename == '':
        flash(translations['no_file'])
        return redirect(url_for('index'))
    
    # Check file extension
    if not file.filename.lower().endswith('.txt'):
        flash(translations['only_txt'])
        return redirect(url_for('index'))
    
    # Get selected icon
    selected_icon_id = request.form.get('icon')
    if not selected_icon_id or int(selected_icon_id) not in ICONS:
        flash(translations['select_icon'])
        return redirect(url_for('index'))
    
    # Get selected link format
    link_format = request.form.get('format', '+')
    if link_format not in ['+', 't.me/+']:
        link_format = '+'
    
    # Get selected group size
    try:
        group_size = int(request.form.get('group_size', 8))
        if group_size not in [3, 6, 8, 10]:
            group_size = 8
    except (ValueError, TypeError):
        group_size = 8
    
    # Get icon details
    icon_id = int(selected_icon_id)
    selected_icon = ICONS[icon_id]
    
    # Save uploaded file
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    try:
        # Process the file
        links = read_links(file_path)
        
        # Check if file has contents
        if not links:
            flash(translations['empty_file'])
            return redirect(url_for('index'))
        
        # Get part number from filename
        part_number = extract_part_number(file_path)
        
        # Split and format
        groups = split_into_groups(links, group_size)
        formatted_groups = format_groups(groups, selected_icon, icon_id, link_format, part_number)
        
        # Determine file prefix based on format choice
        format_prefix = 'A_' if link_format == '+' else 'B_'
        
        # Create output filename with icon name and date
        today = datetime.datetime.now().strftime("%d_%m_%y")
        icon_name = ICON_NAMES.get(icon_id, "ICON")
        output_filename = f"{format_prefix}{icon_name}_{today}_Part_{part_number}.txt"
        output_file_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        # Save results
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(''.join(formatted_groups))
        
        # Generate statistics
        stats = {
            'total_entries': len(links),
            'groups': len(groups),
            'group_size': group_size,
            'output_file': output_filename
        }
        
        return render_template(
            'results.html',
            stats=stats,
            output_file=output_filename,
            translations=translations,
            current_lang=lang,
            current_theme=session.get('theme', 'dark'),
            languages=LANGUAGES
        )
        
    except Exception as e:
        app.logger.error(f"Error processing file: {str(e)}")
        flash(f"{translations['error_processing']}: {str(e)}")
        return redirect(url_for('index'))
    finally:
        # Clean up the uploaded file after processing
        if os.path.exists(file_path):
            os.remove(file_path)

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)