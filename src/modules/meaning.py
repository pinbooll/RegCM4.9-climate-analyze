import netCDF4 as nc
import pandas as pd # библиотека для проведения операций над матрицами
import os
from modules import data_to_df

def meaning_t(date, dir, var, kz, radius, lat, lon):
  """
  Сформировать список усредненных значений температуры за 30 дней в указанном радиусе в указанной точке на указанной высоте.

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
  nc_file_path = os.path.join(dir, f'50ea__ATM.{date}00.nc')
  dataset = nc.Dataset(nc_file_path, 'r')
  list_mean = []
  for time in range(0, len(dataset.variables['time'])):
    df = data_to_df.t_to_df(dataset, time, radius, lat, lon)
    list_mean.append(df.loc[kz][var].mean())

  return list_mean

def meaning_hum(date, dir, var, kz, radius, lat, lon):
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
  nc_file_path = os.path.join(dir, f'50ea__ATM.{date}00.nc')
  dataset = nc.Dataset(nc_file_path, 'r')
  list_mean = []
  for time in range(0, len(dataset.variables['time'])):
    df = data_to_df.hum_to_df(dataset, time, radius, lat, lon, var)
    list_mean.append(df.loc[kz][var].mean())

  return list_mean