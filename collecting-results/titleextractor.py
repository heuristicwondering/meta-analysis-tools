from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from savefullpage import save_fullpage_screenshot
import os, time


class CochraneReviewsExtractor:
    def __init__(self):
        # Cochrane can search several types of info, this specifies which
        self.table_name = self._set_table_name()

        #

        # Needed for screenshots
        image_fldr = './Cochrane-' + self.table_name + '-screenshots-taken-on-' + time.strftime("%Y%m%d-%H%M%S")
        if not os.path.exists(image_fldr):
            os.makedirs(image_fldr)
        self.screenshot_folder = image_fldr

        # All elements that contain article information
        self.article_xpath = '//div[@class=\'search-results-section-body\']/div[@class=\'search-results-item\']'

        # To find information about article
        if self.table_name == "Reviews":
            self.article_title_xpath = './div[@class=\'search-results-item-body\']/h3[@class=\'result-title\']/a'
            self.article_author_xpath = './div[@class=\'search-results-item-body\']/div[@class=\'search-result-authors\']/div'
            self.article_url_xpath = './div[@class=\'search-results-item-body\']/h3[@class=\'result-title\']/a'

        elif self.table_name == "Trials":
            self.article_title_xpath = './div[@class=\'search-results-item-body\']/h3[@class=\'result-title\']/a'
            self.article_author_xpath = './div[@class=\'search-results-item-body\']/div[@class=\'search-result-authors\']/div'
            self.article_url_xpath = './div[@class=\'search-results-item-body\']/h3[@class=\'result-title\']/a'

        # The next button on the page
        self.nxtbtn_xpath = '//div[@class=\'pagination-next-link\']/a'
        self.current_page_xpath = '//div[@class=\'pagination-page-links\']/ul[@class=\'pagination-page-list\']/li[@class=\'pagination-page-list-item active\']/a'

        # Everything the instance has gathered
        self.output = dict(titles=[], authors=[], urls=[])
    def _append_results_to_output(self, thispage_articles):
        self.output['titles'] += thispage_articles['titles']
        self.output['authors'] += thispage_articles['authors']
        self.output['urls'] += thispage_articles['urls']

    def _set_table_name(self):
        table_names = dict(r='Reviews', t='Trials')

        print('\nCochrane Reviews can search several types of information.\n'
              'Right now I can only scrape one of these types at a time.\n')

        while True:
            table_type = input('Which data do you want to scrape?\n'
                               '[r] Reviews, [t] Trials: ').lower()
            if table_type in ["r", "t"]:
                break
            else:
                print('\nThese are the only things I\'m built to grab. Please pick one.\n')

        return table_names[table_type]

    def button_click(self, browser):
        old_page = int(browser.find_element_by_xpath(self.current_page_xpath).text)
        next_btn = browser.find_element_by_xpath(self.nxtbtn_xpath)
        next_btn.click()
        time.sleep(10)
        # scroll to top of page after load
        ActionChains(browser).key_down(Keys.CONTROL).send_keys(Keys.HOME).perform()
        time.sleep(1)
        current_page = int(browser.find_element_by_xpath(self.current_page_xpath).text)

        # If my pagination id hasn't changed, then the button didn't do anything
        if old_page == current_page:
            raise Exception('Attempted button click did not advance page!')

    def get_article_data(self, articles):
        results = dict(titles=[], authors=[], urls=[])


        for entry in articles:
            title_div = entry.find_element_by_xpath(self.article_title_xpath)
            results['titles'].append(title_div.text)

            author_div = entry.find_element_by_xpath(self.article_author_xpath)
            results['authors'].append(author_div.text)

            url_div = entry.find_element_by_xpath(self.article_url_xpath)
            results['urls'].append(url_div.get_attribute('href'))

        self._append_results_to_output(results)

