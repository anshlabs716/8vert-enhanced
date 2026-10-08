# ⚡ 8vert-enhanced

<div align="center">

### 🧮 An All-in-One Conversion, Calculation & Notes Toolkit

**8vert-enhanced is a fork of my friend's original project — [8vert](https://github.com/shozanthebozan/8vert)**

[![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-green?style=for-the-badge&logo=apache&logoColor=white)](https://www.apache.org/licenses/LICENSE-2.0)
[![Platform](https://img.shields.io/badge/Platform-Cross--Platform-orange?style=for-the-badge)](https://github.com/anshlabs716/8vert-enhanced)
[![Language](https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

</div>

---

## 📑 Table of Contents

- [🧠 About](#-about)
- [✨ Features](#-features)
- [☕ Prerequisites](#-prerequisites)
  - [Check what you have](#check-what-you-have)
  - [Installing tkinter](#installing-tkinter)
- [🚀 Installation](#-🚀-installation)
- [🗂️ Where your data lives](#-where-your-data-lives)
- [📂 Project Structure](#-project-structure)
- [📝 Notes System](#-notes-system)
- [💻 Platform](#-platform)
- [🔐 Security](#-security)
- [🤝 Contributing](#-contributing)
- [🐛 Bug Reports](#-bug-reports)
- [🧭 Roadmap](#-roadmap)
- [📜 License](#-license)
- [👨‍💻 Credits](#-credits)

---

## 🧠 About

**8vert-enhanced** is an all-in-one Python conversion and calculation toolkit with an integrated notes system.

This project is a fork of my friend's first programming project, [**8vert**](https://github.com/shozanthebozan/8vert), built on the goal of expanding the original idea into a more capable and useful utility. Full credit for the original concept and design goes to him — this fork carries his work forward.

Alongside conversions and calculations, the project includes a notes system that saves notes as either **Markdown (`.md`)** or **plain text (`.txt`)** files.

---

## ✨ Features

### 🔄 Conversions

- 📏 Unit conversion tools
- 🔢 Conversion-focused utilities
- 🧮 Built-in calculations
- ⚡ Designed as an all-in-one utility

### 📝 Notes

- ✍️ Create notes directly from the program
- 📄 Save notes as Markdown
- 📃 Save notes as plain text
- 💾 Keep your notes as normal files

### 🛠️ Utility

- 🐍 Written entirely in Python
- 🖥️ Designed as a general-purpose desktop/terminal utility
- 🧩 Easy to expand with additional tools
- 🔧 Continued from the original 8vert.py project

---

## ☕ Prerequisites

**8vert-enhanced has no third-party dependencies.** Everything it uses ships with
Python itself — there is nothing to `pip install`.

You need two things:

| Requirement | Notes |
| ----------- | ----- |
| **Python 3.6+** | 3.8 or newer recommended; CI tests 3.8 – 3.13 |
| **tkinter** | Bundled with Python, but sometimes packaged separately |

### Check what you have

~~~~bash
python3 --version
python3 -c "import tkinter; print('tkinter OK')"
~~~~

If that second command errors with `ModuleNotFoundError: No module named 'tkinter'`,
install it using the steps below. This is the single most common setup problem.

### Installing tkinter

**🐧 Debian / Ubuntu / Mint**

~~~~bash
sudo apt update
sudo apt install python3-tk
~~~~

**📦 Arch / Manjaro**

~~~~bash
sudo pacman -S tk
~~~~

**🍎 Fedora**

~~~~bash
sudo dnf install python3-tkinter
~~~~

**🟠 openSUSE**

~~~~bash
sudo zypper install python3-tk
~~~~

**🍎 macOS** (python.org installers)

Tk ships separately as a `.pkg`:

1. Open <https://www.python.org/downloads/macos/>
2. Download the matching installer for your Python version
3. Run it and select **"Install tkinter for Python 3.x"** from the optional components

Homebrew's `python-tk` also works: `brew install python-tk`

**🪟 Windows**

Included with the official installer from <https://www.python.org/downloads/windows/>.
Tick **"tcl/tk and IDLE"** during setup. If you installed Python without it, re-run
the installer and choose Modify.

---

## 🚀 Installation

### Option 1 — Run from source (all platforms)

Clone the repository:

~~~~bash
git clone https://github.com/anshlabs716/8vert-enhanced.git
cd 8vert-enhanced
~~~~

Launch it:

~~~~bash
python3 8vert-enhanced.py
~~~~

On Windows:

~~~~powershell
python 8vert-enhanced.py
~~~~

No install step and no build step — this is the whole thing.

### Option 2 — Download a release (Linux)

Grab `8vert-enhanced` from the [releases page](https://github.com/anshlabs716/8vert-enhanced/releases),
`chmod +x` it, and run it. That binary bundles Python and tkinter, so nothing needs
to be installed:

~~~~bash
chmod +x 8vert-enhanced
./8vert-enhanced
~~~~

### Option 3 — Bundle it yourself

To ship a single-file build of your own:

~~~~bash
pip install pyinstaller
pyinstaller --onefile --name 8vert-enhanced 8vert-enhanced.py
~~~~

The binary lands in `dist/`.

---

## 🗂️ Where your data lives

Settings, calculation history, and saved notes are written to:

~~~~text
~/.8vert-enhanced/
~~~~

Created automatically on first run. Delete that folder to reset the app to a clean
state. Notes you save as Markdown or plain text live here too, so they're plain
files you can back up or read with any editor.

---

## 📂 Project Structure

~~~~text
8vert-enhanced/
├── 8vert-enhanced.py
├── .gitignore
├── LICENSE
├── README.md
└── SECURITY.md
~~~~

---

## 📝 Notes System

One of the main additions carried over from the revamp is the ability to create and save notes.

Notes can be stored as:

### Markdown

~~~~text
note.md
~~~~

Useful when you want your notes to remain formatted and compatible with Markdown editors.

### Plain Text

~~~~text
note.txt
~~~~

Useful for simple notes that don't require formatting.

---

## 💻 Platform

Because the project is written in Python, it is intended to be usable across different operating systems where a compatible Python environment is available.

| Platform | Status |
|---|---|
| 🐧 Linux | ✅ Python |
| 🪟 Windows | ✅ Python |
| 🍎 macOS | ✅ Python |
| 💻 Other Unix-like systems | ⚠️ Depends on environment |

> ⚠️ Some functionality may behave differently depending on the operating system and Python environment.

---

## 🔐 Security

Security information and vulnerability reporting instructions can be found in:

`SECURITY.md`

Please report security issues responsibly rather than publicly exposing vulnerabilities.

---

## 🤝 Contributing

Contributions and ideas are welcome!

1. Fork the repository
2. Create a branch
3. Make your changes
4. Test your changes
5. Commit your work
6. Push the branch
7. Open a Pull Request

---

## 🐛 Bug Reports

Found something broken?

When reporting an issue, include:

- Operating system
- Python version
- What you were trying to do
- What happened
- Any error messages

This makes problems much easier to reproduce and fix.

---

## 🧭 Roadmap

- [x] Expand conversion tools
- [ ] Add more calculators
- [ ] Improve notes
- [ ] Add more file formats
- [x] Improve user interface
- [x] Add configuration options
- [ ] Add more productivity utilities
- [ ] Improve cross-platform compatibility
- [ ] Add automated testing

---

## 📜 License

This project is licensed under the **Apache License 2.0**.

See [`LICENSE`](LICENSE) for the full license text.

---

## 👨‍💻 Credits

**Original project:** [8vert](https://github.com/shozanthebozan/8vert) — created by **shozanthebozan**. This fork would not exist without it, and all credit for the original concept, design, and implementation goes to him.

**This fork:** created and maintained by **Ansh Bhatia**.

---

<div align="center">

### ⚡ 8vert-enhanced

**Convert • Calculate • Write • Save**

Made with 🐍 Python

</div>
