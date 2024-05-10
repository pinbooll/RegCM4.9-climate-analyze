import netCDF4 as nc
import os
from modules import data_to_df

def time_transform(time_index):
  day = 1 + (time_index // 4)
  hour = (time_index % 4) * 6
  return f"{day:02d}{hour:02d}"

# Функции отвечающие за вывод данных
def output(df, var, dir_output, time_index):
  """
  Вывести датафрейм в файл csv.

  Args:
  df (DataFrame): Датафрейм с данными из интернета.
  var (str): Наименование ключа в модели данных.
  dir_output (str): Директория куда нужно экспортировать данные.

  Returns:
  None
  """
  output_dir = os.path.join(dir_output, 'alltime')
  os.makedirs(output_dir, exist_ok=True)
  i = 0
  for z in df.index.unique():
    temp = df.loc[df.index == z].copy()
    csv_file_path = os.path.join(output_dir, f"{var}_{i}_{time_transform(time_index)}.csv")
    temp.to_csv(csv_file_path, header=False, index=False)
    i += 1

def output_main(dir, radius, lat, lon, dir_output, var_list):
  """
  Вывести скорость ветра(uv), температуру(t), относительную(rh) и абсолютную(hus) влажности воздуха в файл csv.

  Args:
  dir (str): Директория где находятся модели данных.
  radius (int): Радиус в котором необходимо рассмотреть данные.
  lat (float): Значение широты точки отсчета.
  lon (float): Значение долготы точки отсчета.
  dir_output (str): Директория куда нужно экспортировать данные.

  Returns:
  None
  """
  dataset = nc.Dataset(dir, 'r')
  for var in var_list:
    if var == 't':
      for time in range(0, len(dataset.variables['time'])):
        df_t = data_to_df.t_to_df(dataset, time, radius, lat, lon)
        output(df_t, 't', dir_output, time)
    if var == 'h':
      for time in range(0, len(dataset.variables['time'])):
        df_hus = data_to_df.hum_to_df(dataset, time, radius, lat, lon, 'hus')
        output(df_hus, 'hus', dir_output, time)
    if var == 'rh':
      for time in range(0, len(dataset.variables['time'])):
        df_rh = data_to_df.hum_to_df(dataset, time, radius, lat, lon, 'rh')
        output(df_rh, 'rh', dir_output, time)
    if var == 'v':
      for time in range(0, len(dataset.variables['time'])):
        df_uv = data_to_df.v_to_df(dataset, time, radius, lat, lon)
        output(df_uv, 'uv', dir_output, time)
    if var == 'ps':
      for time in range(0, len(dataset.variables['time'])):
        df_ps = data_to_df.ps_to_df(dataset, time, radius, lat, lon)
        output(df_ps, 'ps', dir_output, time)