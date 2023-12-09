import json
import random
import time

word_dictionary = json.load(open('russian_nouns.txt',encoding='utf-8'))

class ExitGameError(Exception):
    pass
class WinError(Exception):
    pass
class LooseError(Exception):
    pass

class CheckInput:
    def check_exit(self,message):
        if message == '/exit':
            raise ExitGameError
    def check_rule_word_length(self):
        if self.length not in '456':
            self.length = input('Длина слова от 4 до 6: ')
            self.filter_word_length(self.length)


class Dictionary(CheckInput):
    def __init__(self,dictionary):
        self.dictionary = dictionary
        self.words = list(word_dictionary)
        self.length = 5

    def filter_word_length(self,length):
        if length == '/exit':
            raise ExitGameError
        self.length = length
        self.check_exit(length)
        self.check_rule_word_length()
        self.words = list(filter(lambda x: len(x)==int(self.length),self.words))

    def choose_random_word(self):
        self.w = self.words[random.randint(0,len(self.words)-1)]

    def return_definition(self,word):
        return self.dictionary[word]['definition']

class Game:
    def __init__(self,class_dictionary):
        self.class_dictionary = class_dictionary
        self.w = class_dictionary.w
        self.tries = 0
        self.guess_list = []
        self.guess = ''
        self.length = class_dictionary.length
        self.alphabet = [chr(i) for i in range(ord('а'), ord('я') + 1)]
        self.alphabet.insert(6,'ё')

    def one_try(self):
        if self.tries <=5:
            self.request_guess()
            self.tries += 1
            self.guess_list.append(self.guess)
            self.print_log()
            if self.w == self.guess:
                raise WinError
            self.one_try()

        else:
            raise LooseError

    def print_log(self):
        for guess in self.guess_list:
            print(self.log_row(guess))
        if self.tries <= 5 and self.hint:
            print(f'Доступные буквы: {self.alphabet}')

    def log_row(self,guess):
        log = guess + ' '
        for letter in range(int(self.length)):
            if guess[letter] == self.w[letter]:
                log += '+'
            elif guess[letter] in self.w:
                log += '?'
            else:
                log += '-'
                if guess[letter] in self.alphabet:
                    self.alphabet.remove(guess[letter])
        return log


    def request_guess(self):
        self.guess = input(f'\nПопытка {self.tries+1}/{6}\nВведите догадку из {self.length} букв: ')
        if self.guess == '/exit':
            raise ExitGameError
        if len(self.guess) != int(self.length):
            print('Неверное кол-во букв!')
            self.request_guess()
        elif self.guess not in self.class_dictionary.words:
            print('Я не знаю такого слова!')
            self.request_guess()

    def play_with_hint(self):
        hint = input('Играть с подсказкой доступных букв? да/нет ')
        if hint == 'да':
            self.hint = 1
        elif hint == 'нет':
            self.hint =0
        elif hint == '/exit':
            raise ExitGameError
        else:
            self.play_with_hint()

def end_game(word_dictionary):
    x = input('Сыграем еще? да/нет ')
    if x=='да':
        start_game(word_dictionary)
    elif x == 'нет':
        try:
            raise ExitGameError
        except:
            print('Спасибо за игру!')
            time.sleep(5)
    else:
        print('да или нет?')
        end_game(word_dictionary)

def start_game(word_dictionary):

    try:
        word_game = Dictionary(word_dictionary)
        word_game.filter_word_length(input('Введите длину слова, которое будет загадано (от 4 до 6): '))  # запрашиваем ввод длины слова
        word_game.choose_random_word()  # фиксируем случайное слово
        game = Game(word_game)
        game.play_with_hint()

        game.one_try()
    except WinError:
        print("Вы выиграли!")
        print(f'{game.w} - {word_dictionary[game.w]["definition"]}')
        end_game(word_dictionary)
    except LooseError:
        print(f'Вы проиграли! Слово было {game.w}')
        print(f'{game.w} - {word_dictionary[game.w]["definition"]}')
        end_game(word_dictionary)
    except ExitGameError:
        print('Спасибо за игру!')
        time.sleep(5)


print('''Правила:
Необходимо угадать слово
+  буква стоит на нужном месте
-  такой буквы нет
?  буква есть, но на другом месте

Завершить игру можно в любой момент по команде /exit\n''')

start_game(word_dictionary)








