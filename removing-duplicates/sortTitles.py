import glob
from checkOverlap import checkOverlap


def quantifyOverlap(all_csv_files):
    for i in range(len(all_csv_files)-1):
        for j in range(i + 1, len(all_csv_files)):
            results_1 = all_csv_files[i]; results_2 = all_csv_files[j]

            percent_overlap = checkOverlap(results_1, results_2)
            print('\n\n' + str(results_2) + '\n' + str(results_1) + '\n' +
                  'Percent overlap of the entries of the first with the second: '
                  + str(round(percent_overlap, 2) * 100) + '%')
            percent_overlap = checkOverlap(results_2, results_1)
            print('\n\n' + str(results_1) + '\n' + str(results_2) + '\n' +
                  'Percent overlap of the entries of the first with the second: '
                  + str(round(percent_overlap, 2) * 100) + '%')

def main():
    # list of search engines I have results for
    # these should be the names of subfolders with
    # the results from each search.
    search_engines = ["PubMed"]

    for engine in search_engines:
        csv_path = './' + engine + '/*.csv'
        all_csv_files =  glob.glob(csv_path)

        quantifyOverlap(all_csv_files)



if __name__ == "__main__": main()