class ClinicalTrialsExtractor:
    def __init__(self):
        # Needed for screenshots
        image_fldr = './ClinicalTrialsGov-screenshots-taken-on-' + time.strftime("%Y%m%d-%H%M%S")
        if not os.path.exists(image_fldr):
            os.makedirs(image_fldr)
        self.screenshot_folder = image_fldr

        # All elements that contain article information
        self.article_xpath = '//table[@id=\'theDataTable\']/tbody/tr'

        # To find information about article
        self.article_title_xpath = './/td[4]'
        self.article_status_xpath = './/td[3]'
        self.article_intervention_xpath = './/td[6]/ul/li'
        self.article_condition_xpath = './/td[5]/ul/li'
        self.article_location_xpath = './/td[7]/ul/li'
        self.article_url_xpath = './/td[4]/a'

        # The next button on the page
        self.nxtbtn_xpath = '//div[@id=\'theDataTable_paginate\']/a[@id=\'theDataTable_next\']'

        # The current page of results
        self.pagination = '//div[@id=\'theDataTable_wrapper\']/div[@id=\'theDataTable_info\']'

        # Everything the instance has gathered
        self.output = dict(titles=[], status=[], conditions=[], interventions=[], locations=[],  urls=[])

    def _append_results_to_output(self, thispage_articles):
        self.output['titles'] += thispage_articles['titles']
        self.output['status'] += thispage_articles['status']
        self.output['conditions'] += thispage_articles['conditions']
        self.output['interventions'] += thispage_articles['interventions']
        self.output['locations'] += thispage_articles['locations']
        self.output['urls'] += thispage_articles['urls']

    def button_click(self, browser):
        old_page = browser.find_element_by_xpath(self.pagination)
        old_page = old_page.text

        next_btn = browser.find_element_by_xpath(self.nxtbtn_xpath)
        next_btn.click()
        time.sleep(2)

        current_page = browser.find_element_by_xpath(self.pagination)
        current_page = current_page.text

        # If my url hasn't changed, then the button didn't do anything
        if old_page == current_page:
            raise Exception('Attempted button click did not advance page!')

    def get_article_data(self, articles):
        results = dict(titles=[], status=[], conditions=[], interventions=[], locations=[],  urls=[])

        for entry in articles:
            title_div = entry.find_element_by_xpath(self.article_title_xpath)
            results['titles'].append(title_div.text)

            status_div = entry.find_element_by_xpath(self.article_status_xpath)
            results['status'].append(status_div.text)

            condition_div = entry.find_elements_by_xpath(self.article_condition_xpath)
            condition = ''
            for div in condition_div:
                condition += div.text + '\n'
            results['conditions'].append(condition)

            intervention_div = entry.find_elements_by_xpath(self.article_intervention_xpath)
            intervention = ''
            for div in intervention_div:
                intervention += div.text + '\n'
            results['interventions'].append(intervention)

            location_div = entry.find_elements_by_xpath(self.article_location_xpath)
            location = ''
            for div in location_div:
                location += div.text + '\n'
            results['locations'].append(location)

            url_div = entry.find_element_by_xpath(self.article_url_xpath)
            results['urls'].append(url_div.get_attribute('href'))

        self._append_results_to_output(results)


