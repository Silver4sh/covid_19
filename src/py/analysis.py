import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_in_new_window(x, y, title, xlabel, ylabel, root):
    """Membuka jendela baru untuk menampilkan plot."""
    plot_window = tk.Toplevel(root)
    plot_window.title(title)
    plot_window.geometry("800x600")
    
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x, y, marker='o', linestyle='-', color='blue')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)
    
    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def analysis_continent(data, root, continent):
    if not continent:
        messagebox.showwarning("Input", "Nama continent tidak boleh kosong")
        return
    df_continent = data[data['continent'].str.lower() == continent.lower()]
    if df_continent.empty:
        messagebox.showerror("Error", f"Tidak ada data untuk continent '{continent}'")
        return
    df_grouped = df_continent.groupby('date').agg({'total_cases': 'sum'}).reset_index()
    plot_in_new_window(df_grouped['date'], df_grouped['total_cases'], 
                         f"Total Cases di {continent}", "Tanggal", "Total Cases", root)

def analysis_location(data, root, location):
    if not location:
        messagebox.showwarning("Input", "Nama location tidak boleh kosong")
        return
    df_location = data[data['location'].str.lower() == location.lower()]
    if df_location.empty:
        messagebox.showerror("Error", f"Tidak ada data untuk location '{location}'")
        return
    df_location = df_location.sort_values('date')
    plot_in_new_window(df_location['date'], df_location['total_cases'], 
                         f"Total Cases di {location}", "Tanggal", "Total Cases", root)

def analysis_continent_year(data, root, continent):
    if not continent:
        messagebox.showwarning("Input", "Nama continent tidak boleh kosong")
        return
    df_continent = data[data['continent'].str.lower() == continent.lower()]
    if df_continent.empty:
        messagebox.showerror("Error", f"Tidak ada data untuk continent '{continent}'")
        return
    df_continent['year'] = df_continent['date'].dt.year
    df_year = df_continent.groupby('year').agg({'total_cases': 'sum'}).reset_index()
    plot_in_new_window(df_year['year'], df_year['total_cases'], 
                         f"Total Cases per Year di {continent}", "Tahun", "Total Cases", root)

def analysis_location_year(data, root, location):
    if not location:
        messagebox.showwarning("Input", "Nama location tidak boleh kosong")
        return
    df_location = data[data['location'].str.lower() == location.lower()]
    if df_location.empty:
        messagebox.showerror("Error", f"Tidak ada data untuk location '{location}'")
        return
    df_location['year'] = df_location['date'].dt.year
    df_year = df_location.groupby('year').agg({'total_cases': 'sum'}).reset_index()
    plot_in_new_window(df_year['year'], df_year['total_cases'], 
                         f"Total Cases per Year di {location}", "Tahun", "Total Cases", root)

def analysis_location_month(data, root, location):
    if not location:
        messagebox.showwarning("Input", "Nama location tidak boleh kosong")
        return
    df_location = data[data['location'].str.lower() == location.lower()]
    if df_location.empty:
        messagebox.showerror("Error", f"Tidak ada data untuk location '{location}'")
        return
    df_location['month'] = df_location['date'].dt.month
    df_month = df_location.groupby('month').agg({'total_cases': 'max'}).reset_index()
    plot_in_new_window(df_month['month'], df_month['total_cases'], 
                         f"Total Cases per Month di {location}", "Bulan", "Total Cases", root)

def analysis_year(data, root):
    data['year'] = data['date'].dt.year
    df_year = data.groupby('year').agg({'total_cases': 'sum'}).reset_index()
    plot_in_new_window(df_year['year'], df_year['total_cases'], 
                         "Total Cases per Year (Global)", "Tahun", "Total Cases", root)

def analysis_month(data, root):
    data['month'] = data['date'].dt.month
    if 'new_cases' in data.columns:
        df_month = data.groupby('month').agg({'new_cases': 'sum'}).reset_index()
        y_data = df_month['new_cases']
        title = "Total New Cases per Month (Global)"
        ylabel = "Total New Cases"
    else:
        df_month = data.groupby('month').agg({'total_cases': 'max'}).reset_index()
        y_data = df_month['total_cases']
        title = "Total Cases per Month (Global)"
        ylabel = "Total Cases"
    plot_in_new_window(df_month['month'], y_data, title, "Bulan", ylabel, root)
