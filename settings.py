import openai                                            # https://platform.openai.com/account/api-keys
import pyaudio                                           # https://platform.openai.com/docs/models/gpt-4
from vosk import Model, KaldiRecognizer
import win32com.client as wincl

openai.api_key = "token"                                                    # обязательно вставьте свой api-key !!!

adresopenfiles = 'C:\\Users\\Public\\Desktop\\'                             # адрес папки для команд открытия !

roleplayeng = "You're a gangsta rapper, always answer with rhymes!"         # роль для gpt-3.5-turbo с переводом

roleplayrus = "Отвечай всегда в стиле мастера Йоды!"                        # роль для gpt-3.5-turbo без перевода

speak = wincl.Dispatch("SAPI.SpVoice")
voices = speak.GetVoices()
for voice in voices:
    if voice.GetAttribute("Name") == "Microsoft Irina Desktop":      # Microsoft Pavel Mobile  файлы реестра в папке
        speak.Voice = voice                                          # - need install for pavel voice
        break

speakset = 4                         # скорость озвучки по-умолчанию
speakmax = 10                        # максимальная скорость:   0 - 700 символов = speakset - speakmax
speak.Volume = 100                   # громкость голоса

#                                    # будет ошибка если запускать из консоли!!      с полным адресом должно работать

#                                    #  r"F:\myprojects\Davinchi-voicetalking-main\vosk-model-small-ru-0.22"

rec = KaldiRecognizer(Model(r"vosk-model-small-ru-0.22"), 44100)
p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=44100,                      # частота дискретизации должна быть такой же, как и в системе!
    input=True,                      # звуки > запись > микрофон > свойства > дополнительно > выставляем также и выше
    frames_per_buffer=4000
)
stream.start_stream()  # https://alphacephei.com/vosk/models


def generate_gpt3_response(prompt_gpt):
    completions = openai.Completion.create(
        engine=f"text-davinci-003",                                   # моделька для одиночного вызова
        prompt=prompt_gpt,
        max_tokens=1024,  # ограничивает максимум токенов, которые могут быть использованы для завершения промпта
        n=1,  # указывает, что OpenAI должен возвратить только одно предложение для завершения предложения
        stop=None,  # модель не прекратит генерацию текста после достижения максимального количества токенов
        temperature=0.5,  # 0.1 - 1
    )
    return completions["choices"][0]["text"] if len(completions["choices"]) > 0 else None
    # Возврат ответа, если количество вариантов больше нуля.


def send_message(message_loggpt):
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
