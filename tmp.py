from datetime import date


d = date.today()
start_year = d.year - 5
start_day = d.day
start_month = d.month
num_days = {
    1: 31,
    2: 28,  # can be 29
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
    }
dates = []
for year in range(start_year, d.year+1):
    if year % 4 == 0:
        num_days[2] = 29
    else:
        num_days[2] = 28
    for month in range(start_month, 13):
        for day in range(start_day, num_days[month]+1):
            print(f'{day}.{month}.{year}')
                # dates.append(f'{day}.{month}.{year}')
        start_day = 1
    start_month = 1
