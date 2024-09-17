import pandas as pd
from result_converter import result_converter

# Достаем файлик, удаляем столбец penalty
contest_results = pd.read_csv("standings-67848.csv").set_index('user_name')
contest_results.drop(['Penalty','place'], axis = 1, inplace=True)
students_list = pd.read_csv("students_list.csv").set_index('user_name')

# Объединяем бд
final_list = students_list.merge(contest_results, left_on='user_name', right_on='user_name', how='left')

# Обрабатываем столбец с результатами.
#final_list = final_list.fillna(0)
for task in final_list.columns.tolist()[4:]:
    final_list[task] = final_list[task].fillna(0).apply(result_converter)

# Настройка формата отображения.
pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:,.0f}'.format

# Добавляем столбец с итогами (Суммой)
final_list.loc['Total'] = final_list.sum(numeric_only=True)

# Вывод
#print(final_list[['Score']])
