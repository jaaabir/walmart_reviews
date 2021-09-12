import requests 
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome import options 
from selenium.webdriver.common.action_chains import ActionChains

def get_categories_link(diver):
    sleep(2)
    print('Getting all the categories link ...')
    divs = driver.find_elements_by_class_name('TempoTileCollapsible.FeaturedCategoriesCollapsible')[0]
    cate = divs.find_elements_by_tag_name('a')
    links = []
    for i in cate:
        links.append(i.get_attribute('href'))

    return links

def detect_captcha(driver):
    sleep(3)
    # captcha = driver.find_element_by_class_name('TTXkfzzNvqrLRZT')
    try:
        captcha = driver.find_element_by_class_name('re-captcha')
    except selenium.common.exceptions.NoSuchElementException as error:
        captcha = None
        print('captcha not found')
    if captcha:
        print('captcha detected ...')
        action = ActionChains(driver)
        # print(captcha.get_attribute('innerHTML'))
        action.click_and_hold(on_element = captcha.find_element_by_id('px-captcha'))
        action.pause(6).perform()
        print('finished holding the captcha ...\nwaiting for redirect ...') 
        sleep(60)

def all_products_links(driver):
    products = []
    ul = driver.find_element_by_class_name('search-result-gridview-items.four-items')
    lists = ul.find_elements_by_tag_name('li')
    for li in lists:
        try:
            review = int(li.find_element_by_class_name('stars-reviews-count').text.split()[0])
        except selenium.common.exceptions.NoSuchElementException as err:
            review = 0
        # 
        # print('review : ' + review)
        if review >= 5:
            href = li.find_element_by_class_name('product-title-link.line-clamp.line-clamp-2.truncate-title').get_attribute('href')
            products.append(href)
    
    return products

def get_page_nums(driver, curr_pg = 1):
    ul = driver.find_element_by_class_name('paginator-list')
    a = ul.find_elements_by_tag_name('a')
    final_pg = a[-1].get_attribute('href')
    final_pg_num = int(a[-1].text)
    return final_pg, final_pg_num

    # for ind,pg in enumerate(a):
    #     if pg.get_attribute('class') == 'active':
    #         print(pg.get_attribute('aria-label'))
    #         num = pg.text
    #         if num == curr_pg: return 0
    #         elif num
    #         return int(pg.text) + 1

def get_products(pname, url, driver):
    url = f"https://www.walmart.com/search/?query={pname}&recall_set=primary" if pname else url
    print(url)
    print('scraping all products link')
    curr_page_num = 1
    products = []
    driver.get(url)    
    detect_captcha(driver)
    sleep(6)
    final_pg_url, find_pg_num = get_page_nums(driver)
    products += all_products_links(driver)
    # while curr_page_num < find_pg_num:
    #     curr_page_num += 1
    #     url = final_pg_url.replace('page=21', f'page={curr_page_num}')
    #     driver.get(url)
    #     sleep(5)
    #     products += all_products_links(driver)

    print('finished scraping all products links')
    return products

def get_details(driver, only_reviews = True):
    reviews = driver.find_elements_by_tag_name('p')
    prod_name = driver.find_element_by_class_name('prod-ProductTitle.no-margin.truncated.wyr-product-title.font-normal.hide-content-max-s.heading-b')
    prod_cate = driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "breadcrumb", " " ))]//a[(((count(preceding-sibling::*) + 1) = 1) and parent::*)]')
    return reviews if only_reviews else prod_name, prod_cate, reviews

def get_reviews(prods, driver):
    all_prod_details = dict()
    print('scraping all products reviews')
    for prod in prods:
        item_id = prod.split('/')[-1]
        url = f'https://www.walmart.com/reviews/product/{item_id}?page=1'
        curr_page_num = 1
        all_reviews = []
        driver.get(url)
        detect_captcha(driver)
        sleep(5)
        prod_name, prod_cate, prod_reviews = get_details(driver, False)
        all_reviews += prod_reviews
        final_pg_url, find_pg_num = get_page_nums(driver)

        while curr_page_num < find_pg_num:
            curr_page_num += 1
            url = url.replace('page=1', f'page={curr_page_num}')
            driver.get(url)
            sleep(5)
            all_reviews += get_details(driver)

        print(f'Finished scraping all the reviews for {prod_name}')
        all_prod_details[prod_name] = {
            'category' : prod_cate,
            'reviews' : all_reviews
        }

    return all_prod_details

