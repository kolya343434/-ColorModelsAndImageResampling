# Лабораторная работа №1
# Цветовые модели и передискретизация изображений

Проект на Python, демонстрирующий работу с цветовыми моделями и алгоритмы передискретизации изображений **без использования встроенных функций изменения размера**.

## Исходное изображение

<p align="center">
  <img src="results/01_source.png" alt="Исходное изображение" width="900">
</p>

---

## Обработка цветовых моделей

### Выделение каналов RGB

<table>
  <tr>
    <td align="center"><b>Красный (R)</b></td>
    <td align="center"><b>Зелёный (G)</b></td>
    <td align="center"><b>Синий (B)</b></td>
  </tr>
  <tr>
    <td><img src="results/02_channel_r.png" width="290"></td>
    <td><img src="results/03_channel_g.png" width="290"></td>
    <td><img src="results/04_channel_b.png" width="290"></td>
  </tr>
</table>

### Преобразование RGB → HSI (компонента яркости)

<p align="center">
  <img src="results/05_intensity.png" alt="Компонента яркости (Intensity)" width="900">
</p>

### Инверсия яркости

Яркость инвертируется по формуле: `I' = 1 - I`.

<p align="center">
  <img src="results/06_inverted_intensity.png" alt="Инверсия яркости" width="900">
</p>

---

## Передискретизация изображений

Параметры по умолчанию: `M=3`, `N=2`, `K=M/N=1.5`.

### Растяжение (интерполяция) в M раз (nearest neighbor)

<p align="center">
  <img src="results/07_stretch_M3.png" alt="Растяжение" width="900">
</p>

### Сжатие (децимация) в N раз

<p align="center">
  <img src="results/08_decimate_N2.png" alt="Сжатие" width="600">
</p>

### Передискретизация в два прохода (растяжение → сжатие)

<p align="center">
  <img src="results/09_resample_2pass_K1.5_M3_N2.png" alt="Два прохода" width="900">
</p>

### Передискретизация за один проход (коэффициент K)

<p align="center">
  <img src="results/10_resample_1pass_K1.5.png" alt="Один проход" width="900">
</p>

---

## Установка и запуск

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python scripts\generate_sample_image.py
python main.py --m 3 --n 2
```

Можно указать своё изображение (только `png`/`bmp`, не `jpeg`):

```bash
python main.py --input path\to\image.png --m 3 --n 2
```

