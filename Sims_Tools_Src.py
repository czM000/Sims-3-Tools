import os
import customtkinter as ctk
from tkinter import messagebox, filedialog
import subprocess
import webbrowser
from PIL import Image, ImageTk, ImageEnhance
import configparser

CONFIG_FILE = os.path.join(os.environ['APPDATA'], 'SimsTools.ini')
INITIAL_WIDTH, INITIAL_HEIGHT = 600, 400
BUTTONS = []

def save_sims_directory(path):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'SimsDirectory': path}
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def load_sims_directory():
    if not os.path.exists(CONFIG_FILE):
        return None
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config['DEFAULT'].get('SimsDirectory', None)

def clean_sims_files(event=None):
    try:
        sims_directory = load_sims_directory()
        if not sims_directory:
            messagebox.showerror("Error", "Please select Sims directory first!")
            return

        commands = [
            f'cd "{sims_directory}"',
            r'DEL CASPartCache.package',
            r'DEL compositorCache.package',
            r'DEL scriptCache.package',
            r'DEL simCompositorCache.package',
            r'DEL socialCache.package',
            r'DEL /F /Q Thumbnails',
            r'DEL /F /Q FeaturedItems',
            r'DEL /F /Q WorldCaches',
            f'cd "{sims_directory}\\DCCache"',
            r'DEL missingdeps.idx',
            f'cd "{sims_directory}\\SigsCache"',
            r'DEL *.bin',
            f'cd "{sims_directory}\\Downloads"',
            r'DEL *.bin',
            f'cd "{sims_directory}\\Custom Music"',
            r'DEL *.mp3'
        ]
        
        for command in commands:
            os.system(command)
            
        messagebox.showinfo("Success", "Files cleaned successfully")
    except Exception as e:
        messagebox.showerror("Error", f"An error has occurred : {e}")

def select_sims_directory():
    try:
        sims_directory = filedialog.askdirectory(title="Select the Sims 3 directory")
        if sims_directory:
            save_sims_directory(sims_directory)
            messagebox.showinfo("Success", f"Directory saved:\n{sims_directory}")
            update_directory_display()
    except Exception as e:
        messagebox.showerror("Error", f"An error has occurred : {e}")

def exit_application(event=None):
    try:
        bat_file_path = os.path.join(os.environ['USERPROFILE'], "Desktop", "Sims_Tools", "find_merged_cc.bat")
        file_path = filedialog.askopenfilename(
            title="Select a .package file", 
            filetypes=[("Package files", "*.package")]
        )
        if file_path:
            process = subprocess.Popen([bat_file_path, file_path])
            process.wait()
            if process.returncode == 0:
                messagebox.showinfo("Success", "The .bat file has been executed successfully.")
            else:
                messagebox.showerror("Error", f"The .bat file failed with return code : {process.returncode}")
    except Exception as e:
        messagebox.showerror("Error", f"An error has occurred : {e}")

def open_link(event=None):
    webbrowser.open("https://www.tumblr.com/emmadesignstuff")

def get_round_rectangle_points(x1, y1, x2, y2, radius):
    return [
        x1+radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1
    ]

def create_round_rectangle(canvas, x1, y1, x2, y2, radius=10, **kwargs):
    points = get_round_rectangle_points(x1, y1, x2, y2, radius)
    return canvas.create_polygon(points, smooth=True, **kwargs)

def create_canvas_button(x, y, text, command, button_width=160, button_height=35, font=("Arial", 12)):
    global BUTTONS
    CORNER_RADIUS = 10
    left = x - button_width // 2
    top = y - button_height // 2
    right = x + button_width // 2
    bottom = y + button_height // 2
    
    rect = create_round_rectangle(canvas, left, top, right, bottom, CORNER_RADIUS, fill="#2B2B2B", outline="#2B2B2B")
    txt = canvas.create_text(x, y, text=text, fill="white", font=font)
    
    def on_enter(event):
        canvas.itemconfig(rect, fill="#3B3B3B", outline="#3B3B3B")
        window.config(cursor="hand2")
        
    def on_leave(event):
        canvas.itemconfig(rect, fill="#2B2B2B", outline="#2B2B2B")
        window.config(cursor="")
        
    def on_click(event):
        command()
        
    for item in [rect, txt]:
        canvas.tag_bind(item, "<Enter>", on_enter)
        canvas.tag_bind(item, "<Leave>", on_leave)
        canvas.tag_bind(item, "<Button-1>", on_click)
        
    BUTTONS.append({
        "rect": rect,
        "text": txt,
        "rel_x": x / INITIAL_WIDTH,
        "rel_y": y / INITIAL_HEIGHT,
        "rel_width": button_width / INITIAL_WIDTH,
        "rel_height": button_height / INITIAL_HEIGHT,
        "rel_radius": CORNER_RADIUS / INITIAL_WIDTH
    })

def update_directory_display():
    current_dir = load_sims_directory() or 'Not selected'
    canvas.itemconfig(directory_info, text=f"Current directory of Sims 3: {current_dir}")

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

window = ctk.CTk()
window.title("Sims Tools")
window.geometry(f"{INITIAL_WIDTH}x{INITIAL_HEIGHT}")

assets_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'Sims_Tools', 'assets')
original_bg_image = Image.open(os.path.join(assets_path, "background.jpg"))
original_bg_image = original_bg_image.resize((INITIAL_WIDTH, INITIAL_HEIGHT), Image.LANCZOS)
original_bg_image = ImageEnhance.Brightness(original_bg_image).enhance(0.5)
background_photo = ImageTk.PhotoImage(original_bg_image)

canvas = ctk.CTkCanvas(window, highlightthickness=0)
canvas.pack(fill="both", expand=True)

bg_image_id = canvas.create_image(0, 0, image=background_photo, anchor="nw")
title_text_id = canvas.create_text(INITIAL_WIDTH/2, INITIAL_HEIGHT/8, text="Tools for The Sims", font=("Arial", 18, "bold"), fill="pink")

button_spacing = 100
main_y = INITIAL_HEIGHT/2 - 20
create_canvas_button(INITIAL_WIDTH/2 - button_spacing, main_y, "Clear caches", clean_sims_files)
create_canvas_button(INITIAL_WIDTH/2 + button_spacing, main_y, "Extract the packages", exit_application)

create_canvas_button(INITIAL_WIDTH/2 - button_spacing, main_y + 60, "Select Sims Directory", select_sims_directory, button_width=140, button_height=30, font=("Arial", 10))

directory_info = canvas.create_text(INITIAL_WIDTH/2, INITIAL_HEIGHT - 40, text="Current directory of Sims 3: Not selected", fill="white", font=("Arial", 10))
update_directory_display()

logo_original = Image.open(os.path.join(assets_path, "tumblr.png")).resize((50, 50), Image.LANCZOS)
logo_photo = ImageTk.PhotoImage(logo_original)
logo_item = canvas.create_image(INITIAL_WIDTH - 10, INITIAL_HEIGHT - 10, anchor="se", image=logo_photo)

canvas.tag_bind(logo_item, "<Button-1>", open_link)

window.mainloop()
