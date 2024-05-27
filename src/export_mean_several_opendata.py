import netCDF4 as nc
import pandas as pd
import os
import re
from modules import data_to_df
from modules import meaning
from modules import analyze

def output_main(methods, dir_input, dir_output, radius, lat, lon, dir_opendata):
  """
  Вывести усредненные по времени температуру(t), давление и относительную(rh) влажность воздуха в файл csv.

  Args:
  var_list (str): Переменные для вывода
  methods (str): Методы анализа
  dir_input (str): папка с файлами данных модели.
  dir_output (str): Директория куда нужно экспортировать данные.
  radius (int): Радиус в котором необходимо рассмотреть данные.
  lat (float): Значение широты точки отсчета.
  lon (float): Значение долготы точки отсчета.
  dir_opendata (str): Папка с файлами с фактическими данными.

  Returns:
  None
  """
  result_df_t = pd.DataFrame(columns=['Model'])

  for filename in os.listdir(dir_input):
    if filename.endswith('.nc'):
      file_dir = os.path.join(dir_input, filename)
      dataset = nc.Dataset(file_dir, 'r')

      df_t = data_to_df.t_to_df(dataset, 4, radius, lat, lon)
      temp_t = meaning_main_t(file_dir, df_t.index.unique()[0], radius, lat, lon)
      temp_df_t = pd.DataFrame({'Model': [temp_t['Model'].mean()]})
      if result_df_t.empty:
        result_df_t = temp_df_t
      else:
        result_df_t = pd.concat([result_df_t, temp_df_t], ignore_index=True)
  
  df_opendata = pd.read_csv(dir_opendata, parse_dates=True, sep=';')
  df_opendata.columns = ['T']
  df_opendata = df_opendata.dropna()
  df_opendata.reset_index(drop=True, inplace=True)
  result_df_t['OpenData'] = df_opendata
  print(result_df_t)

  output_dir = os.path.join(dir_output, 'Means')
  os.makedirs(output_dir, exist_ok=True)
  csv_file_path_df_t = os.path.join(output_dir, f"mean_t_several.csv")
  result_df_t.to_csv(csv_file_path_df_t, header=False, index=False, mode='w')
  analyze.analyze(methods, result_df_t, "температура")
        
def meaning_main_t(file_dir, kz, radius, lat, lon):
  mean = meaning.meaning_t(file_dir, 't', kz, radius, lat, lon)

  new_list_model = []
  i = 0
  while i < len(mean):
    temp_model = sum(mean[i:(i+4)])/4
    new_list_model.append(temp_model)
    i +=4

  mean_df = pd.DataFrame(data= new_list_model, columns=['Model'])
  return mean_df