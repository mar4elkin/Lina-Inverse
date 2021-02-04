from PIL import Image, ImageDraw, ImageFont
from Exceptions import ImageGenAttr
import requests
import numpy as np
from Logger import blogger

class ImageGen(object):
    def __init__(self, imgtype, data, old_data):
        if (imgtype != 'overwatch' and imgtype != 'osu'):
            raise ImageGenAttr(imgtype)
        else:
            self.data = data
            self.old_data = old_data

    def drawImgOverwatch(self):
        blogger('drawing new img (overwatch)')
        def checkRank(x):
            if (x == 'None'):
                return '0'
            else:
                return x

        def getDiff(old, new):
            if (old > new):
                return f'- {new}'
            elif (old < new):
                return f'+ {new}'
            elif (old == new):
                return f'+ 0'
            elif (old == 0 and new == 0):
                return ''

        def cutBackground(img):
            im = img.convert('RGBA')
            data = np.array(im)
            rgb = data[:,:,:3]
            color = [246, 213, 139]
            black = [0,0,0, 255]
            white = [255,255,255,255]
            mask = np.all(rgb == color, axis = -1)
            data[mask] = white
            return Image.fromarray(data)

        blogger('getting fonts')
        header_font = ImageFont.truetype('fonts/ov_font.ttf', 50)
        ranks_font = ImageFont.truetype('fonts/ov_font.ttf', 20)

        blogger('getting rolls imgs')
        damage = Image.open('img/overwatch/damage.png').resize((30, 30))
        support = Image.open('img/overwatch/support.png').resize((30, 30))
        tank = Image.open('img/overwatch/tank.png').resize((30, 30))

        playeravatar_data = requests.get(self.data['player']['avatar']).content
        with open('tmp/overwatch/user_avatar.png', 'wb') as handler:
            handler.write(playeravatar_data)
        blogger('downloaded player avatar')
        
        useravatar = Image.open('tmp/overwatch/user_avatar.png')
        useravatar = useravatar.resize((100, 100))

        hero_data = requests.get(self.data['player']['top_hero']).content
        with open('tmp/overwatch/tophero.png', 'wb') as handler:
            handler.write(hero_data)
        blogger('downloaded player top hero')
        
        heroimg = Image.open('tmp/overwatch/tophero.png')
        
        baseimg = Image.open('img/overwatch/ovbackground.png')
        img = baseimg.copy()

        img.paste(useravatar, (15, 15))
        img.paste(cutBackground(heroimg), (-50, 160), cutBackground(heroimg))
        img.paste(cutBackground(damage), (25, 150), cutBackground(damage))
        img.paste(cutBackground(support), (25, 250), cutBackground(support))
        img.paste(cutBackground(tank), (25, 350), cutBackground(tank))

        blogger('drawing icons and hero img')

        if self.data['ranks']['damage']['rank'] != 'None':
            dd = requests.get(self.data['ranks']['damage']['icon']).content
            with open('tmp/overwatch/dd_rank.png', 'wb') as handler:
                handler.write(dd)
            ddimg = Image.open('tmp/overwatch/dd_rank.png').resize((30, 30))
            img.paste(cutBackground(ddimg), (170, 150), cutBackground(ddimg))
            blogger('damage img done!')
            
        if self.data['ranks']['support']['rank'] != 'None':
            sup = requests.get(self.data['ranks']['support']['icon']).content
            with open('tmp/overwatch/sup_rank.png', 'wb') as handler:
                handler.write(sup)
            supimg = Image.open('tmp/overwatch/dd_rank.png').resize((30, 30))
            img.paste(cutBackground(supimg), (170, 250), cutBackground(supimg))
            blogger('support img done!')

        if self.data['ranks']['tank']['rank'] != 'None':
            tank = requests.get(self.data['ranks']['tank']['icon']).content
            with open('tmp/overwatch/tank_rank.png', 'wb') as handler:
                handler.write(tank)
            tankimg = Image.open('tmp/overwatch/dd_rank.png').resize((30, 30))
            img.paste(cutBackground(tankimg), (170, 350), cutBackground(tankimg))
            blogger('tank img done!')
        
        final_img = ImageDraw.Draw(img)
        final_img.text((130,35), self.data['player']['nickname'], (255, 255, 255), font=header_font)

        final_img.text((60,155), checkRank(self.old_data['ranks']['damage']['rank']), (255, 255, 255), font=ranks_font)
        final_img.text((60,255), checkRank(self.old_data['ranks']['support']['rank']), (255, 255, 255), font=ranks_font)
        final_img.text((60,355), checkRank(self.old_data['ranks']['tank']['rank']), (255, 255, 255), font=ranks_font)

        final_img.text((110,155), '>', (255, 255, 255), font=ranks_font)
        final_img.text((110,255), '>', (255, 255, 255), font=ranks_font)
        final_img.text((110,355), '>', (255, 255, 255), font=ranks_font)

        final_img.text((130,155), checkRank(self.data['ranks']['damage']['rank']), (255, 255, 255), font=ranks_font)
        final_img.text((130,255), checkRank(self.data['ranks']['support']['rank']), (255, 255, 255), font=ranks_font)
        final_img.text((130,355), checkRank(self.data['ranks']['tank']['rank']), (255, 255, 255), font=ranks_font)

        final_img.text((200,155), getDiff(checkRank(self.old_data['ranks']['damage']['rank']), checkRank(self.data['ranks']['damage']['rank'])), (255, 255, 255), font=ranks_font)
        final_img.text((200,255), getDiff(checkRank(self.old_data['ranks']['support']['rank']), checkRank(self.data['ranks']['support']['rank'])), (255, 255, 255), font=ranks_font)
        final_img.text((200,355), getDiff(checkRank(self.old_data['ranks']['tank']['rank']), checkRank(self.data['ranks']['tank']['rank'])), (255, 255, 255), font=ranks_font)
        
        img.save('tmp/overwatch/overwatch.png')
        blogger('img saved!')
    
    def drawImgOsu(self):
        pass
