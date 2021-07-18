import random
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

import database.db as db
from design import Ui_MainWindow

app = QtWidgets.QApplication(sys.argv)

MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

# Задаём переменные
question = ''
choose = -1
number = 0
words_file = []
corrent_list = {}
repeated_list = []
answer_list = []


#  Обновляем списки
def bilding_list():
    global corrent_list, words_file

    # Объявляем переменные
    a_list = open("./collection_of_words/words.txt", 'r', encoding='cp1251')
    all_words = open("./collection_of_words/words_list.txt", 'r', encoding='cp1251')
    number = 0

    # Удаляем не нужные символы и добовляем слова в существующий список
    for line in a_list:
        if line != '':
            new_line = line.replace('\n', '')
            number += 1
            new = {number: new_line}
            corrent_list.update(new)

    # Создаем список всех слов
    for line in all_words:
        if line != '':
            new_line = line.replace('\n', '')
            words_file.append(new_line)

    # Закрываем файлы
    all_words.close()
    a_list.close()


# Создаём новый список
def create_new_list():
    global new_list

    try:
        # Объявляем переменные
        number_of_words = int(ui.text_new_list.text())
        corrent_list.clear()
        new_list = []
        lbl_main_settings('Новый список', 40, 10, 341, 51)
        list_of_words = []
        count_of_words = 1

        # Удаляем прошлый список
        erase = open("./collection_of_words/words.txt", 'w', encoding='cp1251')
        erase.close()

        # Создаем список всех имеющихся слов
        for word in words_file:
            list_of_words.append(word)

        # Наполняем новый список рандомными словами
        while len(new_list) != number_of_words:
            random_word = random.randrange(0, len(list_of_words))
            if list_of_words[random_word] not in new_list:
                new_list.append(list_of_words[random_word])

        # Выводим новый список на экран и сохраняем его
        for word in new_list:
            ui.list_corrent_and_add.addItem(str(f'{count_of_words}) {word}'))
            new = {count_of_words: word}
            corrent_list.update(new)
            count_of_words += 1
            word = word + '\n'
            with open('./collection_of_words/words.txt', 'a', encoding='cp1251') as file:
                file.write(word)

        # "Рендрим" окно
        ui.bar_menu.hide()
        ui.bar_list.show()
        ui.btn_back_to_menu.show()
        ui.text_new_list.clear()

    # Сообщаем пользовотелю что нужно вводить цифры
    except ValueError:
        lbl_main_settings('Введите колличество слов', 1, 10, 341, 51)
        ui.text_new_list.clear()


# Добавляем в список слова
def add_words():
    try:

        # Объявляем переменные
        number_to_add = int(ui.text_add_words.text())
        lbl_main_settings('Уже в списке', 40, 10, 341, 51)
        a_list = open("./collection_of_words/words.txt", 'r', encoding='cp1251')
        number = 0
        corrent_count = len(corrent_list)
        add_list = []
        list_of_words = []


        # Удаляем из строки лишние символы
        for line in a_list:
            if line != '':
                new_line = line.replace('\n', '')
                number += 1
                new = {number: new_line}
                corrent_list.update(new)
        a_list.close()

        # Создаем список всех имеющихся слов
        for word in words_file:
            list_of_words.append(word)

        # Наполняем список добавочными словали
        while len(add_list) < number_to_add:
            random_word = random.randrange(1, len(list_of_words))
            if list_of_words[random_word] not in corrent_list:
                add_list.append(list_of_words[random_word])

        # Выводим новый список на экран и добавляем его в файл
        for word in add_list:
            if word != '':
                corrent_count += 1
                new = {corrent_count: word}
                corrent_list.update(new)
                with open('./collection_of_words/words.txt', 'a', encoding='cp1251') as file:
                    word = word + '\n'
                    file.write(word)
            ui.list_corrent_and_add.addItem(str(f'{corrent_count}) {word}'))

        # "Рендрим" окно
        ui.bar_menu.hide()
        ui.bar_list.show()
        ui.btn_back_to_menu.show()
        ui.text_add_words.clear()

    # Сообщаем пользовотелю что нужно вводить цифры
    except ValueError:
        lbl_main_settings('Введите колличество слов', 1, 10, 341, 51)
        ui.text_add_words.clear()


