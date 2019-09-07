import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


##CONSTANTS = pd.read_csv("cc_constants.csv", index_col="n")


def generate_data():
    array = np.random.randint(95, 105, (10, 5))
    return pd.DataFrame(array)


def add_labels(df):
    n_rows, n_cols = df.shape
    rows = ["Group {}".format(x+1) for x in range(n_rows)]
    cols = ["Measure {}".format(x+1) for x in range(n_cols)]
    
    df.columns = cols
    
    df["Group"] = rows
    df.set_index("Group", drop=True, inplace=True)


def get_constant(n, c_name):
    return CONSTANTS.loc[n, c_name]


def get_means(df):
    return df.mean(axis=1)


def get_stds(df):
    return df.std(axis=1)


def get_ranges(df):
    return df.max(axis=1)-df.min(axis=1)


def run_chart(series, centerline=False,
              USL=None, LSL=None,
              x_label="No.", y_label="Measure"):

    n_points = len(series)
    x = np.arange(n_points) + 1
    y = series
    
    plt.plot(x, y, marker="o")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    
    if centerline:
        center = np.mean(y)
        plt.plot(x, [center]*n_points, "k", label="Mean")

    if USL is not None:
        plt.plot(x, [USL]*n_points, "r", label="USL")

    if LSL is not None:
        plt.plot(x, [LSL]*n_points, "r", label="LSL")
    
    plt.legend(loc="right", bbox_to_anchor=(1.25, 0.85))
    plt.show()


def histogram(series, bins=10, x_label="Measure", y_label="Frequency"):
    plt.hist(series, bins=bins)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


def xbar_s_chart(df):
    means = get_means(df)
    stds = get_stds(df)    
    
    X_bar = means.mean()
    s_bar = stds.mean()

    n = df.shape[1]
    A1 = get_constant(n, "A1")
    UCL = X_bar + A1*s_bar
    LCL = X_bar - A1*s_bar

    groups = means.index

    plt.plot(groups, means, marker="o")
    plt.plot(groups, [UCL]*len(groups), "r",
             label="UCL={:.2f}".format(UCL))
    plt.plot(groups, [X_bar]*len(groups), "k",
             label="Mean={:.2f}".format(X_bar))
    plt.plot(groups, [LCL]*len(groups), "r",
             label="LCL={:.2f}".format(LCL))
    plt.xticks(rotation=90)
    plt.ylabel("X-bar")
    plt.legend(loc="right", bbox_to_anchor=(1.35, 0.85))
    
    plt.show()


def s_chart(df):
    stds = get_stds(df)
    s_bar = stds.mean()
    
    n = df.shape[1]
    B4 = get_constant(n, "B4")
    B3 = get_constant(n, "B3")
    UCL = B4 * s_bar
    LCL = B3 * s_bar

    groups = stds.index

    plt.plot(groups, stds, marker="o")
    plt.plot(groups, [UCL]*len(groups), "r",
             label="UCL={:.2f}".format(UCL))
    plt.plot(groups, [r_bar]*len(groups), "k",
             label="s-bar={:.2f}".format(s_bar))
    plt.plot(groups, [LCL]*len(groups), "r",
             label="LCL={:.2f}".format(LCL))
    plt.xticks(rotation=90)
    plt.ylabel("s")
    plt.legend(loc="right", bbox_to_anchor=(1.35, 0.85))
    
    plt.show()


def xbar_r_chart(df):
    means = get_means(df)
    ranges = get_ranges(df)    
    
    X_bar = means.mean()
    r_bar = ranges.mean()

    n = df.shape[1]
    A2 = get_constant(n, "A2")
    UCL = X_bar + A2*r_bar
    LCL = X_bar - A2*r_bar

    groups = means.index

    plt.plot(groups, means, marker="o")
    plt.plot(groups, [UCL]*len(groups), "r",
             label="UCL={:.2f}".format(UCL))
    plt.plot(groups, [X_bar]*len(groups), "k",
             label="Mean={:.2f}".format(X_bar))
    plt.plot(groups, [LCL]*len(groups), "r",
             label="LCL={:.2f}".format(LCL))
    plt.xticks(rotation=90)
    plt.ylabel("X-bar")
    plt.legend(loc="right", bbox_to_anchor=(1.35, 0.85))
    
    plt.show()


def r_chart(df):
    ranges = get_ranges(df)
    r_bar = ranges.mean()
    
    n = df.shape[1]
    D4 = get_constant(n, "D4")
    D3 = get_constant(n, "D3")
    UCL = D4 * r_bar
    LCL = D3 * r_bar

    groups = ranges.index

    plt.plot(groups, ranges, marker="o")
    plt.plot(groups, [UCL]*len(groups), "r",
             label="UCL={:.2f}".format(UCL))
    plt.plot(groups, [r_bar]*len(groups), "k",
             label="R-bar={:.2f}".format(r_bar))
    plt.plot(groups, [LCL]*len(groups), "r",
             label="LCL={:.2f}".format(LCL))
    plt.xticks(rotation=90)
    plt.ylabel("Range")
    plt.legend(loc="right", bbox_to_anchor=(1.35, 0.85))
    
    plt.show()


def group_scattering(df, y_label="Measure"):
    groups = df.index
    n = df.shape[1]
 
    for group in groups:
        plt.scatter([group]*n, df.loc[group, :], c="blue")

    plt.xticks(rotation=90)
    plt.ylabel(y_label)
    plt.show()


def moving_range_chart(df):
    MRs = np.abs(means[1:].values-means[:-1].values)
    indices = [str(x+2) for x in range(len(MRs))]
    
    MR_bar = np.mean(MRs)
    
    D4 = get_constant(2, "D4")
    UCL = D4 * MR_bar
    LCL = 0
    
    plt.plot(indices, MRs, marker="o")
    plt.plot(indices, [UCL]*len(MRs), "r",
             label="UCL={:.2f}".format(UCL))
    plt.plot(indices, [MR_bar]*len(MRs), "k",
             label="MR-bar={:.2f}".format(MR_bar))
    plt.plot(indices, [LCL]*len(MRs), "r",
             label="LCL={:.2f}".format(LCL))
    
    plt.ylabel("Moving Range")
    plt.legend(loc="right", bbox_to_anchor=(1.35, 0.85))
    plt.show()


def six_sigma_hist(df):
    pass


def normality_test(df):
    values = df.values.ravel()
    pass


def Cpk(df):
    return None


def Cp(df):
    return None


def Ppk(df):
    return None


def Pp(df):
    return None
