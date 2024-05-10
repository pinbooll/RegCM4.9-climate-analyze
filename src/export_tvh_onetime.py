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
  output_dir = os.path.join(dir_output, f"tvh_{time_transform(time_index)}")
  os.makedirs(output_dir, exist_ok=True)
  i = 0
  for z in df.index.unique():
    temp = df.loc[df.index == z].copy()
    csv_file_path = os.path.join(output_dir, f"{var}_{i}.csv")
    temp.to_csv(csv_file_path, header=False, index=False)
    i += 1

def output_main(time_index, dir, radius, lat, lon, dir_output):
  """
  Вывести скорость ветра(uv), температуру(t), давление(ps), относительную(rh) и абсолютную(hus) влажности воздуха в файл csv.

  Args:
  time_index (int): Индекс времени в массиве времен (Например 01.01 18:00 - это индекс 3).
  dir (str): Директория где находятся модели данных.
  radius (int): Радиус в котором необходимо рассмотреть данные.
  lat (float): Значение широты точки отсчета.
  lon (float): Значение долготы точки отсчета.
  dir_output (str): Директория куда нужно экспортировать данные.

  Returns:
  None
  """

  dataset = nc.Dataset(dir, 'r')
  df_t = data_to_df.t_to_df(dataset, time_index, radius, lat, lon)
  df_uv = data_to_df.v_to_df(dataset, time_index, radius, lat, lon)
  df_rh = data_to_df.hum_to_df(dataset, time_index, radius, lat, lon, 'rh')
  df_hus = data_to_df.hum_to_df(dataset, time_index, radius, lat, lon, 'hus')
  df_ps = data_to_df.ps_to_df(dataset, time_index, radius, lat, lon)
  output(df_uv, 'uv', dir_output, time_index)
  output(df_t, 't', dir_output, time_index)
  output(df_rh, 'rh', dir_output, time_index)
  output(df_hus, 'hus', dir_output, time_index)
  output(df_ps, 'ps', dir_output, time_index)