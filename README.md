# GSEE Redux: Global Solar Energy Estimator

This is a fork of [GSEE](https://github.com/renewables-ninja/gsee).

`GSEE` is a solar energy simulation library designed for rapid calculations and ease of use. [Renewables.ninja](https://www.renewables.ninja/) uses `GSEE`.

The development of `GSEE` predates the existence of [`pvlib-python`](https://pvlib-python.readthedocs.io/) but builds on its functionality as of v0.4.0. Use `GSEE` if you want fast simulations with sensible defaults and solar energy technologies other than PV, and `pvlib-python` if you need control over the nuts and bolts of simulating PV systems.

## Installation

```
pip install gsee-redux
```

Currently pip is the only supported installation method.

The original GSEE library was intended to be installed through Conda,
but this is not yet possible for this version.
## Documentation

See the [original documentation](https://gsee.readthedocs.io/) for more information on
`GSEE`'s functionality and for examples.

## License

BSD-3-Clause
