openaiapikeyset = "token"                           # обязательно вставьте свой api-key !!! 
modelset = r"vosk-model-small-ru-0.22"              # будет ошибка если запускать из консоли. !! с полным адресом должно работать 
           
adresopenfilesset = 'C:\\Users\\Public\\Desktop\\'  # адрес папки для команд открытия !   

Voiceset = "Microsoft Irina Desktop"                # Microsoft Pavel Mobile  файлы реестра в папке -  need install for pavel voice
speaksetmin = 4                                     # скорость озвучки по-умолчанию     
speaksetmax = 10                                    # максимальная скорость:   0 - 700 символов =  speaksetmin - speaksetmax
speakVolumeset = 100                                # громкость голоса
engineset = 'text-davinci-003'                      # моделька для одиночного вызова  
discretset = 44100                                  # частота дискретизации должна быть такой же, как и в системе
                                                    # звуки > запись > микрофон > свойства > дополнительно > выставляем также

roleplayeng = "You are a helpful assistant."                       # роль для gpt-3.5-turbo с переводом
roleplayrus = "Ты веселая девушка очень любишь смешить людей"      # роль для gpt-3.5-turbo без перевода

  
  
# https://platform.openai.com/account/api-keys
# https://platform.openai.com/docs/models/gpt-4

  
# пример полного адреса  
# modelset = r"F:\myprojects\Davinchi-voicetalking-main\vosk-model-small-ru-0.22" 
