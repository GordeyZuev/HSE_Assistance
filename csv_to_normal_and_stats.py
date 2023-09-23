# Считываем список группы
with open("group_list.txt", "r", encoding='utf-8') as f:
     group_list = f.read().split('\n')

# Считываем csv с результатами контеста
with open("standings-52138 (1).csv", "r", encoding='utf-8') as f:
    list = f.read().split('\n')[:-1]


# Функция для конвертации количества попыток в нормальный формат
def result_converter(result):
    if result:              # Проверка на пустоту
        if result == '+':   # Случай, когда решена одна задача
            return 1
        else:               # Случай, когда было потрачено >1 попытки
            result = int(result)
            return result + 1 if result > 0 else result         # Если не решена - выводим как есть (с минусом), иначе + 1
    return 0                # Случай, когда решения нет



normal_list = []
result = {}

for i in range(len(list)):
    line = list[i]
    normal_line = line.replace('"', '').split(',')
    normal_line.pop(-1)     # Убрал столбец Penalty
    normal_line.pop(2)      # Убрал столбец login
    normal_line.pop(0)      # Убрал столбец place

    line_size = len(normal_line)

    if i != 0:
        for j in range(1, line_size - 1):
            normal_line[j] = result_converter(normal_line[j])
        normal_line[-1] = int(normal_line[-1])

        result[normal_line[0]] = normal_line[-1]

    normal_list.append(normal_line)

for name in group_list:
    if name in result:
        pass
    else:
        result[name] = 0

result = dict(sorted(result.items()))       # Сортируем по фамилии студентов.
normal_list.sort()      # Тут сортировка работает хорошо, потому что идет по первому элементу!


for name in result:
    if name in group_list:
       print(name, '\t', result[name])





# Статистика - Пока тестирую, есть некоторые проблемы.
def contest_stats(normal_list):
    line_size = len(normal_list[0])
    solved_all_num = 0

    min_percentage = 1.0
    hardest_task = ''

    tasks_list = {'Task': ['Solved', 'Attempts', 'Percentage']}
    for i in range(1, line_size - 1):
        tasks_list[normal_list[0][i]] = [0, 0, 0]

    for i in range(1, len(normal_list) - 1):
        for j in range(1, line_size - 1):

            if normal_list[i][j] > 0:
                tasks_list[normal_list[0][j]][0] += 1

            tasks_list[normal_list[0][j]][1] += abs(normal_list[i][j])

    for i in range(1, len(normal_list) - 1):
        for j in range(1, line_size - 1):
            percentage = round(tasks_list[normal_list[0][j]][0] / tasks_list[normal_list[0][j]][1], 3)
            tasks_list[normal_list[0][j]][2] = percentage

            if min_percentage > percentage:
                min_percentage = percentage
                hardest_task = (normal_list[0][j], min_percentage)

    print()
    for task in tasks_list:
        print(f'Задача {task.replace("(", " (")}')
        print(f'Решило: {tasks_list[task][0]}, Попыток: {tasks_list[task][1]}, Процент: {tasks_list[task][2]}')
        print()
    print(f'Самая сложная - {hardest_task[0].replace("(", " (")}')
    print(f'Удачных попыток -  {hardest_task[1]}')

contest_stats(normal_list)
