openaiapikeyset = "token"  # обязательно вставьте свой ключ !!!  https://platform.openai.com/account/api-keys
modelset = Model(r"vosk-model-small-ru-0.22")  # будет ошибка если запускать из консоли. !!
# modelset = r"F:\myprojects\Davinchi voicetalking\vosk-model-small-ru-0.22"  # с вашим полным адресом должно работать
adresopenfilesset = 'C:\\Users\\Public\\Desktop\\'  # адрес папки для команд открытия ! #
# 'C:\\Users\\Usersname\\Desktop\\'
Voiceset = "Microsoft Irina Desktop"  # Microsoft Pavel Mobile  файлы реестра в папке -  need install for pavel voice
speaksetmin = 4  # скорость озвучки по-умолчанию
speaksetmax = 10  # регулируется пропорционально количеству символов запроса:   0 - 700  =  speaksetmin - speaksetmax
speakVolumeset = 100  # громкость голоса
engineset = 'text-davinci-003'  # моделька для одиночного вызова  # https://platform.openai.com/docs/models/gpt-4
