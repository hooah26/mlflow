import os
import pandas as pd

dir_path = 'C:\work\Engineer_Big_Data_Analysis\data\old2\K-Deep-Fashion\패션 액세서리 착용 데이터\원천데이터\제품'

category = []
for (root, directories, files) in os.walk(dir_path):
    for file in files:
        if '.jpg' in file:
            # print(os.path.join(root, file))
            path = (os.path.join(root, file))
            cate = path.split('\\')[-2]
            category.append(cate)


df = pd.DataFrame({'cate':category})
df.to_csv('shapeless_제품', index=False)
# print(df.info)
print(df.value_counts())