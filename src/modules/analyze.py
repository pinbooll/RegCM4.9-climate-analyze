import numpy as np

def willmott_index(observed, modeled):
  """
  Вычисляет индекс согласия Уиллмота.
  
  :param observed: numpy.array, фактические значения
  :param modeled: numpy.array, предсказанные значения
  :return: индекс согласия
  """
  numerator = np.sum((observed - modeled) ** 2)
  denominator = np.sum((np.abs(modeled - np.mean(observed)) + np.abs(observed - np.mean(observed))) ** 2)
  return 1 - numerator / denominator

def analyze(methods, mean_df, var):
  for method in methods:
    if method == 'Корреляция':
      correlation = mean_df['OpenData'].corr(mean_df['Model'])
      print(f"Коэффициент корреляции ({var}) = {correlation}")
    if method == 'Среднеквадратичная ошибка':
      mse = np.mean((mean_df['OpenData'] - mean_df['Model']) ** 2)
      print(f"Среднеквадратичная ошибка ({var}) = {mse}")
    if method == 'Индекс согласия':
      d_index = willmott_index(mean_df['OpenData'].values, mean_df['Model'].values)
      print(f"Индекс согласия Уиллмота ({var}) = {d_index}")