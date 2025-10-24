import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser

from functions import cmyk_to_rgb, rgb_to_cmyk, rgb_to_hex, hsv_to_rgb, rgb_to_hsv

class ColorConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("Color Converter (RGB-CMYK-HSV)")
        master.geometry("500x700")

        self._is_updating = False

        self.rgb_vars = [tk.IntVar() for _ in range(3)]
        self.cmyk_vars = [tk.IntVar() for _ in range(4)]
        self.hsv_vars = [tk.IntVar() for _ in range(3)]

        style = ttk.Style()
        style.theme_use('clam') 
        style.configure("TLabel", font=("Arial", 11))
        style.configure("TButton", font=("Arial", 11, "bold"))
        style.configure("TLabelframe.Label", font=("Arial", 12, "bold"))

        #1. Дисплей для цвета
        self.color_display = tk.Label(master, text="#FFFFFF", font=("Arial", 16, "bold"), relief="sunken", borderwidth=2, height=4)
        self.color_display.pack(fill="x", padx=10, pady=10)

        # 2. Кнопка выбора из палитры 
        self.palette_button = ttk.Button(master, text="🎨 Палитра цветов", command=self.open_color_chooser)
        self.palette_button.pack(fill="x", padx=10, pady=(0, 10))

        # 3. Фреймы для моделей
        self.create_model_frame("RGB", ["R:", "G:", "B:"], self.rgb_vars, [255, 255, 255], self.update_from_rgb)
        self.create_model_frame("CMYK", ["C:", "M:", "Y:", "K:"], self.cmyk_vars, [100, 100, 100, 100], self.update_from_cmyk)
        self.create_model_frame("HSV", ["H:", "S:", "V:"], self.hsv_vars, [359, 100, 100], self.update_from_hsv)
        
        self.update_color(255, 0, 0)

    def create_model_frame(self, title, labels, tk_vars, max_values, update_cmd):
        """Создает секцию (LabelFrame) для одной цветовой модели."""
        frame = ttk.LabelFrame(self.master, text=title, padding=(10, 10))
        frame.pack(fill="x", padx=10, pady=5)
        
        for i, label_text in enumerate(labels):
            ttk.Label(frame, text=label_text, width=3).grid(row=i, column=0, sticky="w", padx=(0, 5))
            
            slider = ttk.Scale(frame, from_=0, to=max_values[i], orient="horizontal", variable=tk_vars[i], command=lambda e, cmd=update_cmd: cmd())
            slider.grid(row=i, column=1, sticky="ew", padx=5)
            
            entry = ttk.Entry(frame, textvariable=tk_vars[i], width=5, font=("Arial", 10))
            entry.grid(row=i, column=2, padx=(5, 0))
            entry.bind("<Return>", lambda e, cmd=update_cmd: cmd())
            entry.bind("<FocusOut>", lambda e, cmd=update_cmd: cmd())

        frame.columnconfigure(1, weight=1)

    def open_color_chooser(self):
        """Вызов стандартной палитры."""
        color_code = colorchooser.askcolor(title="Выберите цвет")
        if color_code and color_code[0]:
            r, g, b = color_code[0]
            self.update_color(r, g, b)

    def update_color(self, r, g, b):
        """
        Главная функция. Устанавливает новый цвет (RGB) обновляет gui.
        """
        if self._is_updating:
            return
        self._is_updating = True
        
        try:
            r = max(0, min(255, round(r)))
            g = max(0, min(255, round(g)))
            b = max(0, min(255, round(b)))

            c, m, y, k = rgb_to_cmyk(r, g, b)
            h, s, v = rgb_to_hsv(r, g, b)
            
            self.rgb_vars[0].set(r)
            self.rgb_vars[1].set(g)
            self.rgb_vars[2].set(b)

            self.cmyk_vars[0].set(c)
            self.cmyk_vars[1].set(m)
            self.cmyk_vars[2].set(y)
            self.cmyk_vars[3].set(k)

            self.hsv_vars[0].set(h)
            self.hsv_vars[1].set(s)
            self.hsv_vars[2].set(v)
            
            hex_color = rgb_to_hex(r, g, b)
            self.color_display.config(background=hex_color)
            
            text_color = "white" if (r + g + b) < 382 else "black"
            self.color_display.config(text=f"{hex_color}\nRGB: ({r}, {g}, {b})", foreground=text_color)

        finally:
            self._is_updating = False

    def update_from_rgb(self):
        try:
            r = self.rgb_vars[0].get()
            g = self.rgb_vars[1].get()
            b = self.rgb_vars[2].get()
            self.update_color(r, g, b)
        except tk.TclError:
            pass 

    def update_from_cmyk(self):
        if self._is_updating:
            return
        try:
            c = self.cmyk_vars[0].get()
            m = self.cmyk_vars[1].get()
            y = self.cmyk_vars[2].get()
            k = self.cmyk_vars[3].get()
            
            r, g, b = cmyk_to_rgb(c, m, y, k)
            self.update_color(r, g, b)
        except tk.TclError:
            pass

    def update_from_hsv(self):
        if self._is_updating:
            return
        try:
            h = self.hsv_vars[0].get()
            s = self.hsv_vars[1].get()
            v = self.hsv_vars[2].get()

            r, g, b = hsv_to_rgb(h, s, v)
            self.update_color(r, g, b)
        except tk.TclError:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    app = ColorConverterApp(root)
    root.mainloop()