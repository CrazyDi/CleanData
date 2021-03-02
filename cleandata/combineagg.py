import pandas as pd
import os
import sys


def adj_means(df: pd.DataFrame, by_var, var, period, change_exclude=None, exclude_type: str=None):
    df = df.sort_values([by_var, period])
    df = df.dropna(subset=[var])

    prev_by_var = 'ZZZ'
    prev_var_value = 0
    row_list = list()
    var_values = df[[by_var, var]].values

    if exclude_type == "ratio" and change_exclude is not None:
        change_exclude = df[var].mean() * change_exclude

    for j in range(len(var_values)):
        by_var = var_values[j][0]
        var_value = var_values[j][1]

        if prev_by_var != by_var:
            if prev_by_var != 'ZZZ':
                row_list.append({'by_var': prev_by_var,
                                 'avg_var': var_sum / by_var_cnt,
                                 'sum_var': var_sum,
                                 'by_var_cnt': by_var_cnt})
            var_sum = 0
            by_var_cnt = 0
            prev_by_var = by_var

        if (change_exclude is None) or (0 <= abs(var_value - prev_var_value) <= change_exclude) or \
                (by_var_cnt == 0):
            var_sum += var_value
            by_var_cnt += 1
        prev_var_value = var_value

    row_list.append({'by_var': prev_by_var,
                     'avg_var': var_sum / by_var_cnt,
                     'sum_var': var_sum,
                     'by_var_cnt': by_var_cnt})
    return pd.DataFrame(row_list)


def check_merge(df_left: pd.DataFrame, df_right: pd.DataFrame, merge_by_left: str, merge_by_right: str):
    """
    Function checks values for merge-by columns on one file but not another
    """
    df_left['in_left'] = "Y"
    df_right['in_right'] = "Y"
    df_both = pd.merge(df_left[[merge_by_left, 'in_left']],
                       df_right[[merge_by_right, 'in_right']],
                       left_on=[merge_by_left],
                       right_on=[merge_by_right],
                       how="outer")
    df_both.fillna('N', inplace=True)
    print(pd.crosstab(df_both.in_left, df_both.in_right))
    print(df_both.loc[(df_both.in_left == 'N') | (df_both.in_right == 'N')].head(20))


def add_files(directory):
    """
    Function concatenates all CSV files in a folder.
    """
    df_out = pd.DataFrame()
    columns_matched = True

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            fileloc = os.path.join(directory, filename)

            with open(fileloc) as f:
                df_new = pd.read_csv(fileloc)
                print(filename + " has " + str(df_new.shape[0]) + " rows.")
                df_out = pd.concat([df_out, df_new])

                column_diff = df_out.columns.symmetric_difference(df_new.columns)

                if not column_diff.empty:
                    print("", "Different columns names for: ", filename, column_diff, "", sep="\n")
                    columns_matched = False

    print("Columns Matched: ", columns_matched)
    return df_out
