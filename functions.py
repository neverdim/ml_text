import csv
import re
from pymongo import MongoClient

symbols = '[;,.,\n,\s,:,-,+,(,),=,/,«,»,@,!,?,"]'

garbagelist = [
    u'спасибо',
    u'пожалуйста',
    u'добрый',
    u'день',
    u'вечер',
    u'заявка',
    u'прошу',
    u'доброе',
    u'утро',
    u'здравствуйте',
    u'необходимо',
    u'нужно'
    ]
    
def get_accuracy():
    client = MongoClient()
    db = client.ml_database
    accuracy_query = db.ml_accuracy.find_one({'item': 'accuracy'})
    return accuracy_query['value']


def split_string_new_issue(string):
    words = []
    for word in re.split(symbols, string):
        if len(word) > 0:
            words.append(word)
    return words


def csv_search_missing(file_obj):
    reader = csv.DictReader(file_obj, delimiter=',')
    for line in reader:
        if line['Категория (раздел)'] is None:
            print(line['Категория (раздел)'], line['id'], line['Текст заявки'])


def csv_dict_reader(file_obj):
    '''
    Читаю файл с помощью csv.DictReader
    '''
    reader = csv.DictReader(file_obj, delimiter=',')
    array1 = []
    for line in reader:
        array1.append(line['Категория (раздел)'])

    array2 = []
    f = open('counts.csv', 'w')
    for i in array1:
        output = str(i) + ': ' + str(array1.count(i))
        if output not in array2:
            array2.append(output)
            # print(output)
            f.write(output + '\n')


def clear_the_data(file_obj):
    with open('data_final.csv', 'w') as final:
        reader = csv.DictReader(file_obj, delimiter=',')
        for line in reader:
            writer = csv.writer(final, delimiter=',', quotechar='"')
            if len(line['Текст заявки'].split(' ')) > 2 and (
                'тестирование' not in line['Текст заявки']
                                                            ) and (
                'Тестирование' not in line['Текст заявки']
                                                                    ):
                writer.writerow([line['id'], line['Текст заявки'], line[
                    'Категория (раздел)'
                                                                        ]])

if __name__ == "__main__":
    # with open("data_test.csv") as f_obj:
        # csv_dict_reader(f_obj)
        # csv_search_missing(f_obj)
        # clear_the_data(f_obj)
    print(split_string_new_issue('Сегодня проблема с 1С, не работает база'))
