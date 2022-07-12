# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MinsuItem(scrapy.Item):
    # 民宿标题
    name = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 区县
    county = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 商圈
    location = scrapy.Field()
    # 房间
    rooms = scrapy.Field()
    # 床位数
    beds = scrapy.Field()
    # 可入住人数
    num = scrapy.Field()
    # 房屋面积
    area = scrapy.Field()
    # 户型
    type = scrapy.Field()
    # 详细描述
    description = scrapy.Field()

    
