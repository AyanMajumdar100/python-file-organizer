# TidyPy

## Overview

**TidyPy** is a desktop-based Python file organizer with a clean GUI that helps you automatically organize cluttered folders into structured categories like Images, Videos, Documents, Code, and more.
It uses a configurable `categories.json` file and provides a visual completion status using a donut chart once organizing is complete.

## Features

- GUI-based folder selection (Tkinter)
- Smart file categorization using extensions
- Automatically creates folders based on file type
- Safely handles duplicate filenames
- Donut chart showing moved vs failed files
- Scrollable view of created folders
- Fully configurable categories via JSON
- Optional dry-run support

## Tech Stack

- **Language**: Python  
- **GUI**: Tkinter  
- **Visualization**: Matplotlib  
- **Configuration**: JSON  

## Setup & Run Instructions

### 1. Clone the repository
```bash
git clone https://github.com/AyanMajumdar100/TidyPy.git
cd TidyPy
````

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

### 4. Install required packages (not inbuilt)

```bash
pip install matplotlib
```

> `tkinter`, `json`, `pathlib`, and `shutil` come bundled with Python.

### 5. Run the application

```bash
py organizer.py
```

## Application Screenshots

### Unorganized folder having files of different formats

![Unorganized Folder](App%20Screenshots/View-Unorganized%20folder.png)

### Folder selection and confirmation

![Folder Selection](App%20Screenshots/File%20Organizer%20Screen%202.png)

### New folder structure created with completion donut chart

![Organizer Result](App%20Screenshots/File%20Organizer%20Screen%203.png)

### View of the organized folder

![Organized Folder](App%20Screenshots/View-Organized%20folder.png)


## Configuration

File categories and extensions can be customized using:

```text
categories.json
```

You can:

* Enable or disable categories
* Add or remove extensions
* Toggle `dry_run` mode

## Project Structure

```text
TidyPy/
│
├── organizer.py
├── ui_styles.py
├── categories.json
├── App Screenshots/
│   ├── View-Unorganized folder.png
│   ├── File Organizer Screen 2.png
│   ├── File Organizer Screen 3.png
│   └── View-Organized folder.png
├── .gitignore
└── LICENSE
```

## License

This project uses a **proprietary license**.
Refer to the `LICENSE` file for more information.


Built to turn chaos into clarity ✨
Happy organizing with **TidyPy** 🚀
