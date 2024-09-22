import pandas as pd
from result_converter import result_converter

# Настройка отображения.
pd.set_option('display.max_columns', None)
pd.options.display.float_format = '{:,.0f}'.format

# Чтение файлов.
contest_file_name = 'standings-knad1.csv'
contest_results = pd.read_csv(contest_file_name).drop(columns=['Penalty', 'place'])
students_list = pd.read_csv("students_list.csv")

# Объединение данных.
final_list = students_list.merge(contest_results, on=['user_name', 'login'], how='left').set_index('user_name').fillna(0)

# Определение индексов столбцов с результатами.
res_start_ind = final_list.columns.get_loc('faculty') + 1
res_end_ind = final_list.columns.get_loc('Score')

# Обработка столбцов с результатами.
tasks = final_list.columns[res_start_ind:res_end_ind]
final_list[tasks] = final_list[tasks].map(result_converter)

# Добавляем столбец с итогами.
final_list.loc['Total'] = final_list.select_dtypes(include='number').sum()

# Привеодим значения к типу int.
final_list[final_list.columns[res_start_ind:]] = final_list[final_list.columns[res_start_ind:]].astype(int)

# Сортировка значений.
final_list.sort_values(by=['faculty', 'user_name'])

# Экспорт результата.
faculty_choosing = ['КНАД242'] # 'КНАД242', 'КНАД241', 'КНАД242', 'ВСН', 'СмолГУ'
export_result = final_list[final_list['faculty'].isin(faculty_choosing)]
export_result.to_csv('result.csv')
