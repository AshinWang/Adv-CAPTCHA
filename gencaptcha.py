import os
import time
import shutil
import random
import pandas as pd
import numpy as np
from tqdm import tqdm
from captcha.image import ImageCaptcha



class GenCAPTCHA:
    def __init__(self, length=4, cover_up=False, width=128, height=64, numbers=500, path='captcha'):
        self.length = length
        self.cover_up = cover_up
        self.width = width
        self.height = height
        self.numbers = numbers
        self.path = path

    def genVCode(self):
        code_list = [] 

        # 0-9
        for i in range(10): 
            code_list.append(str(i))

        if self.cover_up:
            # “A”到“Z”
            for i in range(65, 91): 
                code_list.append(chr(i))
       
        # “a”到“z”
        for i in range(97, 123): 
            code_list.append(chr(i))


        ''' 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ
        import string
        characters = string.digits + string.ascii_uppercase
        print(characters)
        '''

        # 从 list 中随机获取 length 个元素，作为一个片断返回
        myslice = random.sample(code_list, self.length) 
        vcode = ''.join(myslice) # list to string
        return vcode

    def genLabel(self):
        data = pd.DataFrame(columns=['id','label'])
        for idx in (range(self.numbers)):
            data.loc[idx, 'id'] = idx
            vcode = self.genVCode()
            data.loc[idx, 'label'] = vcode
        return data

    
    def genIMG(self):
        path = self.path
        isExists=os.path.exists(path)
        if isExists:
            shutil.rmtree(path)
            os.mkdir(path)
            os.mkdir(path + '/images')
        else:
            os.mkdir(path)
            os.mkdir(path + '/images')
        
        image = ImageCaptcha(width=self.width, height=self.height)
        data = self.genLabel()        
        #data.to_csv(path + '/label.csv', index=False)     
        for id, label in tqdm(zip(data['id'], data['label'])):
            data = label
            image.write(data, path + '/images/{}.png'.format(label))

        print('')    
        print('--------------------------')
        print(' Generated CAPTCHA dataset ')
        print('--------------------------')

if __name__ == '__main__':
    os.chdir('./Desktop/')
    captcha = GenCAPTCHA(length=5, cover_up=False, width=128, height=64, numbers=10000, path='captcha').genIMG()
    