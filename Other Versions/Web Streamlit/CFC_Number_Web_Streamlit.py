import streamlit as st
import os
import datetime
import re

st.set_page_config(page_title="CFC Number v1.0", page_icon="🧩")

icons = {
    "Panda": "🐼", "Nasi": "🍚", "Ninja": "🥷", "Kadal": "🦎",
    "Baterai": "🔋", "Api": "🔥", "Polisi": "👮", "Mobil": "🚗", "Bintang": "✨"
}

st.markdown("<h1 style='text-align: center; color: #00FFFF;'>CFC Number v1.0 - NOAH</h1>", unsafe_allow_html=True)

icon_name = st.selectbox("Pilih Ikon", list(icons.keys()))
format_choice = st.radio("Format Tautan", ["+", "t.me/+"], horizontal=True)
split_choice = st.radio("Bagi per Grup", ["3", "6", "8", "10"], horizontal=True)
uploaded_file = st.file_uploader("Pilih File .txt", type="txt")

if st.button("Proses"):
    if not uploaded_file:
        st.warning("Pilih file .txt dulu!")
        st.stop()

    with st.spinner("Memproses..."):
        link_format = '+' if format_choice == '+' else 't.me/+'
        format_prefix = 'A_' if format_choice == '+' else 'B_'
        tanggal = datetime.datetime.now().strftime("%d_%m_%y")

        lines = [line.strip() for line in uploaded_file.read().decode("utf-8").splitlines() if line.strip()]
        if not lines:
            st.error("File kosong!")
            st.stop()

        split_size = int(split_choice)
        chunks = [lines[i:i + split_size] for i in range(0, len(lines), split_size)]

        filename = uploaded_file.name
        part_match = re.search(r'_Part_(\d+)', filename)
        part_number = part_match.group(1) if part_match else "unknown"

        os.makedirs("output", exist_ok=True)
        output_path = os.path.join("output", f"{format_prefix}{icon_name}_{tanggal}_Part_{part_number}.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            for chunk in chunks:
                for line in chunk:
                    f.write(f"{link_format}{line} {icons[icon_name]} Part_{part_number}\n")
                f.write("\n")

        st.success(f"Berhasil disimpan ke {output_path}")
        with open(output_path, "r", encoding="utf-8") as f:
            st.download_button("Unduh Hasil", f, file_name=os.path.basename(output_path))