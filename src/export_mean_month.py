import netCDF4 as nc
import pandas as pd
import os
from modules import data_to_df
from modules import meaning
from modules import analyze

def output_main(var_list, methods, dir_input, dir_output, radius, lat, lon, dir_opendata):
  """
  Вывести усредненные по времени температуру(t), давление и относительную(rh) влажность воздуха в файл csv.

  Args:
  var_list (str): Переменные для вывода
  methods (str): Методы анализа
  dir_input (str): Файл с данными модели.
  dir_output (str): Директория куда нужно экспортировать данные.
  radius (int): Радиус в котором необходимо рассмотреть данные.
  lat (float): Значение широты точки отсчета.
  lon (float): Значение долготы точки отсчета.
  dir_opendata (str): Файл с фактическими данными.

  Returns:
  None
  """
  dataset = nc.Dataset(dir_input, 'r')

  df_opendata = pd.read_csv(f'{dir_opendata}', parse_dates=True, sep=';', skiprows=[0])
  df_opendata.columns = ['T', 'f', 'P', 'P0']
  df_opendata = df_opendata.dropna()
  df_opendata.reset_index(drop=True, inplace=True)

  for var in var_list:
    if var == 't':
      df_t = data_to_df.t_to_df(dataset, 4, radius, lat, lon)
      meaning_main_t(dir_input, methods, df_t.index.unique()[0], radius, lat, lon, df_opendata, dir_output)
    if var == 'rh':
      df_rh = data_to_df.hum_to_df(dataset, 4, radius, lat, lon, 'rh')
      meaning_main_hum(dir_input, methods, df_rh.index.unique()[17], radius, lat, lon, df_opendata, dir_output)
    if var == 'ps':
      meaning_main_ps(dir_input, methods, 0, radius, lat, lon, df_opendata, dir_output)

def meaning_main_t(dir, methods, kz, radius, lat, lon, df, dir_output):
  """
  Провести усреднение данных температуры каждого дня из 30 дней и вывести в файл csv.

  Args:
  dir (str): Директория где находятся модели данных.
  methods (str): Методы анализа.
  kz (float): Высота (слой атмосферы).
  radius (int): Радиус в котором необходимо рассмотреть данные.
  lat (float): Значение широты точки отсчета.
  lon (float): Значение долготы точки отсчета.
  df (DataFrame): Датафрейм с данными из интернета.
  dir_output (str): Директория куда нужно экспортировать данные.

  Returns:
  None
  """
  output_dir = os.path.join(dir_output, 'Means')
  os.makedirs(output_dir, exist_ok=True)

  mean = meaning.meaning_t(dir, 't', kz, radius, lat, lon)

  list_opendata = []
  i = 0
  while i < len(df):
    list_opendata.append(df['T'].loc[i])
    i +=2
    
  new_list_opendata = []
  new_list_model = []
  i = 0
  while i < len(mean):
    temp_model = sum(mean[i:(i+4)])/4
    new_list_model.append(temp_model)
    temp_opendata = sum(list_opendata[i:(i+4)])/4
    new_list_opendata.append(temp_opendata)
    i +=4

  mean_df = pd.DataFrame(data= new_list_model, columns=['Model'])
  mean_df['OpenData'] = new_list_opendata

  csv_file_path = os.path.join(output_dir, f"mean_t_{kz}.csv")
  mean_df.to_csv(csv_file_path, header=False, index=False, mode='w')
  analyze.analyze(methods, mean_df, "температура")

def meaning_main_hum(dir, methods, kz, radius, lat, lon, df, dir_output):
  """
  Сформировать список усредненных значений влажности за 30 дней в указанном радиусе в указанной точке на указанной высоте.

  Args:
  dir (str): Директория где находятся модели данных.
  methods (str): Методы анализа.
  var (str): Наименование ключа в модели данных.
  kz (float): Высота (слой атмосферы).
  radius (int): Радиус в котором необходимо рассмотреть данные.
  lat (float): Значение широты точки отсчета.
  lon (float): Значение долготы точки отсчета.

  Returns:
  list: Усредненные значения.
  """
  output_dir = os.path.join(dir_output, 'Means')
  os.makedirs(output_dir, exist_ok=True)

  mean = meaning.meaning_hum(dir, 'rh', kz, radius, lat, lon)

  list_opendata = []
  i = 0
  while i < len(df):
    list_opendata.append(df['f'].loc[i])
    i +=2

  new_list_opendata = []
  new_list_model = []
  i = 0
  while i < len(mean):
    temp_model = sum(mean[i:(i+4)])/4
    new_list_model.append(temp_model)
    temp_opendata = sum(list_opendata[i:(i+4)])/4
    new_list_opendata.append(temp_opendata)
    i +=4

  mean_df = pd.DataFrame(data= new_list_model, columns=['Model'])
  mean_df['OpenData'] = new_list_opendata

  csv_file_path = os.path.join(output_dir, f"mean_rh_{kz}.csv")
  mean_df.to_csv(csv_file_path, header=False, index=False, mode='w')
  analyze.analyze(methods, mean_df, "влажность")

def meaning_main_ps(dir, methods, kz, radius, lat, lon, df, dir_output):
  """
  Провести усреднение данных давления каждого дня из 30 дней и вывести в файл csv.

  Args:
  dir (str): Директория где находятся модели данных.
  methods (str): Методы анализа.
  kz (float): Высота (слой атмосферы).
  radius (int): Радиус в котором необходимо рассмотреть данные.
  lat (float): Значение широты точки отсчета.
  lon (float): Значение долготы точки отсчета.
  df (DataFrame): Датафрейм с данными из интернета.
  dir_output (str): Директория куда нужно экспортировать данные.

  Returns:
  None
  """
  output_dir = os.path.join(dir_output, 'Means')
  os.makedirs(output_dir, exist_ok=True)

  mean = meaning.meaning_ps(dir, 'ps', kz, radius, lat, lon)

  list_opendata = []
  i = 0
  while i < len(df):
    list_opendata.append(df['P'].loc[i])
    i +=2

  new_list_opendata = []
  new_list_model = []
  i = 0
  while i < len(mean):
    temp_model = sum(mean[i:(i+4)])/4
    new_list_model.append(temp_model)
    temp_opendata = sum(list_opendata[i:(i+4)])/4
    new_list_opendata.append(temp_opendata)
    i +=4

  mean_df = pd.DataFrame(data= new_list_model, columns=['Model'])
  mean_df['OpenData'] = new_list_opendata
  
  csv_file_path = os.path.join(output_dir, f"mean_ps_{kz}.csv")
  mean_df.to_csv(csv_file_path, header=False, index=False, mode='w')
  analyze.analyze(methods, mean_df, "давление")

