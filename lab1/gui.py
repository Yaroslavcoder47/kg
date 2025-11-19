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
        
        self.prev_cmyk = [0, 0, 0, 0]
        self.prev_hsv = [0, 0, 0]
        
        style = ttk.Style()
        style.theme_use('clam') 
        style.configure("TLabel", font=("Arial", 11))
        style.configure("TButton", font=("Arial", 11, "bold"))
        style.configure("TLabelframe.Label", font=("Arial", 12, "bold"))
        
        self.color_display = tk.Label(master, text="#FFFFFF", font=("Arial", 16, "bold"), relief="sunken", borderwidth=2, height=4)
        self.color_display.pack(fill="x", padx=10, pady=10)

        self.palette_button = ttk.Button(master, text="🎨 Палитра цветов", command=self.open_color_chooser)
        self.palette_button.pack(fill="x", padx=10, pady=(0, 10))

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
            
            slider = ttk.Scale(
                frame,
                from_=0,
                to=max_values[i],
                orient="horizontal",
                variable=tk_vars[i],
                command=lambda value, var=tk_vars[i], cmd=update_cmd: self.on_slider_move(var, cmd, value)
            )
            slider.grid(row=i, column=1, sticky="ew", padx=5)
            
            entry = ttk.Entry(frame, textvariable=tk_vars[i], width=5, font=("Arial", 10))
            entry.grid(row=i, column=2, padx=(5, 0))
            
            entry.bind("<Return>", lambda e, cmd=update_cmd: self.run_update_cmd(cmd))
            entry.bind("<FocusOut>", lambda e, cmd=update_cmd: self.run_update_cmd(cmd))

        frame.columnconfigure(1, weight=1)

    def run_update_cmd(self, cmd):
        self.master.after(0, cmd) 

    def on_slider_move(self, tk_var, cmd, value):
        try:
            value_int = int(round(float(value)))
        except (TypeError, ValueError):
            return
        tk_var.set(value_int)
        self.run_update_cmd(cmd)

    def open_color_chooser(self):
        """Вызов стандартной палитры."""
        color_code = colorchooser.askcolor(title="Выберите цвет")
        if color_code and color_code[0]:
            r, g, b = color_code[0]
            self.update_color(r, g, b)

    def update_color(self, r, g, b, skip_cmyk_update=False, skip_hsv_update=False):
        if self._is_updating:
            return
        self._is_updating = True
        
        try:
            r = max(0, min(255, round(r)))
            g = max(0, min(255, round(g)))
            b = max(0, min(255, round(b)))

            if not skip_cmyk_update:
                c, m, y, k = rgb_to_cmyk(r, g, b)
            if not skip_hsv_update:
                h, s, v = rgb_to_hsv(r, g, b)
            
            self.rgb_vars[0].set(r)
            self.rgb_vars[1].set(g)
            self.rgb_vars[2].set(b)

            if not skip_cmyk_update:
                self.cmyk_vars[0].set(c)
                self.cmyk_vars[1].set(m)
                self.cmyk_vars[2].set(y)
                self.cmyk_vars[3].set(k)
                self.prev_cmyk = [c, m, y, k]

            if not skip_hsv_update:
                self.hsv_vars[0].set(h)
                self.hsv_vars[1].set(s)
                self.hsv_vars[2].set(v)
                self.prev_hsv = [h, s, v]
            
            hex_color = rgb_to_hex(r, g, b)
            self.color_display.config(background=hex_color)
            
            text_color = "white" if (r + g + b) < 382 else "black"
            self.color_display.config(text=f"{hex_color}\nRGB: ({r}, {g}, {b})", foreground=text_color)

        finally:
            self._is_updating = False

    def update_from_rgb(self):
        if self._is_updating: return
        try:
            r = self.rgb_vars[0].get()
            g = self.rgb_vars[1].get()
            b = self.rgb_vars[2].get()
            self.update_color(r, g, b)
        except tk.TclError:
            pass 

    def update_from_cmyk(self):
        if self._is_updating: return
        try:
            c = self.cmyk_vars[0].get()
            m = self.cmyk_vars[1].get()
            y = self.cmyk_vars[2].get()
            k = self.cmyk_vars[3].get()

            prev_c, prev_m, prev_y, prev_k = self.prev_cmyk
            
            c_changed = c != prev_c
            m_changed = m != prev_m
            y_changed = y != prev_y
            k_changed = k != prev_k
            corrected = False
            if prev_k == 100 and k == 100 and (c > 0 or m > 0 or y > 0):
                if (c_changed and c > 0) or (m_changed and m > 0) or (y_changed and y > 0):
                    k = 80 
                    corrected = True
                    self.cmyk_vars[3].set(k)
            
            r, g, b = cmyk_to_rgb(c, m, y, k)
            skip_cmyk = corrected or (c_changed or m_changed or y_changed or k_changed)
            self.prev_cmyk = [c, m, y, k]
            self.update_color(r, g, b, skip_cmyk_update=skip_cmyk)
        except tk.TclError:
            pass 

    def update_from_hsv(self):
        if self._is_updating: return
        try:
            h = self.hsv_vars[0].get()
            s = self.hsv_vars[1].get()
            v = self.hsv_vars[2].get()

            prev_h, prev_s, prev_v = self.prev_hsv
        
            h_changed = h != prev_h
            s_changed = s != prev_s
            v_changed = v != prev_v
            corrected = False
            if prev_v == 0 and v == 0 and (s > 0 or h > 0):
                if (h_changed and h > 0) or (s_changed and s > 0):
                    v = 100
                    corrected = True
                    self.hsv_vars[2].set(v)

            r, g, b = hsv_to_rgb(h, s, v)
            skip_hsv = corrected or (h_changed or s_changed)
            self.prev_hsv = [h, s, v]
            self.update_color(r, g, b, skip_hsv_update=skip_hsv)
        except tk.TclError:
            pass 


if __name__ == "__main__":
    root = tk.Tk()
    app = ColorConverterApp(root)
    root.mainloop()