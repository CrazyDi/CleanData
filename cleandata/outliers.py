import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as scistat
import math


def get_dist_prop(series_to_test: pd.Series):
    """
    The function takes a series and generates measures of central tendency, shape, and spread.
    """
    out = dict()
    norm_stat, norm_p_value = scistat.shapiro(series_to_test)

    if not math.isnan(norm_stat):
        out['norm_stat'] = norm_stat
        if norm_p_value >= 0.05:
            out['norm_p_value'] = str(round(norm_p_value, 2)) + ": Accept Normal"
        elif norm_p_value < 0.05:
            out['norm_p_value'] = str(round(norm_p_value, 2)) + ": Reject Normal"

    out['mean'] = series_to_test.mean()
    out['median'] = series_to_test.median()
    out['std'] = series_to_test.std()
    out['kurtosis'] = series_to_test.kurtosis()
    out['skew'] = series_to_test.skew()
    out['count'] = series_to_test.count()

    return out


def get_outliers(df_in: pd.DataFrame, sum_vars: list, other_vars: list):
    """
    Function returns dataframe of outliers
    """
    df_in = df_in[sum_vars + other_vars]
    df_out = pd.DataFrame(columns=df_in.columns, data=None)
    df_sums = df_in[sum_vars]

    for col in df_sums.columns:
        third_q, first_q = df_sums[col].quantile(0.75), df_sums[col].quantile(0.25)
        interquartile_range = 1.5 * (third_q - first_q)
        outlier_high, outlier_low = interquartile_range + third_q, first_q - interquartile_range
        df = df_in.loc[(df_in[col] > outlier_high) | (df_in[col] < outlier_low)]
        df = df.assign(varname=col, threshlow=outlier_low, threshhigh=outlier_high)
        df_out = pd.concat([df_out, df])

    return df_out


def make_plot(series_to_plot: pd.Series, title: str, xlabel: str, plot_type: str="hist"):
    """
    Function generates histograms and boxplots
    """
    if plot_type == "hist":
        plt.hist(series_to_plot)
        plt.axvline(series_to_plot.mean(), color='red', linestyle='dashed', linewidth=1)
        plt.xlabel(xlabel)
        plt.ylabel("Frequency")
    elif plot_type == "box":
        plt.boxplot(series_to_plot.dropna(), labels=[xlabel])

    plt.title(title)
    plt.show()
