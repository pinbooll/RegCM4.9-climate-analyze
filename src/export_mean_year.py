import netCDF4 as nc
import pandas as pd # библиотека для проведения операций над матрицами
import os
from modules import data_to_df
from modules import meaning

def meaning_main_t(dir, date, kz, radius, lat, lon, df):
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
  mean = meaning.meaning_t(date, dir, 't', kz, radius, lat, lon)

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
  return mean_df

def meaning_main_hum(dir, date, kz, radius, lat, lon, df):
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
  mean = meaning.meaning_hum(date, dir, 'rh', kz, radius, lat, lon)

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
  return mean_df

def output_main(date_list, dir_input, dir_output, radius, lat, lon, opendata):
  dataset = nc.Dataset(f'{dir_input}/50ea__ATM.{date_list[0]}00.nc', 'r')
  df_t = data_to_df.t_to_df(dataset, 4, radius, lat, lon)
  df_rh = data_to_df.hum_to_df(dataset, 4, radius, lat, lon, 'rh')

  result_df_t = pd.DataFrame(columns=['Model', 'OpenData'])
  result_df_rh = pd.DataFrame(columns=['Model', 'OpenData'])

  for date in date_list:
    df_opendata = pd.read_csv(f'{opendata}', parse_dates=True, sep=';', skiprows=[0])
    df_opendata.columns = ['T', 'f', 'P', 'P0']
    df_opendata = df_opendata.dropna()
    df_opendata.reset_index(drop=True, inplace=True)
    temp_t = meaning_main_t(dir_input, date, df_t.index.unique()[0], radius, lat, lon, df_opendata)
    temp_rh = meaning_main_hum(dir_input, date, df_rh.index.unique()[17], radius, lat, lon, df_opendata)
    result_df_t = pd.concat([result_df_t, temp_t], ignore_index=True)
    result_df_rh = pd.concat([result_df_rh, temp_rh], ignore_index=True)

  output_dir = f'{dir_output}\\Means'
  os.makedirs(output_dir, exist_ok=True)
  result_df_t.to_csv(f'{output_dir}\\mean_t_0_{date_list[0]}-{date_list[len(date_list)-1]}.csv', header=False, index=False, mode='w')
  result_df_rh.to_csv(f'{output_dir}\\mean_rh_0_{date_list[0]}-{date_list[len(date_list)-1]}.csv', header=False, index=False, mode='w')