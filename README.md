# Військова Операція (Military Operation)

Цей проект реалізує інтерфейс для управління військовими операціями, використовуючи Python з бібліотеками Tkinter і tkintermapview для створення графічного інтерфейсу та відображення карти. Інтерфейс дозволяє вибирати позиції та використовувати артилерію для атаки, а також забезпечує інтерактивність з картою для отримання координат.

## Опис

Ця програма дозволяє користувачу:

1. Вибирати позиції з комбінованих списків.
2. Вибирати артилерію.
3. Вводити координати (широту та довготу) вручну або натискати на мітки на карті для автоматичного заповнення полів координат.
4. Здійснювати атаку на вибрану позицію з використанням вибраної артилерії.

## Особливості

- **Карта**: Використовується бібліотека `tkintermapview`, яка дозволяє інтерактивно працювати з картою та додавати мітки на різні точки. Користувач може натискати на карту, і координати цього місця автоматично з'являються в полях введення.
- **База даних SQLite**: Додаток підключається до бази даних SQLite для отримання інформації про артилерію та позиції.
- **Інтерфейс**: Графічний інтерфейс користувача створено за допомогою бібліотеки Tkinter, з комбінованими списками для вибору позицій та артилерії.

