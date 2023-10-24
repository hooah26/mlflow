from PIL import Image, ExifTags
import os
import pandas as pd


def change_orientation(path):
    try:
        dir_path = path
        file_path = []
        error_file = []
        for (root, directories, files) in os.walk(dir_path):
            for file in files:
                if '.jpg' in file:
                    file_path.append(os.path.join(root, file))
        imgs = file_path
        percentage = 0
        print("Total img :", len(imgs))
        for idx, img in enumerate(imgs):
            if idx % 5 == 0:
                print('현재이미지/총이미지:', idx,'/',len(imgs))
            if ((idx/len(imgs)*100) // 10) != percentage:
                print('\n##############', int(idx/len(imgs)*100), '% 완료##############')
            percentage = int(((idx / len(imgs)) * 100) // 10)

            try:
                image = Image.open(img)
                img_exif = image.getexif()
                print(img_exif)
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = dict(image._getexif().items())
                try:
                    if exif[orientation] == 3:
                        image = image.rotate(180, expand=True)
                        del img_exif[orientation]
                    elif exif[orientation] == 6:
                        image = image.rotate(270, expand=True)
                        del img_exif[orientation]
                    elif exif[orientation] == 8:
                        image = image.rotate(90, expand=True)
                        del img_exif[orientation]
                    # print('\ntrans_completed', img)
                except:
                    print('\nimg_save_error', img)
                    error_file.append((img, 'save_error'))
                    pass
                image.save(img, quality=95, subsampling=0, exif=img_exif)
                image.close()
            except:
                print('\nimg_open_error', img)
                error_file.append((img, 'open_error'))
                pass

        if len(error_file) > 1:
            error_list = pd.DataFrame({'not_save_file':error_file})
            error_list.to_csv('error_list.csv', index=False)
            print('####완료 및 error_list 저장####', "\nTotal img :", len(imgs), "\nerror img :", len(error_file))

        else:
            print('####에러 없이 완료####',"\nTotal img :", len(imgs))
    except :
        print('error')

path = 'C:\work\Engineer_Big_Data_Analysis'
change_orientation(path)