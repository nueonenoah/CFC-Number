# 🧩 CFC Number v2.4

A user-friendly GUI application to automate icon tagging for Telegram number lists, keeping contact and broadcast lists organized and visually appealing with just a few clicks.

🖥️ Launch the app, configure your settings, and let it handle the tedious work while you focus on the fun stuff.

## ✨ What It Does
This application handles:
- 🔢 Selecting an icon from a preset list or inputting a custom emoji
- 📥 Importing single or multiple `.txt` files with links or numbers
- 🍰 Splitting lists into groups (3, 6, 8, or 10 entries)
- 📆 Saving results with icon and date stamps in a custom output directory
- 🛠️ Batch processing with progress feedback and cancel option
- 📂 Opening the output folder directly from the app

Perfect for Telegram users or marketers who want clean, professional-looking number lists.

## 🛠️ How It Works
The app provides an intuitive GUI built with Python and Tkinter. All you need is a `.txt` file with links or numbers. You'll go through:
1. 👀 Choosing an icon from a preset list or entering a custom emoji
2. 🔗 Selecting a link format (`+` or `t.me/+`)
3. 🧮 Setting the group size (3, 6, 8, or 10)
4. 📂 Choosing an output directory and uploading `.txt` file(s)
5. 🚀 Processing files with real-time progress and the option to cancel
6. 💾 Auto-saving results with tidy formatting and current date

The result? A polished, organized contact layout ready for sharing.

## 🧰 Example Use
Imagine you have a Telegram broadcast list of 80 numbers. This app:
- Groups them into 10 chunks (if group size is 8)
- Tags each chunk with your chosen icon (e.g., 🐼 or a custom emoji)
- Saves the output in your chosen folder with a filename like `A_Panda_18_04_25_Part_1.txt`
- Lets you process multiple files at once and open the output folder instantly

Ideal for frequent list management, ensuring quick and clean edits for Telegram sharing.

## 📋 Features
- No manual editing required
- Flexible group sizes (3, 6, 8, or 10) for easy sending
- Auto-formatting with icons, dates, and link prefixes
- Supports batch processing of multiple `.txt` files
- Custom output directory and direct folder access
- User-friendly GUI with tooltips and progress bar
- Cancel option for interrupting long processes

> 💡 **Tip:** Use it to format numbers before pasting into Telegram messages to enhance visual clarity and keep your broadcasts tidy.

## ⚙️ Requirements
- Python 3.x
- `tkinter` (included with Python)
- `ttkthemes` (`pip install ttkthemes`)
- A `.txt` file with links or numbers

## 📸 Screenshots
*Coming soon! Check back for visuals of the GUI in action.*

## 📋 Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/nueonenoah/CFC-Number.git
   ```
2. Install dependencies:
   ```bash
   pip install ttkthemes
   ```
3. Run the app:
   ```bash
   python CFC_Number_v2.4_GUI.py
   ```

## 📜 Changelog
See [CHANGELOG.txt](CHANGELOG.txt) for a detailed version history, including the transition from terminal-based to GUI-based features.

## 👨‍💻 About the Creator
Created by NOAH, the kindest person in the world! Connect with me:
- 💻 [GitHub: @nueonenoah](https://github.com/nueonenoah)
- 📱 [Telegram: @nueonenoah](https://t.me/nueonenoah)

---

*Built with ❤️ for Telegram users and list organizers everywhere.*