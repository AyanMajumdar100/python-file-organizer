from tkinter import font

BG_WHITE = "#ffffff"
CARD_BG = "#efefef"
PRIMARY = "#2563eb"
DANGER = "#ef4444"
TEXT_PRIMARY = "#0f172a"
TEXT_SECONDARY = "#64748b"
BORDER = "#e5e7eb"

def load_fonts(root):
    available = set(font.families(root))
    
    family = "Arial" 
    preferred_fonts = ["Poppins", "Segoe UI", "Helvetica Neue", "Helvetica"]
    
    for f in preferred_fonts:
        if f in available:
            family = f
            break

    return {
        "title": font.Font(root, family=family, size=20, weight="bold"),
        "body": font.Font(root, family=family, size=11),
        "small": font.Font(root, family=family, size=9),
        "button": font.Font(root, family=family, size=11, weight="bold")
    }