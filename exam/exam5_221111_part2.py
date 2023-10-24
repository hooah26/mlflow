import pandas as pd
import numpy as np


'''
데이터셋(basic1.csv)의 앞에서 순서대로 70% 데이터만 활용해서,
'f1'컬럼 결측치를 중앙값으로 채우기 전후의 표준편차를 구하고
두 표준편차 차이 계산하기

'''

df = pd.read_csv('../datasets/basic1.csv')
# print(df.head)


# print(len(df)*0.7)
df70 = df.iloc[:70]
df30 = df.iloc[:30]

#np 이용 해서 나누기
# df70 ,df30 = np.split(df, [int(len(df)*0.7)])
# print(df70)

# print(df70.isna().sum())
std1 = df70['f1'].std()
print('std1',std1)
df70['f1'] = df70['f1'].fillna(df['f1'].median())
std2 = df70['f1'].std()
print('std2',std2)
print(std1-std2)


