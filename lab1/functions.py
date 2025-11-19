# RGB -> CMYK
def rgb_to_cmyk(r : int, g : int, b : int):
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    
    k = min(1 - r / 255.0, 1 - g / 255.0, 1 - b / 255.0)

    if k >= 0.999: 
        return 0, 0, 0, 100

    if abs(1 - k) < 1e-6:
        return 0, 0, 0, 100

    c = (1 - r / 255.0 - k) / (1 - k)
    m = (1 - g / 255.0 - k) / (1 - k)
    y = (1 - b / 255.0 - k) / (1 - k)

    c = int(max(0, min(100, round(c * 100))))
    m = int(max(0, min(100, round(m * 100))))
    y = int(max(0, min(100, round(y * 100))))
    k = int(max(0, min(100, round(k * 100))))

    return c, m, y, k


# CMYK -> RGB
def cmyk_to_rgb(c : int, m : int, y : int, k : int):
    c = max(0, min(100, c))
    m = max(0, min(100, m))
    y = max(0, min(100, y))
    k = max(0, min(100, k))
    
    r = 255 * (1 - c / 100.0) * (1 - k / 100.0)
    g = 255 * (1 - m / 100.0) * (1 - k / 100.0)
    b = 255 * (1 - y / 100.0) * (1 - k / 100.0)
    
    r = int(max(0, min(255, round(r))))
    g = int(max(0, min(255, round(g))))
    b = int(max(0, min(255, round(b))))
    
    return r, g, b

# RGB -> HEX
def rgb_to_hex(r: int, g: int, b: int) -> str:
    r = int(max(0, min(255, round(r))))
    g = int(max(0, min(255, round(g))))
    b = int(max(0, min(255, round(b))))
    return f"#{r:02X}{g:02X}{b:02X}"


# RGB -> HSV
def rgb_to_hsv(r : int, g : int, b : int):
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    
    r_normalize, g_normalize, b_normalize = r / 255.0, g / 255.0, b / 255.0

    c_max = max(r_normalize, g_normalize, b_normalize)
    c_min = min(r_normalize, g_normalize, b_normalize)
    delta = c_max - c_min

    if delta == 0.0:
        h = 0.0
    elif c_max == r_normalize:
        h = 60 * ((g_normalize - b_normalize) / delta)
        if h < 0:
            h += 360
    elif c_max == g_normalize:
        h = 60 * ((b_normalize - r_normalize) / delta + 2)
    elif c_max == b_normalize:
        h = 60 * ((r_normalize - g_normalize) / delta + 4)
    else: 
        h = 0.0
    
    s = 0.0 if c_max == 0 else delta / c_max
    v = c_max

    h = int(round(h)) % 360
    s = int(max(0, min(100, round(s * 100))))
    v = int(max(0, min(100, round(v * 100))))
    
    return h, s, v

# HSV -> RGB
def hsv_to_rgb(h : int, s : int, v : int):
    h = h % 360
    s = max(0, min(100, s))
    v = max(0, min(100, v))
    
    s_normalize = s / 100.0
    v_normalize = v / 100.0

    c = v_normalize * s_normalize
    
    x = c * (1 - abs((h / 60.0) % 2 - 1))
    
    m = v_normalize - c

    r, g, b = 0.0, 0.0, 0.0
    
    h_sector = h / 60.0

    if 0 <= h_sector < 1:
        r, g, b = c, x, 0
    elif 1 <= h_sector < 2:
        r, g, b = x, c, 0
    elif 2 <= h_sector < 3:
        r, g, b = 0, c, x
    elif 3 <= h_sector < 4:
        r, g, b = 0, x, c
    elif 4 <= h_sector < 5:
        r, g, b = x, 0, c
    elif 5 <= h_sector < 6:
        r, g, b = c, 0, x
    else: 
        r, g, b = c, x, 0

    r_final = (r + m) * 255
    g_final = (g + m) * 255
    b_final = (b + m) * 255

    r_final = int(max(0, min(255, round(r_final))))
    g_final = int(max(0, min(255, round(g_final))))
    b_final = int(max(0, min(255, round(b_final))))

    return r_final, g_final, b_final