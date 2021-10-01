from urllib.parse import quote_plus, unquote

from bs4 import BeautifulSoup
from requests import Session


class Anime:
    """CLI crawler for anime4up website"""

    def __init__(self):
        self.__base_url = "https://ww.anime4up.com/"
        self.__session = Session()
        self.__anime_status = {
            "مكتمل": "Completed",
            "يعرض الان": "now streaming"}

    def __soup_gen(self, url: str):
        """This Function Helps To make the code more cleaner"""
        req = self.__session.get(url).content
        soup = BeautifulSoup(req, features="html.parser")
        return soup

    def search(self, searchQuiery: str):
        """This Function Searches within the website
        if you want to save the resuts just add another argument --save
        """
        searchq = quote_plus(searchQuiery.lower())
        url = f"{self.__base_url}?search_param=animes&s={searchq}"
        search_soup = self.__soup_gen(url)
        search_item = search_soup.find_all(
            "div",
            class_="col-lg-2 col-md-4 col-sm-6 col-xs-6 col-no-padding col-mobile-no-padding",
        )
        # print(search_item)
        if len(search_item) == 0:
            print(f"No Results Found ! For {searchQuiery}")
            return None
        else:
            search_results = []
            for i, item in enumerate(search_item):
                anime_title = (
                    item.select_one(
                        "div.anime-card-details > div.anime-card-title > h3 > a"
                    )
                    .text.strip()
                    .title()
                )

                anime_url = item.select_one(
                    "div.anime-card-details > div.anime-card-title > h3 > a"
                ).get("href")
                anime_link = unquote(anime_url)
                anime_type = (
                    item.find("div", class_="anime-card-type")
                    .find("a")
                    .text.strip()
                    .upper()
                )

                anime_status_ar = (
                    item.find(
                        "div",
                        class_="anime-card-status").find("a").text.strip())
                story = item.find(
                    "div", class_="anime-card-title").get("data-content")
                # print(story)

                anime_image = item.find(
                    "img", class_="img-responsive").get("src")
                try:
                    anime_status = self.__anime_status[anime_status_ar]
                except BaseException:
                    anime_status = anime_status_ar
                search_result = {
                    "index": i + 1,
                    "title": anime_title,
                    "story": story,
                    "type": anime_type,
                    "link": anime_link,
                    "status": anime_status,
                    "image": anime_image,
                }
                search_results.append(search_result)
            return search_results


class Show:
    def __init__(self, link):
        self.url = link
        self.__base_url = "https://ww.anime4up.com/"
        self.__session = Session()

    def __soup_gen(self):
        req = self.__session.get(self.url).content
        soup = BeautifulSoup(req, features="html.parser")
        return soup

    #############################

    def title(self):
        search_soup = self.__soup_gen()
        try:
            title = search_soup.find("h1", class_="anime-details-title").text
        except BaseException:
            title = "غير موجود"
        finally:
            return title

    #############################

    def info(self, as_list=False):
        search_soup = self.__soup_gen()
        info = []
        types = search_soup.find_all("div", class_="col-md-6 col-sm-12")
        if as_list:
            for ty in types:
                bb = ty.find("div", class_="anime-info").text.replace("\n", "")
                info.append(bb)
            return info
        else:
            switcher = {
                "النوع": "type",
                "بداية العرض": "started_on",
                "حالة الأنمي": "status",
                "عدد الحلقات": "episodes",
                "مدة الحلقة": "duration",
                "الموسم": "season",
                "المصدر": "from",
            }

            dict = {
                switcher.get(
                    t.find("div", class_="anime-info")
                    .text.replace("\n", "")
                    .split(":")[0]
                    .strip()
                ): t.find("div", class_="anime-info")
                .text.replace("\n", "")
                .split(":")[1]
                .strip()
                for t in types
            }
            return dict

    #############################

    def category(self, as_list=False):
        search_soup = self.__soup_gen()
        category = []
        gen = search_soup.find("ul", class_="anime-genres").find_all("a")

        for h in gen:
            v = h.text.strip()
            category.append(v)

        liststr = ", ".join([str(elem) for elem in category])

        if as_list:
            return category
        else:
            return liststr

    #############################

    def story(self):
        search_soup = self.__soup_gen()
        story = None
        try:
            story = search_soup.find("p", class_="anime-story").text
        except BaseException:
            return "غير متوفرة"
        finally:
            return story

    #############################

    def image(self):
        search_soup = self.__soup_gen()
        img = None
        try:
            img = search_soup.find(
                "img", class_="thumbnail img-responsive").get("src")
        except BaseException:
            img = "https://i.imgur.com/kbuaAuP.jpg"
        finally:
            return img

    #############################

    def trailer(self):
        search_soup = self.__soup_gen()
        trailer = None
        try:
            trailer = search_soup.find("a", class_="anime-trailer").get("href")
        except BaseException:
            trailer = "https://youtu.be/dQw4w9WgXcQ"
        finally:
            return trailer


class GetEpisodes:
    def __init__(self, link):
        self.url = link
        self.__base_url = "https://ww.anime4up.com/"
        self.__session = Session()

    def __soup_gen(self):
        req = self.__session.get(self.url).content
        soup = BeautifulSoup(req, features="html.parser")
        return soup

    def all_eps(self):
        soup = self.__soup_gen()
        eps = []
        n = soup.find_all("div", class_="episodes-card-title")
        for i in n:
            link = i.a["href"]
            ep = i.a.get_text()
            re = {"name": ep, "link": link}
            eps.append(re)

        return eps

    def total(self):
        soup = self.__soup_gen()
        eps = 0
        n = soup.find_all("div", class_="episodes-card-title")
        for i in n:
            eps += 1

        return eps

    def get_ep(self, n: int):
        k = self.all_eps()
        num = n - 1
        return k[num]


class Episode:
    def __init__(self, link):
        self.url = link
        self.__base_url = "https://ww.anime4up.com/"
        self.__session = Session()

    def __soup_gen(self):
        req = self.__session.get(self.url).content
        soup = BeautifulSoup(req, features="html.parser")
        return soup

    def dl_links(self):
        soup = self.__soup_gen()
        lis = soup.find("ul", {"class": "nav nav-tabs"}).find_all("li")
        espoid_src = []

        for li in lis:
            re = {"host": li.a.get_text(), "link": li.a["data-ep-url"]}
            espoid_src.append(re)
        return espoid_src


"""
    def direct_link(self):
        try:
            s = requests.get(self.link).text
            t = "".join(re.findall('<a id="solidfiles-6" data-ep-url="(.*?)"', str(s)))
            m = requests.get(t).text
            url = "".join(re.findall('"streamUrl":"(.*?)"', str(m)))
        except BaseException:
            return None
        finally:
            return url
"""
