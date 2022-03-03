
from icrawler.builtin import BingImageCrawler

number = 300

classes = ['metal round wheel', 'metal round parts']

for c in classes:
    bing_crawler = BingImageCrawler(storage={'root_dir':f'n/{c.replace(" ", "_")}'})
    bing_crawler.crawl(keyword=c, filters=None, max_num=number, offset=0)

