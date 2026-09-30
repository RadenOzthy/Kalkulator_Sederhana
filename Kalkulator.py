import tkinter as tk
from tkinter import ttk, messagebox
import math

class AppKalkulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator Ilmiah Sederhana")
        self.root.geometry("520x800")
        self.root.resizable(False, False)

        # Styling
        style = ttk.Style()
        style.theme_use('clam')

        # Notebook (Tab Navigation)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Inisialisasi Tab
        self.tab_kalkulator = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_kalkulator, text="Kalkulator")

        # Membangun Tampilan Masing-Masing Tab
        self.buat_tab_kalkulator()

        # Hubungkan Input Keyboard Laptop
        self.bind_keyboard()

    # ==========================================
    # TAB 1: KALKULATOR TOMBOL GUI
    # ==========================================
    def buat_tab_kalkulator(self):
        # Layar Tampilan Angka
        self.ekspresi = ""
        self.string_var = tk.StringVar(value="0")

        frame_screen = tk.Frame(self.tab_kalkulator, bg="#2d3748", bd=5)
        frame_screen.pack(fill="x", padx=15, pady=15)

        # state='readonly' agar kursor mengetik tidak membingungkan, 
        # namun input tetap ditangani oleh event binding Tkinter.
        entry_screen = tk.Entry(
            frame_screen, 
            textvariable=self.string_var, 
            font=("Consolas", 22, "bold"), 
            bg="#1a202c", 
            fg="#63b3ed", 
            justify="right", 
            bd=0,
            highlightthickness=0,
            state="readonly"
        )
        entry_screen.pack(fill="x", ipady=12, padx=5, pady=5)

        # Grid Tombol
        frame_buttons = tk.Frame(self.tab_kalkulator)
        frame_buttons.pack(fill="both", expand=True, padx=15, pady=(0, 15))


        # Layout Tombol (8 Baris x 4 Kolom)
        tombol_layout = [
            # --- BARIS FUNGSI ILMIAH ---
            ('sin', 0, 0, '#c05621'), ('cos', 0, 1, '#c05621'), ('tan', 0, 2, '#c05621'), ('log', 0, 3, '#c05621'),
            ('π', 1, 0, '#c05621'),   ('e', 1, 1, '#c05621'),   ('rad', 1, 2, '#c05621'), ('n!', 1, 3, '#c05621'),

            # --- BARIS TOMBOL UTAMA ---
            ('C', 2, 0, '#e53e3e'), ('⌫', 2, 1, '#e53e3e'), ('%', 2, 2, '#4a5568'), ('√', 2, 3, '#4299e1'),
            ('(', 3, 0, '#4a5568'), (')', 3, 1, '#4a5568'), ('^', 3, 2, '#4a5568'), ('/', 3, 3, '#4299e1'),
            ('7', 4, 0, '#2d3748'), ('8', 4, 1, '#2d3748'), ('9', 4, 2, '#2d3748'), ('*', 4, 3, '#4299e1'),
            ('4', 5, 0, '#2d3748'), ('5', 5, 1, '#2d3748'), ('6', 5, 2, '#2d3748'), ('-', 5, 3, '#4299e1'),
            ('1', 6, 0, '#2d3748'), ('2', 6, 1, '#2d3748'), ('3', 6, 2, '#2d3748'), ('+', 6, 3, '#4299e1'),
            ('0', 7, 0, '#2d3748'), ('.', 7, 1, '#2d3748'), ('=', 7, 2, '#319795')
        ]

        # Konfigurasi Grid
        for i in range(8):
            frame_buttons.grid_rowconfigure(i, weight=1)
        for j in range(4):
            frame_buttons.grid_columnconfigure(j, weight=1)

        for item in tombol_layout:
            teks, baris, kolom, warna = item[0], item[1], item[2], item[3]
            colspan = 2 if teks == '=' else 1
            
            btn = tk.Button(
                frame_buttons, 
                text=teks, 
                font=("Arial", 13, "bold"), 
                bg=warna, 
                fg="white", 
                bd=0, 
                activebackground="#718096",
                activeforeground="white",
                command=lambda t=teks: self.tekan_tombol(t)
            )
            btn.grid(row=baris, column=kolom, columnspan=colspan, sticky="nsew", padx=3, pady=3)

    # ==========================================
    # MANAJEMEN KEYBOARD BINDING
    # ==========================================
    def bind_keyboard(self):
        """Mendaftarkan tombol keyboard laptop ke fungsi kalkulator"""
        self.root.bind("<Key>", self.tangani_keypress)

    def tangani_keypress(self, event):
        char = event.char
        keysym = event.keysym

        # 1. Tombol Hitung Hasil (Enter / Return / '=')
        if keysym in ('Return', 'KP_Enter') or char == '=':
            self.tekan_tombol('=')
        
        # 2. Tombol Backspace
        elif keysym == 'Backspace':
            self.tekan_tombol('⌫')
        
        # 3. Tombol Reset Clear (Escape, Delete, atau huruf 'c'/'C')
        elif keysym in ('Escape', 'Delete') or char.lower() == 'c':
            self.tekan_tombol('C')
        
        # 4. Input Angka, Titik, dan Operator Matematika
        elif char in '0123456789.+-*/%^()':
            self.tekan_tombol(char)

    # ==========================================
    # LOGIKA PERHITUNGAN
    # ==========================================
    def hitung_ekspresi(self):
        """Menerjemahkan string ekspresi menjadi ekspresi Python yang bisa dievaluasi"""
        expr = self.ekspresi

        # Substitusi simbol dasar
        expr = expr.replace('^', '**')
        expr = expr.replace('π', 'math.pi')
        expr = expr.replace('e', 'math.e')
        expr = expr.replace('√', 'math.sqrt')
        expr = expr.replace('%', '/100')
        expr = expr.replace('log', 'math.log10')
        expr = expr.replace('rad', 'math.radians')
        expr = expr.replace('n!', 'math.factorial')

        # Substitusi Trigonometri (mengonversi input derajat ke radian)
        expr = expr.replace('sin', 'math.sin_deg')
        expr = expr.replace('cos', 'math.cos_deg')
        expr = expr.replace('tan', 'math.tan_deg')

        # Fungsi pembantu untuk trigonometri berbasis derajat
        namespace = {
            'math': math,
            'sin_deg': lambda x: math.sin(math.radians(x)),
            'cos_deg': lambda x: math.cos(math.radians(x)),
            'tan_deg': lambda x: math.tan(math.radians(x)),
        }
        
        # Tambahkan fungsi wrapper ke namespace math
        math.sin_deg = namespace['sin_deg']
        math.cos_deg = namespace['cos_deg']
        math.tan_deg = namespace['tan_deg']

        return eval(expr, {"__builtins__": None}, namespace)

    def tekan_tombol(self, karakter):
        # 1. Clear Screen
        if karakter == 'C':
            self.ekspresi = ""
            self.string_var.set("0")
        
        # 2. Backspace
        elif karakter == '⌫':
            self.ekspresi = self.ekspresi[:-1]
            if not self.ekspresi:
                self.string_var.set("0")
            else:
                self.string_var.set(self.ekspresi)

        # 3. Menghitung Hasil Akhir (=)
        elif karakter == '=':
            try:
                hasil = self.hitung_ekspresi()
                
                # Pembulatan desimal halus untuk trigonometri
                if isinstance(hasil, float):
                    hasil = round(hasil, 10)
                    if hasil.is_integer():
                        hasil = int(hasil)
                
                self.string_var.set(str(hasil))
                self.ekspresi = str(hasil)
            except Exception:
                messagebox.showerror("Error", "Format Ekspresi Tidak Valid!")
                self.ekspresi = ""
                self.string_var.set("0")

        # 4. Input Fungsi dengan Kurung Buka Otomatis: sin(, cos(, tan(, log(, rad(, √(, n!(
        elif karakter in ('sin', 'cos', 'tan', 'log', 'rad', '√', 'n!'):
            if self.string_var.get() == "0":
                self.ekspresi = karakter + "("
            else:
                self.ekspresi += karakter + "("
            self.string_var.set(self.ekspresi)

        # 5. Input Angka & Operator Lainnya
        else:
            if self.string_var.get() == "0" and karakter not in ('.', '+', '-', '*', '/', '^', '%'):
                self.ekspresi = karakter
            else:
                self.ekspresi += str(karakter)
            self.string_var.set(self.ekspresi)


if __name__ == "__main__":
    root = tk.Tk()
    app = AppKalkulatorGUI(root)
    root.mainloop()