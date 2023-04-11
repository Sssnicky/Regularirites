import csv
import re
with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


def change_phones():
    pattern = r'(\+7|8)(\s*)(\(*)(\d{3})(\)|\s)' \
                  r'*(\-*)(\d{3})(\s|\-)*(\d{2})(\s|\-)*(\d{2})(\s|\()*(доб)*(\.*)(\s*)(\d+)*(\)*)'
    subst = r'+7(\4)\7-\9-\11 \13\14\16'
    for line in contacts_list:
        line[5] = re.sub(pattern, subst, f'{line[5]}')


def make_info_lists():
    for info in contacts_list:
        if ' ' in info[0]:
            fullname = info[0].split()
            if len(fullname) == 3:
                lastnames.append(fullname[0])
                firstnames.append(fullname[1])
                surnames.append(fullname[2])
            elif len(fullname) == 2:
                lastnames.append(fullname[0])
                firstnames.append(fullname[1])
        else:
            lastnames.append(info[0])
        if ' ' in info[1]:
            fullname = info[1].split()
            firstnames.append(fullname[0])
            surnames.append(fullname[1])
        elif info[1]:
            firstnames.append(info[1])
        if info[2]:
            surnames.append(info[2])
        elif info[0] == 'Лагунцов Иван':
            surnames.append('')
        organizations.append(info[3])
        positions.append(info[4])
        phones.append(info[5])
        emails.append(info[6])


def make_dict():
    data = {}
    for i in range(len(surnames)):
        if lastnames[i] not in data:
            data[lastnames[i]] = {'Фамилия': lastnames[i], 'Имя': firstnames[i], 'Отчество': surnames[i],
                                  'Организация': organizations[i],
                                  'Должность': positions[i], 'Телефон': phones[i], 'Почта': emails[i]}
        else:
            if data[lastnames[i]]['Организация'] == '':
                data[lastnames[i]]['Организация'] = organizations[i]
            if data[lastnames[i]]['Должность'] == '':
                data[lastnames[i]]['Должность'] = positions[i]
            if data[lastnames[i]]['Телефон'] == '':
                data[lastnames[i]]['Телефон'] = phones[i]
            if data[lastnames[i]]['Почта'] == '':
                data[lastnames[i]]['Почта'] = emails[i]
    return data


if __name__ == '__main__':
    with open("phonebook_raw.csv") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
        lastnames = []
        firstnames = []
        surnames = []
        organizations = []
        positions = []
        phones = []
        emails = []
        change_phones()
        make_info_lists()
        res = make_dict()
        titles = contacts_list.pop(0)
    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerow(['lastname', 'firstname', 'surname', 'organization', 'position', 'phone', 'email'])
        for k, v in res.items():
            if k != 'lastname':
                row = [v['Фамилия'], v['Имя'], v['Отчество'], v['Организация'], v['Должность'], v['Телефон'],
                       v['Почта']]
                datawriter.writerow(row)
