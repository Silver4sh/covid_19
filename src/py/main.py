# gui.py
import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.ttk as ttk
import pandas as pd
from analysis import (analysis_continent, analysis_location, analysis_continent_year, 
                      analysis_location_year, analysis_location_month, analysis_year, analysis_month)
from autocomplete import AutocompleteCombobox

global_data = None

def import_csv(root, analysis_frame, file_label):
    file_path = filedialog.askopenfilename(
        title="Pilih file CSV",
        filetypes=[("CSV Files", "*.csv")]
    )
    if file_path:
        try:
            data = pd.read_csv(file_path)
            if 'date' in data.columns:
                data['date'] = pd.to_datetime(data['date'])
            messagebox.showinfo("Sukses", f"Data berhasil diimpor!\nJumlah baris: {len(data)}")
            global global_data
            global_data = data
            analysis_frame.grid()  # Tampilkan menu analisis
            file_label.config(text=f"File: {file_path.split('/')[-1]}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengimpor file CSV:\n{e}")
    else:
        messagebox.showwarning("Perhatian", "Tidak ada file yang dipilih!")

def get_autocomplete_input(root, title, label_text, options):
    """Menampilkan dialog input dengan AutocompleteCombobox dan mengembalikan nilai yang dipilih."""
    dialog = tk.Toplevel(root)
    dialog.title(title)
    dialog.resizable(False, False)
    dialog.geometry("350x150")
    
    style = ttk.Style(dialog)
    style.theme_use('clam')
    
    label = ttk.Label(dialog, text=label_text, font=("Arial", 12))
    label.grid(row=0, column=0, padx=10, pady=(20,10), sticky="w")
    
    var = tk.StringVar()
    ac_box = AutocompleteCombobox(dialog, textvariable=var, font=("Arial", 12))
    ac_box.set_completion_list(options)
    ac_box.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
    
    selected_value = {"value": None}
    
    def on_ok():
        selected_value["value"] = var.get()
        dialog.destroy()
    
    ok_button = ttk.Button(dialog, text="OK", command=on_ok)
    ok_button.grid(row=2, column=0, padx=10, pady=10, sticky="e")
    
    dialog.grab_set()
    root.wait_window(dialog)
    return selected_value["value"]

def create_gui():
    root = tk.Tk()
    root.title("Aplikasi Analisis Data COVID-19")
    root.geometry("700x550")
    root.resizable(False, False)
    
    style = ttk.Style(root)
    style.theme_use('clam')
    
    # Header Frame
    header_frame = ttk.Frame(root, padding="10")
    header_frame.grid(row=0, column=0, sticky="ew")
    
    header_label = ttk.Label(header_frame, text="Aplikasi Analisis Data COVID-19", font=("Arial", 16, "bold"))
    header_label.pack(side="top", pady=10)
    
    # File Import Frame
    import_frame = ttk.Frame(root, padding="10")
    import_frame.grid(row=1, column=0, sticky="ew")
    
    import_button = ttk.Button(import_frame, text="Import CSV", command=lambda: import_csv(root, analysis_frame, file_label))
    import_button.grid(row=0, column=0, padx=5, pady=5)
    
    file_label = ttk.Label(import_frame, text="Belum ada file yang diimpor", font=("Arial", 10))
    file_label.grid(row=0, column=1, padx=5, pady=5)
    
    # Analysis Menu Frame (disembunyikan sampai file diimpor)
    analysis_frame = ttk.Frame(root, padding="10")
    analysis_frame.grid(row=2, column=0, sticky="nsew")
    analysis_frame.grid_remove()
    
    menu_label = ttk.Label(analysis_frame, text="Pilih Menu Analisis:", font=("Arial", 14))
    menu_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))
    
    # Tombol-tombol menu analisis
    btn1 = ttk.Button(analysis_frame, text="1. Analisis per Continent", command=lambda: handle_analysis_continent(root))
    btn1.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    
    btn2 = ttk.Button(analysis_frame, text="2. Analisis per Location", command=lambda: handle_analysis_location(root))
    btn2.grid(row=1, column=1, padx=10, pady=5, sticky="w")
    
    btn3 = ttk.Button(analysis_frame, text="3. Analisis per Continent per Year", command=lambda: handle_analysis_continent_year(root))
    btn3.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    
    btn4 = ttk.Button(analysis_frame, text="4. Analisis per Location per Year", command=lambda: handle_analysis_location_year(root))
    btn4.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    
    btn5 = ttk.Button(analysis_frame, text="5. Analisis per Location per Month", command=lambda: handle_analysis_location_month(root))
    btn5.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    
    btn6 = ttk.Button(analysis_frame, text="6. Analisis per Year (Global)", command=lambda: analysis_year(global_data, root))
    btn6.grid(row=3, column=1, padx=10, pady=5, sticky="w")
    
    btn7 = ttk.Button(analysis_frame, text="7. Analisis per Month (Global)", command=lambda: analysis_month(global_data, root))
    btn7.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    
    # Handler untuk input dengan autocomplete dan pemanggilan analisis
    def handle_analysis_continent(root):
        if global_data is None:
            messagebox.showerror("Error", "Data belum diimpor!")
            return
        continents = sorted(global_data['continent'].dropna().unique().tolist())
        continent = get_autocomplete_input(root, "Pilih Continent", "Masukkan atau pilih continent:", continents)
        if continent:
            analysis_continent(global_data, root, continent)
    
    def handle_analysis_location(root):
        if global_data is None:
            messagebox.showerror("Error", "Data belum diimpor!")
            return
        locations = sorted(global_data['location'].dropna().unique().tolist())
        location = get_autocomplete_input(root, "Pilih Location", "Masukkan atau pilih location:", locations)
        if location:
            analysis_location(global_data, root, location)
    
    def handle_analysis_continent_year(root):
        if global_data is None:
            messagebox.showerror("Error", "Data belum diimpor!")
            return
        continents = sorted(global_data['continent'].dropna().unique().tolist())
        continent = get_autocomplete_input(root, "Pilih Continent", "Masukkan atau pilih continent:", continents)
        if continent:
            analysis_continent_year(global_data, root, continent)
    
    def handle_analysis_location_year(root):
        if global_data is None:
            messagebox.showerror("Error", "Data belum diimpor!")
            return
        locations = sorted(global_data['location'].dropna().unique().tolist())
        location = get_autocomplete_input(root, "Pilih Location", "Masukkan atau pilih location:", locations)
        if location:
            analysis_location_year(global_data, root, location)
    
    def handle_analysis_location_month(root):
        if global_data is None:
            messagebox.showerror("Error", "Data belum diimpor!")
            return
        locations = sorted(global_data['location'].dropna().unique().tolist())
        location = get_autocomplete_input(root, "Pilih Location", "Masukkan atau pilih location:", locations)
        if location:
            analysis_location_month(global_data, root, location)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
