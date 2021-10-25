
# Plugin System

## What is Bumblebee?

Bumblebee is a low-code spreadsheet-like user interface to handle data at scale.
Bumblebee has more than +100 functions to prepare, join and transform strings, numbers, dates, and many more datatype.
Bumblebee can run over many dataframes engines like pandas, cuDF, Dask, Dask-cuDF, Vaex, and Spark.
The idea behind a plugin system is that anyone can expand the Bumblebee functionality which means that you can write a 
python function to make and operation over your data and expose it via the Bumblebee user interface.
 
## How to create a Plugin

To define a plugin you will need to creted at least three files:
* index.json that define how the plugin is presented in Bumblebee.
* .py file with the function definition.
* requirements.txt with python libraries required to run the function you defined.

### index.json

The index.json file is a json object that helps you to define how the plugin in is going to be presented to the user
in the Bumblebee user interface.
Bellow is an example of a json file structure.

```json
"knn_impute": {
    "text": "Impute (KNN)",
    "function": "df__cols__knn_impute",
    "command": "cols.knn_impute",
    "preview": "late",
    "columns": true,
    "parameters": {
      "n_neighbors": {
        "label": "Neighbors",
        "type": "int",
        "value": 5
      },
      "weights": {
        "label": "Weights",
        "type": "string",
        "value": "uniform",
        "items": {
          "uniform": "Uniform",
          "distance": "Distance"
        }
      }
    }
 ``` 

Let explore the json definition:

#### main dictionary key
In this case `knn_impute`. This is the name of the python file where the plugin code will live.

#### text
This define the xxxx in this case `Impute (KNN)` is going to be present to the user xxx.

#### function
This is the name of the function defined in the `knn_impute.py` file.

#### command
xxxx

#### preview
xxxx

#### dialog
xxxx

#### columns
xxxx

#### parameters

There are the params used by the python function you create and that will be shown in the Bumblebee user interface.
The children keys are the name of the parameters in the python function.
The children of the parameter keys support the following.

##### label
xxxx

##### type

* int. An integer value.
* string. An string value
* column. A column name presented in the dataframe.
* select. A list of options

##### value
The default value presented to the user.

##### items 
Values to select from a combobox. Used in case the `type` used is `select`.
 
### Python file
Thi is the file is which you are going to implement your plugin.
Remember that Bumblebee runs over Optimus which can handle many engines like pandas, cuDF. The idea is that 
you use the Optimus native functions, so it can your data using any engine.
Let see and example:


```python
def df__cols__knn_impute(df, cols="*", n_neighbors=5, weights="uniform", metric="nan_euclidean", output_cols=None):
    def _knn_impute(series, n_neighbors=5, weights="uniform", metric="nan_euclidean"):

        from sklearn.impute import KNNImputer
        imputer = KNNImputer(n_neighbors=n_neighbors, weights=weights, metric=metric)
        return imputer.fit_transform(series.values.reshape(-1, 1))
    
    from optimus.helpers.columns import parse_columns, get_output_cols, prepare_columns_arguments

    cols = parse_columns(df, cols)

    n_neighbors, weights, metric = prepare_columns_arguments(cols, n_neighbors, weights, metric)
    output_cols = get_output_cols(cols, output_cols)

    for col_name, output_col, _n_neighbors, _weights, _metric in zip(cols, output_cols, n_neighbors, weights, metric):

        df = df.cols.to_float(col_name)
        df = df.cols.apply(col_name, _knn_impute, output_cols=output_col, args=(_n_neighbors, _weights, _metric), mode="vectorized")

    return df
```

In this case because `_knn_impute` use `sklearn` it will only be compatible whe using `pandas` as engine.
If you want to make different implmentation that covers every engine. You cam implement something like.

```python

    from optimus import Engine
    engine = df.engine
    
    if engine == Engine.PANDAS.value:
        # Pandas Code

    elif engine == Engine.VAEX.value:
        # Vaex Code
        
    elif engine == Engine.SPARK.value:
        # Spark Code
        
    elif engine == Engine.DASK.value:
        # Dask Code
        
    elif engine == Engine.IBIS.value:
        # Ibis Code
        
    elif engine == Engine.CUDF.value:
        # cuDF Code
        
    elif engine == Engine.DASK_CUDF.value:
        # Dask-cuDF Code
        
    else:
        RaiseIt.value_error(engine, Engine.list())
        
```

#### Name Convention 
For sake of legibility we recommend name your function like:
```df__(cols/rows)__(function_name)```

Here the steps:
* First `df` to identify that you using a operation over a dataframe.
* Then `cols` or `rows` to identify that you are operating over columns or rows.
* Then the function name in snakecase `knn_impute`.

In this case the name of our function is `df__cols__knn_impute`

### requirements.txt

This handle your python code dependencies. This libraries are installed by Bumblebee when it load the plugin in the front end.

```text
scikit-learn==0.24.2

```