url = 'https://www.walmart.com/'
options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])
with webdriver.Chrome( executable_path = 'C:\geckodriver-v0.27.0-win64\chromedriver.exe', options = options) as driver:
# with webdriver.Firefox( executable_path = 'C:\geckodriver-v0.27.0-win64\geckodriver.exe') as driver:
    cookie = 'TB_Latency_Tracker_100=1; TB_Navigation_Preload_01=1; vtc=csAPSMFQ7i4WyWQn_snW2A; TS013ed49a=01538efd7c3e052d3ba248b03a18557b38b79adee2cebe0461b54f1bc407dab22dad36e85bfc765964d26751a22df0ea9ba8adc82f; TBV=7; pxcts=61fce360-12d5-11ec-9b2e-37dc4946b010; _pxvid=06ff03b2-12d3-11ec-bed8-43536b50654a; cart-item-count=0; _gcl_au=1.1.941604196.1631346824; viq=Walmart; tb_sw_supported=true; TB_SFOU-100=1; cbp=876662893-1631350383976; athrvi=RVI~h3440d06d; TS012768cf=010a1f4366522d212f2c1178ba4d7d9df6a19992535e7a1b4668db3c846d4202753342252a4224c7107693c1f216de1fd23df687c6; TS01a90220=010a1f4366522d212f2c1178ba4d7d9df6a19992535e7a1b4668db3c846d4202753342252a4224c7107693c1f216de1fd23df687c6; TS53c903a2027=088f51dd52ab2000d9450d4054ab5521def1ac323f3269a813c6e8e4cc744f7757bacb88c5a95d4e0836131ea11130004d5adb717e4e0dc149f93672999822037d744a72a5dca71745022b04e6f4e1927be38a93ffcfe7f0d4833ff324937536; _sp_id.ad94=60a6b53f-3e79-45ef-aabf-b9465df7cf05.1631350389.2.1631357217.1631350392.d76750f8-d2bd-4b2e-b5e1-2b1240bd8baa; _ga=GA1.2.1049020711.1631363457; _gid=GA1.2.1711467022.1631363457; _pxhd=434I/MmPEU3g6K-rTFPFqbT/6q44/shxObPvY7MS80lQNimHXpLnjAX25wAMYSmmtI88QiBwWjlE-PPGIsWC-w==:usZUXb6KZvzda2ln1f-Fglm4v-qbRtHe45a-ZhjBbFu3myOfzGxbFnIJC5NK3wLPrZYI3gYdnbofw4VBrhUjNj9xY4lI6rfXjtTcF9lKNyU=; DL=94066%2C%2C%2Cip%2C94066%2C%2C; _abck=izo2hizmsddlb2ofsbas_2037; rtoken=MDgyNTUyMDE4BprLG0%2FxBWUHweHPfmCJillWqBAaj2QR3B9u%2B6uJOxkkDAwedz%2BRH27CdnVeaaCgSR%2BsfMz4iar9%2FfIKkgjtjooMGd6hdQrncJnF4VUykW2GPdOrmoVdnaSnkEaB1oxkPEakwa%2FyN6zOk8kXuKwdI3rMPoNMFFVoifoV35kqL4DPEwm6rj3PcaxoyG3axBut%2BM%2FkY8nxIZINwWb%2Bg8tFaZqPky0K6hHbyYd6PaYhlqIvBc65M5ZjbYvdmmmnKBjiLsfcLED2ShA2eog0q9uU2BiVQ0Fccg%2BhGbd9Kd1ftkgcGysbAs6Fnk0BBOn8EJ4VRAaBsGXYjXIWyIkbC104F%2BErr6pW5jiSnMHn6anGCpH4B2GjoX%2FKct%2F6jv4M%2F4XLZFqFEGHvPUhboUZh6Z5NgJ0xFt6zfk0dItWbF0UUcZo%3D; SPID=d7df859a43a50763d9ac9936cca34ed200d37ec22f67ceff1ec00bd988cff1dff0fd6a96f3df6643e5d573e2fa851448cprof; CID=2292f5f4-f284-4538-816f-ec08d67dd1e5; hasCID=1; customer=%7B%22firstName%22%3A%22muhammed%22%2C%22lastNameInitial%22%3A%22j%22%2C%22rememberme%22%3Atrue%7D; type=REGISTERED; WMP=4; TS01af768b=01538efd7c78e83767eb7e8e21eaaff5906e948135c3a70944efb6e8be485e3bcf9d9b23ebf3faa47f94884d3387838da34ec4706f; TS012c809b=01538efd7c78e83767eb7e8e21eaaff5906e948135c3a70944efb6e8be485e3bcf9d9b23ebf3faa47f94884d3387838da34ec4706f; ONEAPP_CUSTOMER=true; member=0; GCRT=9dc215cc-cee8-47ad-888b-6294e86735f3; hasGCRT=1; s_vi=[CS]v1|309E804C32803DE7-40001BEA68CCA724[CE]; s_pers_2=+s_fid%3D1E1B6AC73DAFA945-351646D871F4F067%7C1694460002380%3B+s_v%3DY%7C1631389802387%3B+s_cmpstack%3D%255B%255B%2527wmt%2527%252C%25271631388002416%2527%255D%255D%7C1789154402416%3B+gpv_p11%3DHomepage%7C1631389802449%3B+gpv_p44%3Dno%2520value%7C1631389802455%3B+s_vs%3D1%7C1631389802466%3BuseVTC%3DN%7C1694503228; TS01bae75b=01538efd7c6072b847370bfff6c9d3c81e404682fda08c7d760f01ef92acdbf89c2f579159fb985b69b46592dd15f2523bd9454427; wm_ul_plus=INACTIVE|1631474574050; wm_mystore=Fe26.2**753ccaff77617a3cc5f23ec1967d39b1299f0fa8e67c7bfe0109f75174ecf0ef*rd8N_VlncSFG-vpL7KY-lA*8WILnnKm5i-a4C2KDVgCuf3r7Yv1fIUKj0q320kbzSD-spZ7kDw9mOwsKzYzpgpTgpzLeYD32bNW4fxnaMDF-c4y4eKo6oZoqHsyPBMlct0B3_McG1yiypacytqV0JSAMmm0aLiBPtH5tba8JORCu6z8wJKDS6P2dKf-CTNaQh98-Qr6DautUAhGbYh8My8SD4OOSRutfawf7YJZ9Fm9qO9ydM2S5kBrE0rg9eyPefrXkzxyjkgxLl-OXBOZ8IlDsjETjfQ4XwoTF7Dw8tzLVwGKiXKXrwTxwqcD0KhNLEh2-A4djTh6h79LvYkqLieZVFKvrTnIvWyuSSGpWpWEU4wOPnng1cNquP5pUynbGZGqcOBG0X-LxRYWdMh8CAE-ae2iGXDINSJAtDYckfiFsY-8FHRFjpuYW3rmfnkXdEgRUvn9XOUYTKfM20VNtEelPxcHQnbtqQBUYPwqYuJAy-YbiMuNKU7_svBEQGcV25kvEOVnfI2BLblW_IF-e2NutFYqgAtJjijD8JGTIEc_49E5Ox4hwQvh3hy2m4CdLo8ON7yclaM5340FbBu-pplQ2PFvBjgrrxn3Em6-pkeJlwUhF7Dsq2GZQB_5UfaVe0Xbci1USCRAnoqH6_RGIZ4h690EOKAbpbFJBE_hpLx1dgiK2BElRWtvJI8ZSHnEQU8azuRYxiVuDGrM9zQWpinyTbU1KfL7gUWoEvnwZ8hqdfgzys67I_vngck6N1YL9pUmI2ltMYE3AjhqmXGvTTvzYE-HciheJFJ2ycTy7tSgJl_365NqISqpQinGOR_q_3SGUg4dQR2Gmt21ijNYQFVN32mqy0kCEPuem2s1WAY8dtxZNMuDi1BF1QNoqCmYifW__0lvz7YYdB2A86h2z2DN-GXWvwqaHp1FgTA46E_MHT7XDWbd-Fotqah_5Vy7AXwlgNzetcvvQxz1BSxtCxo4BcLlMEf_SiSoiSDYcLvdLg**5455d2ebf994115e87a237e5748030742c20e16b201531bccf65295ac9e84475*Y6HFs60CcQAJMtV_VUbw4PJcq5DEQjgldPZ05A0awqw; s_pers=%20s_fid%3D1E1B6AC73DAFA945-351646D871F4F067%7C1694460175075%3B%20s_v%3DY%7C1631389975082%3B%20s_cmpstack%3D%255B%255B%2527wmt%2527%252C%25271631388175115%2527%255D%255D%7C1789154575115%3B%20gpv_p11%3DHomepage%7C1631389975119%3B%20gpv_p44%3Dno%2520value%7C1631389975126%3B%20s_vs%3D1%7C1631389975136%3B; s_sess=%20cmp%3Dwmt%253A%3B%20ent%3DLAY_VIEWzipgate_geo_sniff%3B%20s_cc%3Dtrue%3B%20chan%3Dwmt%3B%20v59%3D%3B%20v54%3DHomePage%257COVERLAY_VIEW%2520zipgate_geo_sniff%3B%20cps%3D0%3B%20s_sq%3D%3B; x-csrf-jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiY29va2llIiwidXVpZCI6ImFhOGQ4YWMwLTEzMzUtMTFlYy05NmU4LWUxYzFiOTQzYjNmNiIsImlhdCI6MTYzMTM4ODE3NSwiZXhwIjoxNjMyNDY4MTc1fQ.502_sHnR_-d3C_rQBQxHInhyNPAY28H4JPgyFHe2u0Q; akavpau_p14=1631388776~id=1e319892497a28574674555b55f0eb52; s_sess_2=ps%3D1; bstc=dAgCYMaUsWnpjCBaOZVPvw; next-day=1631466900|true|false|1631534400|1631421962; location-data=94066%3ASan%20Bruno%3ACA%3A%3A0%3A0|21k%3B%3B15.22%2C46y%3B%3B16.96%2C1kf%3B%3B19.87%2C1rc%3B%3B23.22%2C46q%3B%3B25.3%2C2nz%3B%3B25.4%2C2b1%3B%3B27.7%2C4bu%3B%3B28.38%2C2er%3B%3B29.12%2C1o1%3B%3B30.14|2|7|1|1xun%3B16%3B0%3B2.44%2C1xtf%3B16%3B1%3B4.42%2C1xwj%3B16%3B2%3B7.04%2C1ygu%3B16%3B3%3B8.47%2C1xwq%3B16%3B4%3B9.21; TB_DC_Flap_Test=0; mobileweb=0; xpa=U20On|ZBgxL|lJPtJ|mIMAn; xpm=1%2B1631421962%2BcsAPSMFQ7i4WyWQn_snW2A~2292f5f4-f284-4538-816f-ec08d67dd1e5%2B0; auth=MTAyOTYyMDE4sZi1Lg0n8vmRqGuc1OqAVtBBEICKwwJ0E3M9F7e25YD%2BMSt0kMxfgCMTi8QxjM%2FziNc%2BHeET1YhIw2ec2Ma16zreKh7yCzxu8zVUwgzKsi52faNy4xK57I8j8gR%2FH852oHOs%2FstByN418DB3KSmMosRPrkijxYcdFnUG2KNSZRMTUCuFRBUh2riAhtb%2BYLfn2xqx21RPz1E4%2BIXsiB9oZ2xVon1qX0ChQbDsykETs9h2lkaFTC28LdzqmkDL%2FoZNywI05adPtwc9%2Fm5r1ONHR6nYz%2Fp5v4ioBEi2OQR5GuBEUU6k0zfluyxhJkOB9bk2c5sQw%2FDv%2BEP3%2FfxBwwF3MJ8V0amnEL4sjMVTejpky8S1lp5myXlO6v8ngJdyxui9iUV%2FDQDbMM%2BX6eG6uGwydEjyrOXbKKhH072NS%2FW0j%2FU%3D; _uetsid=6342f46012d511ec85ffdb184224d845; _uetvid=63433ad012d511ecaef53f9d92d075df; com.wm.reflector="reflectorid:0000000000000000000000@lastupd:1631422464244@firstcreate:1631383640836"; xptwg=930850280:55BF4032EFFE98:E1BE00:9449CE31:351526AE:92095721:; TS01b0be75=01538efd7c5e40d3ec71df10b0e3779f31ecd11e073073f8b2b0a12934b189cc6e6e78bbb1be0ce0607b6976356ef5cf5cd6a3438d; akavpau_p8=1631423064~id=b44082e214422398add2a73dcb4721cc'
    url = 'https://www.walmart.com/browse/clothing/womens-clothing-apparel/5438_133162?athcpid=4b5ee050-63f5-4e43-bf4b-8bba10fc6bfc&athpgid=athenaHomepage&athznid=athenaModuleZone&athmtid=AthenaFeaturedCategory&athtvid=1&athena=true'
    try:
        prods = get_products(None, url, driver)[0:]
        details = get_reviews(prods, driver)
        print(details)
    except selenium.common.exceptions.NoSuchElementException as err:
        print(err)


# cate_links = get_categories_link(driver)
    # for link in cate_links:
    #     driver.get(link)
    #     detect_captcha(driver)
    #     print(driver.title)
    #     sleep(1)
# driver.add_cookie({'name' : 'cookie', 'value' : cookie})
    # driver.get(url)
    # detect_captcha(driver)