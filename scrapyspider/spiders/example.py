# coding:utf-8

import scrapy

# http://www.cnblogs.com/wanghzh/p/5824181.html
# 引擎打开一个网站(open a domain)，找到处理该网站的Spider并向该spider请求第一个要爬取的URL(s)。
# 引擎从Spider中获取到第一个要爬取的URL并在调度器(Scheduler)以Request调度。
# 引擎向调度器请求下一个要爬取的URL。
# 调度器返回下一个要爬取的URL给引擎，引擎将URL通过下载中间件(请求(request)方向)转发给下载器(Downloader)。
# 一旦页面下载完毕，下载器生成一个该页面的Response，并将其通过下载中间件(返回(response)方向)发送给引擎。
# 引擎从下载器中接收到Response并通过Spider中间件(输入方向)发送给Spider处理。
# Spider处理Response并返回爬取到的Item及(跟进的)新的Request给引擎。
# 引擎将(Spider返回的)爬取到的Item给Item Pipeline，将(Spider返回的)Request给调度器。
# (从第二步)重复直到调度器中没有更多地request，引擎关闭该网站。
#  jiandanSpider.py ------Spider 蜘蛛
# items.py - ----------------对要爬取数据的模型定义
# pipelines.py - ------------咱们最终要存储的数据
# settings.py - ---------------对Scrapy的配置
from scrapyspider.items import ScrapyspiderItem


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ["xiaohuar.com"]
    start_urls = ["http://www.xiaohuar.com/p-1-64.html"]
    download_headers = {
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
        'Accept-Encoding': 'deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'DNT': '1',
        'Pragma': 'no-cache',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://www.ugirls.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
    }

    def parse(self, response):
        item = ScrapyspiderItem()
        item['image_urls'] = response.xpath('//img//@src').extract()  # 提取图片链接
        print('item_images', item)
        # item['images'].add(response.xpath('//img//@src').extract())
        for index in range(len(item['image_urls'])):
            if not (item['image_urls'][index].startswith("http")):
                item['image_urls'][index] = 'http://www.xiaohuar.com' + item['image_urls'][index]

            if not (item['image_urls'][index].endswith("php")):
                print("item['image_urls'][index]", item['image_urls'][index])
                item['image_urls'][index] = item['image_urls'][index].replace("php", "jpg")
        yield item
        # 获得下个url
        urls = response.xpath('//a/@href').extract()
        for url in urls:
            if str(url).__contains__(self.allowed_domains[0]):
                yield scrapy.Request(url, callback=self.parse)
    # print 'new_url',new_url
    # if new_url:
    #     yield scrapy.Request(new_url, callback=self.parse)

    # titles = response.xpath('//img//@src').extract()
    # for title in titles:
    #     print(title.strip())
    # current_url = response.url  # 爬取时请求的url
    # body = response.body  # 返回的html
    # unicode_body = response.body_as_unicode()  # 返回的html unicode编码
    # print("unicode_body", unicode_body)
    # hxs = HtmlXPathSelector(response)  # 创建查询对象
    # type(hxs)
    # 如果url是 http://www.xiaohuar.com/list-1-\d+.html
    # print("hxs---------", hxs.xpath("//img//@lazysrc"))
    # if hxs.match('http://www.xiaohuar.com/list-1-\d+.html', response.url):  # 如果url能够匹配到需要爬取的url，即本站url
    #     print("hxs---------hxs.match")
    #     items = hxs.select('//div[@class="item_list infinite_scroll"]/div')  # select中填写查询目标，按scrapy查询语法书写
    #     for i in range(len(items)):
    #         src = hxs.select(
    #             '//div[@class="item_list infinite_scroll"]/div[%d]//div[@class="img"]/a/img/@src' % i).extract()  # 查询所有img标签的src属性，即获取校花图片地址
    #         name = hxs.select(
    #             '//div[@class="item_list infinite_scroll"]/div[%d]//div[@class="img"]/span/text()' % i).extract()  # 获取span的文本内容，即校花姓名
    #         school = hxs.select(
    #             '//div[@class="item_list infinite_scroll"]/div[%d]//div[@class="img"]/div[@class="btns"]/a/text()' % i).extract()  # 校花学校
    #         if src:
    #             ab_src = "http://www.xiaohuar.com" + src[0]  # 相对路径拼接
    #             file_name = "%s_%s.jpg" % (
    #                 school[0].encode('utf-8'),
    #                 name[0].encode('utf-8'))  # 文件名，因为python27默认编码格式是unicode编码，因此我们需要编码成utf-8
    #             file_path = os.path.join("D:/python/image", file_name)
    #             urllib.urlretrieve(ab_src, file_path)

    # lazysrc = hxs.xpath("//img//@lazysrc")
    # # HtmlXPathSelector
    # for entity in lazysrc:
    #     src = entity.extract()
    #     print("src---------", src)
    #     if src:
    #         ab_src = "http://www.xiaohuar.com/" + src  # 相对路径拼接
    #         # name = hxs.select(
    #         #     '//div[@class="item_list infinite_scroll"]/div[%d]//div[@class="img"]/span/text()' % entity).extract()  # 获取span的文本内容，即校花姓名
    #         # school = hxs.select(
    #         #     '//div[@class="item_list infinite_scroll"]/div[%d]//div[@class="img"]/div[@class="btns"]/a/text()' % entity).extract()  # 校花学校
    #         # file_name = "%s_%s.jpg" % (school[0].encode('utf-8'),
    #         #                            name[0].encode('utf-8'))  # 文件名，因为python27默认编码格式是unicode编码，因此我们需要编码成utf-8
    #         file_name = src.split('/')[-1]
    #         file_path = os.path.join("D:/python/image", file_name)
    #         # urllib.urlretrieve(src, file_path)
    #         with open(file_path, 'wb')as f:
    #             f.write(self.get_response_download(src))
    #
    # all_urls = hxs.select('//a/@href').extract()
    # for url in all_urls:
    #     if url.startswith('http://www.xiaohuar.com/list-1-'):
    #         yield Request(url, callback=self.parse)

# scrapy crawl example --nolog   格式：scrapy crawl+爬虫名  --nolog即不显示日志
