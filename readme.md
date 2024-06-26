# Сайт с аналитикой текстов группы "Король и шут"

## Цель проекта

Это pet-проект, в котором я решил совместить 2 увлечения: анализ данных и веб-программирование.


Группу "Король и шут" я выбрал, потому что слушаю её на протяжении 10 лет. 
Её творчество прочно вошло в мою жизнь. Было интересно посмотреть, как менялись
содержание песен от альбома к альбому. Насколько изменялись слова и эмоциональная 
окраска песен. 
 
Цель - сайт с визуализациями, которые показывает содержание текстов в виде облаков слов 
и их эмоциональную окраску. Также важно чтобы пользователь мог сам выбирать, 
какие года и альбому отобразить в визуализации. Это позволяет пользователю изучать творчество в динамике.

## Технологии

Для аналитики использовались следующие библиотеки:
* `pymorphy2` - приведения слов к нормальной форме
* `razdel` - токенизация текстов
* `BeautifulSoup4` - парсинг текстов с сайта [korol-i-shut.su](https://korol-i-shut.su/albums/)
* `plotly` - визуализация данных
* `dostoevsky` - эмоциональный анализ текстов


Для backend:
* `django-rest-framework` 
* `PostgreSQL`
  
frontend:
* `Vue.js` - фреймфорк для JS
* `axios` - для запросов к backend
* `Vuetife` - UI библиотека

## Результат


| ![Главная страница](https://github.com/VsevolodKozlov-git/korol-i-shut-web-drf/blob/assets/images/main.png) |
|:--:|
| Главная страница | 


| ![Меню с выбором годов и альбомов](https://github.com/VsevolodKozlov-git/korol-i-shut-web-drf/blob/assets/images/image.png) |
|:--:|
| Меню с выбором годов и альбомов | 


| ![Облако слов по выбранным альбомам](https://github.com/VsevolodKozlov-git/korol-i-shut-web-drf/blob/assets/images/image-1.png)  |
|:--:|
| Облака слов по выбранным альбомам. </br> Цвет - эмоциональная окраска слова; размер - частота употребления | 


| ![Распределение песен по эмоциональной окраске](https://github.com/VsevolodKozlov-git/korol-i-shut-web-drf/blob/assets/images/image-2.png)  |
|:--:|
| Распределение песен по эмоциональной окраске среди выбранных альбомов| 

| ![Поиск песен по запросу](https://github.com/VsevolodKozlov-git/korol-i-shut-web-drf/blob/assets/images/image-3.png) |
|:--:|
| Поиск песен по запросу | 
