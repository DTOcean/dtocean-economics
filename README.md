[![appveyor](https://ci.appveyor.com/api/projects/status/github/DTOcean/dtocean-economics?branch=master&svg=true)](https://ci.appveyor.com/project/DTOcean/dtocean-economics)
[![codecov](https://codecov.io/gh/DTOcean/dtocean-economics/branch/master/graph/badge.svg)](https://codecov.io/gh/DTOcean/dtocean-economics)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/bb34506cc82f4df883178a6e64619eaf)](https://www.codacy.com/project/H0R5E/dtocean-economics/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=DTOcean/dtocean-economics&amp;utm_campaign=Badge_Grade_Dashboard&amp;branchId=8410911)
[![release](https://img.shields.io/github/release/DTOcean/dtocean-economics.svg)](https://github.com/DTOcean/dtocean-economics/releases/latest)

# DTOcean Economics Module

The DTOcean Economics Module provides functions to assess and compare the 
economic performance of arrays designed by DTOcean. It also acts as a support 
library for the [dtocean-maintenance]( 
https://github.com/DTOcean/dtocean-maintenance) module. It aggregates the "bill 
of materials" produced by the [dtocean-electrical]( 
https://github.com/DTOcean/dtocean-electrical) and [dtocean-moorings]( 
https://github.com/DTOcean/dtocean-moorings) modules and generates metrics such 
as the levelised cost of energy (LCOE). The module can accept multiple 
operational expenditure and energy production records.


See [dtocean-app](https://github.com/DTOcean/dtocean-app) or [dtocean-core](
https://github.com/DTOcean/dtocean-app) to use this package within the DTOcean
ecosystem.

* For python 2.7 only.

## Installation

Installation and development of dtocean-economics uses the [Anaconda 
Distribution](https://www.anaconda.com/distribution/) (Python 2.7)

### Conda Package

To install:

```
$ conda install -c dataonlygreater dtocean-economics
```

### Source Code

Conda can be used to install dependencies into a dedicated environment from
the source code root directory:

```
$ conda create -n _dtocean_econ python=2.7 pip
```

Activate the environment, then copy the `.condrc` file to store installation  
channels:

```
$ conda activate _dtocean_econ
$ copy .condarc %CONDA_PREFIX%
```

Install dtocean-economics and its dependencies using conda and pip:

```
$ conda install --file requirements-conda-dev.txt
$ pip install -e .
```

To deactivate the conda environment:

```
$ conda deactivate
```

### Tests

A test suite is provided with the source code that uses [pytest](
https://docs.pytest.org).

If not already active, activate the conda environment set up in the [Source 
Code](#source-code) section:

```
$ conda activate _dtocean_econ
```

Install packages required for testing to the environment (one time only):

```
$ conda install -y pytest
```

Run the tests:

``` 
$ py.test tests
```

### Uninstall

To uninstall the conda package:

```
$ conda remove dtocean-economics
```

To uninstall the source code and its conda environment:

```
$ conda remove --name _dtocean_econ --all
```

## Usage

An example of calculating the LCOE from a bill of materials, and two different
operational expenditure (OPEX) and energy histories.

Create the bill of materials first:

```python
>>> import pandas as pd

>>> bom_dict = {'phase': ["One", "One", "One", "Two", "Two", "Two"],
...             'unitary_cost': [0.0, 100000.0, 100000.0, 1, 1, 1],
...             'project_year': [0, 1, 2, 0, 1, 2],
...             'quantity': [1, 1, 1, 1, 10, 20]}
>>> bom_df = pd.DataFrame(bom_dict, columns=["phase",
...                                          "project_year",
...                                          "quantity",
...                                          "unitary_cost"])
>>> bom_df
  phase  project_year  quantity  unitary_cost
0   One             0         1           0.0
1   One             1         1      100000.0
2   One             2         1      100000.0
3   Two             0         1           1.0
4   Two             1        10           1.0
5   Two             2        20           1.0
```

Now build two independent OPEX records:

```python
>>> opex_dict = {'project_year': [0, 1, 2, 3, 4, 5],
>>>              'cost 0': [0.0, 100000.0, 100000.0, 1, 1, 1],
>>>              'cost 1': [0.0, 100000.0, 0, 1, 1, 100000.0]}
>>> opex_df = pd.DataFrame(opex_dict, columns=["project_year",
...                                            "cost 0",
...                                            "cost 1"])
>>> opex_df
   project_year    cost 0    cost 1
0             0       0.0       0.0
1             1  100000.0  100000.0
2             2  100000.0       0.0
3             3       1.0       1.0
4             4       1.0       1.0
5             5       1.0  100000.0
```

And the related energy production records:

```python
>>> energy_dict = {'project_year': [0, 1, 2, 3, 4, 5],
...                'energy 0': [0, 1, 2, 0, 10, 20],
...                'energy 1': [0, 1, 32, 0, 0, 20]}
>>> energy_df = pd.DataFrame(energy_dict, columns=["project_year",
...                                                "energy 0",
...                                                "energy 1"])
>>> energy_df
   project_year  energy 0  energy 1
0             0         0         0
1             1         1         1
2             2         2        32
3             3         0         0
4             4        10         0
5             5        20        20
```

Finally, collect the LCOE values, and take the mean:

```python
>>> from dtocean_economics import main

>>> result = main(bom_df, opex_df, energy_df)
>>> lcoe_values = result['LCOE']
>>> lcoe_values
0    12122.242424
1     7547.792453
dtype: float64

>>> lcoe_values.mean()
9835.017438536306
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.

See [this blog post](
https://www.dataonlygreater.com/latest/professional/2017/03/09/dtocean-development-change-management/)
for information regarding development of the DTOcean ecosystem.

Please make sure to update tests as appropriate.

## Credits

This package was initially created as part of the [EU DTOcean project](
https://www.dtoceanplus.eu/About-DTOceanPlus/History) by:

 * Mathew Topper at [TECNALIA](https://www.tecnalia.com)
 * Marta Silva at [WavEC](https://www.wavec.org/)

It is now maintained by Mathew Topper at [Data Only Greater](
https://www.dataonlygreater.com/).

## License

[GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/)
