import gpt_service as gpt

system_role = "You're a helpful assistant and expert on analyzing python library documentation"

ai = gpt.GPTService(system_role=system_role, temperature=0.2)

ai.prompt = """Using the documentation below, summarize the seaborn lineplot function, respond with fields \
for description, parameters, attributes, code examples:
def lineplot(data=None, *, x=None, y=None, hue=None, size=None, style=None, units=None, palette=None, hue_order=None, hue_norm=None, sizes=None, size_order=None, size_norm=None, dashes=True, markers=None, style_order=None, estimator='mean', errorbar=('ci', 95), n_boot=1000, seed=None, orient='x', sort=True, err_style='band', err_kws=None, legend='auto', ci='deprecated', ax=None, **kwargs)
Draw a line plot with possibility of several semantic groupings.

The relationship between x and y can be shown for different subsets of the data using the hue, size, and style parameters. These parameters control what visual semantics are used to identify the different subsets. It is possible to show up to three dimensions independently by using all three semantic types, but this style of plot can be hard to interpret and is often ineffective. Using redundant semantics (i.e. both hue and style for the same variable) can be helpful for making graphics more accessible.

See the tutorial <relational_tutorial> for more information.

The default treatment of the hue (and to a lesser extent, size) semantic, if present, depends on whether the variable is inferred to represent "numeric" or "categorical" data. In particular, numeric variables are represented with a sequential colormap by default, and the legend entries show regular "ticks" with values that may or may not exist in the data. This behavior can be controlled through various parameters, as described and illustrated below.

By default, the plot aggregates over multiple y values at each value of x and shows an estimate of the central tendency and a confidence interval for that estimate.

Parameters
data : pandas.DataFrame, numpy.ndarray, mapping, or sequence
    Input data structure. Either a long-form collection of vectors that can be assigned to named variables or a wide-form dataset that will be internally reshaped.
x, y : vectors or keys in data
    Variables that specify positions on the x and y axes.
hue : vector or key in data
    Grouping variable that will produce lines with different colors. Can be either categorical or numeric, although color mapping will behave differently in latter case.
size : vector or key in data
    Grouping variable that will produce lines with different widths. Can be either categorical or numeric, although size mapping will behave differently in latter case.
style : vector or key in data
    Grouping variable that will produce lines with different dashes and/or markers. Can have a numeric dtype but will always be treated as categorical.
units : vector or key in data
    Grouping variable identifying sampling units. When used, a separate line will be drawn for each unit with appropriate semantics, but no legend entry will be added. Useful for showing distribution of experimental replicates when exact identities are not needed.
palette : string, list, dict, or matplotlib.colors.Colormap
    Method for choosing the colors to use when mapping the hue semantic. String values are passed to color_palette. List or dict values imply categorical mapping, while a colormap object implies numeric mapping.
hue_order : vector of strings
    Specify the order of processing and plotting for categorical levels of the hue semantic.
hue_norm : tuple or matplotlib.colors.Normalize
    Either a pair of values that set the normalization range in data units or an object that will map from data units into a [0, 1] interval. Usage implies numeric mapping.
sizes : list, dict, or tuple
    An object that determines how sizes are chosen when size is used. List or dict arguments should provide a size for each unique data value, which forces a categorical interpretation. The argument may also be a min, max tuple.
size_order : list
    Specified order for appearance of the size variable levels, otherwise they are determined from the data. Not relevant when the size variable is numeric.
size_norm : tuple or Normalize object
    Normalization in data units for scaling plot objects when the size variable is numeric.
dashes : boolean, list, or dictionary
    Object determining how to draw the lines for different levels of the style variable. Setting to True will use default dash codes, or you can pass a list of dash codes or a dictionary mapping levels of the style variable to dash codes. Setting to False will use solid
    lines for all subsets. Dashes are specified as in matplotlib: a tuple of (segment, gap) lengths, or an empty string to draw a solid line.
markers : boolean, list, or dictionary
    Object determining how to draw the markers for different levels of the style variable. Setting to True will use default markers, or you can pass a list of markers or a dictionary mapping levels of the style variable to markers. Setting to False will draw marker-less lines. Markers are specified as in matplotlib.
style_order : list
    Specified order for appearance of the style variable levels otherwise they are determined from the data. Not relevant when the style variable is numeric.
estimator : name of pandas method or callable or None
    Method for aggregating across multiple observations of the y variable at the same x level. If None, all observations will be drawn.
errorbar : string, (string, number) tuple, or callable
    Name of errorbar method (either "ci", "pi", "se", or "sd"), or a tuple with a method name and a level parameter, or a function that maps from a vector to a (min, max) interval.
n_boot : int
    Number of bootstraps to use for computing the confidence interval.
seed : int, numpy.random.Generator, or numpy.random.RandomState
    Seed or random number generator for reproducible bootstrapping.
orient : "x" or "y"
    Dimension along which the data are sorted / aggregated. Equivalently, the "independent variable" of the resulting function.
sort : boolean
    If True, the data will be sorted by the x and y variables, otherwise lines will connect points in the order they appear in the dataset.
err_style : "band" or "bars"
    Whether to draw the confidence intervals with translucent error bands or discrete error bars.
err_kws : dict of keyword arguments
    Additional parameters to control the aesthetics of the error bars. The kwargs are passed either to matplotlib.axes.Axes.fill_between or matplotlib.axes.Axes.errorbar, depending on err_style.
legend : "auto", "brief", "full", or False
    How to draw the legend. If "brief", numeric hue and size variables will be represented with a sample of evenly spaced values. If "full", every group will get an entry in the legend. If "auto", choose between brief or full representation based on number of levels. If False, no legend data is added and no legend is drawn.
ci : int or "sd" or None
    Size of the confidence interval to draw when aggregating.

ax : matplotlib.axes.Axes
    Pre-existing axes for the plot. Otherwise, call matplotlib.pyplot.gca internally.
kwargs : key, value mappings
    Other keyword arguments are passed down to matplotlib.axes.Axes.plot.
"""

answer = ai.get_response(ai.prompt, table=True)

print(answer)

answer['description']
answer['parameters']
answer['examples']



