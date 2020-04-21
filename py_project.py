
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

def linear_regression(df, xval, yval):
    #make sure we have a fresh index in the data frame
    df.reset_index(drop=True)

    #sum of all x values
    xsum = df[xval].sum()
    #sum of all y values
    ysum = df[yval].sum()
    #sum of products of pairs
    df['xy'] = df[xval]*df[yval]
    xysum = df['xy'].sum()
    #total squared x
    df['x2'] = df[xval]**2
    x2sum = df['x2'].sum()
    #total squared y
    df['y2'] = df[yval]**2
    y2sum = df['y2'].sum()
    #number of values
    n = len(df.index)

    #for slope of linear line y=m*x+b
    m = ((n*xysum)-(xsum*ysum))/((n*x2sum)-(xsum*xsum))

    b = ((x2sum*ysum)-(xsum*xysum))/((n*x2sum)-(xsum*xsum))

    return m,b

def get_rsquared(df, xval, yval):
    #make sure we have a fresh index in the data frame
    df.reset_index(drop=True)

    #sum of all x values
    xsum = df[xval].sum()
    #sum of all y values
    ysum = df[yval].sum()
    #sum of products of pairs
    df['xy'] = df[xval]*df[yval]
    xysum = df['xy'].sum()
    #total squared x
    df['x2'] = df[xval]**2
    x2sum = df['x2'].sum()
    #total squared y
    df['y2'] = df[yval]**2
    y2sum = df['y2'].sum()
    #number of values
    n = len(df.index)

    r2= (((n*xysum)-(xsum*ysum))**2)/(((n*x2sum)-(xsum*xsum))*((n*y2sum)-(ysum*ysum)))

    return r2

def get_stdv(df,cols):

    stdv = df[cols].std()

    return stdv
    
    




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
    with pd.option_context('display.max_columns', None):

        print('\nrecords per year\n','------------------------\n' ,comd_df.groupby('year').count())

    #we can see that some values will be of NaN.  Interpolate to fill in those gaps
    comd_df_intp = comd_df.interpolate()
    
    #lets generate a correlation matrix for analysis
    corr_matrix = comd_df_intp.corr(method='pearson')

    comd_df_intp[['Happiness Score']].plot.hist()
    comd_df_intp[['Health']].plot.hist()
    comd_df_intp[['Economy']].plot.hist()
    comd_df_intp[['Family']].plot.hist()


    with pd.option_context('display.max_columns', None):

        print(corr_matrix)

    #health, economy, and family have highest corr vale
        
    
    #comd_df_intp[['Happiness Score','Health']].plot(y='Health', x='Happiness Score', kind='scatter')
    #comd_df_intp[['Happiness Score','Family']].plot(y='Family', x='Happiness Score', kind='scatter')
    #comd_df_intp[['Happiness Score','Generosity']].plot(y='Generosity', x='Happiness Score', kind='scatter')


    
    #plt.show()

    #Calculate and Display the R^2 value
    print('Happiness ~ Economy Rsquared=',get_rsquared(comd_df_intp,'Happiness Score','Economy'))
    print('Happiness ~ Health Rsquared=',get_rsquared(comd_df_intp,'Happiness Score','Health'))
    print('Happiness ~ Family Rsquared=',get_rsquared(comd_df_intp,'Happiness Score','Family'))
    print('Happiness ~ Generosity Rsquared=',get_rsquared(comd_df_intp,'Happiness Score','Generosity'))

    
    #Calculate and display the standard deviation
    print('Standard Deviation Economy:',get_stdv(comd_df_intp,'Economy'))
    print('Standard Deviation Health:',get_stdv(comd_df_intp,'Health'))
    print('Standard Deviation Family:',get_stdv(comd_df_intp,'Family'))
    print('Standard Deviation Generosity:',get_stdv(comd_df_intp,'Generosity'))

    me,be = linear_regression(comd_df_intp,'Happiness Score','Economy')
    mh,bh = linear_regression(comd_df_intp,'Happiness Score','Health')
    mf,bf = linear_regression(comd_df_intp,'Happiness Score','Family')
    mg,bg = linear_regression(comd_df_intp,'Happiness Score','Generosity')

    #add trendline values to the dataframe based on y=mx+b
    comd_df_intp['linee'] = me*comd_df_intp[['Happiness Score']] + be
    comd_df_intp['lineh'] = mh*comd_df_intp[['Happiness Score']] + bh
    comd_df_intp['linef'] = mf*comd_df_intp[['Happiness Score']] + bf
    comd_df_intp['lineg'] = mg*comd_df_intp[['Happiness Score']] + bg


    # Plot the best fit line over the actual values
    comd_df_intp[['Happiness Score','Economy']].plot(y='Economy', x='Happiness Score', kind='scatter')
    plt.scatter(comd_df_intp[['Happiness Score']], comd_df_intp[['Economy']])
    plt.plot(comd_df_intp[['Happiness Score']], comd_df_intp[['linee']], 'b')
    plt.title('Happiness vs. Economy')

    comd_df_intp[['Happiness Score','Health']].plot(y='Health', x='Happiness Score', kind='scatter')
    plt.scatter(comd_df_intp[['Happiness Score']], comd_df_intp[['Health']])
    plt.plot(comd_df_intp[['Happiness Score']], comd_df_intp[['lineh']], 'b')
    plt.title('Happiness vs. Health')

    comd_df_intp[['Happiness Score','Family']].plot(y='Family', x='Happiness Score', kind='scatter')
    plt.scatter(comd_df_intp[['Happiness Score']], comd_df_intp[['Family']])
    plt.plot(comd_df_intp[['Happiness Score']], comd_df_intp[['linef']], 'b')
    plt.title('Happiness vs. Family')

    comd_df_intp[['Happiness Score','Generosity']].plot(y='Generosity', x='Happiness Score', kind='scatter')
    plt.scatter(comd_df_intp[['Happiness Score']], comd_df_intp[['Generosity']])
    plt.plot(comd_df_intp[['Happiness Score']], comd_df_intp[['lineg']], 'b')
    plt.title('Happiness vs. Generosity')


    #plt.show()

    

    

main()
