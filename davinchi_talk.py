import os
import re
import time
import openai
import random
import pyaudio
import pyttsx3
import requests
import keyboard
import pyautogui
import win32com.client as wincl
from vosk import Model, KaldiRecognizer
from colorama import init, Fore, Style
from googletrans import Translator
from urllib.parse import quote

from settings import openaiapikeyset, modelset, adresopenfilesset, \
    Voiceset, speaksetmin, speaksetmax, speakVolumeset, engineset, discretset, roleplayrus, roleplayeng

translator = Translator()
init(convert=True)
tts = pyttsx3.init()
speak = wincl.Dispatch("SAPI.SpVoice")
voices = speak.GetVoices()

openai.api_key = openaiapikeyset
model = Model(modelset)
adresopenfiles = adresopenfilesset
for voice in voices:
    if voice.GetAttribute("Name") == Voiceset:
        speak.Voice = voice
        break
speakset = speaksetmin
speakmax = speaksetmax
speak.Volume = speakVolumeset
engine = engineset
discret = discretset

rec = KaldiRecognizer(model, discret)  # частота дискретизации должна быть такой же, как и в системе
p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=discret,  # звуки > запись > микрофон > свойства > дополнительно > выставляем также тут и выше
    input=True,
    frames_per_buffer=4000
)
stream.start_stream()  # https://alphacephei.com/vosk/models


def generate_gpt3_response(prompt_gpt):
    completions = openai.Completion.create(
        engine=f"{engine}",
        prompt=prompt_gpt,
        max_tokens=1024,  # ограничивает максимум токенов, которые могут быть использованы для завершения промпта
        n=1,  # указывает, что OpenAI должен возвратить только одно предложение для завершения предложения
        stop=None,  # модель не прекратит генерацию текста после достижения максимального количества токенов
        temperature=0.5,  # 0.1 - 1
    )
    return completions["choices"][0]["text"] if len(completions["choices"]) > 0 else None
    # Возврат ответа, если количество вариантов больше нуля.


def send_message(message_loggpt):
    # Отправляем сообщения в OpenAI API и получаем ответ
    responseturbo = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_loggpt,  # журнал сообщений, содержащий сообщения от пользователя и ответы ассистента
        max_tokens=2000,  # максимальное количество токенов в ответе
        stop=None,  # последовательность, которая остановит генерацию ответа
        temperature=0.7,  # параметр, определяющий "творческий" уровень генерации ответов
    )

    # Перебираем все варианты ответов из объекта response
    for choice in responseturbo.choices:
        # Если в текущем варианте есть поле "text"
        if "text" in choice:
            # Возвращаем текст этого варианта
            return choice.text

    # Если ни один вариант не содержит поля "text", то возвращаем текст первого сообщения
    return responseturbo.choices[0].message.content


colors = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN,
          Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTBLUE_EX,
          Fore.LIGHTYELLOW_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX]

print(''
      '\n'
      ' Одноразовый вызов:\n'
      '    | слушай | слышь | слышь ты | слышишь | слэш | >>>\n'
      '\n'
      ' Многоразовый вызов:\n'
      '    | начать разговор | давай поговорим | начать диалог |\n'
      '>>> | заверши(ть) разговор | конец разговор(а) | закончи(ть) разговор | обычный режим |\n'
      '\n'
      ' Многоразовый вызов без перевода:\n'
      '    | поговорим нормально | нормальный разговор | разговор по-русски |\n'
      '>>> | заверши(ть) разговор | конец разговор(а) | закончи(ть) разговор | обычный режим |\n'
      '\n'
      ' Запись в курсор:\n'
      '    | начать запись | записывать звук | запись звука | запись | запиши | включи запись | включить запись |\n'
      '>>> | конец записи | обычный режим |\n'
      '\n'
      ' запись в курсор с переводом:\n'
      '    | английский язык | запись на английском | >>> | конец записи | русский язык | обычный режим |\n'
      '\n'
      ' рисование:\n'
      '    | нарисуй | рисуй | рисования | рисунок | рисование | >>> \n'
      '\n'
      ' открытие файлов:\n'
      '    c расширением .txt :               - | блокнот + < 5 "слов" |\n'
      '    c расширением .lnk :               - | ярлык   + < 5 "слов" |\n'
      '    c расширением .lnk на английском : - | открыть + < 5 "слов" |\n'
      '    найти в строке пуска :             - | найти   + < 5 "слов" |\n'
      '    в строке пуска на английском :     - | серч    + < 5 "слов" |\n'
      '    для поиска в гугле:                - | окей гугл  + "слова" |\n'
      '\n'
      ' режим паузы:\n'
      '    | пауза | остановка | остановись | заблокировать | стоп программа | режим паузы |\n'
      '    | остановка программы | заблокировать ассистента | блокировка ассистента | >>> \n'
      '    | запуск | запусти | запустить | стартуем | я сказал стартуем | разблокировать ассистента |\n'
      '    | разблокировка | разблокировать | запуск программы | старт программа | программа запуск | обычный режим |\n'
      '\n'
      ' для экстренного отключения звука:\n'
      '    | заткнись на хрен | громкость на ноль |    ну ка тихо быстро заткнись    |\n'
      '    |   да не ари так  | да не ари ты так  | заткнись быстро | завали хлебало |\n'
      '\n'
      ' Управление компьютером:\n'
      '    | компьютер перезагрузить | компьютер выключить  | компьютер спящий режим | компьютер засни |\n'
      '    | компьютер перезагрузка  | компьютер выключение |    компьютер спячка    | компьютер спать |\n'
      )


