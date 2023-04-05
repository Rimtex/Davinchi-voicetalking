# Davinchi-voicetalking

Представляю вашему вниманию голосового помощника на Python, который умеет выполнять команды и общаться с пользователем.
Он позволяет пользователям выполнить различные задачи, включая запуск приложений, поиск информации в Интернете, запись текста и другое.
Этот помощник работает с помощью голосовых команд, которые пользователи могут произносить вслух. 
Кроме того, этот голосовой помощник также может общаться с пользователями, используя синтез речи и языковую модель. 

<h2>Основные требования</h2>

https://www.python.org/

Скачать языковую модель для распознавания русской речи, закинуть папку туда же где программа. 

https://alphacephei.com/vosk/models/vosk-model-ru-0.42.zip          
легкая версия для команд вполне годится

https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip    
тяжелая распознает заметно лучше, но грузится у меня например почти 4 минуты

Обязательно нужно получить token для работы с API  

https://platform.openai.com/account/api-keys

токен надо записать в переменные openai.api_key

openai.api_key = "token"</br>    (24 строчка в файле davinchi talk.py)

engine='text-davinci-003'</br>   Менять тип используемой модели можно на(43 строчке)

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

Эти библиотеки необходимы для для работы программы. 
win + R > cmd > enter > ctrl + v 
если вставить все сразу - у вас должно установиться все по порядку, наверное.

для голоса Microsoft Pavel Mobile нужно запустить файлы реестра в папке -
need install for pavel voice и поменять его на (33 строчке)

возможно для голоса нужно будет установить
pip install Microsoft Pavel Mobile

мне еще пришлось установить 
pip install --upgrade googletrans==4.0.0-rc1

<h2>Принцип работы</h3>

проще показать чем расписывать видео будет чуть позже
