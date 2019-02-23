from selenium.webdriver import Firefox
from savefullpage import save_fullpage_screenshot
import os, time


class PubMedExtractor:
    def __init__(self):
        # Needed for screenshots
        image_fldr = './PubMed-screenshots-taken-on-' + time.strftime("%Y%m%d-%H%M%S")
        if not os.path.exists(image_fldr):
            os.makedirs(image_fldr)
        self.screenshot_folder = image_fldr

        # All elements that contain article information
        self.article_xpath = '//div[@class=\'rprt\']'

        # To find information about article
        self.article_title_xpath = './/p[@class=\'title\']/a'
        self.article_author_xpath = './/div[@class=\'supp\']/p[@class=\'desc\']'
        self.article_details_xpath = './/div[@class=\'supp\']/p[@class=\'details\']'
        self.article_url_xpath = './/p[@class=\'title\']/a'

        # The next button on the page
        self.nxtbtn_xpath = '//div[@class=\'pagination\']/a[text()=\'Next >\']'
        self.current_page_xpath = '//div[@class=\'title_and_pager bottom\']/div[@class=\'pagination\']/h3[@class=\'page\']/input'

        # Everything the instance has gathered
        self.output = dict(titles=[], authors=[], details=[], urls=[])

    def _append_results_to_output(self, thispage_articles):
        self.output['titles'] += thispage_articles['titles']
        self.output['authors'] += thispage_articles['authors']
        self.output['details'] += thispage_articles['details']
        self.output['urls'] += thispage_articles['urls']

    def button_click(self, browser):
        old_page = browser.find_element_by_xpath(self.current_page_xpath).get_attribute('value')

        next_btn = browser.find_element_by_xpath(self.nxtbtn_xpath)
        next_btn.click()
        time.sleep(2)

        current_page = browser.find_element_by_xpath(self.current_page_xpath).get_attribute('value')

        # If my pagination id hasn't changed, then the button didn't do anything
        if old_page == current_page:
            raise Exception('Attempted button click did not advance page!')

    def get_article_data(self, articles):
        results = dict(titles=[], authors=[], details=[], urls=[])

        for entry in articles:
            title_div = entry.find_element_by_xpath(self.article_title_xpath)
            results['titles'].append(title_div.text)

            author_div = entry.find_element_by_xpath(self.article_author_xpath)
            results['authors'].append(author_div.text)

            details_div = entry.find_element_by_xpath(self.article_details_xpath)
            results['details'].append(details_div.text)

            url_div = entry.find_element_by_xpath(self.article_url_xpath)
            results['urls'].append(url_div.get_attribute('href'))

        self._append_results_to_output(results)

class GoogleExtractor:
    def __init__(self):
        # Needed for screenshots
        image_fldr = './GoogleScholar-screenshots-taken-on-' + time.strftime("%Y%m%d-%H%M%S")
        if not os.path.exists(image_fldr):
            os.makedirs(image_fldr)
        self.screenshot_folder = image_fldr

        # All elements that contain article information
        self.article_xpath = ("//div[contains(@class, 'gs_r') "
                              "and contains(@class, 'gs_or') "
                              "and contains(@class, 'gs_scl')]")

        # The next button on the page
        self.nxtbtn_xpath = ('//div[@id=\'gs_top\']'
                             '/div[@id=\'gs_bdy\']'
                             '/div[@id=\'gs_bdy_ccl\']'
                             '/div[@id=\'gs_res_ccl\']'
                             '/div[@id=\'gs_res_ccl_bot\']'
                             '/div[@id=\'gs_nm\']'
                             '/button[@class=\'gs_btnPR gs_in_ib gs_btn_lrge gs_btn_half gs_btn_lsu\']')

        # Everything the instance has gathered
        self.output = dict(titles=[], authors_year=[], urls=[])

    def _append_results_to_output(self, thispage_articles):
        self.output['titles'] += thispage_articles['titles']
        self.output['authors_year'] += thispage_articles['authors_year']
        self.output['urls'] += thispage_articles['urls']

    def button_click(self, browser):
        old_url = browser.current_url

        next_btn = browser.find_element_by_xpath(self.nxtbtn_xpath)
        next_btn.click()

        # If my url hasn't changed, then the button didn't do anything
        if old_url == browser.current_url:
            raise Exception('Attempted button click did not advance page!')

    def get_article_data(self, articles):
        results = dict(titles=[], authors_year=[], urls=[])

        for entry in articles:
            # Not every title has a convenient url to grab
            try:
                title_div = entry.find_element_by_css_selector('h3.gs_rt a')
                results['titles'].append(title_div.text)
            except:
                results['titles'].append(entry.text.split('\n')[1])  # To-Do: rewrite as regex

            author_year_div = entry.find_element_by_css_selector('.gs_a')
            results['authors_year'].append(author_year_div.text)

            url_divs = entry.find_elements_by_css_selector('.gs_or_ggsm a')

            all_links = ''
            for url in url_divs:
                all_links += url.get_attribute('href') + '\n'

            results['urls'].append(all_links)

        self._append_results_to_output(results)


# Generic extractor class.
class TitleExtractor:
    def __init__(self, search_engine):
        self.browser = Firefox()
        self.currentpage = 1

        # defining things that are specific to the search engine
        if search_engine == "g":
            self.browser.get("https://scholar.google.com/")
            self.extractor = GoogleExtractor()
        elif search_engine == "p":
            self.browser.get("https://www.ncbi.nlm.nih.gov/pubmed/")
            self.extractor = PubMedExtractor()

    def _extract_data_from_page(self):
        articles = self.browser.find_elements_by_xpath(self.extractor.article_xpath)

        self.extractor.get_article_data(articles)

    def _try_clicking(self):
        self.extractor.button_click(self.browser)

    def _take_screen_shot(self):
        image_fldr = './' + self.extractor.screenshot_folder + '/image-of-page-' + str(self.currentpage)
        if not os.path.exists(image_fldr):
            os.makedirs(image_fldr)
        else:
            raise Exception("screenshot of url queried already exists. remove these files first")
        save_fullpage_screenshot(self.browser, image_fldr)
        self.currentpage += 1

    def execute_multipage_extraction(self):

        nxtbtn = True
        while nxtbtn:
            # first take a screen shot just in case we need to go back and visually inspect the search results
            self._take_screen_shot()

            # results automatically recorded in the extractor class output field
            self._extract_data_from_page()

            usr_ans = {'y': True, 'n': False, '': True}

            try:  # click the next button to load another page
                self._try_clicking()

            except:
                # Check for captcha. User will need to click for us.
                print('\nSo looks like we weren\'t able to click over...\n'
                      'We will need some human assistance here.\n'
                      'Please solve any captcha and click the button to load the next page.\n')

                ispageloaded = input("Has the next page loaded? (If there are no more pages, just say 'n') [y/n]: ")

                if not usr_ans[ispageloaded]:
                    nxtbtn = False
                    self.browser.quit()

        return self.extractor.output