class NIHreporterExtractor:
    def __init__(self):
        # NIH can search several types of info, this specifies which
        self.table_name = self._set_table_name()

        # Needed for screenshots
        image_fldr = './NIHrePORTER-' + self.table_name + '-screenshots-taken-on-' + time.strftime("%Y%m%d-%H%M%S")
        if not os.path.exists(image_fldr):
            os.makedirs(image_fldr)
        self.screenshot_folder = image_fldr

        # All elements that contain article information
        self.article_xpath = '//div[@class=\'proj_tab_content\']/table/tbody/tr'

        # To find information about article
        if self.table_name == "Projects":
            self.article_title_xpath = './td[4]'
            self.article_author_xpath = './td[5]'
            self.article_url_xpath = './td[4]/a'
            self.article_projectID_xpath = './td[2]/table[@class=\'proj_search_pnum\']/tbody/tr/td[3]/a'
        elif self.table_name == "Publications":
            self.article_title_xpath = './td[2]'
            self.article_author_xpath = './td[4]'
            self.article_url_xpath = './td[3]/a[1]'
            self.article_projectID_xpath = './td[1]'
        elif self.table_name == "Patents":
            self.article_title_xpath = './td[3]'
            self.article_author_xpath = './td[4]'
            self.article_url_xpath = './td[3]/a'
            self.article_projectID_xpath = './td[1]'
        elif self.table_name == "Clinical-Studies":
            self.article_title_xpath = './td[3]'
            self.article_author_xpath = ''
            self.article_url_xpath = './td[3]/a'
            self.article_projectID_xpath = './td[1]'

        # The next button on the page
        self.nxtbtn_xpath = '//div[@class=\'page_counter\']/div[@class=\'pager\']/a[@class=\'single_arrow\']'

        # The current page of results
        if self.table_name == "Projects":
            self.pagination = '//div[@class=\'page_counter\']/div[@class=\'pager\']/input[@id=\'sr_pagetogo\']'
        else:
            self.pagination = '//div[@class=\'page_counter\']/div[@class=\'pager\']'

        # Everything the instance has gathered
        self.output = dict(titles=[], authors=[], urls=[], projectID=[])

    def _set_table_name(self):
        table_names = dict(p='Projects', a='Publications', i='Patents', c='Clinical-Studies')

        print('\nNIHrePORTER can search several types of information.\n'
              'Right now I can only scrape one of these types at a time.\n')

        while True:
            table_type = input('Which data do you want to scrape?\n'
                               '[p] Projects, [a] Publications, [i] Patents, [c] Clinical Studies: ').lower()
            if table_type in ["p", "a", "i", "c"]:
                break
            else:
                print('\nThese are the only things I\'m built to grab. Please pick one.\n')

        return table_names[table_type]

    def _append_results_to_output(self, thispage_articles):
        self.output['titles'] += thispage_articles['titles']
        self.output['authors'] += thispage_articles['authors']
        self.output['urls'] += thispage_articles['urls']
        self.output['projectID'] += thispage_articles['projectID']

    def button_click(self, browser):
        old_page = browser.find_element_by_xpath(self.pagination)

        if self.table_name == "Projects":
            old_page = old_page.get_attribute('value')
        else:
            old_page = old_page.text

        next_btn = browser.find_element_by_xpath(self.nxtbtn_xpath)  # will fail on last page
        next_btn.click()
        time.sleep(2)

        current_page = browser.find_element_by_xpath(self.pagination)

        if self.table_name == "Projects":
            current_page = current_page.get_attribute('value')
        else:
            current_page = current_page.text

        # If my pagination hasn't changed, then the button didn't do anything
        if old_page == current_page:
            raise Exception('Attempted button click did not advance page!')

    def get_article_data(self, articles):
        results = dict(titles=[], authors=[], urls=[], projectID=[])

        for entry in articles:
            try:
                # Will fail if this row is the table headers
                title_div = entry.find_element_by_xpath(self.article_title_xpath)
                results['titles'].append(title_div.text)
            except:
                continue

            if self.table_name != 'Clinical-Studies':
                author_div = entry.find_element_by_xpath(self.article_author_xpath)
                results['authors'].append(author_div.text)
            else:
                results['authors'].append('NA')

            url_div = entry.find_element_by_xpath(self.article_url_xpath)
            results['urls'].append(url_div.get_attribute('href'))

            projectID_div = entry.find_element_by_xpath(self.article_projectID_xpath)
            results['projectID'].append(projectID_div.text)

        self._append_results_to_output(results)


class PsychInfoExtractor:
    def __init__(self):
        # Needed for screenshots
        image_fldr = './PsychInfo-screenshots-taken-on-' + time.strftime("%Y%m%d-%H%M%S")
        if not os.path.exists(image_fldr):
            os.makedirs(image_fldr)
        self.screenshot_folder = image_fldr

        # All elements that contain article information
        self.article_xpath = '//ul[@class=\'resultItems\']/li[@class=\'resultItem ltr\']'

        # To find information about article
        self.article_title_xpath = './/a[@id=\'citationDocTitleLink\']/div[@class=\'truncatedResultsTitle\']'
        self.article_title_altxpath = './/a[@id=\'citationDocTitleLink\']/div[@class=\'truncatedResultsTitle truncatedEffect\']'
        self.article_author_xpath = './/span[@class=\'titleAuthorETC\']'
        self.article_url_xpath = './/a[@id=\'citationDocTitleLink\']'

        # The next button on the page
        self.nxtbtn_xpath = '//nav/ul[@class=\'pagination\']/li/a'

        # Everything the instance has gathered
        self.output = dict(titles=[], authors=[], urls=[])

    def _append_results_to_output(self, thispage_articles):
        self.output['titles'] += thispage_articles['titles']
        self.output['authors'] += thispage_articles['authors']
        self.output['urls'] += thispage_articles['urls']

    def button_click(self, browser):
        old_page = browser.current_url
        # for some reason text() in xpath is not working so doing it this way.
        next_btn = browser.find_elements_by_xpath(self.nxtbtn_xpath)
        next_btn = next_btn[-1]
        if next_btn.text == 'Next page':
            next_btn.click()
        time.sleep(2)

        current_page = browser.current_url

        # If my url hasn't changed, then the button didn't do anything
        if old_page == current_page:
            raise Exception('Attempted button click did not advance page!')

    def get_article_data(self, articles):
        results = dict(titles=[], authors=[], urls=[])

        for entry in articles:
            try:
                title_div = entry.find_element_by_xpath(self.article_title_xpath)
                results['titles'].append(title_div.text)
            except:  # handling long titles
                title_div = entry.find_element_by_xpath(self.article_title_altxpath)
                results['titles'].append(title_div.text)

            author_div = entry.find_element_by_xpath(self.article_author_xpath)
            results['authors'].append(author_div.text)

            url_div = entry.find_element_by_xpath(self.article_url_xpath)
            results['urls'].append(url_div.get_attribute('href'))

        self._append_results_to_output(results)


