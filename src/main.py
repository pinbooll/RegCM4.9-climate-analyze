import export_tvh_onetime
import export_tvh_alltime
import export_mean_month
import export_mean_year
import os
import time

date_list = input("Даты через запятую в формате ГГГГММДД: ").strip()
date_list = date_list.split(", ")
dir_input = input("Путь до директории с входными данными: ").strip()
dir_output = input("Путь до директории с выходными данными: ").strip()
lat = float(input("Широта: "))
lon = float(input("Долгота: "))
radius = int(input("Радиус (при указании точки в г. Волгоград от 1 до 145): ")) # 1 = 10км

while True:
  print("\nКакие действия необходимо произвести?")
  print("1 вывести распределения температуры, влажности воздуха, скорости ветра в определенный момент времени.")
  print("2 вывести распределения температуры, влажности воздуха, скорости ветра за все время.")
  print("3 вывести усреднение температуры по месяцам.")
  print("4 вывести усреднение температуры за несколько месяцев.")
  print("0 закрыть приложение.")
  choice = input("\n")
  
  if(int(choice) == 1):
    start_time = time.time()
    #Входные параметры
    #date_list = ['20050101'] # даты, в которые проводились измерения
    #dir_input = 'C:\\Datasets' # директория где находятся данные
    #dir_output = 'C:\\Outputs' # директория куда надо сохранить данные
    #time_index = 3 # 01.01 18:00
    #lat = 44.603898 # широта
    #lon = 33.511477 # долгота
    #radius = 5 # радиус (1 = 10км)
    time_index = int(input("Момент времени (от 0 до 119): ")) # 3 - 01.01 18:00
    for date in date_list:
      export_tvh_onetime.output_main(date, time_index, dir_input, radius, lat, lon, dir_output)
    print("\nДействие выполнено успешно")
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Время выполнения: {execution_time} секунд")

  if(int(choice) == 2):
    start_time = time.time()
    print("\nПеременные, которые необходимо вывести, через запятую (t, h, rh, v)")
    print("t - температура воздуха")
    print("h - абсолютная влажность воздуха")
    print("rh - относительная влажность воздуха")
    print("v - скорость ветра")
    var_list = input()
    var_list = var_list.split(", ")
    for date in date_list:
      export_tvh_alltime.output_main(date, dir_input, radius, lat, lon, dir_output, var_list)
    print("\nДействие выполнено успешно")
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Время выполнения: {execution_time} секунд")

  if(int(choice) == 3):
    start_time = time.time()
    dir_opendata = input("Путь с именем файла данных для сравнения: ").strip()
    export_mean_month.output_main(date_list, dir_input, dir_output, radius, lat, lon, dir_opendata)
    print("\nДействие выполнено успешно")
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Время выполнения: {execution_time} секунд")

  if(int(choice) == 4):
    start_time = time.time()
    dir_opendata = input("Путь до директории с файлами данных для сравнения: ").strip()
    for root, dirs, files in os.walk(dir_opendata):
      for file in files:
          opendata = os.path.join(root, file)
          export_mean_year.output_main(date_list, dir_input, dir_output, radius, lat, lon, opendata)
    

    print("\nДействие выполнено успешно")
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Время выполнения: {execution_time} секунд")

  if(int(choice) == 0):
    exit()

