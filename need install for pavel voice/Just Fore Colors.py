from colorama import init, Fore, Style, Back
import random
import keyboard

init(convert=True)

print(" + Style.BRIGHT + устанавливает яркий стиль текста (bold/bright).\n"
      " + Style.DIM + устанавливает бледный стиль текста (dim/faint).\n"
      " + Style.NORMAL + устанавливает нормальный стиль текста.\n"
      " + SStyle.RESET_ALL + сбрасывает все стили текста и возвращает их в исходное состояние.")

print(Fore.RED, "+ Fore.RED + 1234567890qwertyuiopASDFGHJKLzxcvbnm !@#$%^&№;:?_*+-=≡(){}[]<>;:'/|\\")
print(Fore.LIGHTRED_EX, "+ Fore.LIGHTRED_EX + 1234567890qwertyuiopASDFGHJKLzxcvbnm")
print(Fore.YELLOW, "+ Fore.YELLOW + 1234567890qwertyuiopASDFGHJKLzxcvbnm")
print(Fore.LIGHTYELLOW_EX, "+ Fore.LIGHTYELLOW_EX + 1234567890qwertyuiopASDFGHJKLzxcvbnm")
print(Fore.BLUE, "+ Fore.BLUE + 1234567890qwertyuiopASDFGHJKLzxcvbnm")
print(Fore.LIGHTBLUE_EX, "+ Fore.LIGHTBLUE_EX + 1234567890qwertyuiopASDFGHJKLzxcvbnm")
print(Fore.CYAN, "+ Fore.CYAN + 1234567890qwertyuiopASDFGHJKLzxcvbnm")
print(Fore.LIGHTCYAN_EX, "+ Fore.LIGHTCYAN_EX + 1234567890qwertyuiopASDFGHJKLzxcvbnm")
print(Fore.GREEN, "+ Fore.GREEN + 1234567890qwertyuiopASDFGHJKLzxcvbnm")
print(Fore.LIGHTGREEN_EX, "+ Fore.LIGHTGREEN_EX + 1234567890qwertyuiopASDFGHJKLzxcvbnm")
print(Fore.MAGENTA, "+ Fore.MAGENTA + 1234567890qwertyuiopASDFGHJKLzxcvbnm")
print(Fore.LIGHTMAGENTA_EX, "+ Fore.LIGHTMAGENTA_EX + 1234567890qwertyuiopASDFGHJKLzxcvbnm")

print(Fore.WHITE, "+ Fore.WHITE + 1234567890qwertyuiopASDFGHJKLzxcvbnm")
print(Fore.BLACK + Back.WHITE + " + Fore.BLACK + Back.WHITE + 1234567890qwertyuiopASDFGHJKLzxcvbnm")

print(Back.RED, "+ Back.RED + 1234567890qwertyuiopASDFGHJKLzxcvbnm")
print(Back.LIGHTRED_EX, "+ Back.LIGHTRED_EX + 1234567890qwertyuiopASDFGHJKLzxcvbnm")
print(Back.YELLOW, "+ Back.YELLOW + 1234567890qwertyuiopASDFGHJKLzxcvbnm")
print(Back.LIGHTYELLOW_EX, "+ Back.LIGHTYELLOW_EX + 1234567890qwertyuiopASDFGHJKLzxcvbnm")
print(Back.BLUE, "+ Back.BLUE + 1234567890qwertyuiopASDFGHJKLzxcvbnm")
print(Back.LIGHTBLUE_EX, "+ Back.LIGHTBLUE_EX + 1234567890qwertyuiopASDFGHJKLzxcvbnm")
print(Back.CYAN, "+ Back.CYAN + 1234567890qwertyuiopASDFGHJKLzxcvbnm")
print(Back.LIGHTCYAN_EX, "+ Back.LIGHTCYAN_EX + 1234567890qwertyuiopASDFGHJKLzxcvbnm")
print(Back.GREEN, "+ Back.GREEN + 1234567890qwertyuiopASDFGHJKLzxcvbnm")
print(Back.LIGHTGREEN_EX, "+ Back.LIGHTGREEN_EX + 1234567890qwertyuiopASDFGHJKLzxcvbnm")
print(Back.MAGENTA, "+ Back.MAGENTA + 1234567890qwertyuiopASDFGHJKLzxcvbnm")
print(Back.LIGHTMAGENTA_EX, "+ Back.LIGHTMAGENTA_EX + 1234567890qwertyuiopASDFGHJKLzxcvbnm" + Style.RESET_ALL)

# словарь цветов
colors = {
    'black': Fore.BLACK,
    'red': Fore.RED,
    'green': Fore.GREEN,
    'yellow': Fore.YELLOW,
    'blue': Fore.BLUE,
    'magenta': Fore.MAGENTA,
    'cyan': Fore.CYAN,
    'white': Fore.WHITE
}

# словарь фонов
backgrounds = {
    'black': Back.BLACK,
    'red': Back.RED,
    'green': Back.GREEN,
    'yellow': Back.YELLOW,
    'blue': Back.BLUE,
    'magenta': Back.MAGENTA,
    'cyan': Back.CYAN,
    'white': Back.WHITE
}

while True:
    # считываем клавишу с клавиатуры
    key = keyboard.read_event()

    # если нажата клавиша символа
    if key.event_type == 'down' and key.name.isprintable():
        # генерируем случайный цвет и фон
        color = random.choice(list(colors.values()))
        background = random.choice(list(backgrounds.values()))

        # выводим символ с соответствующим цветом и фоном
        print(color + background + key.name + Style.RESET_ALL, end='', flush=True)
    # если нажата клавиша Backspace
    # elif key.event_type == 'down' and key.name == 'backspace':
    # стираем последний символ из вывода
    # print('\b \b', end='', flush=True)
