import os
from scrapy.cmdline import execute
import sys
sys.path.append('D:\\workspace\\python\\image_crawler')

os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    execute(
        [
            'scrapy',
            'crawl',
            'wheelspider',
            '-o',
            'out.json',
        ]
    )
except SystemExit:
    pass