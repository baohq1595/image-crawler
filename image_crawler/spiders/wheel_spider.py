import scrapy

class WheelSpider(scrapy.Spider):
    name = 'wheelspider'
    allowed_domains = ['maluzen.com']
    start_urls = ['https://www.maluzen.com/wheelcatalog/?wd=4&wz=&wc=2&wb=&wm=&wma=&wyo=']

    image_src_url_prefix = 'https://www.maluzen.com/_upimages/photos/'

    shape_mapping = {1: 'other', 2: 'spoke', 3: 'dish', 4: 'mesh'}
    color_mapping = {2: 'silver', 4: 'chrome', 6: 'gunmetal',
                    7: 'gold', 8: 'white', 9: 'black',
                    10: 'bronze', 11: 'polish', 12: 'titanium',
                    13: 'pink', 14: 'yellow', 15: 'green',
                    16: 'red', 17: 'blue', 1: 'other'}
    color_marker = 'wc='
    shape_marker = 'wd='

    def get_image_attrs(self, url: str):
        shape = 'other'
        color = 'other'
        shape_pos = url.find(WheelSpider.shape_marker)
        color_pos = url.find(WheelSpider.color_marker)
        if shape_pos != -1:
            marked_pos = shape_pos + len(WheelSpider.shape_marker) 
            shape = WheelSpider.shape_mapping.get(
                int(url[marked_pos:marked_pos + 1]), 'other'
            )
        
        if color_pos != -1:
            marked_pos = color_pos + len(WheelSpider.color_marker)
            color = WheelSpider.color_mapping.get(
                int(url[marked_pos:marked_pos + 1]), 'other'
            )

        return shape, color
    
    def rertrieve_image_link(self, disply_image_url: str):
        '''
        Form full-resolution (800x800) download-able link from display
        image url (which shown in the webpage)

        For ex:
            display url: //file.maluzen.com/www/_upimages/200/01_011706_00_00_00000_%23_%23_000_00.jpg
            full-res url wiil be: https://www.maluzen.com/_upimages/photos/01_011706_00_00_00000_%23_%23_000_00.jpg
        '''
        pass

    def parse(self, reponse):
        print('Processing ', reponse.url)
        # Extract data using xpath

        catalog_list = reponse.xpath('string(//*[@id="catalog-list"]/ul[1]/li[2]/a/img//@src)').extract()
        print(catalog_list)
        for item in catalog_list:
            print(item)
            # Extract link to image source to download
            scrapped_info = {'link': item}

            yield scrapped_info
