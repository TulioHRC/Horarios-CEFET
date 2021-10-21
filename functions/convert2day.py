def convertNumToDay(numDay):
    days = {
        '2': 'segunda',
        '3': 'terça',
        '4': 'quarta',
        '5': 'quinta',
        '6': 'sexta',
    }
    return days[str(numDay)]

def convertDayToNum(day):
    days = {
        'segunda': '2',
        'terça': '3',
        'quarta': '4',
        'quinta': '5',
        'sexta': '6',
    }
    return days[day]
