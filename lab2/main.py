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
   
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    
    h, s, v = cv2.split(image_hsv)
    
    v_eq = cv2.equalizeHist(v)
    
    merged_hsv = cv2.merge([h, s, v_eq])
    
    return cv2.cvtColor(merged_hsv, cv2.COLOR_HSV2BGR)



def order_statistic_filters(image, ksize=3):
    """
    Применяет медианный, минимальный и максимальный фильтры.
    ksize - размер окна (должен быть нечетным, например 3, 5, 7)
    """
    median_filtered = cv2.medianBlur(image, ksize)
    
    kernel = np.ones((ksize, ksize), np.uint8)
    min_filtered = cv2.erode(image, kernel)
    
    max_filtered = cv2.dilate(image, kernel)
    
    return median_filtered, min_filtered, max_filtered


if __name__ == "__main__":
    
    print("--- Демонстрация Задачи 1: Контрастирование ---")
    
    try:
        low_contrast_img = cv2.imread('test.jpg') 
        low_contarst_color_img = cv2.imread('test.jpg')
        if low_contrast_img is None or low_contarst_color_img is None:
            raise FileNotFoundError
    except (FileNotFoundError, NameError):
        print("Тестовое изображение не найдено.")


    gray_img = cv2.cvtColor(low_contrast_img, cv2.COLOR_BGR2GRAY)


    linear_stretched = linear_contrast_stretching(gray_img)
    print("Линейное контрастирование (серое)...")
    show_images_and_histograms(gray_img, linear_stretched, 
                               "Малоконтрастный оригинал", "Линейное контрастирование")

    histogram_equalized = histogram_equalization_grayscale(gray_img)
    print("Эквализация гистограммы (серое)...")
    show_images_and_histograms(gray_img, histogram_equalized, 
                               "Малоконтрастный оригинал", "Эквализация гистограммы")

    print("Сравнение RGB и HSV эквализации...")
    
    rgb_equalized = histogram_equalization_color_rgb(low_contarst_color_img)
    hsv_equalized = histogram_equalization_color_hsv(low_contarst_color_img)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    axes[0].imshow(cv2.cvtColor(low_contrast_img, cv2.COLOR_BGR2RGB))
    axes[0].set_title("Малоконтрастный оригинал")
    axes[0].axis('off')
    
    axes[1].imshow(cv2.cvtColor(rgb_equalized, cv2.COLOR_BGR2RGB))
    axes[1].set_title("Эквализация в RGB")
    axes[1].axis('off')
    
    axes[2].imshow(cv2.cvtColor(hsv_equalized, cv2.COLOR_BGR2RGB))
    axes[2].set_title("Эквализация в HSV")
    axes[2].axis('off')
    
    plt.tight_layout()
    plt.show()


    print("\n--- Демонстрация Задачи 2: Нелинейные фильтры ---")

    try:
        color_img_noisy = cv2.imread('noise_2.jpg')
        if color_img_noisy is None:
            raise FileNotFoundError(f"Не удалось загрузить изображение")
    except FileNotFoundError as e:
        print(f"Ошибка: {e}. Файл не найден.")

    
    base_gray_noisy = cv2.cvtColor(color_img_noisy, cv2.COLOR_BGR2GRAY)
    
    median, minimum, maximum = order_statistic_filters(base_gray_noisy, ksize=5)


    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    fig.canvas.manager.set_window_title('Демонстрация: Нелинейные фильтры')
    

    axes[0, 0].imshow(base_gray_noisy, cmap='gray')
    axes[0, 0].set_title("Оригинал с шумом (Grayscale)")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(median, cmap='gray')
    axes[0, 1].set_title("Медианный фильтр")
    axes[0, 1].axis('off')
    
    axes[1, 0].imshow(minimum, cmap='gray')
    axes[1, 0].set_title("Фильтр минимума")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(maximum, cmap='gray')
    axes[1, 1].set_title("Фильтр максимума")
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    plt.show()

    print("\nРабота завершена.")