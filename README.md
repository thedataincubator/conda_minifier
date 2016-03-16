# Conda `environment.yml` minifier
This is a python script to return only the top-level dependencies from an `environment.yml` file with only their version information (no binary info).

Top-level dependencies are the ones upon which nothing depends (source nodes in a DAG). E.g. `pandas` depends on `bokeh`, so we can just include `bokeh` in our `environment.yml`.

The goal of this is to make `environment.yml` files more platform-agnostic.

## Requirements
A `conda` executable.

## Usage
```
  python dep_minifier.py path_to_environment.yml > minified_environment.yml
```

