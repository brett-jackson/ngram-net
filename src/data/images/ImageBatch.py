from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
class ImageBatch:
    def __init__(self,proxy=False):
        if proxy:
            chrome_options = Options()
            chrome_options.add_extension(proxy)
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            print("Using proxy extension"+str(proxy))
        else:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    def fetch_image_urls(self, query, max_links_to_fetch, sleep_time = 1):
        
        # build the google query
        search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
    
        # load the page
        self.driver.get(search_url.format(q=query))
    
        image_urls = set()
        image_count = 0
        results_start = 0
        while image_count < max_links_to_fetch:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(sleep_time) 
    
            # get all image thumbnail results
            thumbnail_results = self.driver.find_elements(by=By.CSS_SELECTOR,value="img.Q4LuWd")
            number_results = len(thumbnail_results)
            
            print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
            
            for img in thumbnail_results[results_start:number_results]:
                # try to click every thumbnail such that we can get the real image behind it
                try:
                    img.click()
                    time.sleep(sleep_time)
                except Exception:
                    continue
    
                # extract image urls    
                actual_images = self.driver.find_elements(by=By.CSS_SELECTOR,value='img.n3VNCb')
                for actual_image in actual_images:
                    if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                        image_urls.add(actual_image.get_attribute('src'))
    
                image_count = len(image_urls)
    
                if len(image_urls) >= max_links_to_fetch:
                    print(f"Found: {len(image_urls)} image links, done!")
                    break
            else:
                print("Found:", len(image_urls), "image links, looking for more ...")
                time.sleep(30)
                return
                load_more_button = self.driver.self.driver.find_elements(by=By.CSS_SELECTOR,value=".mye4qd")
                if load_more_button:
                    self.driver.execute_script("document.querySelector('.mye4qd').click();")
    
            # move the result startpoint further down
            results_start = len(thumbnail_results)
        self.image_urls=image_urls
        return image_urls
