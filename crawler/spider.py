# 构建爬虫
import asyncio
import json
from downloader import Downloader
from parser import PageParser
from utils.logger import logger


class Spider:
    def __init__(self):
        self.base_url = "https://www.zhihu.com/api/v3/feed/topstory/recommend?page_number={}"
        self.downloader = Downloader()
        self.parser = PageParser()

    async def process(self):
        result_data = []
        for page in range(1, 30+1):
            try:
                res = await self.downloader.fetch_get(self.base_url.format(page))
                results = self.parser.parser_data(res)
                result_data.extend(results)
            except Exception as e:
                logger.error(e)

        with open("../data/spider_result.json", "w", encoding="utf-8") as f:
            json.dump(result_data, f, ensure_ascii=False, indent=4)
            f.close()


if __name__ == '__main__':

    spider = Spider()
    asyncio.run(spider.process())
