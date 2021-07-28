import random
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from database.db import *
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

repeated_list = []
answer_list = []


def bilding_list():
    """Обнавляем список."""
    # Объявляем переменные
    all_words = open("./collection_of_words/words_list.txt", 'r', encoding='cp1251')
    # Создаем список всех слов
    for line in all_words:
        if line != '':
            new_line = line.replace('\n', '')
            add_word_db(new_line)
    # Закрываем файлы
    all_words.close()


def create_new_list():
    """Создаём новый список слов."""
    try:
        # Объявляем переменные
        number_of_words = int(ui.text_new_list.text())
        clear_current_db()  # Удаляем прошлый список
        lbl_main_settings('Новый список', 40, 10, 341, 51)

        # Наполняем новый список рандомными словами
        if get_current_amount_db() is None:
            random_id = random.randrange(0, get_amount_db())
            random_word = get_word_db(random_id)
            add_into_current_list_db(get_word_db(random_word))
        else:
            while len(get_current_amount_db()) != number_of_words:
                random_id = random.randrange(0, get_amount_db())
                random_word = get_word_db(random_id)
                if get_current_wordid_db(random_word) is None:
                    add_into_current_list_db(random_word)

        # Выводим новый список на экран и сохраняем его
        current = get_current_list()
        for word in current:
            ui.list_corrent_and_add.addItem(str(
                f'{get_current_wordid_db(word)[0]}) {word}')
            )

        # "Рендрим" окно
        ui.bar_menu.hide()
        ui.bar_list.show()
        ui.btn_back_to_menu.show()
        ui.text_new_list.clear()

    # Сообщаем пользовотелю что нужно вводить цифры
    except ValueError:
        lbl_main_settings('Введите число', 1, 10, 341, 51)
        ui.text_new_list.clear()


def add_words():
    """Добавляем в список слова."""
    try:
        # Объявляем переменные
        number_to_add = int(ui.text_add_words.text())
        lbl_main_settings('Уже в списке', 40, 10, 341, 51)
        current_count = len(get_current_amount_db())
        add_list = []

        # Наполняем список добавочными словали
        while len(get_current_amount_db()) < (number_to_add + current_count):
            random_id = random.randrange(0, get_amount_db())
            random_word = get_word_db(random_id)
            if get_current_wordid_db(random_word) is None:
                add_into_current_list_db(random_word)
                add_list.append(random_word)

        # Выводим новый список на экран и добавляем его в файл
        for word in add_list:
            ui.list_corrent_and_add.addItem(str(
                f'{get_current_wordid_db(word)[0]}) {word}')
            )

        # "Рендрим" окно
        ui.bar_menu.hide()
        ui.bar_list.show()
        ui.btn_back_to_menu.show()
        ui.text_add_words.clear()

    # Сообщаем пользовотелю что нужно вводить цифры
    except ValueError:
        lbl_main_settings('Введите число', 1, 10, 341, 51)
        ui.text_add_words.clear()


def checkup_question():
    """Задаём вопрос."""
    global question, choose, number

    # Объявляем переменные
    number = random.randrange(1, len(get_current_list()) + 1)
    choose = random.randrange(0, 2)

    # Проверяем: есть ли еще слова на которые пользовотель не ответил
    if len(get_current_list()) == len(repeated_list):
        ui.lbl_question.setText(' Вы запонлили все слова, УРА!!')

    # Проверяем: если слово нет в списке уже отвеченых
    elif get_current_word_db(number) not in repeated_list:

        # Проверяем: вопрос - это номер или слово
        if choose == 0:
            ui.lbl_question.setText(f'  {get_current_word_db(number)} - номер?')
            question = number

        else:
            ui.lbl_question.setText(f'  {number} - слово?')
            question = get_current_word_db(number)

    # "Заход на повторный круг"
    else:
        checkup_question()

    # "Рендрим" окно
    ui.text_answer.clear()
    ui.bar_menu.hide()
    ui.bar_chechup.show()
    ui.btn_back_to_menu.show()
    lbl_main_settings('Проверить себя', 100, 10, 250, 51)


def checkup_compering():
    """Проверяем ответ."""
    global question, answer_list
    # Объявляем переменные
    answer = ui.text_answer.text()
    # Проверяем на пустую строку
    if answer.strip() != '':
        # С равниваем ответ с првильным вариатном
        if str(question) == str(answer):
            # Добовляем ответ в список уже отвеченных  и выводим результат
            repeated_list.append(get_current_word_db(number))
            ui.list_chechup.clear()
            answer_list.append(f'Да! {number}) - это {get_current_word_db(number)}')
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


def show_current_list():
    """Показываем существующий список слов."""
    for word in get_current_list():
        ui.list_corrent_and_add.addItem(str(
            f'{get_current_wordid_db(word)[0]}) {word}')
        )
    # "Рендрим" окно
    ui.bar_menu.hide()
    ui.bar_list.show()
    ui.btn_back_to_menu.show()
    lbl_main_settings('Текущий список', 100, 10, 250, 51)


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
ui.btn_show_corrent_list.clicked.connect(show_current_list)  # Кнопка "Показать список"
ui.btn_answer.clicked.connect(checkup_compering)  # Кнопка "Ответить" в окне проверить себя
ui.text_add_words.returnPressed.connect(add_words)  # Добавлям слова в список

# "Рендрим меню
ui.btn_back_to_menu.hide()
ui.bar_chechup.hide()
ui.bar_list.hide()
sys.exit(app.exec_())
