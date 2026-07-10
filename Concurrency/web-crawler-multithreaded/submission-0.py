from typing import List
from concurrent.futures import ThreadPoolExecutor

class Solution:
    def crawl(self, startUrl: str, htmlParser: 'HtmlParser') -> List[str]:
        hostname = self.getHost(startUrl)
        visited = {startUrl}

        with ThreadPoolExecutor(max_workers=10) as executor:
            q = [startUrl]

            while q:
                next_level = []

                for urls in executor.map(htmlParser.getUrls, q):
                    for url in urls:
                        if self.getHost(url) == hostname and url not in visited:
                            visited.add(url)
                            next_level.append(url)

                q = next_level

        return list(visited)

    def getHost(self, url: str) -> str:
        return url.replace("http://", "").split("/")[0]
