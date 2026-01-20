import tkinter as tk
from tkinter import ttk, filedialog

FONT_MAIN = ("Noto Sans Khmer", 12)
FONT_HEADER = ("Noto Sans Khmer", 16, "bold")

COLOR_BG = "#F3F4F6"        # Light Gray background
COLOR_WHITE = "#FFFFFF"     # White for containers
COLOR_PRIMARY = "#4F46E5"   # Indigo/Blue for main actions
COLOR_DANGER = "#EF4444"    # Red for delete/clear
COLOR_TEXT = "#1F2937"      # Dark gray for text
COLOR_BORDER = "#E5E7EB"    # Light border color

CONSONANTS = ["ក","ខ","គ","ឃ","ង","ច","ឆ","ជ","ឈ","ញ",
              "ដ","ឋ","ឌ","ឍ","ណ","ត","ថ","ទ","ធ","ន",
              "ប","ផ","ព","ភ","ម","យ","រ","ល","វ",
              "ស","ហ","ឡ","អ"]

DEPENDENT_VOWELS = ["ា","ិ","ី","ឹ","ឺ","ុ","ូ","ួ","ើ","ឿ",
                    "ៀ","េ","ែ","ៃ","ោ","ៅ","ំ","ះ","ុំ","ាំ",
                    "ុះ","េះ","ោះ"]

INDEPENDENT_VOWELS = ["អ","អា","ឥ","ឦ","ឧ","ឩ","ឪ","ឫ","ឬ","ឭ","ឮ",
                      "ឯ","ឰ","ឱ","ឲ","ឳ"]

ALL_LETTERS = CONSONANTS + DEPENDENT_VOWELS + INDEPENDENT_VOWELS

class StrokeCollectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Khmer Stroke Collector")
        self.root.geometry("520x750")
        self.root.configure(bg=COLOR_BG)
        
        # Data
        self.selected_char = tk.StringVar(value=ALL_LETTERS[0]) # Default to first
        self.strokes = []
        self.current_stroke = []

        # UI and Styles
        self.setup_styles()
        self.build_header()
        self.build_selector()
        self.build_canvas()
        self.build_buttons()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')  # 'clam' provides a good base for custom coloring
        
        # Configure TCombobox
        style.configure("TCombobox", 
                        fieldbackground=COLOR_WHITE, 
                        background=COLOR_WHITE,
                        foreground=COLOR_TEXT,
                        arrowcolor=COLOR_PRIMARY,
                        bordercolor=COLOR_BORDER,
                        lightcolor=COLOR_BORDER,
                        darkcolor=COLOR_BORDER)

    def build_header(self):
        header_frame = tk.Frame(self.root, bg=COLOR_WHITE, pady=15, padx=20)
        header_frame.pack(fill="x", side="top")
        
        border = tk.Frame(self.root, bg=COLOR_BORDER, height=1)
        border.pack(fill="x", side="top")

        title = tk.Label(header_frame, text="Khmer Stroke Collector", 
                         font=FONT_HEADER, bg=COLOR_WHITE, fg=COLOR_PRIMARY)
        title.pack(anchor="center")

    # Label
    def build_selector(self):
        container = tk.Frame(self.root, bg=COLOR_BG, pady=20)
        container.pack(fill="x", padx=20)
        
        lbl = tk.Label(container, text="Select Character:", font=FONT_MAIN, bg=COLOR_BG, fg=COLOR_TEXT)
        lbl.pack(side="left", padx=(20, 10))
        
        # Listing all character in label
        self.dropdown = ttk.Combobox(container, textvariable=self.selected_char, 
                                     values=ALL_LETTERS, font=FONT_MAIN, state="readonly", width=15)
        self.dropdown.pack(side="left")
        
    # User drawing
    def build_canvas(self):
        canvas_frame = tk.Frame(self.root, bg=COLOR_WHITE, padx=5, pady=5)
        canvas_frame.pack(padx=20, pady=10)
        
        self.canvas = tk.Canvas(canvas_frame, bg="white", width=460, height=420, 
                                highlightthickness=1, highlightbackground=COLOR_BORDER, highlightcolor=COLOR_PRIMARY)
        self.canvas.pack()

        # Mouse events
        self.canvas.bind("<ButtonPress-1>", self.start_stroke)
        self.canvas.bind("<B1-Motion>", self.draw_stroke)
        self.canvas.bind("<ButtonRelease-1>", self.end_stroke)

    def start_stroke(self, event):
        self.current_stroke = [(event.x, event.y)]

    def draw_stroke(self, event):
        x, y = event.x, event.y
        last_x, last_y = self.current_stroke[-1]
        self.canvas.create_line(last_x, last_y, x, y, width=4, capstyle=tk.ROUND, joinstyle=tk.ROUND, fill="black")
        self.current_stroke.append((x, y))

    def end_stroke(self, event):
        if self.current_stroke and len(self.current_stroke) > 1:
            self.strokes.append(self.current_stroke)
            self.current_stroke = []
        else:
            self.current_stroke = []

    def build_buttons(self):
        btn_frame = tk.Frame(self.root, bg=COLOR_BG)
        btn_frame.pack(pady=20, padx=20, fill="x")

        def create_modern_btn(parent, text, command, bg_color, text_color="white"):
            btn = tk.Button(parent, text=text, font=FONT_MAIN, command=command,
                            bg=bg_color, fg=text_color, activebackground=bg_color, activeforeground=text_color,
                            relief="flat", cursor="hand2", padx=20, pady=8, borderwidth=0)
            
            def on_enter(e):
                pass 
                
            btn.bind("<Enter>", on_enter)
            return btn

        inner_frame = tk.Frame(btn_frame, bg=COLOR_BG)
        inner_frame.pack()

        btn_clear = create_modern_btn(inner_frame, "លុប (Clear)", self.clear_canvas, COLOR_DANGER)
        btn_clear.pack(side="left", padx=10)

        btn_save = create_modern_btn(inner_frame, "រក្សាទុក (Save)", self.save, COLOR_PRIMARY)
        btn_save.pack(side="left", padx=10)

        btn_save_as = create_modern_btn(inner_frame, "រក្សាទុកជា (Save As)", self.save_as, "#10B981") # Green
        btn_save_as.pack(side="left", padx=10)

    # Clear character
    def clear_canvas(self):
        self.canvas.delete("all")
        self.strokes.clear()

    # File format
    def get_formatted_data(self):
        char = self.selected_char.get()
        stroke_strings = []
        for stroke in self.strokes:
            points_str = " ".join([f"{x} {y}" for x, y in stroke])
            stroke_strings.append(points_str)
        
        # stroke sperator 
        full_data = f"{char} " + " # ".join(stroke_strings) + " #"
        return full_data

    def save_data_to_file(self, filename):
        if not self.strokes:
            print("No strokes to save.")
            return

        data = self.get_formatted_data()
        try:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(data + "\n")
            print(f"Saved to {filename}")
        except Exception as e:
            print(f"Error saving file: {e}")

    def save(self):
        if hasattr(self, 'current_file') and self.current_file:
            self.save_data_to_file(self.current_file)
        else:
            self.save_as()

    def save_as(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Save Strokes As"
        )
        if filename:
            self.current_file = filename
            self.save_data_to_file(filename)


if __name__ == "__main__":
    root = tk.Tk()
    app = StrokeCollectorApp(root)
    root.mainloop()
