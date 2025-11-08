import json
import time

import httpx
import random
import asyncio


from selenium import webdriver
from selenium.webdriver.chrome.webdriver import Options
from utils.logger import logger
from utils.retry import retry_on_error


class Downloader:
    """需要支持代理池"""
    def __init__(self):
        """
        初始化需要完成如下几个步骤：
        1. 使用selenium登录网站
        2. 将cookie保存为json文件
        """
        self.get_cookies()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Cookie': self.set_cookies()
        }
        self.client = httpx.AsyncClient(
            # 后面可以完全配置在配置文件中
            timeout=30,
            headers=self.headers,
            follow_redirects=True
        )

    def get_cookies(self):
        """登录账号 获取cookies"""
        options = Options()
        # options.add_argument(r'--headless')
        options.add_argument(r"--user-data-dir=D:\Wrok\ScriptProjects\ArticleMakerAgent\data\UserData\selenium_profile")

        driver = webdriver.Chrome(options=options)
        driver.get("https://www.zhihu.com")
        cookies = driver.get_cookies()
        print(cookies)
        driver.quit()
        for c in cookies:
            if "expiry" in c:
                try:
                    c["expiry"] = int(c["expiry"])
                except Exception as e:
                    c.pop("expiry", None)
                    logger.error(e)
        with open(r"../data/cookies.json", "w", encoding="utf-8") as f:
            json.dump(cookies, f, ensure_ascii=False, indent=4)

    def set_cookies(self):
        """Read cookie file add cookie for request"""
        cookie_value = ""
        with open(r"../data/cookies.json", "r", encoding="utf-8") as f:
            cookies = json.load(f)
        for cookie in cookies:
            print(cookie)
            cookie_value += f"{cookie['name']}={cookie['value']};"
        print(cookie_value)
        return cookie_value

    @retry_on_error(max_attempts=3)
    async def fetch_get(self, url: str) -> str:
        """Get Request"""
        try:
            await asyncio.sleep(random.uniform(0, 3))
            logger.info(f"GET: {url}")
            response = await self.client.get(url)
            response.raise_for_status()
            logger.success(f"Success: {url}")
            return response.text
        except Exception as e:
            logger.error(f"Failed: {url} - {e}")
            raise

    async def fetch_post(self, url: str) -> str:
        """Post Request"""
        try:
            await asyncio.sleep(random.uniform(0, 3))
            logger.info(f"POST: {url}")
            response = await self.client.post(url)
            response.raise_for_status()
            logger.success(f"Success: {url}")
            return response.text
        except Exception as e:
            logger.error(f"Failed: {url} - {e}")
            raise


async def main():
    downloader = Downloader()
    try:
        res = await downloader.fetch_get("https://www.zhihu.com")
        print(res)
    finally:
        await downloader.client.aclose()

if __name__ == '__main__':
    asyncio.run(main())
