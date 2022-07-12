# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import openpyxl 


class MinsuPipeline:
    
    def __init__(self) -> None:
        self.num = 0
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.title = '邯郸民宿'
        self.ws.append(('序号','名称','价格','区县','商圈','地址','详情描述','房屋面积','户型','房间','床位','可住人数'))

    def close_spider(self,spider):
        self.wb.save('邯郸民宿.xlsx')
    
    def process_item(self, item, spider):
        # name = item.get('name','')
        self.num += 1
        self.ws.append((self.num,item['name'],item['price'],item['county'],
                        item['location'],item['address'],item['description'],
                        item['area'],item['type'],item['rooms'],item['beds'],
                        item['num']))
        return item