def print_models():
    modelka = openai.Model.list()
    for modelka in modelka.data:
        print(modelka.id)


if __name__ == '__main__':
    print("start")
    while True:
        while True:
            speak.Rate = speakset
            data = stream.read(4000)
            if rec.AcceptWaveform(data):
                prompt = rec.Result()  # выдает - {   "text" : "слова" }
                # print(prompt)
                prompt = prompt[13:-2]  # вырезаем лишнее из промпта, оставляем кавычки вокруг слов
                words = prompt[1:-1].split()  # слова это символы в запросе без кавычек разделённые пробелом

                if prompt == '""':  # индикатор вывода стрима '-' значит тишина
                    print(random.choice(colors) + '-' + Style.RESET_ALL, sep='', end='')

                # Одноразовый вызов:
                elif any(word in prompt for word in ('"слушай"', '"слышь"', '"слышь ты"', '"слышишь"', '"слэш"')):
                    print(Fore.LIGHTRED_EX + '\n' + prompt + Style.RESET_ALL)
                    speak.Speak("Че надо кожаный мешок с костями!?")
                    tts.runAndWait()
                    while True:
                        data = stream.read(4000)
                        if rec.AcceptWaveform(data):
                            prompt = rec.Result()
                            prompt = prompt[14:-3]
                            if prompt != '' and len(prompt) > 7:
                                print(Fore.LIGHTYELLOW_EX + prompt + Style.RESET_ALL)
                                trans = translator.translate(prompt, dest="en")
                                print(Fore.YELLOW + trans.text + Style.RESET_ALL)
                                response = generate_gpt3_response(trans.text)
                                print(Fore.GREEN + response[2:])
                                trans = translator.translate(response, dest="ru")
                                print(Fore.LIGHTGREEN_EX + trans.text + Style.RESET_ALL)
                                if len(trans.text) <= 700:
                                    speak.rate = speakset + (speakmax - speakset) * len(trans.text) / 700
                                elif len(trans.text) > 700:
                                    speak.Rate = speakmax
                                speak.Speak(trans.text)
                                tts.runAndWait()
                                break

                # Многоразовый вызов:
                elif any(word in prompt for word in
                         ('"начать разговор"', '"давай поговорим"', '"начать диалог"')):
                    print('\nразговор начат!')
                    speak.Speak("разговор начат!")
                    tts.runAndWait()
                    playroleeng = roleplayeng
                    message_log = [{"role": "system", "content": playroleeng}]
                    while True:
                        data = stream.read(4000)
                        if rec.AcceptWaveform(data):
                            prompt = rec.Result()
                            prompt = prompt[14:-3]
                            if prompt == 'завершить разговор' or prompt == 'конец разговора' \
                                    or prompt == 'обычный режим' or prompt == 'конец разговор' \
                                    or prompt == 'заверши разговор' or prompt == 'закончи разговор' \
                                    or prompt == 'закончить разговор':
                                print('разговор завершен!')
                                speak.rate = speakset
                                speak.Speak("разговор завершен!")
                                tts.runAndWait()
                                break
                            elif prompt != '' and len(prompt) > 7:
                                print(Fore.LIGHTYELLOW_EX + prompt + Style.RESET_ALL)
                                trans = translator.translate(prompt, dest="en")
                                print(Fore.YELLOW + trans.text + Style.RESET_ALL)
                                user_input = trans.text
                                message_log.append({"role": "user", "content": user_input})
                                response = send_message(message_log)
                                message_log.append({"role": "assistant", "content": response})
                                print(Fore.GREEN + response + Style.RESET_ALL)
                                trans = translator.translate(response, dest="ru")
                                print(Fore.LIGHTGREEN_EX + trans.text + Style.RESET_ALL)
                                if len(response) <= 700:
                                    speak.rate = speakset + (speakmax - speakset) * len(response) / 700
                                elif len(response) > 700:
                                    speak.Rate = speakmax
                                speak.Speak(trans.text)
                                tts.runAndWait()

                # Многоразовый вызов без перевода:
                elif any(word in prompt for word in
                         ('"поговорим нормально"', '"нормальный разговор"', '"разговор по-русски"')):
                    print('\nразговор без перевода начат!')
                    speak.Speak("разговор начат!")
                    tts.runAndWait()
                    playrolerus = roleplayrus
                    message_log = [{"role": "system", "content": playrolerus}]
                    while True:
                        data = stream.read(4000)
                        if rec.AcceptWaveform(data):
                            prompt = rec.Result()
                            prompt = prompt[14:-3]
                            if prompt == 'завершить разговор' or prompt == 'конец разговора' \
                                    or prompt == 'обычный режим' or prompt == 'конец разговор' \
                                    or prompt == 'заверши разговор' or prompt == 'закончи разговор' \
                                    or prompt == 'закончить разговор':
                                print('разговор завершен!')
                                speak.rate = speakset
                                speak.Speak("разговор завершен!")
                                tts.runAndWait()
                                break
                            elif prompt != '' and len(prompt) > 7:
                                print(Fore.LIGHTYELLOW_EX + prompt + Style.RESET_ALL)
                                user_input = prompt
                                message_log.append({"role": "user", "content": user_input})
                                response = send_message(message_log)
                                message_log.append({"role": "assistant", "content": response})
                                print(Fore.LIGHTGREEN_EX + response + Style.RESET_ALL)
                                if len(response) <= 700:
                                    speak.rate = speakset + (speakmax - speakset) * len(response) / 700
                                elif len(response) > 700:
                                    speak.Rate = speakmax
                                speak.Speak(response)
                                tts.runAndWait()

                # Запись в курсор:
                elif prompt in ('"начать запись"', '"записывать звук"', '"запись звука"', '"запись"',
                                '"запиши"', '"включи запись"', '"включить запись"'):
                    print('*', sep='', end='')
                    print(Fore.LIGHTYELLOW_EX + '\nзаписываю звуки в текст, говори!' + Style.RESET_ALL)
                    speak.Speak("записываю звуки в текст, говори!")
                    tts.runAndWait()
                    while True:
                        data = stream.read(4000)
                        if rec.AcceptWaveform(data):
                            prompt = rec.Result()
                            prompt = prompt[14:-3]
                            if prompt != '' and prompt != 'конец записи' and prompt != 'обычный режим':
                                keyboard.write(prompt)  # запись prompt с микрофона в курсор
                            if prompt == 'конец записи' or prompt == 'обычный режим':
                                print('запись отключена!')
                                speak.Speak("запись отключена!")
                                tts.runAndWait()
                                break

                # запись в курсор с переводом:
                elif prompt == '"английский язык"' or prompt == '"запись на английском"':
                    break

                # рисование:
                elif prompt in ('"нарисуй"', '"рисуй"', '"рисования"', '"рисунок"', '"рисование"'):
                    print(Fore.LIGHTCYAN_EX + "\nчто вам в нарисовать?" + Style.RESET_ALL)
                    speak.Speak("что вам в нарисовать?")
                    tts.runAndWait()
                    while True:
                        data = stream.read(4000)
                        if rec.AcceptWaveform(data):
                            prompt = rec.Result()
                            prompt = prompt[14:-3]
                            if prompt != '':
                                print(Fore.LIGHTYELLOW_EX + f"рисую: {prompt}" + Style.RESET_ALL)
                                trans = translator.translate(prompt, dest="en")
                                print(Fore.LIGHTGREEN_EX + f"paint: {trans.text} >" + Style.RESET_ALL)
                                speak.Speak(f"рису ю! {prompt}")
                                tts.runAndWait()
                                response = openai.Image.create(
                                    # prompt=prompt, #  запрос без переводчика
                                    prompt=trans.text,
                                    n=1,
                                    size="1024x1024")
                                image_url = response['data'][0]['url']
                                response = requests.get(image_url)
                                with open(adresopenfiles + 'cat.jpg', 'wb') as f:
                                    f.write(response.content)
                                os.startfile(adresopenfiles + 'cat.jpg')
                                print(Fore.LIGHTCYAN_EX + "рисунок готов!" + Style.RESET_ALL)
                                speak.Speak("рисунок готов!")
                                tts.runAndWait()
                                break
                                # можно добавить режим другого варианта той же фотографии но смысла нет для такой мазни

                # открытие файлов:
                elif 1 < len(words) <= 5 and words[0] in ('блокнот', 'найти', 'открыть', 'ярлык', 'серч'):
                    if words[0] == 'блокнот':
                        try:
                            os.startfile(f"{adresopenfiles}{prompt[9:-1]}.txt")  # открытие файлов с расширением .txt
                            print("+\n" + prompt[9:-1] + ".txt")
                        except FileNotFoundError:
                            print("0", end="")

                    elif words[0] == 'ярлык':
                        try:
                            os.startfile(f"{adresopenfiles}{prompt[7:-1]}.lnk")  # открытие ярлыков .lnk
                            print("+\n" + prompt[7:-1] + ".lnk")
                        except FileNotFoundError:
                            print("0", end="")

                    elif words[0] == 'открыть':
                        trans = translator.translate(prompt[9:-1], dest="en")
                        try:
                            os.startfile(f"{adresopenfiles}{trans.text}.lnk")  # с переводом на английский .lnk
                            print("+\n" + trans.text + ".lnk")
                        except FileNotFoundError:
                            print("0", end="")

                    elif words[0] == 'найти':
                        prompt = prompt[7:-1]  # убираем первое слово и кавычки из принта
                        try:  # пробуем...
                            pyautogui.hotkey("winleft", "й")  # Открываем окно поиска в пуске
                            time.sleep(0.1)  # Ждем, пока окно поиска загрузится
                            keyboard.write(prompt)  # Вводим слова
                            time.sleep(0.1)  # Ждем на всякий случай
                            keyboard.press("enter")  # Нажимаем Enter
                            print("+\n" + 'найти', prompt)  # пишем в консоль запрос
                        except FileNotFoundError:  # если не получилось...
                            print("0", end="")  # пишем нолик в консоль

                    elif words[0] == 'серч':  # с переводом на английский
                        prompt = prompt[6:-1]  # или так: - prompt = prompt[len(words[0]) + 1:-1]
                        try:
                            trans = translator.translate(prompt, dest="en")
                            pyautogui.hotkey("winleft", "й")
                            time.sleep(0.1)
                            keyboard.write(trans.text)
                            time.sleep(0.1)
                            keyboard.press("enter")
                            print(Fore.LIGHTGREEN_EX + "+\n" + Style.RESET_ALL + 'серч', trans.text)
                        except FileNotFoundError:
                            print("0", end="")

                elif words[0] == 'окей' and words[1] == 'гугл':  # команда для поиска в гугле
                    if prompt == '"окей гугл"':
                        speak.Speak("что вам найти?")
                        tts.runAndWait()
                        while True:
                            data = stream.read(4000)
                            if rec.AcceptWaveform(data):
                                prompt = rec.Result()
                                prompt = prompt[14:-3]
                                if prompt != '':
                                    os.startfile(f'https://www.google.com/search?q={prompt}')
                                    url = "https://www.google.com/search?q=" + quote(prompt)
                                    print(f'\n{url}')
                                    break
                                elif prompt == '':
                                    time.sleep(5)
                                    break

                    elif prompt != '"окей гугл"':
                        prompt = prompt[11:-1]
                        try:
                            os.startfile(f'https://www.google.com/search?q={prompt}')
                            url = "https://www.google.com/search?q=" + quote(prompt)
                            print(f'\n{url}')
                        except FileNotFoundError:
                            print('0', sep='', end='')

                # режим паузы:
                elif prompt in ('"заблокировать ассистента"', '"блокировка ассистента"', '"пауза"', '"остановка"',
                                '"остановись"', '"стоп программа"', '"заблокировать"', '"остановка программы"',
                                '"режим паузы"'):
                    print("\nрежим паузы включён!")
                    speak.Speak("режим паузы включён!")
                    tts.runAndWait()
                    while True:
                        data = stream.read(4000)
                        if rec.AcceptWaveform(data):
                            prompt = rec.Result()
                            prompt = prompt[13:-2]
                            if prompt in ('"разблокировать ассистента"', '"разблокировка"', '"программа запуск"',
                                          '"запустить"', '"запусти"', '"старт программа"', '"разблокировать"',
                                          '"запуск программы"', '"запуск"', '"стартуем"', '"я сказал стартуем"',
                                          '"обычный режим"'):
                                print("\nзапускаю обычный режим!")
                                speak.Speak("запускаю обычный режим!")
                                tts.runAndWait()
                                break
                            elif prompt == '""':
                                print('.', sep='', end='')
                            elif prompt != '""':
                                print(':', sep='', end='')

                # для экстренного отключения звука:
                elif any(word in prompt[1:-1]
                         for word in ('заткнись на хрен', 'громкость на ноль', 'ну ка тихо быстро заткнись',
                                      'да не ари так', 'да не ари ты так', 'заткнись быстро', 'завали хлебало')):
                    print(prompt[1:-1])
                    pyautogui.press('volumemute')

                # Управление компьютером:
                elif prompt == '"компьютер перезагрузить"' or prompt == '"компьютер перезагрузка"':
                    os.system('shutdown /r /t 1')  # перезагрузка компа
                elif prompt == '"компьютер выключить"' or prompt == '"компьютер выключение"':
                    os.system('shutdown /s /t 1')  # выключение компа
                elif prompt == '"компьютер спящий режим"' or prompt == '"компьютер спячка"':
                    os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')  # гибернациия
                elif prompt == '"компьютер сон"' or prompt == '"компьютер спать"' or prompt == '"компьютер засни"':
                    os.system('shutdown /h')  # сон

                # управление голосом:
                elif prompt == '"альт"' or prompt == '"аль"':
                    keyboard.press("Altleft")
                elif prompt == '"пробел"':
                    keyboard.press("Space")
                elif prompt == '"бек спэйс"' or prompt == '"стереть"' or prompt == '"стирание"':
                    keyboard.press("backspace")
                elif prompt in ('"энтер"', '"эндер"', '"интер"', '"нтр"', '"строка"', '"строчка"', '"введите"'):
                    keyboard.press("enter")
                elif prompt in ('"эскейп"', '"выход"', '"выйти"'):
                    keyboard.press("Escape")
                elif prompt in ('"контрол"', '"контур"', '"контр"'):
                    keyboard.press("Control")
                elif prompt in ('"делит"', '"удали"', '"удалить"', '"удаления"', '"удали"', '"удаление"'):
                    keyboard.press("delete")
                elif prompt in ('"таб"', '"та бы"', '"тоб"', '"смена"', '"сменить"', '"поменять"'):
                    keyboard.press("tab")

                elif prompt == '"фиксация"' or prompt == '"цифры"' or prompt == '"цифра"' or prompt == '"циферки"':
                    keyboard.press("numlock")
                elif prompt in ('"капс лок"', '"большими буквами"', '"капс лак"', '"сменить регистр"', '"регистр"'):
                    keyboard.press("Caps Lock")
                elif prompt in ('"альт четыре"', '"закрыть окно"', '"закрой окно"', '"альт эф четыре"'):
                    pyautogui.hotkey('altleft', 'F4')
                elif prompt in ('"шифт альт"', '"раскладка"', '"сменить язык"', '"поменять язык"', '"смена языка"'):
                    pyautogui.hotkey('shiftleft', 'altleft')
                elif prompt in ('"альт шифт"', '"альт шрифт"', '"айд шифт"'):
                    pyautogui.hotkey('altleft', 'shiftleft')

                elif prompt in ('"лево"', '"влево"', '"лева"', '"в лево"', '"налево"'):
                    keyboard.press('left')
                elif prompt in ('"право"', '"вправо"', '"права"', '"в право"', '"направо"'):
                    keyboard.press("right")
                elif prompt in ('"верх"', '"вверх"', '"в верх"', '"в вверх"', '"наверх"'):
                    keyboard.press("up")
                elif prompt in ('"низ"', '"вниз"', '"в вниз"', '"в ввниз"', '"на вниз"'):
                    keyboard.press("down")

                elif prompt in ('"закрыть вкладку"', '"крестик"', '"минус вкладка"', '"закрой вкладку"'):
                    pyautogui.hotkey('ctrlleft', 'w')

                elif prompt in ('"вернуть"', '"верни"', '"отмени"', '"верни назад"', '"взад"', '"отмена"'):
                    pyautogui.hotkey('ctrlleft', 'z')
                elif prompt in ('"возвращение"', '"по-умолчанию"', '"туда-сюда"', '"прошлое"', '"бывшая"', '"бывшие"'):
                    pyautogui.hotkey('altleft', 'z')
                elif prompt in ('"копировать"', '"скопируй"', '"копирование"', '"альт це"', '"копия"'):
                    pyautogui.hotkey('ctrlleft', 'c')
                elif prompt in ('"вставлять"', '"вставь"', '"вставка"', '"ставка"', '"выставка"', '"вставляй"',
                                '"вставить"'):
                    pyautogui.hotkey('ctrlleft', 'v')
                elif prompt in ('"буфер"', '"буфера обмена"', '"список копий"', '"список копировании"'):
                    pyautogui.hotkey('winleft', 'v')

                elif prompt == '"поиск"' or prompt == '"астрал эф"' or prompt == '"поиск слов"' \
                        or prompt == '"контр эф"':
                    pyautogui.hotkey('ctrlleft', 'f')

                elif prompt in ('"окно влево"', '"окно налево"', '"окно лево"', '"окно лева"', '"разверни влево"',
                                '"разверни лево"', '"разверни налево"', '"разверни лева"'):
                    pyautogui.hotkey('winleft', 'Left')
                elif prompt in ('"окно вправо"', '"окно направо"', '"окно право"', '"окно права"', '"разверни вправо"',
                                '"разверни право"', '"разверни направо"', '"разверни права"'):
                    pyautogui.hotkey('winleft', 'Right')
                elif prompt in ('"развернуть"', '"развернуть окно"', '"разверни"', '"разворачивания"', '"разворот"'):
                    pyautogui.hotkey('winleft', 'Up')
                elif prompt in ('"свернуть"', '"свернуть окно"', '"сверни"', '"сворачивание"', '"свергнуть окно"'):
                    pyautogui.hotkey('winleft', 'Down')

                elif prompt in ('"альт таб"', '"аль таб"', '"альта"', '"смена окна"', '"другое окно"', '"смена окон"'):
                    pyautogui.hotkey('altleft', 'tab')
                elif prompt in ('"окна"', '"вин таб"', '"показать окна"', '"режим окон"', '"окошки"'):
                    pyautogui.hotkey('winleft', 'tab')
                elif prompt in ('"свернуть все окна"', '"свернуть все"', '"сверни все"', '"сверни все окна"'):
                    pyautogui.hotkey('winleft', 'd')
                elif prompt in ('"закрыть все окна"', '"закрыть все"', '"закрой все"', '"закрой все окна"'):
                    pyautogui.hotkey('winleft', 'Home')

                elif prompt != '""' and len(prompt) > 15:  # '≡' если символов больше 15
                    print(random.choice(colors) + '≡' + Style.RESET_ALL, sep='', end='')
                elif prompt != '""':  # '=' значит слышит слова
                    print(random.choice(colors) + '=' + Style.RESET_ALL, sep='', end='')
                else:
                    pass

        #  запись в курсор с переводом:
        print('*', sep='', end='')
        print(Fore.LIGHTGREEN_EX + '\nзаписываю текст на английском!' + Style.RESET_ALL)
        speak.Speak("записываю текст на английском!")
        tts.runAndWait()
        while True:
            data = stream.read(4000)
            if rec.AcceptWaveform(data):
                prompt = rec.Result()
                prompt = prompt[14:-3]
                if prompt != '' and prompt != 'конец записи' and prompt != 'русский язык' and prompt != 'обычный режим':
                    trans = translator.translate(prompt, dest="en")  # переводим наш голос на английский
                    keyboard.write(trans.text)
                if prompt == 'конец записи' or prompt == 'русский язык' or prompt == 'обычный режим':
                    print('обычный режим включён!')
                    speak.Speak("обычный режим включён!")
                    tts.runAndWait()
                    break
