VERSION = 23.1121

import sys
import os
import pickle
import time
import random
import urllib.request
from datetime import datetime

from util import conf, db
from workman.worker import Worker

try:
	from selenium import webdriver
	from selenium.webdriver.common.keys import Keys
	from selenium.webdriver.common.by import By
	from selenium.webdriver.common.action_chains import ActionChains
	from selenium.common.exceptions import *
except ImportError:
	print("http://selenium-python.readthedocs.io/installation.html")
	print("Selenium and Selenium Chrome webdriver must be installed on your system to run this program.")


tbl = db.Table('Captions',
    caption = "text NOT NULL",
    title = "text",
    username = "varchar(50)",
    url = "varchar(500)",
    referer = "varchar(500)"
)


class Logger:
    def __init__(self, cb : callable = None) -> None:
        self.callback = cb

    def _notify(self, msg):
        print("\n", msg, flush=True)
        if self.callback: self.callback(msg)

    def add_callback(self, cb : callable):
        self.callback = cb

    def i(self, msg, *arg):
        self._notify("I :: " + str(msg).format(*arg))

    def w(self, msg, *arg):
        self._notify("W :: " + str(msg).format(*arg))

    def E(self, msg, *arg):
        self._notify("E :: " + str(msg).format(*arg))

    def Q(self, msg, *arg):
        self._notify("QUIT :: " + str(msg).format(*arg))


