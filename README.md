# Davinchi-voicetalking

Представляю вашему вниманию голосового помощника на Python, который умеет выполнять команды и общаться с пользователем.
Он позволяет пользователям выполнить различные задачи, включая запуск приложений, поиск информации в Интернете, запись текста и другое.
Этот помощник работает с помощью голосовых команд, которые пользователи могут произносить вслух. 
Кроме того, этот голосовой помощник также может общаться с пользователями, используя синтез речи и языковую модель. 

<h2>Основные требования</h2>

скачать языковую модель для распознавания русской речи https://alphacephei.com/vosk/models 

https://alphacephei.com/vosk/models/vosk-model-ru-0.42.zip
https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip

Обязательно нужно получить token для работы с API - https://platform.openai.com/account/api-keys

токен надо записать в переменные openai.api_key (24 строчка в файле davinchi talk.py)

openai.api_key = "token"</br>

Менять тип используемой модели можно на(43 строчке)

engine='text-davinci-003'</br>

<h2>Необходимые зависимости</h2>

Теперь необходимо установить следующие библиотеки

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