# Задаём вопрос
def checkup_question():
    global question, choose, number

    # Объявляем переменные
    number = random.randrange(1, len(corrent_list) + 1)
    choose = random.randrange(0, 2)

    # Проверяем: есть ли еще слова на которые пользовотель не ответил
    if len(corrent_list) == len(repeated_list):
        ui.lbl_question.setText(' Вы запонлили все слова, УРА!!')

    # Проверяем: если слово нет в списке уже отвеченых
    elif corrent_list[number] not in repeated_list:

        # Проверяем: вопрос - это новер или слово
        if choose == 0:
            ui.lbl_question.setText(f'  {corrent_list[number]} - номер?')
            question = number

        else:
            ui.lbl_question.setText(f'  {number} - слово?')
            question = corrent_list[number]

    # "Заход на павторный круг"
    else:
        checkup_question()

    # "Рендрим" окно
    ui.text_answer.clear()
    ui.bar_menu.hide()
    ui.bar_chechup.show()
    ui.btn_back_to_menu.show()
    lbl_main_settings('Проверить себя', 90, 10, 250, 51)


# Проверяем ответ
def checkup_compering():
    global question, answer_list

    # Объявляем переменные
    answer = ui.text_answer.text()

    # Проверяем на пустую строку
    if answer != '':

        # С равниваем ответ с првильным вариатном
        if str(question) == str(answer):

            # Добовляем ответ в список уже отвеченных  и выводим результат
            repeated_list.append(corrent_list[number])
            ui.list_chechup.clear()
            answer_list.append(f'Да! {number}) - это {corrent_list[number]}')
            answer_list.reverse()
            for line in answer_list:
                ui.list_chechup.addItem(line)
            answer_list.reverse()
            ui.text_answer.clear()

        else:

            # Выводим сообщение, о том, что ответ неверный
            ui.list_chechup.clear()
            answer_list.append(f'Нет, ответ не верный.')
            answer_list.reverse()
            for line in answer_list:
                ui.list_chechup.addItem(line)
            answer_list.reverse()
            ui.text_answer.clear()



        checkup_question()


# Показываем существующий список слов
def show_corrent_list():
    # Обновляем списки
    bilding_list()

    # Выводим список на экран
    for i in corrent_list:
        ui.list_corrent_and_add.addItem(str(f'{i}) {corrent_list[i]}'))

    # "Рендрим" окно
    ui.bar_menu.hide()
    ui.bar_list.show()
    ui.btn_back_to_menu.show()
    lbl_main_settings('Текущуй список', 90, 10, 250, 51)


# Создаём фунцию возрата в меню
def back_to_menu():

    # "Рендрим" меню
    ui.bar_list.hide()
    ui.bar_chechup.hide()
    ui.bar_menu.show()
    ui.btn_back_to_menu.hide()
    ui.list_corrent_and_add.clear()
    lbl_main_settings('Меню', 110, 10, 121, 51)


# Функция вывода сообщения и названий окон
def lbl_main_settings(lbl_name, pos_x, pos_y, size_x, size_y):
    ui.lbl_status.setText(lbl_name)
    ui.lbl_status.setGeometry(QtCore.QRect(pos_x, pos_y, size_x, size_y))
    font = QtGui.QFont()
    font.setFamily("Aharoni")
    font.setPointSize(18)
    font.setBold(True)
    font.setWeight(75)
    ui.lbl_status.setFont(font)
    ui.lbl_status.setStyleSheet("color:")
    ui.lbl_status.setAlignment(QtCore.Qt.AlignCenter)
    ui.lbl_status.setObjectName("lbl_status")


ui.btn_back_to_menu.clicked.connect(back_to_menu)  # Кнопка "Назад" - возврат в меню
ui.text_new_list.returnPressed.connect(create_new_list)  # Создание нового списка
ui.btn_checkup.clicked.connect(checkup_question)  # Кнопка "Проверить себя"
ui.btn_show_corrent_list.clicked.connect(show_corrent_list)  # Кнопка "Показать список"
ui.btn_answer.clicked.connect(checkup_compering)  # Кнопка "Ответить" в окне проверить себя
ui.text_add_words.returnPressed.connect(add_words)  # Добавлям слова в список

# "Рендрим меню
ui.btn_back_to_menu.hide()
ui.bar_chechup.hide()
ui.bar_list.hide()

bilding_list()

sys.exit(app.exec_())
