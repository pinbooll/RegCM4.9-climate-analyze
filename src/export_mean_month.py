import netCDF4 as nc
import pandas as pd # библиотека для проведения операций над матрицами
import os
from modules import data_to_df
from modules import meaning

def meaning_main_t(dir, date, kz, radius, lat, lon, df, dir_output):
  """
  Провести усреднение данных температуры каждого дня из 30 дней и вывести в файл csv.

  Args:
  dir (str): Директория где находятся модели данных.
  date (str): Дата.
  kz (float): Высота (слой атмосферы).
  radius (int): Радиус в котором необходимо рассмотреть данные.
  lat (float): Значение широты точки отсчета.
  lon (float): Значение долготы точки отсчета.
  df (DataFrame): Датафрейм с данными из интернета.
  dir_output (str): Директория куда нужно экспортировать данные.

  Returns:
  None
  """
  output_dir = f'{dir_output}\\{date}\\Means'
  os.makedirs(output_dir, exist_ok=True)

  mean = meaning.meaning_t(date, dir, 't', kz, radius, lat, lon)

  list_opendata = []
  i = 0
  while i < len(df):
    list_opendata.append(df['T'].loc[i])
    i +=2

  mean_df = pd.DataFrame(data= mean, columns=[f'{date}'])
  mean_df['opendata'] = list_opendata
  correlation = mean_df['opendata'].corr(mean_df[f'{date}'])
  print(f"Коэффициент корреляции (температура) = {correlation}")
  mean_df.to_csv(f'{output_dir}\\mean_t_{kz}_{date}.csv', header=False, index=False, mode='w')

def meaning_main_hum(dir, date, kz, radius, lat, lon, df, dir_output):
  """
  Сформировать список усредненных значений влажности за 30 дней в указанном радиусе в указанной точке на указанной высоте.

  Args:
  date (str): Дата.
  dir (str): Директория где находятся модели данных.
  var (str): Наименование ключа в модели данных.
  kz (float): Высота (слой атмосферы).
  radius (int): Радиус в котором необходимо рассмотреть данные.
  lat (float): Значение широты точки отсчета.
  lon (float): Значение долготы точки отсчета.

  Returns:
  list: Усредненные значения.
  """
  output_dir = f'{dir_output}\\{date}\\Means'
  os.makedirs(output_dir, exist_ok=True)

  mean = meaning.meaning_hum(date, dir, 'rh', kz, radius, lat, lon)

  list_opendata = []
  i = 0
  while i < len(df):
    list_opendata.append(df['f'].loc[i])
    i +=2

  mean_df = pd.DataFrame(data= mean, columns=[f'{date}'])
  mean_df['opendata'] = list_opendata
  correlation = mean_df['opendata'].corr(mean_df[f'{date}'])
  print(f"Коэффициент корреляции (влажность) = {correlation}")
  mean_df.to_csv(f'{output_dir}\\mean_rh_{kz}_{date}.csv', header=False, index=False, mode='w')

def output_main(date_list, dir_input, dir_output, radius, lat, lon, dir_opendata):
  dataset = nc.Dataset(f'{dir_input}\\50ea__ATM.{date_list[0]}00.nc', 'r')
  df_t = data_to_df.t_to_df(dataset, 4, radius, lat, lon)
  df_rh = data_to_df.hum_to_df(dataset, 4, radius, lat, lon, 'rh')

  for date in date_list:
    df_opendata = pd.read_csv(f'{dir_opendata}', parse_dates=True, sep=';', skiprows=[0])
    df_opendata.columns = ['T', 'f', 'P', 'P0']
    df_opendata = df_opendata.dropna()
    df_opendata.reset_index(drop=True, inplace=True)
    meaning_main_t(dir_input, date, df_t.index.unique()[0], radius, lat, lon, df_opendata, dir_output)
    meaning_main_hum(dir_input, date, df_rh.index.unique()[17], radius, lat, lon, df_opendata, dir_output)