class ProQuestExtractor:
    def __init__(self):
        # Needed for screenshots
        image_fldr = './ProQuest-screenshots-taken-on-' + time.strftime("%Y%m%d-%H%M%S")
        if not os.path.exists(image_fldr):
            os.makedirs(image_fldr)
        self.screenshot_folder = image_fldr

        # All elements that contain article information
        self.article_xpath = '//ul[@class=\'resultItems\']/li[@class=\'resultItem ltr\']'

        # To find information about article
        self.article_title_xpath = './/a[@id=\'citationDocTitleLink\']/div[@class=\'truncatedResultsTitle\']'
        self.article_title_altxpath = './/a[@id=\'citationDocTitleLink\']/div[@class=\'truncatedResultsTitle truncatedEffect\']'
        self.article_author_xpath = './/span[@class=\'titleAuthorETC\']'
        self.article_url_xpath = './/a[@id=\'citationDocTitleLink\']'

        # The next button on the page
        self.nxtbtn_xpath = '//nav/ul[@class=\'pagination\']/li/a'

        # Everything the instance has gathered
        self.output = dict(titles=[], authors=[], urls=[])

    def _append_results_to_output(self, thispage_articles):
        self.output['titles'] += thispage_articles['titles']
        self.output['authors'] += thispage_articles['authors']
        self.output['urls'] += thispage_articles['urls']

    def button_click(self, browser):
        old_page = browser.current_url
        # for some reason text() in xpath is not working so doing it this way.
        next_btn = browser.find_elements_by_xpath(self.nxtbtn_xpath)
        next_btn = next_btn[-1]
        if next_btn.text == 'Next page':
            next_btn.click()
        time.sleep(2)

        current_page = browser.current_url

        # If my url hasn't changed, then the button didn't do anything
        if old_page == current_page:
            raise Exception('Attempted button click did not advance page!')

    def get_article_data(self, articles):
        results = dict(titles=[], authors=[], urls=[])

        for entry in articles:
            try:
                title_div = entry.find_element_by_xpath(self.article_title_xpath)
                results['titles'].append(title_div.text)
            except:  # handling long titles
                title_div = entry.find_element_by_xpath(self.article_title_altxpath)
                results['titles'].append(title_div.text)

            author_div = entry.find_element_by_xpath(self.article_author_xpath)
            results['authors'].append(author_div.text)

            url_div = entry.find_element_by_xpath(self.article_url_xpath)
            results['urls'].append(url_div.get_attribute('href'))

        self._append_results_to_output(results)


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
        time.sleep(4)

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
        elif search_engine == "q":
            self.browser.get("https://search.proquest.com/dissertations/index")
            self.extractor = ProQuestExtractor()
        elif search_engine == "s":
            self.browser.get("https://search.proquest.com/psycinfo/advanced?accountid=14553")
            self.extractor = PsychInfoExtractor()
        elif search_engine == "n":
            self.browser.get("https://projectreporter.nih.gov/reporter.cfm")
            self.extractor = NIHreporterExtractor()
        elif search_engine == "c":
            self.browser.get("https://clinicaltrials.gov/ct2/search/advanced?cond=&term=&cntry=&state=&city=&dist=")
            self.extractor = ClinicalTrialsExtractor()
        elif search_engine == "r":
            self.browser.get("https://www.cochranelibrary.com/advanced-search?q=&t=1")
            self.extractor = CochraneReviewsExtractor()

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
