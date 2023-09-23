# Считываем список группы
with open("group_list.txt", "r", encoding='utf-8') as f:
     group_list = f.read().split('\n')

# Считываем csv с результатами контеста
with open("standings-52138 (1).csv", "r", encoding='utf-8') as f:
    list = f.read().split('\n')[:-1]


# Функция для конвертации количества попыток в нормальный формат
def result_converter(result: str) -> int:
    if result:              # Проверка на пустоту
        if result == '+':   # Случай, когда решена одна задача
            return 1
        else:               # Случай, когда было потрачено >1 попытки
            result = int(result)
            return result + 1 if result > 0 else result         # Если не решена - выводим как есть (с минусом), иначе + 1
    return 0                # Случай, когда решения нет


# Создаем переменные
normal_list = []                # Список с результатами по всем задачам
result = {}                     # 'Name': 'Solved' - Словарь для пар Имя - количество решенных

# Цикл, который обрабатывает строчку, убирая лишняя и форматируя данные
for i in range(len(list)):
    line = list[i]
    normal_line = line.replace('"', '').split(',')
    normal_line.pop(-1)     # Убрал столбец Penalty
    normal_line.pop(2)      # Убрал столбец login
    normal_line.pop(0)      # Убрал столбец place

    line_size = len(normal_line)

    if i != 0:      # Проверяем - не 0, так как normal_line[0] - имя студента
        for j in range(1, line_size - 1):
            normal_line[j] = result_converter(normal_line[j])       # Переделываем результат из строки в цифру.
        normal_line[-1] = int(normal_line[-1])                      # Для результата правила иные - просто переделываем число в integer

        result[normal_line[0]] = normal_line[-1]        # Добавляем в словарь result пару "Ученик" - "Балл"

    normal_list.append(normal_line)                     # Добавляем отформатированную строку в табличку.

for name in group_list:     # Проверяем, есть ли студент в списке группы
    if name in result:
        pass                # Студент есть Балл остается тем же
    else:
        result[name] = 0    # Студента нет -> Балл = 0

result = dict(sorted(result.items()))       # Сортируем по фамилии студентов.
#normal_list.sort()      # Тут сортировка работает хорошо, потому что идет по первому элементу!

# Выводим список студентов

print('-' * 3 + 'Results' + '-' * 3, '\n')
for name in result:
    if name in group_list:      # Проверяем, есть ли студент в группе.
       print(result[name], '\t', name)


# Статистика по контесту в целом - Тестовое.
def contest_stats(normal_list: list):
    participants_num = len(normal_list) - 1
    line_size = len(normal_list[0])
    solved_all_num = 0

    min_percentage = 1.0
    hardest_task = ''

    tasks_list = {}             # 'Task': ['Solved', 'Attempts', 'Percentage']
    for i in range(1, line_size - 1):
        tasks_list[normal_list[0][i]] = [0, 0, 0]

    for i in range(1, len(normal_list)):
        for j in range(1, line_size):
            if j < line_size - 1:
                if normal_list[i][j] > 0:
                    tasks_list[normal_list[0][j]][0] += 1

                tasks_list[normal_list[0][j]][1] += abs(normal_list[i][j])
            else:
                if j - 1 == normal_list[i][j]:
                    solved_all_num += 1


    # Добавляем долю успешных поссылок и определяем самую низкую
    for task in tasks_list:
        percentage = round(tasks_list[task][0] / tasks_list[task][1],3)
        tasks_list[task][2] = percentage

        if min_percentage > percentage:             # Поиск самой низкой доли
            min_percentage = percentage
            hardest_task = (task, min_percentage)

    # Оформление вывода
    print('\n\n', '-' * 3 + 'Main Statistics' + '-' * 3, '\n')

    print(f'Всего решали - {participants_num}')
    print(f'Решили всё - {solved_all_num}')

    print(f'\n- Самая сложная задача - {hardest_task[0].replace("(", " (")} человек.')
    print(f'Удачных попыток -  {hardest_task[1]}')

    print('\n\n', '-' * 3 + 'Task Statistics' + '-' * 3, '\n')

    for task in tasks_list:
        print(f'- Задача {task.replace("(", " (")}')
        print(f'Решило: {tasks_list[task][0]}, Попыток: {tasks_list[task][1]}, Процент: {tasks_list[task][2]}')
        print()

# Вызов функции статистики.
contest_stats(normal_list)
