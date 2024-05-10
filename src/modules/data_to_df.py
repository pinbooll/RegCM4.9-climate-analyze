import numpy as np # библиотека для создания таблицы
import pandas as pd # библиотека для проведения операций над матрицами
from itertools import product # функция product создает все возможные комбинации элементов из итерируемых объектов.

def getclosest_ij(lats,lons,latpt,lonpt):
  """
  Найти индекс точки (x, y) по заданным ширине и долготе.

  Args:
  lats (array): Массив значений широт из исследуемой модели.
  lons (array): Массив значений долгот из исследуемой модели.
  latpt (float): Заданная широта.
  lonpt (float): Заданная долгота.

  Returns:
  shape(x, y): Координаты x и y.
  """
  # найти квадраты расстояний между всеми точками сетки
  dist_sq = (lats-latpt)**2 + (lons-lonpt)**2
  # найти индекс в 1 мерном массиве
  minindex_flattened = dist_sq.argmin()
  # найти индекс (x,y) в 2 мерном массиве и вернуть его значение
  return np.unravel_index(minindex_flattened, lats.shape)

def t_to_df(dataset, index_current_time, radius, lat, lon):
  """
  Сформировать датафрейм с данными температуры.

  Args:
  dataset (netCDF): Исходные данные модели.
  index_current_time (int): Индекс отрезка времени в массиве времен модели.

  Returns:
  DataFrame: Данные температуры в определенный момент времени.
  """
  latvals = dataset.variables['xlat'][:]
  lonvals = dataset.variables['xlon'][:]

  iy_min, ix_min = getclosest_ij(latvals, lonvals, lat, lon)
  left_border_x = ix_min - radius
  right_border_x = ix_min + radius
  left_border_y = iy_min - radius
  right_border_y = iy_min + radius

  jx = dataset.variables['jx'][left_border_x:right_border_x]
  iy = dataset.variables['iy'][left_border_y:right_border_y]
  kz = dataset.variables['kz'][:]
  ts_current = dataset.variables['ts'][index_current_time, left_border_y:right_border_y, left_border_x:right_border_x]
  t_current = dataset.variables['ta'][index_current_time, :, left_border_y:right_border_y, left_border_x:right_border_x]

  grid = [iy, jx]
  df = pd.DataFrame(np.array(list(product(*grid))), columns=['iy', 'jx'])
  df['t'] = np.ravel(ts_current) - 273
  df['kz'] = 0


  for z, index in enumerate(t_current):
    df_t = pd.DataFrame(np.array(list(product(*grid))), columns=['iy', 'jx'])
    df_t['kz'] = kz[z]
    df_t['t'] = np.ravel(t_current[z]) - 273
    df = pd.concat([df, df_t], ignore_index=True)
  df.set_index('kz', inplace=True)
  return df

def v_to_df(dataset, index_current_time, radius, lat, lon):
  """
  Сформировать поле скоростей ветра в определенный момент времени.

  Args:
  dataset (netCDF): Исходные данные модели.
  index_current_time (int): Индекс отрезка времени в массиве времен модели.

  Returns:
  DataFrame: Поле скоростей ветра в определенный момент времени.
  """
  latvals = dataset.variables['xlat'][:]
  lonvals = dataset.variables['xlon'][:]

  iy_min, ix_min = getclosest_ij(latvals, lonvals, lat, lon)
  left_border_x = ix_min - radius
  right_border_x = ix_min + radius
  left_border_y = iy_min - radius
  right_border_y = iy_min + radius

  jx = dataset.variables['jx'][left_border_x:right_border_x]
  iy = dataset.variables['iy'][left_border_y:right_border_y]
  kz = dataset.variables['kz'][:]
  u_current = dataset.variables['ua'][index_current_time, :, left_border_y:right_border_y, left_border_x:right_border_x]
  v_current = dataset.variables['va'][index_current_time, :, left_border_y:right_border_y, left_border_x:right_border_x]

  grid = [iy, jx]
  df = pd.DataFrame(np.array(list(product(*grid))), columns=['iy', 'jx'])
  df['ua'] = np.ravel(u_current[0])
  df['va'] = np.ravel(v_current[0])
  df['kz'] = kz[0]

  for z, data in enumerate(v_current.data[:]):
    if z > 0:
      df_new = pd.DataFrame(np.array(list(product(*grid))), columns=['iy', 'jx'])
      df_new['kz'] = kz[z]
      df_new['ua'] = np.ravel(u_current[z])
      df_new['va'] = np.ravel(v_current[z])
      df = pd.concat([df, df_new], ignore_index=True)

  df.set_index('kz', inplace=True)
  return df

def hum_to_df(dataset, index_current_time, radius, lat, lon, key):
  """
  Сформировать данные влажности воздуха в определенный момент времени.

  Args:
  dataset (netCDF): Исходные данные модели.
  index_current_time (int): Индекс отрезка времени в массиве времен модели.
  key (str): Наименование ключа в модели данных.

  Returns:
  DataFrame: Данные влажности воздуха в определенный момент времени.
  """
  latvals = dataset.variables['xlat'][:]
  lonvals = dataset.variables['xlon'][:]

  iy_min, ix_min = getclosest_ij(latvals, lonvals, lat, lon)
  left_border_x = ix_min - radius
  right_border_x = ix_min + radius
  left_border_y = iy_min - radius
  right_border_y = iy_min + radius

  jx = dataset.variables['jx'][left_border_x:right_border_x]
  iy = dataset.variables['iy'][left_border_y:right_border_y]
  kz = dataset.variables['kz'][:]
  hum_current = dataset.variables[f'{key}'][index_current_time, :, left_border_y:right_border_y, left_border_x:right_border_x]

  grid = [iy, jx]
  df = pd.DataFrame(np.array(list(product(*grid))), columns=['iy', 'jx'])
  df['kz'] = kz[0]
  df[f'{key}'] = np.ravel(hum_current[0])

  for z, data in enumerate(hum_current.data[:]):
    if z > 0:
      df_new = pd.DataFrame(np.array(list(product(*grid))), columns=['iy', 'jx'])
      df_new['kz'] = kz[z]
      df_new[f'{key}'] = np.ravel(hum_current[z])
      df = pd.concat([df, df_new], ignore_index=True)

  df.set_index('kz', inplace=True)
  return df

def ps_to_df(dataset, index_current_time, radius, lat, lon):
  """
  Сформировать данные давления в определенный момент времени.

  Args:
  dataset (netCDF): Исходные данные модели.
  index_current_time (int): Индекс отрезка времени в массиве времен модели.

  Returns:
  DataFrame: Данные влажности воздуха в определенный момент времени.
  """
  latvals = dataset.variables['xlat'][:]
  lonvals = dataset.variables['xlon'][:]

  iy_min, ix_min = getclosest_ij(latvals, lonvals, lat, lon)
  left_border_x = ix_min - radius
  right_border_x = ix_min + radius
  left_border_y = iy_min - radius
  right_border_y = iy_min + radius

  jx = dataset.variables['jx'][left_border_x:right_border_x]
  iy = dataset.variables['iy'][left_border_y:right_border_y]
  kz = dataset.variables['kz'][:]
  ps_current = dataset.variables['ps'][index_current_time, left_border_y:right_border_y, left_border_x:right_border_x]


  grid = [iy, jx]
  df = pd.DataFrame(np.array(list(product(*grid))), columns=['iy', 'jx'])
  df['kz'] = kz[0]
  df['ps'] = np.ravel(ps_current) * 0.01

  df.set_index('kz', inplace=True)
  return df