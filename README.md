# Davinchi-voicetalking

В этом проекте я покажу как на компьютере при помощи Python3 дать возможность ChatGPT слушать вас и отвечать на вопросы без использования клавиатуры и дисплея.

<h2>Получение токенов</h2>

Для начала нужно получить token для работы с API и organiztion id. Это можно сделать на следующих страницах:

https://platform.openai.com/account/api-keys

https://platform.openai.com/account/org-settings

Ссылка на страницу с документацией

https://platform.openai.com/docs/api-reference/introduction

<h2>Дополнительные настройки</h2>

Эти значения надо записать в переменные openai.api_key и openai.organization (13 и 14 строчки в файле ChatGPT.py)

openai.organization = "organiztion id"</br>
openai.api_key = "token"</br>

Менять тип используемой модели можно здесь(38 строчка)

engine='text-davinci-003'</br>
Максимальное количество токенов (слов) в ответе(41 строка). Количество ограниченно в бесплатной версии.

<h2>Необходимые зависимости</h2>

Теперь необходимо установить следующие библиотеки
pip install openai
pip install pyaudio
pip install googletrans
pip unstall vosk
pip install pyttsx3

Эти библиотеки необходимы для распознавания речи, перевода текста в английский и обратно и для синтеза речи. В репозитарии на гитхабе уже лежит языковая модель для распознавания русской речи. Хорошо работает только в тишине.

<h2>Принцип работы</h3>

После запуска программы необходимо произнести слов "слушай". Компьютер ответит "Говори. Слушаю внимательно" и далее все произнесенные слова будут отправлены сначало в гугл переводчик, а затем уже отправлены в бота. Это сделано в целях получения более конкретного ответа от бота. Затем после получения ответа от бота данные отправляются в синтезатор речи.

Ну и результат на видео

https://youtu.be/tUXxKgZnv88






pip install colorama  
pip install keyboard  
pip install pyautogui  
pip install openai   
pip install pyaudio   
pip install vosk   
pip install pyttsx3  
pip install requests  
pip install quote  
pip install googletrans   

импорт библиотек
win + R > cmd > enter > ctrl + v 
если вставить все сразу - у вас должно установиться все по порядку, наверное.

для голоса Microsoft Pavel Mobile нужно запустить файлы реестра в папке - need install for pavel voice

возможно для голоса нужно будет установить
pip install Microsoft Pavel Mobile

мне еще пришлось установить 
pip install --upgrade googletrans==4.0.0-rc1
