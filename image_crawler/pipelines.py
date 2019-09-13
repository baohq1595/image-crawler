# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from .spiders.utils import *
import os
import pandas as pd
import requests
from PIL import Image

import sys
sys.path.append('.\\')

class ImageCrawlerPipeline(object):
    def __init__(self):
        self.label_db = 'data/label/label.csv'
        self.image_db = 'data/images'

        label = pd.DataFrame(columns=['image_id', 'shape', 'color', 'width', 'height'])

        # Ensure db paths
        if not os.path.exists(os.path.dirname(self.label_db)):
            os.makedirs(os.path.dirname(self.label_db))
            label.to_csv(self.label_db, encoding='utf-8', index=False)
        else:
            label = pd.read_csv(self.label_db)
        if not os.path.exists(os.path.dirname(self.image_db)):
            os.makedirs(os.path.dirname(self.image_db))

    def process_item(self, item, spider):
        shape, color = get_image_attrs(item['url'])

        # Retrieve image
        item['img_name'] = item['img_name'].replace(' ', '')
        img_path = os.path.join(self.image_db, item['img_name'] + '.jpg')

        if not os.path.exists(img_path):
            img_data = requests.get(item['img_link']).content
            with open(img_path, 'wb') as handler:
                handler.write(img_data)
        else:
            return item

        img = Image.open(img_path)
        img_w, img_h = img.size

        # Form label
        lb = dict({'image_id': [item['img_name']],
                    'shape': [shape],
                    'color': [color],
                    'width': [img_w],
                    'height': [img_h]})

        df = pd.DataFrame(data=lb)

        # Write label
        label_db = pd.read_csv(self.label_db)
        label_db = pd.concat([label_db, df])
        label_db.to_csv(self.label_db, encoding='utf-8', index=False)

        return item
