import netCDF4 as nc
import pandas as pd
import os
import re
from modules import data_to_df
from modules import meaning
from modules import analyze

def output_main(var_list, methods, dir_input, dir_output, radius, lat, lon, dir_opendata):
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
  result_df_t = pd.DataFrame(columns=['Model', 'OpenData'])
  result_df_rh = pd.DataFrame(columns=['Model', 'OpenData'])
  result_df_ps = pd.DataFrame(columns=['Model', 'OpenData'])

  for filename in os.listdir(dir_input):
    if filename.endswith('.nc'):
      file_dir = os.path.join(dir_input, filename)
      dataset = nc.Dataset(file_dir, 'r')

      #найти .csv файл с той же датой что и у файла .nc
      date_pattern = re.compile(r'.*\.(\d{8})\d*\.nc$')
      match = date_pattern.match(filename)
      date = match.group(1)
      csv_filename = f"{date}.csv"
      csv_filepath = os.path.join(dir_opendata, csv_filename)

      df_opendata = pd.read_csv(csv_filepath, parse_dates=True, sep=';', skiprows=[0])
      df_opendata.columns = ['T', 'f', 'P', 'P0']
      df_opendata = df_opendata.dropna()
      df_opendata.reset_index(drop=True, inplace=True)

      for var in var_list:
        if var == 't':
          df_t = data_to_df.t_to_df(dataset, 4, radius, lat, lon)
          temp_t = meaning_main_t(file_dir, df_t.index.unique()[0], radius, lat, lon, df_opendata)
          temp_df_t = pd.DataFrame({'Model': [temp_t['Model'].mean()], 'OpenData': [temp_t['OpenData'].mean()]})
          if result_df_t.empty:
            result_df_t = temp_df_t
          else:
            result_df_t = pd.concat([result_df_t, temp_df_t], ignore_index=True)
        if var == 'rh':
          df_rh = data_to_df.hum_to_df(dataset, 4, radius, lat, lon, var)
          temp_rh = meaning_main_hum(file_dir, df_rh.index.unique()[17], radius, lat, lon, df_opendata)
          temp_df_rh = pd.DataFrame({'Model': [temp_rh['Model'].mean()], 'OpenData': [temp_rh['OpenData'].mean()]})
          if result_df_rh.empty:
            result_df_rh = temp_df_rh
          else:
            result_df_rh = pd.concat([result_df_rh, temp_df_rh], ignore_index=True)
        if var == 'ps':
          temp_ps = meaning_main_ps(file_dir, 0, radius, lat, lon, df_opendata)
          temp_df_ps = pd.DataFrame({'Model': [temp_ps['Model'].mean()], 'OpenData': [temp_ps['OpenData'].mean()]})
          if result_df_ps.empty:
            result_df_ps = temp_df_ps
          else:
            result_df_ps = pd.concat([result_df_ps, temp_df_ps], ignore_index=True)
  
  output_dir = os.path.join(dir_output, 'Means')
  os.makedirs(output_dir, exist_ok=True)
  for var in var_list:
    if var == 't':
      csv_file_path_df_t = os.path.join(output_dir, f"mean_t_several.csv")
      result_df_t.to_csv(csv_file_path_df_t, header=False, index=False, mode='w')
      analyze(methods, result_df_t, "температура")
    if var == 'rh':
      csv_file_path_df_rh = os.path.join(output_dir, f"mean_rh_several.csv")
      result_df_rh.to_csv(csv_file_path_df_rh, header=False, index=False, mode='w')
      analyze(methods, result_df_rh, "влажность")
    if var == 'ps':
      csv_file_path_df_ps = os.path.join(output_dir, f"mean_ps_several.csv")
      result_df_ps.to_csv(csv_file_path_df_ps, header=False, index=False, mode='w')
      analyze(methods, result_df_ps, "давление")
        
def meaning_main_t(file_dir, kz, radius, lat, lon, df):
  mean = meaning.meaning_t(file_dir, 't', kz, radius, lat, lon)

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

def meaning_main_hum(file_dir, kz, radius, lat, lon, df):
  mean = meaning.meaning_hum(file_dir, 'rh', kz, radius, lat, lon)

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

def meaning_main_ps(file_dir, kz, radius, lat, lon, df):
  mean = meaning.meaning_ps(file_dir, 'ps', kz, radius, lat, lon)

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
  return mean_df