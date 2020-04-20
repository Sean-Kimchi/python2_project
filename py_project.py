
import pandas as pd
import matplotlib.pyplot as plt


#this is going to be called for each file to create dataframes
def load_data(filename):
    df = pd.read_csv(filename)

    return df

#dynamically getting the headers from a dataframe
def get_column_headers(data_frame):

    col_list = []

    for col in data_frame.columns:
        col_list.append(col)

    return list(col_list)

#this will return a set of the common columns
def gen_col_intersect(list_of_col_list):

    result = set(list_of_col_list[0])
    for s in list_of_col_list[1:]:
        result.intersection_update(s)
    return list(result)

def df_add_col_def_val(df, col_name, value):
    df[col_name] = value
    return df

def extrapolate_trend(x,y):

    #do extrapolation here

    return extrapolated_dataframe




def main():

    col_header_list = []
    sublist = []

    #create data frames of each csv
    df_2015 = load_data('2015_rtd.csv')
    df_2016 = load_data('2016_rtd.csv')
    df_2017 = load_data('2017_rtd.csv')
    df_2018 = load_data('2018_rtd.csv')
    df_2019 = load_data('2019_rtd.csv')

    #add the column year with default value to segregate the data
    df_2015 = df_add_col_def_val(df_2015, 'year', '2015')
    df_2016 = df_add_col_def_val(df_2016, 'year', '2016')
    df_2017 = df_add_col_def_val(df_2017, 'year', '2017')
    df_2018 = df_add_col_def_val(df_2018, 'year', '2018')
    df_2019 = df_add_col_def_val(df_2019, 'year', '2019')


    #creating sublists of column names to find common columns among all files
    sublist= get_column_headers(df_2015)
    col_header_list.append(sublist)
    sublist = []
    sublist= get_column_headers(df_2016)
    col_header_list.append(sublist)
    sublist = []
    sublist= get_column_headers(df_2017)
    col_header_list.append(sublist)
    sublist = []
    sublist= get_column_headers(df_2018)
    col_header_list.append(sublist)
    sublist = []
    sublist= get_column_headers(df_2019)
    col_header_list.append(sublist)

    #all common columns
    select_list = gen_col_intersect(col_header_list)

    print(select_list)

    #concat into one data frame
    frames = [df_2015,df_2016,df_2017,df_2018,df_2019]
    
    comd_df = pd.concat([df_2015[select_list],df_2016[select_list],df_2017[select_list],df_2018[select_list],df_2019[select_list] ],axis=0)

    comd_df.reset_index(drop=True)

    #now all data is in one dataframe
    print(comd_df)

    #lets start looking at some statistics of the file

    print('\nrecords per year\n','------------------------\n' ,comd_df.groupby('year').count())

    #we can see that some values will be of NaN.  Interpolate to fill in those gaps
    comd_df_intp = comd_df.interpolate()
    
    #lets generate a correlation matrix for analysis
    corr_matrix = comd_df_intp.corr(method='pearson')

    with pd.option_context('display.max_columns', None):

        print(corr_matrix)

    #health, economy, and family have highest corr vale
        
    comd_df_intp[['Happiness Score','Economy']].plot(y='Economy', x='Happiness Score', kind='scatter')
    comd_df_intp[['Happiness Score','Health']].plot(y='Health', x='Happiness Score', kind='scatter')
    comd_df_intp[['Happiness Score','Family']].plot(y='Family', x='Happiness Score', kind='scatter')


    plt.show()


    

main()
