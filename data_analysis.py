import import_utils as iu
import pandas as pd
import pprint as pp
import numpy as np
import re
import pandasql as psql
import matplotlib.pyplot as plt

def extract_retweet_from(df):
    for i in range(len(df)):
        m = re.search('RT @(.+?):', df.loc[i, 'text'])
        if m:
            df.loc[i, 'retweet_from_user'] = m.group(1)
        else:
            df.loc[i, 'retweet_from_user'] = np.nan
    return df

# Rank row by rank_col and get top 10 row of index_col
def get_rank_col_by_index_col(df, rank_col, index_col, num_result=10):
    output = df.sort_values(by=[rank_col], ascending=False)
    output.drop_duplicates(subset=[index_col], keep='first', inplace=True)
    output = output.loc[:, [index_col, rank_col]].reset_index(drop=True)
    output = output.head(num_result)
    # print(output)
    return output

def get_top_count_by(df, groupby_col, num_result=10):
    query = "SELECT {}, COUNT(*) AS count FROM df GROUP BY {} ORDER BY count DESC".format(groupby_col, groupby_col)
    output = psql.sqldf(query).head(num_result)
    # output[groupby_col] = output[groupby_col].str.slice(0,30)
    # print(output)
    return output

def get_histogram_of_col(df, col_name, num_bin=10, plot=True):
    series = df[col_name]
    count, division = np.histogram(series, density=True, bins=num_bin)
    if plot == True:
        plt.hist(series, bins = num_bin)
        plt.title("histogram of {}".format(col_name))
        plt.xlabel(col_name)
        plt.ylabel('frequency')
        plt.show()
    return count, division

if __name__ == "__main__":
    # print(iu.get_csv_from_dir('data', filename='tweets_blacklivesmatter_TJun-07-2020N50000'))
    df = pd.read_csv('data/tweets_blacklivesmatter_TJun-07-2020N50000.csv')
    df = extract_retweet_from(df)
    df.drop(columns=['tweet_id', 'user_id'], inplace=True)
    df.to_csv('tweets_blacklivesmatter_TJun-07-2020N50000_cleaned.csv', index=False)
    # print(df.columns)

    # get_top_count_by(df, 'text')
    # get_top_count_by(df, 'retweet_from_user')
    # get_top_count_by(df, 'user')
    # get_rank_col_by_index_col(df, 'user_follower_count', 'user', 25)
    # get_rank_col_by_index_col(df, 'user_favorite_count', 'user', 25)
    # get_rank_col_by_index_col(df, 'retweet_count', 'text', 25)
    # get_histogram_of_col(df, 'user_favorite_count', 30, False)



