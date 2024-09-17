def result_converter(result: str) -> int:
    '''
    # Функция для конвертации количества попыток в нормальный формат
    '''
    if result:  # Проверка на пустоту
        if result == "+":  # Случай, когда решена одна задача
            return 1
        else:  # Случай, когда было потрачено >1 попытки
            result = int(result)
            return (result + 1 if result > 0 else result)  # Если не решена - выводим как есть (с минусом), иначе + 1
    return 0  # Случай, когда решения нет
