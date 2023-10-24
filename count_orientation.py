from PIL import Image, ExifTags
import os
import pandas as pd
import csv


path1 = 'C:\work\Engineer_Big_Data_Analysis'
path2 = '/workspace/data/old2/K-Deep-Fashion/패션 액세서리 착용 데이터/원천데이터'


def count_orientation(path):
    try:
        dir_path = path
        total_img = []
        error_file = []
        total_orient_list = []
        dir_list = []
        # csv_name = ''.join(path.split('/')[-3:-1])
        for (root, directories, files) in os.walk(dir_path):
            for file in files:
                if '.jpg' in file:
                    total_img.append(os.path.join(root, file))
                    if root not in dir_list:
                        dir_list.append(root)
                        print(root)

        dir_list = list(set(dir_list))
        print('##########################################################')
        print('폴더수', len(dir_list))
        print('이미지수', len(total_img))
        print('##########################################################')

        for idx, directory in enumerate(dir_list):
            jpgs = []
            dir_oriental = []
            try:
                for file in os.listdir(directory):
                    if '.jpg' in file:
                        jpgs.append(os.path.join(directory, file))
                for index, jpg in enumerate(jpgs):
                    if index % 1000 == 0:
                        print('폴더수:', idx ,'/',len(dir_list))
                        print('현재이미지/폴더내이미지:', index, '/', len(jpgs))
                    try:
                        image = Image.open(jpg)
                        for orientation in ExifTags.TAGS.keys():
                            if ExifTags.TAGS[orientation] == 'Orientation':
                                break
                        exif = dict(image._getexif().items())

                        if exif[orientation]==1:
                            orient = 'Rotate 0'
                        elif exif[orientation]==3:
                            orient = 'Rotate180'
                        elif exif[orientation]==6:
                            orient = 'Rotate90(시계방향)'
                        elif exif[orientation]==8:
                            orient = 'Rotate270(시계방향)'
                        else:
                            orient = exif[orientation]
                        total_orient_list.append(orient)
                        dir_oriental.append(orient)
                        image.close()
                    except:
                        print('\n--------------------------------------open_error------------------------------------', jpg)
                        error_file.append((jpg, 'open_error'))
                        orient = 'open_error'
                        total_orient_list.append(orient)
                        dir_oriental.append(orient)
                        pass

                    if len(dir_oriental) == len(jpgs):
                        orientation_list = pd.DataFrame({'img_path': jpgs, 'orientation': dir_oriental})
                        imname = ''.join(directory.split('\\'))
                        # imname = ''.join(directory.split('/')[-4:])
                        orientation_list.to_csv(imname+'.csv', index=False, encoding='utf-8')
                        vc = orientation_list['orientation'].value_counts()
                        print(imname, "\n폴더 내 Total img :", len(jpgs),'\n', vc)
                        print('###################################################################################')
                        total_count = '########### 폴더 내 총 개수'+str(len(dir_oriental))+'###########'
                        with open(imname+'.csv', 'a', encoding="utf-8") as f:
                            wr = csv.writer(f)
                            wr.writerow([total_count])
                            for k, v in vc.items():
                                wr.writerow([k,v])
            except:
                print('폴더 에러', directory)
                pass

        if len(total_img) == len(total_orient_list):
            print('###################################################################################')
            t_orientation_list = pd.DataFrame({'img_path':total_img, 'orientation':total_orient_list})
            t_orientation_list.to_csv('total.csv', index=False, encoding='utf-8')
            t_vc = t_orientation_list['orientation'].value_counts()
            print('####완료####', "\nTotal img :", len(total_img),'\n', t_vc)
            total_count = '###########  이미지 총 개수'+str(len(total_img))+'  ###########'
            with open('total.csv', 'a', encoding="utf-8") as f:
                wr = csv.writer(f)
                wr.writerow([total_count])
                for k, v in t_vc.items():
                    wr.writerow([k, v])

        elif len(error_file) > 1:
            error_list = pd.DataFrame({'not_save_file':error_file})
            error_list.to_csv('error_list.csv', index=False)
            print('####error_list 저장####', "\nerror img :", len(error_file))

        else:
            print('####에러 없이 완료####')
    except :
        print('error')


count_orientation(path1)
# count_orientation(path2)
