from __future__ import annotations

import sys
import json
import shutil
import threading
from pathlib import Path
from tkinter import *
from tkinter import filedialog, messagebox, ttk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import ui_styles


class FileOrganizerApp:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title("File Organizer")
        self.root.geometry("800x400")
        self.root.configure(bg=ui_styles.BG_WHITE)

        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

        self.fonts = ui_styles.load_fonts(root)

        self.categories: dict[str, str] = {}
        self.dry_run = False
        self._load_categories()

        self.moved = 0
        self.failed = 0
        self.created_folders: set[str] = set()

        self._build_ui()

    # UI Elements

    def _build_ui(self):
        Label(
            self.root,
            text="File Organizer Dashboard",
            bg=ui_styles.BG_WHITE,
            fg=ui_styles.TEXT_PRIMARY,
            font=self.fonts["title"]
        ).pack(anchor="w", padx=40, pady=(30, 15))

        path_frame = Frame(self.root, bg=ui_styles.BG_WHITE)
        path_frame.pack(fill="x", padx=40)

        self.path_var = StringVar()
        Entry(
            path_frame,
            textvariable=self.path_var,
            font=self.fonts["body"],
            width=70,
            relief="solid",
            bd=1
        ).pack(side=LEFT, ipady=6)

        Button(
            path_frame,
            text="Browse",
            font=self.fonts["button"],
            bg=ui_styles.CARD_BG,
            highlightbackground=ui_styles.BORDER,
            fg=ui_styles.TEXT_PRIMARY,
            relief="flat",
            padx=32,
            pady=8,
            command=self._browse
        ).pack(side=LEFT, padx=10)

        Button(
            self.root,
            text="Organize Files",
            bg=ui_styles.PRIMARY,
            fg="white",
            font=self.fonts["button"],
            relief="flat",
            padx=24,
            pady=10,
            command=self._start_organize
        ).pack(pady=25)

        self.main = Frame(self.root, bg=ui_styles.BG_WHITE)
        self.main.pack(fill="both", expand=True, padx=40, pady=10)

        # Left side: Scrollable area for folders
        self.folder_container = Frame(self.main, bg=ui_styles.BG_WHITE)
        self.folder_container.pack(side=LEFT, fill="both", expand=True)

        # Right side: Chart
        self.chart_frame = Frame(self.main, bg=ui_styles.BG_WHITE, width=300)
        self.chart_frame.pack(side=RIGHT, fill="y", padx=(20, 0))
        self.chart_frame.pack_propagate(False)

    # LOGIC

    def _browse(self):
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)

    def _start_organize(self):
        path_str = self.path_var.get().strip()

        if not path_str:
            messagebox.showwarning("Selection Required", "Please select a folder to organize.")
            return

        base = Path(path_str)

        if not base.exists():
            messagebox.showerror("Error", "Invalid folder path")
            return

        if not messagebox.askyesno(
            "Confirm",
            f"Organize files in:\n{base}\n\nThis cannot be undone."
        ):
            return

        self.root.geometry("1100x650")
        self._reset_state()

        threading.Thread(
            target=self._organize,
            args=(base,),
            daemon=True
        ).start()

    def _organize(self, base: Path):
        for file in base.iterdir():
            if file.is_dir() or file.name.startswith("."):
                continue

            if file.resolve() == Path(__file__).resolve():
                continue

            category = self.categories.get(file.suffix.lower(), "Others")
            target_dir = base / category
            target_dir.mkdir(exist_ok=True)

            self.created_folders.add(category)

            destination = self._unique_path(target_dir / file.name)

            try:
                if not self.dry_run:
                    shutil.move(str(file), str(destination))
                self.moved += 1
            except (PermissionError, OSError):
                self.failed += 1

        self.root.after(0, self._render_results)

    # HELPER METHODS
    def _load_categories(self):
        with open("categories.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        self.dry_run = data.get("dry_run", False)

        for category in data.get("categories", []):
            if not category.get("enabled", False):
                continue

            name = category["name"]
            for ext in category.get("extensions", []):
                self.categories[ext.lower()] = name

    def _unique_path(self, path: Path) -> Path:
        if not path.exists():
            return path

        i = 1
        while True:
            candidate = path.with_stem(f"{path.stem}_{i}")
            if not candidate.exists():
                return candidate
            i += 1

    def _reset_state(self):
        self.moved = self.failed = 0
        self.created_folders.clear()

        for widget in self.folder_container.winfo_children():
            widget.destroy()
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

    def _on_closing(self):
        if not messagebox.askokcancel("Quit", "Do you want to quit?"):
            return
        self.root.destroy()
        sys.exit(0)

    # RENDER
    def _render_results(self):
        if self.moved == 0 and self.failed == 0:
            messagebox.showinfo("Nothing to organize", "No files were found to organize.")
            return

        # 1. Scrollable Folder Section
        Label(
            self.folder_container,
            text="Folders Created",
            bg=ui_styles.BG_WHITE,
            fg=ui_styles.TEXT_PRIMARY,
            font=self.fonts["body"]
        ).pack(anchor="w", pady=(0, 10))

        # Canvas and Scrollbar
        canvas = Canvas(self.folder_container, bg=ui_styles.BG_WHITE, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.folder_container, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg=ui_styles.BG_WHITE)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=LEFT, fill="both", expand=True)
        scrollbar.pack(side=RIGHT, fill="y")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Folder Grid Cards
        folders = sorted(self.created_folders)
        columns = 3
        
        for i, folder in enumerate(folders):
            card = Frame(
                scrollable_frame,
                bg=ui_styles.CARD_BG,
                width=160,
                height=100,
                highlightbackground=ui_styles.BORDER,
                highlightthickness=1
            )
            card.grid(row=i // columns, column=i % columns, padx=10, pady=10)
            card.grid_propagate(False)

            Label(
                card,
                text=folder,
                bg=ui_styles.CARD_BG,
                fg=ui_styles.TEXT_PRIMARY,
                font=self.fonts["body"]
            ).place(relx=0.5, rely=0.5, anchor="center")

        # 2. Circular Donut Chart
        Label(
            self.chart_frame,
            text="Status",
            bg=ui_styles.BG_WHITE,
            fg=ui_styles.TEXT_PRIMARY,
            font=self.fonts["body"]
        ).pack(anchor="n", pady=(0, 10))

        sizes = [self.moved, self.failed]
        colors = [ui_styles.PRIMARY, ui_styles.DANGER]

        if sum(sizes) == 0:
            sizes = [1]
            colors = [ui_styles.BORDER]

        fig, ax = plt.subplots(figsize=(5, 4), subplot_kw=dict(aspect="equal"))
        fig.patch.set_facecolor(ui_styles.BG_WHITE)

        wedges, texts = ax.pie(
            sizes,
            colors=colors,
            startangle=90,
            counterclock=False,
            wedgeprops=dict(width=0.3, edgecolor=ui_styles.BG_WHITE, linewidth=2)
        )

        ax.text(
            0, 0, 
            f"{self.moved} Moved\n{self.failed} Failed", 
            ha="center", va="center", 
            fontsize=10, 
            fontweight="bold",
            color=ui_styles.TEXT_PRIMARY, 
            fontfamily="sans-serif"
        )

        canvas_chart = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas_chart.get_tk_widget().pack(fill="both", expand=True)
        canvas_chart.draw()


if __name__ == "__main__":
    root = Tk()
    FileOrganizerApp(root)
    root.mainloop()