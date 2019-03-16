import glob, re, os, pandas

results_fldr = './raw-results'
if not os.path.exists(results_fldr):
    os.makedirs(results_fldr)

print('Hi! Welcome to the next phase of meta-analysis results processing.\n'
      'Now that you have collected all the results from the search engines I support,\n'
      'we can collect these results into a single file and remove duplicate title names.')
print('\nTo do that, please copy all the results you want to sort into the \'raw-results\'\n'
      'folder in this directory. Right now I\'m a little fragile so please don\'t change\n'
      'the names of these files.\n')

input('Press enter when you\'re ready for me to start...')

csv_path = results_fldr + '/*.csv'
all_csv_files =  glob.glob(csv_path)

# collecting results across all csv files
allData = pandas.DataFrame()
for csv_file in all_csv_files:
    name_parts = re.findall(r"[\w']+", csv_file)
    if name_parts[3] == 'all':
        engine = '-'.join([name_parts[2]]+name_parts[5:-1])
    else:
        engine = '-'.join(name_parts[2:4]+name_parts[6:-1])

    this_data = pandas.read_csv(csv_file)
    this_data['engineName'] = engine

    allData = pandas.concat([allData, this_data], axis=0, ignore_index=True, sort=False)


# remove duplicates and alphabetize
allData = allData.drop_duplicates(subset='titles')
allData = allData.sort_values('titles')

# save results
allData.to_csv('./results-dulplicates-removed.csv')

print('\nThat\'s it! You\'re data should now be ready to review and\n'
      'is stored in a csv file in the folder this script was run from.')
