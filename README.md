# Davinchi-voicetalking

Представляю вашему вниманию примитивного голосового помощника на Python.  
Он позволяет пользователям выполнять различные задачи, включая запуск приложений, поиск информации в Интернете, запись текста и другое. Этот помощник работает с помощью голосовых команд, которые пользователи могут произносить вслух. Кроме того, этот голосовой помощник также может общаться с пользователями, используя синтез речи и языковую модель.       

<h2>Основные требования</h2>  

https://www.python.org/  

Скачать языковую модель для распознавания русской речи, закинуть папку туда же где программа.  

https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip          
легкая версия для команд вполне годится 

https://alphacephei.com/vosk/models/vosk-model-ru-0.42.zip   
тяжелая распознает заметно лучше, но грузится у меня например почти 4 минуты  
если используете тяжёлую версию нужно будет поменять адрес на (26 строчке)  

для работы из консоли нужно прописать полный путь к модели на (26 строчке) как на (28) 

Обязательно нужно получить token для работы с API   

https://platform.openai.com/account/api-keys 

токен надо записать в переменные openai.api_key 

openai.api_key = "token"</br>    (24 строчка в файле davinchi talk.py) 

engine='text-davinci-003'</br>   Менять тип используемой модели можно на (43 строчке) 

номер телефона для OpenAI я брал сдесь - https://onlinesim.io/ru  

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

мне еще пришлось установить   
pip install --upgrade googletrans==4.0.0-rc1  

для голоса Microsoft Pavel Mobile нужно запустить файлы реестра в папке -  
need install for pavel voice и поменять его на (33 строчке)  
  
возможно для голоса нужно будет установить  
pip install Microsoft Pavel Mobile  
   
<h2>Принцип работы</h3> 

все команды в файле - команды.txt   

https://www.youtube.com/watch?v=NeodPCxl3xs&t=1s&ab_channel=RimtexSE  

Данный код по сути модифицированная версия этого проекта - https://github.com/beetlea/SayChatGPT  
откуда я нагло позаимствовал и или украл код и доработал/переделал с помощью нейросетей  
т.к. в програмировании я еще нубас. не судите строго...  
