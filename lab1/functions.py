# RGB -> CMYK
def rgb_to_cmyk(r : int, g : int, b : int):
    k = min(1 - r / 255.0, 1 - g / 255.0, 1 - b / 255.0)

    if k == 1: 
        return 0, 0, 0, 100

    c = (1 - r / 255 - k) / (1 - k)
    m = (1 - g / 255 - k) / (1 - k)
    y = (1 - b / 255 - k) / (1 - k)

    c = round(c * 100)
    m = round(m * 100)
    y = round(y * 100)
    k = round(k * 100)

    return c, m, y, k


# CMYK -> RGB
def cmyk_to_rgb(c : int, m : int, y : int, k : int):
    r = 255 * (1 - c / 100.0) * (1 - k / 100.0)
    g = 255 * (1 - m / 100.0) * (1 - k / 100.0)
    b = 255 * (1 - y / 100.0) * (1 - k / 100.0)

    return round(r), round(g), round(b)

# RGB -> HSV (Hue, Saturation, Value)
def rgb_to_hsv(r : int, g : int, b : int):
    r_normalize, g_normalize, b_normalize = r / 255.0, g / 255.0, b / 255.0

    c_max = max(r_normalize, g_normalize, b_normalize)
    c_min = min(r_normalize, g_normalize, b_normalize)
    delta = c_max - c_min

    if delta == 0.0:
        h = 0.0
    elif c_max == r_normalize:
        h = 60 * ((g_normalize - b_normalize) / delta % 6)
    elif c_max == g_normalize:
        h = 60 * ((b_normalize - r_normalize) / delta + 2)
    elif c_max == b_normalize:
        h = 60 * ((r_normalize - g_normalize) / delta + 4)
    
    s = 0.0 if c_max == 0 else delta / c_max

    v = c_max

    return round(h) % 360, round(s * 100), round(v * 100)

# HSV -> RGB
def hsv_to_rgb(h : int, s : int, v : int):
    h = h % 360 
    s_normalize = s / 100.0
    v_normalize = v / 100.0

    c = v_normalize * s_normalize
    
    x = c * (1 - abs((h / 60.0) % 2 - 1))
    
    m = v_normalize - c
    
    if 0 <= h < 60:
        r_prime, g_prime, b_prime = c, x, 0
    elif 60 <= h < 120:
        r_prime, g_prime, b_prime = x, c, 0
    elif 120 <= h < 180:
        r_prime, g_prime, b_prime = 0, c, x
    elif 180 <= h < 240:
        r_prime, g_prime, b_prime = 0, x, c
    elif 240 <= h < 300:
        r_prime, g_prime, b_prime = x, 0, c
    else:
        r_prime, g_prime, b_prime = c, 0, x
        
    r = (r_prime + m) * 255
    g = (g_prime + m) * 255
    b = (b_prime + m) * 255
    
    return int(round(r)), int(round(g)), int(round(b))
    

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"
    