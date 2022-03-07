import numpy as np
import matplotlib.pyplot as plt

def plot_variable(ds, param, add_deployments=True):
    """Function to plot the timeseries with deployment info.

    Parameters
    ----------
    ds: (xarray.Dataset)
        An xarray dataset downloaded from OOINet
    param: (str)
        The parameter name of the data variable in the OOI
        dataset to plot
    add_deployments: (boolean)
        Also plot deployment information

    Returns
    -------
    fig, ax: (matplotlib figs)
        Figure and axis handles for the matplotlib image
    """
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Calculate the figure bounds
    yavg = ds[param].mean()
    ystd = ds[param].std()
    ymed = np.nanmedian(ds[param])
    # Need to check for way out-of-bounds values by comparison with median
    if ystd > ymed:
        yavg = ymed
        ystd = ymed*0.2
    ymin = yavg - 4*ystd
    ymax = yavg + 4*ystd
    
    # Generate the plot figure
    if add_deployments:
        s = ds.plot.scatter("time", param, ax=ax, hue="deployment", hue_style="discrete")
    else:
        s = ds.plot.scatter("time", param, ax=ax)
        
    # Add in limits and labels
    ax.set_ylim((ymin, ymax))
    xlabel = ax.get_xlabel()
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ds[param].attrs["long_name"], fontsize=14)
    ax.set_title(ds.attrs["id"], fontsize=16)
    ax.grid()
    
    # Add in legend if deployments added
    if add_deployments:
        ax.legend(edgecolor="black", loc="center left", bbox_to_anchor=(1, 0.5), fontsize=12, title="Deployments")
        deployments = np.unique(ds["deployment"])
        for depNum in deployments:
            dt = ds.where(ds["deployment"] == depNum, drop=True)["time"].min()
            ax.vlines(dt.values, yavg-4*ystd, yavg+4*ystd)
            ax.text(dt.values, yavg-3*ystd, str(int(depNum)), fontsize=14, weight="bold")
            
    fig.autofmt_xdate()
    
    return fig, ax


def plot_gross_range(ds, param, gross_range):
    """Plot the data with the associated climatology values.

    Parameters
    ----------
    ds: (xarray.Dataset)
        An xarray dataset downloaded from OOINet
    param: (str)
        The parameter name of the data variable in the OOI
        dataset to plot.
    gross_range: (qartod.gross_range object)
        An object containing the calculated gross_range values
        for the associated dataset and variable
        
    Returns
    -------
    fig, ax: (matplotlib figs)
        Figure and axis handles for the matplotlib image
    """
    # Initialize the data
    fig, ax = plt.subplots(figsize=(12, 8))

    # Scatter plot the data
    ax.plot(ds.time, ds[param], linestyle="", marker=".", color="tab:red")
    ax.fill_between(ds.time, gross_range.suspect_min, gross_range.suspect_max, color="tab:red", alpha=0.3)
    yavg, ystd = ds[param].mean(), ds[param].std()
    ax.set_ylim(yavg-5*ystd, yavg+5*ystd)
    ax.grid()
    ax.set_ylabel(ds[param].attrs["long_name"])
    ax.set_title(ds.attrs["id"])
    
    return fig, ax


def plot_climatology(ds, param, climatology):
    """Plot the data with the associated climatology values.

    Parameters
    ----------
    ds: (xarray.Dataset)
        An xarray dataset downloaded from OOINet
    param: (str)
        The parameter name of the data variable in the OOI
        dataset to plot.
    climatology: (qartod.climatology object)
        An object containing the calculated climatology values
        for the associated dataset and variable
    
    Returns
    -------
    fig, ax: (matplotlib figs)
        Figure and axis handles for the matplotlib image
    """
    # Initialize the plots
    fig, ax = plt.subplots(figsize = (12, 8))

    # Observations
    ax.plot(ds.time, ds[param], marker=".", linestyle="", color="tab:red", zorder=0, label="Observations")
    yavg, ystd = np.mean(ds[param]), np.std(ds[param])
    ymin, ymax = yavg-ystd*5, yavg+ystd*5
    ax.set_ylim((ymin, ymax))

    # Standard Deviation +/- 3
    for t in climatology.fitted_data.index:
        t0 = pd.Timestamp(year=t.year, month=t.month, day=1)
        mu = climatology.monthly_fit.loc[t.month]
        std = climatology.monthly_std.loc[t.month]
        ax.hlines(mu, t0, t, color="black", linewidth=3, label="Climatological Fit")
        ax.fill_between([t0, t], [mu+3*std, mu+3*std], [mu-3*std, mu-3*std], color="tab:red", alpha=0.3, label="3*$\sigma$")
    ax.grid()

    # Add legend and labels
    handles, labels = ax.get_legend_handles_labels()[0][0:3], ax.get_legend_handles_labels()[1][0:3]
    ax.legend(handles, labels, fontsize=12)
    ax.set_title("-".join((ds.attrs["id"].split("-")[0:4])), fontsize=16)
    ax.set_ylabel(ds[param].attrs["long_name"], fontsize=16)
    fig.autofmt_xdate()
    
    return fig, ax