class SeleniumBrowser:
    def __init__(self) -> None:
        self.url = None
        self.visited = []
        self.captions = []
        self.driver = None
        self.cookie_file = 'cookies.pkl'
        self.visited_file = 'visited.pkl'
        self.log : Logger = Logger()

    def set_logger(self, logger : Logger):
        self.log = logger

    def launch_chrome(self, headless = False):
        chromedriver = os.path.join(os.getcwd(), "chromedriver")
        os.environ["webdriver.chrome.driver"] = chromedriver

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--disable-blink-features")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        if headless:
            options.add_argument('--headless')

        try:
            self.driver = webdriver.Chrome(options=options)
        except:
            raise RuntimeError("Could not load Chrome. Please install Chrome webdriver and add it to the environment PATH.")
        
    def init(self, page : str = None):
        self.driver.set_window_size(770,640)
        self.driver.set_window_position(-5,0)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride',
                            {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})        
        self.driver.set_page_load_timeout(5)

        if page:
            self.navigate(page)
        self.loadStuff()

    def _saveCookies(self):
        pickle.dump(self.driver.get_cookies(), open(self.cookie_file, 'wb'))
        print("Cookies saved:", self.cookie_file)

    def _loadCookies(self):
        if not os.path.exists(self.cookie_file):
            return

        try:
            cookies = pickle.load(open(self.cookie_file, "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        except Exception as err:
            self.log.E("failed to load cookies from {}", self.cookie_file)
            self.log.E("Error: {}", err)
            pass

    def loadStuff(self):
        try:
            self.visited = pickle.load(open(self.visited_file, 'rb'))
            print("Load OK:", len(self.visited), "past visited links.")
        except Exception as e:
            print(e)
        self._loadCookies()

    def saveCaptions(self, savepath):
        with open(savepath, 'w') as fp:
            fp.writelines([l + "\n" for l in self.captions])
        self.log.i("Save OK: {}", savepath)

    def saveOnly(self):
        pickle.dump(self.visited, open(self.visited_file, 'wb+'))
        self._saveCookies()

    def saveNQuit(self):
        self.saveOnly()
        raise RuntimeError("Quit called")

    def wait(self, reason):
        ttw = random.uniform(3, 5)
        print("     -- waiting {:.2f} secs - {}".format(ttw, reason))
        time.sleep(ttw)

    def download(self, url : str, savepath : str):
        userAgent = self.driver.execute_script("return navigator.userAgent;")
        seleniumCookies= self.driver.get_cookies()
        cookies = ''
        for cookie in seleniumCookies:
            cookies += '%s=%s;' % (cookie['name'], cookie['value'])

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', userAgent)]
        opener.addheaders.append(('Cookie', cookies))
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, savepath)
        self.visited.append(url)
        self.log.i("Download OK: {}", savepath)
        self.wait('download')

    def _clean_text(self, text : str) -> str:
        valid = []
        for sent in text.split(". "):
            sent = sent.strip()
            lowercased = sent.lower()
            words = lowercased.split()
            criteria = [
                len(words) < 4,
                len(sent) < 4,
                '%' in lowercased,
                'markup' in lowercased,
            ]
            if not any(criteria):
                valid.append(sent + ".")

        text = " ".join(valid)
        return text

    def addCaption(self, text : str, by : str, title : str, referer : str):
        self.captions.append(text)
        self.log.i("Caption [{}] => {}", by, text)
        tbl.insert_row(
            caption = text,
            url = self.url,
            username = by,
            title = title,
            referer = referer,
        )

    def navigate(self, url):
        try:
            print("Loading page -", url)
            try:
                self.url = url
                self.visited.append(url)
                self.driver.get(url)
                print("Load OK: {}", url)
            except:
                pass
            self.wait('page load')
        except Exception as err:
            self.log.E("Page navigation error: {}", err)


class IWCBrowser(SeleniumBrowser):
    def __init__(self, baseurl) -> None:
        super().__init__()
        self.baseurl = baseurl
        self.outpath = "services/data/"
        self.cookie_file = os.path.join(self.outpath, self.cookie_file)
        self.visited_file = os.path.join(self.outpath, self.visited_file)

    def init(self):
        os.makedirs(self.outpath, exist_ok=True)
        super().init(self.baseurl)
        self.acceptPopup()

    def acceptPopup(self):
        try:
            enter = self.driver.find_elements(By.ID, "enter")[0]
            ActionChains(self.driver).move_to_element(enter).click().perform()
        except: pass

    def parseMediaLinks(self, page):
        folder = os.path.join(self.outpath, page.split("/")[-1])
        os.makedirs(folder, exist_ok=True)
        self.acceptPopup()

        videos = self.driver.find_elements(By.XPATH, "//video")
        for vid in videos:
            src = vid.get_attribute('data-src')
            if not src:
                src = vid.get_attribute('src')
            if not src:
                self.log.E("Failed to identify video src")
                continue

            if src not in self.visited:
                try:
                    savepath = os.path.join(folder, src.split("/")[-1])
                    self.download(src, savepath)
                except Exception as err:
                    self.log.E("Download failed: {}", err)


    def parseMediaDesc(self, page):
        accname = page.split("/")[-1]
        self.acceptPopup()
        innerpages = [
            item.get_attribute('href')
            for item in self.driver.find_elements(
                By.XPATH, "//div[@class='pop-hitarea']//a[@class='click-hit']")
        ]

        if not innerpages:
            self.log.E("No innerpages found: {}", self.url)
            return

        referer = self.url
        old = None

        for url in innerpages:
            if url in self.visited:
                continue
            self.navigate(url)
            self.acceptPopup()

            accname = self.url.split("/")[5]

            desc = self.driver.find_elements(
                By.XPATH,
                "//div[@id='description-collapse']//div[contains(@class, 'description')]//span")
            
            titleEl = self.driver.find_elements(
                By.XPATH, "//div[contains(@class, ' title')]//span")
            
            if len(titleEl):
                title = titleEl[0].get_attribute('innerText')
            else: title = ""
            
            if len(desc):
                text = desc[0].get_attribute('innerText')
                if text != old:
                    self.addCaption(text, accname, title, referer)
                    old = text

        savepath = os.path.join(self.outpath, accname + ".txt")
        self.saveCaptions(savepath)
        self.saveOnly()


    def gotoPage(self, page, *, i = 0, media=False):
        url = page
        while url in self.visited:
            i += 1
            if i <= 1:
                pagesuffix = ""
            else:
                pagesuffix = "?page=%d" %i
            url = page + pagesuffix
        
        self.navigate(url)
        if media:
            self.parseMediaLinks(page)
        self.parseMediaDesc(page)
        self.saveOnly()


if __name__ == '__main__':
    # Run once. -----------------------
    tbl.index('caption', 'text')
    tbl.index('username', 'varchar')
    tbl.create_all()

    if len(sys.argv) < 2:
        workerid = 'iwc-worker'
    else:
        workerid = sys.argv[1]

    browser = IWCBrowser(conf.Workers.iwc_url)
    browser.launch_chrome(headless=True)
    browser.init()

    with Worker(conf.WorkMan.mgr_url, 'iwc-caption', workerid) as worker:
        worker.define(
            "IWC", "Crawl IWC pages",
            page = dict(type=str, help="Page/URL to crawl."),
            media = dict(default=False, help="Download media or not."),
        )

        while True:
            request = worker.receive()
            media = request.media.lower() not in ["", "no", "false", "0"]
            browser.log.add_callback(worker.update)

            try:
                browser.gotoPage(request.page, media=media)
            except Exception as err:
                browser.log.Q("Exception raised: {}", err)
            finally:
                worker.done(f"Done: {request.page}")
                browser.log.callback = None
