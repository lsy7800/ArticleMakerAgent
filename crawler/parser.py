import json
from datetime import datetime, timezone


class PageParser:

    def parser_data(self, page_data):
        """提取标题和链接"""
        json_data = json.loads(page_data)
        data = json_data["data"]
        results = []

        for item in data:
            title = item["target"]["question"]["title"]
            url = item["target"]["question"]["url"]
            created_time = item["created_time"]
            results.append({"title": title, "url": self.clear_url(url), "created": self.transform_time(created_time)})

        return results

    def transform_time(self, time_data: int):
        """转换时间戳"""
        dt_utc = datetime.fromtimestamp(time_data, tz=timezone.utc)
        return dt_utc.strftime("%Y-%m-%d %H:%M:%S")

    def clear_url(self, url: str):
        """重构url页面"""
        cleaned_url = url.replace("api.", "").replace("questions", "question")
        return cleaned_url
