import netCDF4 as nc
import os
from modules import data_to_df

def time_transform(time_index):
  day = 1 + (time_index // 4)
  hour = (time_index % 4) * 6
  return f"{day:02d}{hour:02d}"

# Функции отвечающие за вывод данных
def output(df, date, var, dir_output, time_index):
  """
  Вывести датафрейм в файл csv.

  Args:
  df (DataFrame): Датафрейм с данными из интернета.
  date (str): Дата.
  var (str): Наименование ключа в модели данных.
  dir_output (str): Директория куда нужно экспортировать данные.

  Returns:
  None
  """
  output_dir = f'{dir_output}\\{date}\\tvh_{time_transform(time_index)}'
  os.makedirs(output_dir, exist_ok=True)
  i = 0
  for z in df.index.unique():
    temp = df.loc[df.index == z].copy()
    temp.to_csv(f'{output_dir}\\{var}_{i}_{date}.csv', header=False, index=False)
    i += 1

def output_main(date, time_index, dir, radius, lat, lon, dir_output):
  """
  Вывести скорость ветра(uv), температуру(t), относительную(rh) и абсолютную(hus) влажности воздуха в файл csv.

  Args:
  date (str): Дата.
  time_index (int): Индекс времени в массиве времен (Например 01.01 18:00 - это индекс 3).
  dir (str): Директория где находятся модели данных.
  radius (int): Радиус в котором необходимо рассмотреть данные.
  lat (float): Значение широты точки отсчета.
  lon (float): Значение долготы точки отсчета.
  dir_output (str): Директория куда нужно экспортировать данные.

  Returns:
  None
  """
  dataset = nc.Dataset(f'{dir}\\50ea__ATM.{date}00.nc', 'r')
  df_t = data_to_df.t_to_df(dataset, time_index, radius, lat, lon)
  df_uv = data_to_df.v_to_df(dataset, time_index, radius, lat, lon)
  df_rh = data_to_df.hum_to_df(dataset, time_index, radius, lat, lon, 'rh')
  df_hus = data_to_df.hum_to_df(dataset, time_index, radius, lat, lon, 'hus')
  output(df_uv, date, 'uv', dir_output, time_index)
  output(df_t, date, 't', dir_output, time_index)
  output(df_rh, date, 'rh', dir_output, time_index)
  output(df_hus, date, 'hus', dir_output, time_index)