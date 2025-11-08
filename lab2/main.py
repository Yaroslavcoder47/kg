import cv2
import numpy as np
import matplotlib.pyplot as plt


def plot_histogram(image, title, ax):
    """Строит гистограмму для изображения"""
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    ax.plot(hist)
    ax.set_title(title)
    ax.set_xlabel("Интенсивность")
    ax.set_ylabel("Кол-во пикселей")
    ax.set_xlim([0, 256])

def show_images_and_histograms(original, processed, title_original, title_processed):
    """Отображает два изображения и их гистограммы для сравнения."""
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    axes[0, 0].imshow(original, cmap='gray')
    axes[0, 0].set_title(title_original)
    axes[0, 0].axis('off')
    
    plot_histogram(original, f'Гистограмма: {title_original}', axes[1, 0])
    
    axes[0, 1].imshow(processed, cmap='gray')
    axes[0, 1].set_title(title_processed)
    axes[0, 1].axis('off')
    
    plot_histogram(processed, f'Гистограмма: {title_processed}', axes[1, 1])
    
    plt.tight_layout()
    plt.show()

def add_salt_and_pepper_noise(image, amount=0.05):
    row, col = image.shape
    noisy_image = np.copy(image)
    
    num_salt = np.ceil(amount * image.size * 0.5)
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
    noisy_image[coords[0], coords[1]] = 255
    
    num_pepper = np.ceil(amount * image.size * 0.5)
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
    noisy_image[coords[0], coords[1]] = 0
    
    return noisy_image


def linear_contrast_stretching(image):
    """Реализует линейное контрастирование."""
    normalized_image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
    return normalized_image

def histogram_equalization_grayscale(image):
    """Реализует эквализацию гистограммы для серого изображения"""
    return cv2.equalizeHist(image)

def histogram_equalization_color_rgb(image_bgr):
    """Реализует эквализацию для цветного изображения в RGB."""
    b, g, r = cv2.split(image_bgr)
    
    b_eq = cv2.equalizeHist(b)
    g_eq = cv2.equalizeHist(g)
    r_eq = cv2.equalizeHist(r)
    
    return cv2.merge([b_eq, g_eq, r_eq])

def histogram_equalization_color_hsv(image_bgr):
    """Реализует эквализацию для цветного изображения в HSV."""
    #Конвертируем в HSV
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    
    #Разделяем на каналы H, S, V
    h, s, v = cv2.split(image_hsv)
    
    #Применяем эквализацию ТОЛЬКО к каналу яркости (V) 
    v_eq = cv2.equalizeHist(v)
    
    #Собираем каналы H, S, V_eq обратно
    merged_hsv = cv2.merge([h, s, v_eq])
    
    #Конвертируем обратно в BGR
    return cv2.cvtColor(merged_hsv, cv2.COLOR_HSV2BGR)



def order_statistic_filters(image, ksize=5):
    """
    Применяет медианный, минимальный и максимальный фильтры.
    ksize - размер окна (должен быть нечетным, например 3, 5, 7)
    """
    # 1. Медианный фильтр (Median Filter)
    median_filtered = cv2.medianBlur(image, ksize)
    
    # 2. Фильтр минимума (Min Filter / Erosion)
    kernel = np.ones((ksize, ksize), np.uint8)
    min_filtered = cv2.erode(image, kernel)
    
    # 3. Фильтр максимума (Max Filter / Dilation)
    max_filtered = cv2.dilate(image, kernel)
    
    return median_filtered, min_filtered, max_filtered

if __name__ == "__main__":
    
    print("--- Демонстрация Задачи 1: Контрастирование ---")
    
    try:
        color_img = cv2.imread('images (1).jpg') 
        if color_img is None:
            raise FileNotFoundError
    except (FileNotFoundError, NameError):
        print("Тестовое изображение не найдено. Создаю синтетическое.")
        color_img = np.zeros((400, 600, 3), dtype=np.uint8)
        cv2.rectangle(color_img, (100, 100), (500, 300), (255, 180, 100), -1)
        color_img = cv2.GaussianBlur(color_img, (101, 101), 0)

    low_contrast_img = cv2.addWeighted(color_img, 0.4, 0, 0, 50) 

    gray_img = cv2.cvtColor(low_contrast_img, cv2.COLOR_BGR2GRAY)


    linear_stretched = linear_contrast_stretching(gray_img)
    print("Показываю: Линейное контрастирование (серое)...")
    show_images_and_histograms(gray_img, linear_stretched, 
                               "Малоконтрастный оригинал", "Линейное контрастирование")

    histogram_equalized = histogram_equalization_grayscale(gray_img)
    print("Показываю: Эквализация гистограммы (серое)...")
    show_images_and_histograms(gray_img, histogram_equalized, 
                               "Малоконтрастный оригинал", "Эквализация гистограммы")

    print("Показываю: Сравнение RGB и HSV эквализации...")
    
    rgb_equalized = histogram_equalization_color_rgb(low_contrast_img)
    hsv_equalized = histogram_equalization_color_hsv(low_contrast_img)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    axes[0].imshow(cv2.cvtColor(low_contrast_img, cv2.COLOR_BGR2RGB))
    axes[0].set_title("Малоконтрастный оригинал")
    axes[0].axis('off')
    
    axes[1].imshow(cv2.cvtColor(rgb_equalized, cv2.COLOR_BGR2RGB))
    axes[1].set_title("Эквализация в RGB (плохо, цвета искажены)")
    axes[1].axis('off')
    
    axes[2].imshow(cv2.cvtColor(hsv_equalized, cv2.COLOR_BGR2RGB))
    axes[2].set_title("Эквализация в HSV (хорошо, цвета сохранены)")
    axes[2].axis('off')
    
    plt.tight_layout()
    plt.show()


    print("\n--- Демонстрация Задачи 2: Нелинейные фильтры ---")

    base_gray = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
    noisy_img = add_salt_and_pepper_noise(base_gray, amount=0.1)
    

    median, minimum, maximum = order_statistic_filters(noisy_img, ksize=5)

    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    
    axes[0, 0].imshow(noisy_img, cmap='gray')
    axes[0, 0].set_title("Оригинал с шумом")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(median, cmap='gray')
    axes[0, 1].set_title("Медианный фильтр (шум удален)")
    axes[0, 1].axis('off')
    
    axes[1, 0].imshow(minimum, cmap='gray')
    axes[1, 0].set_title("Фильтр минимума (Эрозия)")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(maximum, cmap='gray')
    axes[1, 1].set_title("Фильтр максимума (Дилатация)")
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.show()

    print("\nРабота завершена.")