import pandas as pd


def get_first_look(df: pd.DataFrame, row_num: int=5, unique_ids: str=None):
    """
    Summary information of DataFrame
    """
    out = dict()
    out['head'] = df.head(row_num)
    out['dtypes'] = df.dtypes
    out['row_num'] = df.shape[0]
    out['col_num'] = df.shape[1]
    out['index'] = df.index

    if unique_ids is not None:
        out['unique_ids'] = df[unique_ids].nunique()

    return out


def display_dict(dict_to_display: dict):
    """
    Pretty up the display of a dictionary
    """
    print(*(': '.join(map(str, x)) for x in dict_to_display.items()), sep='\n\n')


def get_totals(df: pd.DataFrame):
    """
    The function takes a pandas DataFrame and creates a dictionary with selected summary statistics.
    """
    out = dict()
    out['min'] = df.min()
    out['per15'] = df.quantile(0.15)
    out['qr1'] = df.quantile(0.25)
    out['median'] = df.median()
    out['qr3'] = df.quantile(0.75)
    out['per85'] = df.quantile(0.85)
    out['max'] = df.max()
    out['count'] = df.count()
    out['mean'] = df.mean()
    out['iqr'] = out['qr3'] - out['qr1']

    return pd.DataFrame(out)


def get_miss(df: pd.DataFrame, by_row_perc: bool=False):
    """
    The function return information about missing values
    """
    return df.isnull().sum(), df.isnull().sum(axis=1).value_counts(normalize=by_row_perc).sort_index()


def make_freq(df: pd.DataFrame, out_file):
    """
    The function writes to the file frequencies and percentages of columns
    """
    freq_out = open(out_file, 'w')
    for col in df.select_dtypes(include=['category']):
        print(col, "----------------------",
              'frequencies', df[col].value_counts().sort_index(),
              'percentages', df[col].value_counts(normalize=True).sort_index(),
              sep="\n\n", end="\n\n\n", file=freq_out)
    freq_out.close()


def get_count(df: pd.DataFrame, category_list: list, row_selected: str=None):
    """
    The function counts the number of rows for each combination of column values
    """
    total = category_list[:-1]
    category_count = df.groupby(category_list).size().reset_index(name='category_count')
    total_count = df.groupby(total).size().reset_index(name='total_count')
    percent_list = pd.merge(category_count, total_count, left_on=total, right_on=total, how='left')
    percent_list['percent'] = percent_list.category_count / percent_list.total_count
    if row_selected is not None:
        percent_list = percent_list.loc[eval("percent_list." + row_selected)]

    return percent_list
