# easy_meeting  
![photo_2021-10-20 12 07 05](https://user-images.githubusercontent.com/74874309/138611209-1bb05449-4635-44a0-8416-b20a639c09b9.jpeg)

Website - http://cf5c-62-192-251-83.ngrok.io/
Speach Recognitions  

В корневой директории создать папку "models"  
В нее поместить файлы находящиеся в папке models на облаке:  
https://drive.google.com/drive/folders/1Bkzutf6FJf7Qm05GEf9C6Dmd05wBzjjk?usp=sharing  

Все глоб переменные менять только в config.py (выбираем device модели там же)


Запустить в cmd:  
pip install -r requirements.txt   
streamlit run app_run.py  
  
  
Нужно исправить:   
1. Убрать кнопки выбора загруки - после выбора того или иного метода
2. Добавить спинер при выборе ютуба и загрузке файла
3. Сделать спинеры графическими 
4. Высоту окна распознанного текста сделать больше добавить скролл? (Очень неудобно смотреть текст, не говоря уже о том чтобы что то исправлять, особенно когда текст будет на 13 страниц..)
6. Видео с ютуба не качать. (очень медленно качает...) Найти способ получать ссылку сразу на аудио.  
6. Запись с микрофона сделать понятней. (Кнопка "записать" и "начать запись" - путают)    

  


