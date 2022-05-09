import os
from zipfile import ZipFile
import urllib.request
import regex as re

############ LINKS TO USE FOR REFERENCE

# Found hrefs of files to be downloaded
## Household data: https://www.meps.ahrq.gov/mepsweb/data_stats/download_data_files_results.jsp?cboDataYear=All&cboDataTypeY=1%2CHousehold+Full+Year+File&buttonYearandDataType=Search&cboPufNumber=All&SearchTitle=Medical+Conditions 
## Prescribed medicine: https://www.meps.ahrq.gov/mepsweb/data_stats/download_data_files_results.jsp?cboDataYear=All&cboDataTypeY=2%2CHousehold+Event+File&buttonYearandDataType=Search&cboPufNumber=All&SearchTitle=Prescribed+Medicines&sortBy=year_for_display_D

## 2019 medical conditions: https://www.meps.ahrq.gov/mepsweb/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-216
## Have to get for each year

# 2019-2017 prescribed medicine excel files
prescribed_medicine_excel = ["https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h213a/h213axlsx.zip",
                             "https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h206a/h206axlsx.zip",
                             "https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h197a/h197axlsx.zip"]

# 2019-2014 prescribed medicine ascii files
prescribed_medicine_ascii = ["https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h213a/h213adat.zip",
                            "https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h206a/h206adat.zip",
                            "https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h197a/h197adat.zip",
                            "https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h188adat.zip",
                            "https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h178adat.zip",
                            "https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h170dat.zip"]

# 2019-2017 med conditions excel files
med_conditions_excel = ["https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h214/h214xlsx.zip",
                        "https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h207/h207xlsx.zip",
                        "https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h199/h199xlsx.zip"]

#2019-2014 med conditions ascii files
med_conditions_ascii = ["https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h214/h214dat.zip",
                        "https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h207/h207dat.zip",
                        "https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h199/h199dat.zip",
                        "https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h190dat.zip",
                        "https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h180dat.zip",
                        "https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h170dat.zip"]

# 2019-2017 household excel files
household_excel = ["https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h216/h216xlsx.zip",
                   "https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h209/h209xlsx.zip",
                   "https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h201/h201xlsx.zip"]

# 2019-2014 household ascii files
household_ascii = ["https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h216/h216dat.zip",
                   "https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h209/h209dat.zip",
                   "https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h201/h201dat.zip",
                   "https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h192dat.zip",
                   "https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h181dat.zip",
                   "https://www.meps.ahrq.gov/mepsweb/data_files/pufs/h171dat.zip"]

combined_ascii_links = prescribed_medicine_ascii + med_conditions_ascii + household_ascii

####### CATEGORIZE LINKS

prescribed_medicine_filenames = ["h213a.dat", "h206A.dat", "h197a.dat", "h188a.dat", "h178a.dat", "h170.dat"]
med_conditions_filenames = ["h214.dat", "h207.dat", "h199.dat", "h190.dat", "h180.dat", "h170.dat"]
household_filenames = ["h216.dat", "h209.dat","h201.dat", "h192.dat", "h181.dat", "h171.dat"]
total_file_names = prescribed_medicine_filenames + med_conditions_filenames + household_filenames

final_file_names_format = "[?year]_[?name].dat"

final_file_categories = ["prescribed_medicine", "med_conditions", "household"]

final_file_years = [2019, 2018, 2017, 2016, 2015, 2014]

####### EXTRACT LINKS

def go(final_file_categories, final_file_years, download_links, final_file_names_format):
    '''
    Creates a new data folder and reads in data

    Inputs:
        final_file_categories (list): list of categories of files to download (e.g. prescribed med)
        final_file_years (list): years downloading        
        download_links (list): List of links to download
        final_file_names_format (str): How to format downloaded files

    Returns: None (new directory with files made)
    '''
    home_path = os.getcwd()
    try:
        slash = re.findall("(?<=C:).*?(?=\w)", home_path)[0]
    except:
        slash = '/'

    try:
        data_folder = home_path + slash + "MEPS_data"
        os.mkdir(data_folder)
        print("made parent data folder")
    except:
        print(home_path, slash)
        print("data folder already exists, not going to read data")
        return
    read_samples(final_file_categories, final_file_years, download_links, final_file_names_format, data_folder, slash)

def read_samples(final_file_categories, final_file_years, download_links, final_file_names_format, current_dir, slash):
    '''
    Reads samples in and puts them into folders

    Inputs:
        final_file_categories (list): list of categories of files to download (e.g. prescribed med)
        final_file_years (list): years downloading        
        download_links (list): List of links to download
        final_file_names_format (str): How to format downloaded files
        current_dir (path): filepath to add new folders to (to house files)
        slash (str): slashes used on operating system for filepaths

    Returns: None (files downloaded)
    '''
    for i, category in enumerate(final_file_categories):
        new_path = current_dir + slash + category
        print("downloading", category)
        try:
            os.mkdir(new_path)
        except:
            print(category, " already exists, trying next folder")
            continue
        counter = 0
        for j, year in enumerate(final_file_years):
            combo_idx = i*(len(final_file_years) - 1) + j
            download_link = download_links[combo_idx]
            try:
                file, _ = urllib.request.urlretrieve(download_link)
                with ZipFile(file, 'r') as zip:
                    zip.extractall(new_path)
                    zip.close()
                download_name = total_file_names[combo_idx]
                final_name = final_file_names_format.replace("[?year]", str(year))
                final_name = final_name.replace("[?name]", category)
                os.rename(new_path + slash + download_name, new_path + slash + final_name)
                counter += 1
            except:
                print("file download failed in", category)
                print(download_link)
        print("downloaded", counter, "files into", category)

go(final_file_categories, final_file_years, combined_ascii_links, final_file_names_format)