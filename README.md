# Pytest code coverage examples

This repository demonstrates various ways of collecting code coverage using
[`pytest`](https://docs.pytest.org/en/latest/) with
[`pytest-cov`](https://pytest-cov.readthedocs.io/en/latest/) (which leverages
[`coverage.py`](https://coverage.readthedocs.io/en)) against the local in-src
package and also against installed versions of the package. We look at two
common project layouts: the first, the [`basic_layout`](./basic_layout) where the package resides
at the root of the project directory, and the [`src_layout`](./src_layout) where the package
resides in a `src` subdirectory of the project directory.

After getting your [environment set up](#environment-set-up), head over to the
example

- [`basic_layout`](./basic_layout)
- [`src_layout`](./src_layout)

This repository serves as an accompaniment to my [blog post on collecting code
coverage in python](http://willprice.org/2019/01/03/python-code-coverage.html)

## Environment set up
To test these examples you'll need python 3.6+ and you'll want to set up a
virtualenv:

```bash
$ python -m venv .venv
$ pip install -r requirements.txt
```
