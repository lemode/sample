import csv
import glob
import os
import pandas as pd


class LocalFileService:
    def __init__(self, local_directory):
        self.local_directory = local_directory

    def load_excel_sheet_to_dataframe(self, local_file_name, sheet_name):
        local_file_path = "{0}/{1}".format(self.local_directory, local_file_name)
        df = pd.read_excel(local_file_path, sheet_name)
        df.columns = df.columns.str.replace(" ", "_")
        df.reset_index(drop=True, inplace=True)
        df.columns = map(str.lower, df.columns)
        return df

    def load_csv_to_dataframe(self, local_file_name):
        local_file_path = "{0}/{1}".format(self.local_directory, local_file_name)
        df = pd.read_csv(local_file_path, encoding="utf-8", index_col=False)
        df.columns = df.columns.str.replace(" ", "_")
        df.reset_index(drop=True, inplace=True)
        df.columns = map(str.lower, df.columns)
        return df


    def load_csv_folder_to_dataframe(self,local_folder_path):

        all_files = glob.iglob(os.path.join(local_folder_path, "*.csv"))     # advisable to use os.path.join as this makes concatenation OS independent

        print(all_files)

        df_from_each_file = (pd.read_csv(f) for f in all_files)



        # csv_files = glob.iglob(os.path.join(local_folder_path, "*.csv"))

        # list_csvs = []

        # print(csv_files)

        # for f in csv_files:
        #     df = self.load_csv_to_dataframe(f)
        #     list_csvs.append(df)



        # df_combined = pd.concat(list_csvs, axis=0, ignore_index=True)
        df_combined   = pd.concat(df_from_each_file, ignore_index=True)
        # return df_combined


    def copy_results_to_csv(self, local_file_name, dataframe):
        dataframe.to_csv(local_file_name, encoding="utf-8", index=False)

    def copy_json_results_to_py(self, file_name, json_data):
        """
        :param file_name: directory with
        output to file with py extension
        :param json_data: data formatted as json -- list of dicts
        ie ./common/ags/tests/mocks/output.py' -- str
        """
        data_file = open(file_name, "w")
        data_file.write(str(json_data))
        data_file.close()

    def copy_json_results_to_csv(self, file_name, json_data):
        """
        :param file_name: directory with
        output to file with csv extension
        :param json_data: data formatted as json -- list of dicts
        ie /common/ags/tests/mocks/data_file.csv' -- str
        """
        # now we will open a file for writing
        data_file = open(file_name, "w")

        # create the csv writer object
        csv_writer = csv.writer(data_file)

        # Counter variable used for writing
        # headers to the CSV file
        count = 0

        for data_row in json_data:
            if count == 0:

                # Writing headers of CSV file
                header = data_row.keys()
                csv_writer.writerow(header)
                count += 1

            # Writing data of CSV file
            csv_writer.writerow(data_row.values())

        data_file.close()


# local_directory="~/Downloads/FraserSalesOrderError"
# local_file = LocalFileService(local_directory)
# df = local_file.load_csv_folder_to_dataframe(local_directory)
# df.head()


path = r'/Users/lindaemode/Downloads/FraserSalesOrderError/**/*.csv'
# path = '~/Downloads/FraserSalesOrderError/**/*.csv'
# formatted_path = ('r'{path}'.format(os.path.abspath(path)))

all_rec = glob.iglob(path, recursive=True)
dataframes = (pd.read_csv(f) for f in all_rec)
df_combined = pd.concat(dataframes, ignore_index=True)
print(df_combined)

