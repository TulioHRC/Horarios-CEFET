def convertNumToDay(numDay):
    try:
        days = {
            '2': 'segunda',
            '3': 'terça',
            '4': 'quarta',
            '5': 'quinta',
            '6': 'sexta',
        }
        return days[str(numDay)]
    except:
        return numDay

def convertDayToNum(day):
    try:
        days = {
            'segunda': '2',
            'terça': '3',
            'quarta': '4',
            'quinta': '5',
            'sexta': '6',
        }
        return days[day]
    except:
        return day

def convertNumToHour(numHour):
    try:
        hours = {
            '1': '7:00',
            '2': '7:50',
            '3': '8:40',
            '4': '9:30',
            '5': '10:40',
            '6': '11:30',
            '7': '13:00',
            '8': '13:50',
            '9': '14:40',
            '10': '15:30',
            '11': '16:40',
            '12': '17:30',
        }
        return hours[str(numHour)]
    except:
        return numHour

def convertHourToNum(Hour):
    try:
        hours = {
            '7:00': '1',
            '7:50': '2',
            '8:40': '3',
            '9:30': '4',
            '10:40': '5',
            '11:30': '6',
            '13:00': '7',
            '13:50': '8',
            '14:40': '9',
            '15:30': '10',
            '16:40': '11',
            '17:30': '12',
        }

        return hours[str(Hour)]
    except:
        return Hour
