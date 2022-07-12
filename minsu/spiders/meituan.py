from urllib.request import Request
import scrapy
from minsu.items import MinsuItem


class MeituanSpider(scrapy.Spider):
    name = 'meituan'
    allowed_domains = ['minsu.dianping.com']
    start_urls = ['http://minsu.meituan.com/']
    city = 'handan'
    cookies = '_lxsdk_cuid=181892fa2dcc8-002ac9079bbd46-714e2d2d-13c680-181892fa2ddc8; _hc.v=74e68927-ecce-2436-28f8-765657b93da5.1655864010; _ga=GA1.2.587754288.1655864010; _gid=GA1.2.1091618640.1657007582; zgwww=8031ef40-fc42-11ec-bb18-cdc0491b4715; uuid=342C318B81886D6A9AA754423B5D7AAA3C07E353D93941DB7539B4A721888C1E; iuuid=342C318B81886D6A9AA754423B5D7AAA3C07E353D93941DB7539B4A721888C1E; _lxsdk=342C318B81886D6A9AA754423B5D7AAA3C07E353D93941DB7539B4A721888C1E; zg.userid.untrusted=482055829; token2=9RzXI4iLuh3jl3josFjp9bUBEnQAAAAAvRIAALmJ4Noh64ZVON0YWWJ5an9W4idVjD-yEBgeqJHV98PsnHldVx2ap0dcl1YEJs6uog; userid=3035149485; XSRF-TOKEN=PJqDiP1U-zPJBy0oX7saNrHjtoy23xvEv-88; _lxsdk_s=181d0d976fc-6b3-d34-a9f||48'
    cookie_dict = {}
    
    # 将cokkie字符串处理成scrapy中Request对象可用的cookie
    def get_cookie(self):
        cookie_dict = {}
        for item in self.cookies.split(';'):
            key,value = item.split('=',maxsplit=1)
            cookie_dict[key] = value
        return cookie_dict

    def start_requests(self):
        self.cookie_dict = self.get_cookie()
        for page in range(1,18):
            base_url = f'https://minsu.dianping.com/{self.city}/pn{page}/'
            yield scrapy.Request(url=base_url,cookies=self.cookie_dict,callback=self.parse)

    def parse(self, response):
        self.cookie_dict = self.get_cookie()
        all = response.xpath('.//div[@class="r-card-list v-stretch h-stretch"]').xpath('.//div[@class="r-card-list__item shrink-in-sm"]')
        for i in all:
            item = MinsuItem()
            item['name'] = i.xpath('./div/a/figure/figcaption/div/text()').extract_first().replace('\n','')
            item['price'] = i.xpath('.//span[@class="product-card__price__latest"]/text()').extract_first()
            item['location'] = i.xpath('./div/a/figure/figcaption/div/div[@class="mt-2"]/text()').extract_first()
            item['rooms'] = i.xpath('./div/a/figure/figcaption/div/div[1]/text()').extract_first().split('·')[0]
            item['beds'] = i.xpath('./div/a/figure/figcaption/div/div[1]/text()').extract_first().split('·')[1]
            try:
                item['num'] = i.xpath('./div/a/figure/figcaption/div/div[1]/text()').extract_first().split('·')[2]
            except:
                item['num'] = i.xpath('./div/a/figure/figcaption/div/div[1]/text()').extract_first().split('·')[1]
                print( i.xpath('./div/a/figure/figcaption/div/div[1]/text()').extract_first())
            hrefs = i.xpath('.//a[@class="product-card-container"]/@href').extract_first()
            href = response.urljoin(hrefs)
            yield scrapy.Request(url=href,callback=self.parse2,meta={'item': item},cookies=self.cookie_dict)
        
    def parse2(self,response):
        item = response.meta['item']
        sel = scrapy.Selector(response)
        # 区县
        county = sel.re('"districtId":[0-9]{6},"districtName":"[\u4e00-\u9fa5]{1,10}"')
        item['county'] = eval(county[0].split(':')[2])
        # 地址
        # addr = sel.re('"fullAddress":"[\u4e00-\u9fa5]{1,100}"') 
        # addr = sel.re('"fullAddress":"[\u4e00-\u9fa5a-zA-Z0-9]+"') 
        addr = sel.re('"fullAddress":"[ /\s\(\)\\\-\u3002\u002d\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\u4e00-\u9fa5a-zA-Z0-9]+"') 
        if addr :
            item['address'] = eval(addr[0].split(':')[1])
        else:
            item['address'] = ''
        # 房屋面积
        # item['area'] = eval(sel.re('"usableArea":"[0-9]{1,4}"')[0].split(':')[1])
        room_type = sel.xpath('.//div[@class="subvalue"]/text()').extract()
        # 户型
        item['type'] = room_type[1]
        # 房屋面积
        item['area'] = room_type[0]
        # 简介描述
        desc = sel.xpath('.//div[@class="text-clamp just-pointer"]/text()').extract()
        item['description'] = desc[1].replace('\r\n','')
        yield item