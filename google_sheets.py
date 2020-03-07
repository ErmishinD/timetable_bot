# pip - Windows, pip3 - Linux
# pip3 (pip) install google-api-python-client
# pip3 (pip) install oauth2client

import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

import data_base


# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'creds.json'
# ID Google Sheets документа (можно взять из его URL)
spreadsheet_id = '1YcDc6gkL3dcGvCp-72iw1qCmVtHQKR40m_b2GtQ-kVQ'

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)



def fill_db():
    # чтение данных из гугл таблицы
    data = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range='A1:N100',
        majorDimension='ROWS'
    ).execute()


    fields = data["values"]  # строки таблицы
    for pair in fields[4:]:  # проход по всем сторкам, кроме верхних 4-ех

        week_day, week_form, pair_start, pair_end = (pair[:4])

        pair_name1, form_of_pair1, teacher1, housing1, lecture_hall1 = (pair[4:9])
        sub_group1 = [pair_name1, form_of_pair1, teacher1, housing1, lecture_hall1, pair_start, pair_end,
                      week_day, week_form, "математический", 1, "6.1219-2", 1]
        
        pair_name2, form_of_pair2, teacher2, housing2, lecture_hall2 = (pair[9:14])
        sub_group2 = [pair_name2, form_of_pair2, teacher2, housing2, lecture_hall1, pair_start, pair_end,
                      week_day, week_form, "математический", 1, "6.1219-2", 2]

        data_base.Pair(*sub_group1).add_to_base()
        data_base.Pair(*sub_group2).add_to_base()

fill_db()