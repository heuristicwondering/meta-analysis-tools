from titleextractor import TitleExtractor
import csv, os, time

# Currently supported search engines
engine_names = dict(g="GoogleScholar", p="Pubmed", q="ProquestDisseration",
                    s="PsychInfo", n="NIHrePORTER", c="ClinicalTrialsGov")

print("Hello! This is a very crude version of a webscraper built to help \n"
      "gather search results from database queries. Unfortunately, some \n"
      "databases (*cough* *cough* Google Scholar *cough*) are not so friendly \n"
      "to this kind of automated scraping so we require a bit of human clicking \n"
      "to help. This mean you will have to interact with the webpage and with \n"
      "me on the command line. Just follow my instructions and I should handle rest.\n")

# Gathering info about what the user wants to search.
print("To get started, please tell me what search engine you\'re scraping info from today.")
while True:
    search_engine = input("[g] Google Scholar, [p] Pubmed, [q] Proquest Dissertations, \n"
                          "[s] PsychInfo, [n] NIH rePORTER, [c] ClinicalTrial.gov: ").lower()

    if search_engine in ["g", "p", "q", "s", "n", "c"]:
        break
    else:
        print("\nRight now I\'m only built to scrape these engines.\n"
              "If you find me useful and want more support or more automation,\n"
              "then you\'ll have to give the author a postdoc.\n")

print("\nThanks. I\'m going to open up a window to take us to that search engine.\n"
      "Check back here for the next instruction.")
time.sleep(3)

title_extractor = TitleExtractor(search_engine)

print("\nOk, the next step is to run what ever search you want results for.\n"
      "When the first page is loaded, come back here to let me know.\n")

# Extra Instructions
if search_engine == "n":
    print("\nFor NIHrePORTER you also need to make sure that you are on the \"" + title_extractor.extractor.table_name + "\" tab.\n")
if search_engine == "c":
    print("\nFor ClinicalTrials.gov I can only scrape the default settings right now.\n"
          "Please make sure that you don\'t hide these columns and that you stay in the list view tab.\n"
          "If you find you need to scrape more information than this, please make a feature request.\n")

input("Press enter when the first page is loaded and I\'ll try scraping the results.")

search_results = title_extractor.execute_multipage_extraction()

keywords = input('\nGreat! Well, I think I\'ve gotten all I can here.\n'
                 'I\'d like to save these results to file. Please provide\n'
                 'a descriptive name for this search so I can make a folder.\n'
                 'Generally telling me the keywords you used is the most helpful: ')



# Saving results to file
results_fldr = './searchResults-' + time.strftime("%Y%m%d")
if not os.path.exists(results_fldr):
    os.makedirs(results_fldr)


# Naming the file
if search_engine == "n":
    csv_file = results_fldr + '/' + engine_names[search_engine] + '-' + title_extractor.extractor.table_name \
               + '-all-titles-' + "-".join(keywords.split(' ')) + '.csv'
else:
    csv_file = results_fldr + '/' + engine_names[search_engine] + '-all-titles-' + "-".join(keywords.split(' ')) + '.csv'
csv_columns = list(search_results.keys())

try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(search_results.keys())
        writer.writerows(zip(*search_results.values()))

    print('\n\nEverything should be saved now. Check the folder you\'re running\n'
          'this script in for your results and screenshots of the pages we scraped.\n'
          '\nThanks for using!\n')
except IOError:
    print("I/O error")

