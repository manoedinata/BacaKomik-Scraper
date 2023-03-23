import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, quote_plus, urljoin, urlparse
import re

BK_BASE_URL = "https://bacakomik.co"
BK_SEARCH_URL = BK_BASE_URL + "/?s="
BK_COMIC_URL = BK_BASE_URL + "/komik/"
BK_CHAPTER_URL = BK_BASE_URL + "/chapter/"

class Scraper(object):
    def __init__(self) -> None:
        self.BK_BASE_URL = BK_BASE_URL
        self.BK_SEARCH_URL = BK_SEARCH_URL
        self.BK_COMIC_URL = BK_COMIC_URL
        self.BK_CHAPTER_URL = BK_CHAPTER_URL

        self.search_result = {}
        self.comic_info = {}
        self.comic_eps = []
        self.comic_images = []

        self.session = requests.Session()

    def req_parse(self, URL):
        req = self.session.get(URL)
        parse = BeautifulSoup(req.text, "html.parser")

        return parse
    
    def search_comics(self, query):
        access = self.req_parse(self.BK_SEARCH_URL + quote_plus(query))

        # Parse elements
        animepost = access.find_all("div", {"class": "animepost"})
        if animepost:
            results = []
            for anime in animepost:
                anchor = anime.find("a")
                image = anime.find("img")

                title = anchor["title"]
                link = anchor["href"]
                thumbnail = urljoin(image["src"], urlparse(image["src"]).path)

                results.append({
                    "title": title,
                    "thumbnail": thumbnail,
                    "link": link
                })        

        data = {
            "query": quote_plus(query),
            "results": results
        }
        self.search_result = data
        return self.search_result
    
    def get_comic_info(self, comic_name):
        access = self.req_parse(self.BK_COMIC_URL + comic_name)

        title = access.find("h1", {"class": "entry-title"}).text.strip()
        sinopsis = access.find("div", {"itemprop": "description"}).find("p").text.strip()

        comicInfos = access.find("div", {"class": "spe"}).find_all("span")
        status = comicInfos[0].find("b").next_sibling.text.strip()
        format = comicInfos[1].find("b").next_sibling.text.strip()
        releaseDate = comicInfos[2].find("b").next_sibling.text.strip()
        author = comicInfos[3].find("b").next_sibling.text.strip()
        caraBaca = comicInfos[6].find("b").next_sibling.text.strip()
        lastUpdate = comicInfos[8].find("b").find_next("time").text.strip() # TODO: Parse time object instead

        chapterList = access.find("div", {"id": "chapter_list"}).find_all("li")
        chapters = []
        for chapter in chapterList:
            anchor = chapter.find("a")

            chapterName = anchor.text.strip()
            url = anchor["href"]
            slug = url.split("https://bacakomik.co/chapter/")[1]

            chapters.append({
                "chapter": chapterName,
                "slug": slug,
                "url": url,
            })
        availableEps = len(chapters)

        data = {
            "title": title,
            "author": author,
            "release_date": releaseDate,
            "status": status,
            "last_update": lastUpdate,
            "sinopsis": sinopsis,
            "cara_baca": caraBaca,
            "format": format,
            "available_eps": availableEps,
        }

        # Seperate comic info and chapters list
        self.comic_info = data
        self.comic_eps = chapters

    def get_ep_images(self, chapter_slug):
        access = self.req_parse(self.BK_CHAPTER_URL + chapter_slug)

        imagesEl = access.find("div", {"id": "chimg-auh"}).find_all("img")
        for image in imagesEl:
            onError = image["onerror"]
            regex = re.compile("this.onerror=null;this.src='(.*?)';")
            match = regex.match(onError)
            src = match.groups()[0]

            self.comic_images.append(src)

        return self.comic_images
