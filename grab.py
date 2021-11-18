import requests
from bs4 import BeautifulSoup as bsoup


class Grab:
    def __init__(self, logger, search):
        # TODO: ADD valid TOKEN and channel ID for telegram
        self.__TOKEN = ''
        self.__CHANNEL = ''
        self.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'"}
        self.logger = logger
        self.search = search
        self.new_sended = ''
        self.results = []

    def __del__(self):
        self.new_sended = ''
        self.results = []

    def run(self):
        # Grabbing data
        self.__xkom()
        self.__mediaexpert()
        self.__morele()
        self.__komputronik()
        self.__euro()
        self.__electro()

        # Update sended urls
        with open('sended_urls', 'a') as f:
            f.write(self.new_sended)

    def __send_into_telegram(self, element):
        print(element[0])
        return True 

    def __check_results(self, results):
        with open('sended_urls', 'r') as f:
            sended = f.read()

        for element in results:
            if self.search in element[0].lower():
                if element[1] not in sended:
                    self.logger.info(f"Founded {element[0]}")
                    self.__send_into_telegram(element)
                    self.results.append(element)
                    self.new_sended += element[1]
        return True if len(results) > 0 else False

    def __make_request(self, url):
        _search = self.search.replace(" ", "%20")
        url = url.replace("replaceMe", _search)
        response = requests.get(url, headers=self.headers)
        self.logger.info(f"[{response.status_code}] response from {url}")
        return bsoup(response.content, 'html.parser') if response.status_code == 200 or response.status_code == 444 else False

    def __xkom(self):
        results = []
        ctx = self.__make_request(
            "https://www.x-kom.pl/szukaj?q=replaceMe&f%5Bgroups%5D%5B5%5D=1").find(id="listing-container")

        if not ctx:
            self.logger.debug("Nothing to return from xkom")
            return False

        for element in ctx.findChildren("div", recursive=False):
            _main = element.findChildren("div", recursive=False)[
                0].findChildren("div", recursive=False)[1]
            _title = _main.find("h3").text
            _link = str("https://www.x-kom.pl/" + _main.findChildren("div",
                        recursive=False)[1].find("a")['href'])
            _price = _main.findChildren("div", recursive=False)[
                2].find("span").text
            results.append([_title, _link, _price])
        return True if self.__check_results(results) else False

    def __mediaexpert(self):
        results = []
        ctx = self.__make_request(
            "https://www.mediaexpert.pl/search?query%5Bmenu_item%5D=&query%5Bquerystring%5D=replaceMe&page=1&limit=50&sort=price_desc").find_all('div', class_=['c-grid_col', 'is-grid-col-1'])

        for offer in ctx:
            _header = offer.find("h2", attrs={"data-zone": "OFFERBOX_NAME"})

            try:
                _title = _header.text
                _link = str("https://www.mediaexpert.pl" +
                            _header.find('a')['href'])
                if offer.find("div", class_="is-not_available"):
                    break
                else:
                    _price = offer.find_all(
                        "span", class_="a-price_price")[1].text
                    results.append([_title, _link, _price])
            except:
                pass

        return True if self.__check_results(results) else False

    def __morele(self):
        results = []
        ctx = self.__make_request(
            "https://www.morele.net/kategoria/karty-graficzne-12/?q=replaceMe")

        if ctx.find('div', class_="cat-list-empty"):
            return False

        ctx = ctx.find_all(
            'div', class_="cat-list-products")[0].findChildren("div", recursive=False)

        for i in ctx:
            _main = i.find_all('div', class_='cat-product-content')[0]
            _title = _main.find_all('a', class_='productLink')[0].text.strip()
            _link = str("https://www.morele.net" + _main.find_all('a',
                        class_='productLink')[0]['href']).strip()
            _price = _main.find_all("div", class_="price-new")[0].text.strip()
            results.append([_title, _link, _price])
        return True if self.__check_results(results) else False

    def __komputronik(self):
        results = []
        ctx = self.__make_request(
            "https://www.komputronik.pl/search/category/1099/keywordUrl/0?query=replaceMe&showBuyActiveOnly=1")

        if len(ctx.find("div", class_="corrections").text.strip()) > 0:
            return False

        ctx = ctx.find_all(
            'ul', class_="product-entry2-wrap")[0].findChildren("li", recursive=False)

        for i in ctx:
            _main = i.findChildren("div", recursive=False)
            _title = _main[0].find_all("a")[0].text.strip()
            _link = _main[0].find_all("a")[0]['href'].strip()
            _price = _main[5].find("span", class_="price").text.strip()
            results.append([_title, _link, _price])

        return True if self.__check_results(results) else False

    def __euro(self):
        results = []
        soup = self.__make_request(
            "https://www.euro.com.pl/search/karty-graficzne.bhtml?keyword=replaceMe")

        # if req.history:
        #         self.logger.debug(f"Redirected to {req.url}")
        #         if self.search in soup.title.text:
        #             return [soup.title.text, req.url, "not found pirce"]
        #         else:
        #             return False

        ctx = soup.find("div", id="products").findChildren(
            "div", recursive=False)

        if self.search not in soup.find(id="products-header").find("h1").text or soup.find(id="empty-search"):
            self.logger.debug(f"Not found any interseting cards")
            return False

        for i in ctx:
            _title = i.find_all("a")[2].text.strip()
            _link = str("https://www.euro.com.pl" +
                        i.find_all("a")[2]['href'].strip())
            _price = i.find(
                "div", class_=["price-normal", "selenium-price-normal"]).text.strip()
            results.append([_title, _link, _price])

        return True if self.__check_results(results) else False

    def __electro(self):
        results = []
        ctx = self.__make_request(
            "https://www.electro.pl/search?query%5Bmenu_item%5D=&query%5Bquerystring%5D=replaceMe&page=1&limit=50&sort=").find_all("div", class_="c-offerBox")

        for i in ctx:
            _title = i.find_all('a')[0].text.strip()
            _link = str("https://www.electro.pl" +
                        i.find_all('a')[0]['href'].strip())
            if not i.find_all("div", class_=["c-availabilityNotification_text", "is-heading"]):
                _price = i.find_all(
                    "span", class_="a-price_price")[0].text.strip()
                results.append([_title, _link, _price])
            else:
                pass

        return True if self.__check_results(results) else False
