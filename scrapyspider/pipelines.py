# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import urllib

from scrapyspider import settings


# Item Pipeline负责处理被spider提取出来的item。典型的处理有清理、 验证及持久化(例如存取到数据库中)
class ScrapyspiderPipeline(object):
    def process_item(self, item, spider):
        # self.down_pic(item, spider)
        print("-----------process_item")

    def down_pic(self, item, spider):
        dir_path = '%s/%s' % (settings.IMAGES_STORE, spider.name)  # 存储路径
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        for image_url in item['images1']:
            try:
                print('images1', image_url)
                list_name = image_url.split('/')
                file_name = list_name[len(list_name) - 1]  # 图片名称
                # print 'filename',file_name
                file_path = '%s/%s' % (dir_path, file_name)
                # print 'file_path',file_path
                if os.path.exists(file_name):
                    continue
                with open(file_path, 'wb') as file_writer:
                    conn = urllib.request.urlopen(image_url)  # 下载图片
                    file_writer.write(conn.read())
                file_writer.close()
            except urllib.error.URLError as e:
                print("urllib.error::::" + e.reason + "  strerror:::" + str(e.strerror))
                pass
            except Exception as e:
                print("Exception ::::" + str(e))
                pass

    # return item
