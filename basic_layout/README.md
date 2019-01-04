# Basic layout coverage example

## Testing in-src code
```bash
$ pytest --cov mypackage

============================= test session starts =============================
platform linux -- Python 3.7.1, pytest-4.0.2, py-1.7.0, pluggy-0.8.0
rootdir: /home/will/projects/pytest-coverage-examples/basic_layout, inifile:
plugins: cov-2.6.0
collected 0 items / 3 errors
Coverage.py warning: No data was collected. (no-data-collected)

=================================== ERRORS ====================================
___________________ ERROR collecting tests/test_module_c.py ___________________
ImportError while importing test module '/home/will/projects/pytest-coverage-examples/basic_layout/tests/test_module_c.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
tests/test_module_c.py:1: in <module>
    from mypackage.module_c import c
E   ModuleNotFoundError: No module named 'mypackage'
_________________ ERROR collecting tests/test_subpackage_a.py _________________
ImportError while importing test module '/home/will/projects/pytest-coverage-examples/basic_layout/tests/test_subpackage_a.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
tests/test_subpackage_a.py:1: in <module>
    from mypackage.subpackage_a import a
E   ModuleNotFoundError: No module named 'mypackage'
_________________ ERROR collecting tests/test_subpackage_b.py _________________
ImportError while importing test module '/home/will/projects/pytest-coverage-examples/basic_layout/tests/test_subpackage_b.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
tests/test_subpackage_b.py:1: in <module>
    from mypackage.subpackage_b import b
E   ModuleNotFoundError: No module named 'mypackage'

----------- coverage: platform linux, python 3.7.1-final-0 -----------
Name                                 Stmts   Miss  Cover
--------------------------------------------------------
mypackage/__init__.py                    0      0   100%
mypackage/module_c.py                    2      2     0%
mypackage/subpackage_a/__init__.py       0      0   100%
mypackage/subpackage_a/module_a.py       2      2     0%
mypackage/subpackage_b/__init__.py       0      0   100%
mypackage/subpackage_b/module_b.py       2      2     0%
--------------------------------------------------------
TOTAL                                    6      6     0%

!!!!!!!!!!!!!!!!!!! Interrupted: 3 errors during collection !!!!!!!!!!!!!!!!!!!
=========================== 3 error in 0.12 seconds ===========================
```

The reason for the tests failing to import the package is due to `pytest`
removing `$PWD` from `sys.path` to avoid importing development code instead of
installed code. This can be mitigated by either setting `PYTHONPATH=.` or adding
a `__init__.py` to `tests` (which has the side effect of pytest adding `$PWD` to
`sys.path`).

```bash
$ PYTHONPATH=. pytest  --cov mypackage
============================= test session starts =============================
platform linux -- Python 3.7.1, pytest-4.0.2, py-1.7.0, pluggy-0.8.0
rootdir: /home/will/projects/pytest-coverage-examples/basic_layout, inifile:
plugins: cov-2.6.0
collected 3 items

tests/test_module_c.py .                                                [ 33%]
tests/test_subpackage_a.py .                                            [ 66%]
tests/test_subpackage_b.py .                                            [100%]

----------- coverage: platform linux, python 3.7.1-final-0 -----------
Name                                 Stmts   Miss  Cover
--------------------------------------------------------
mypackage/__init__.py                    0      0   100%
mypackage/module_c.py                    2      0   100%
mypackage/subpackage_a/__init__.py       1      0   100%
mypackage/subpackage_a/module_a.py       2      0   100%
mypackage/subpackage_b/__init__.py       1      0   100%
mypackage/subpackage_b/module_b.py       2      0   100%
--------------------------------------------------------
TOTAL                                    8      0   100%


========================== 3 passed in 0.07 seconds ===========================
```

Now for the `tests/__init__.py` solution:

```bash
$ touch tests/__init__.py
$ pytest --cov mypackage
============================= test session starts =============================
platform linux -- Python 3.7.1, pytest-4.0.2, py-1.7.0, pluggy-0.8.0
rootdir: /home/will/projects/pytest-coverage-examples/basic_layout, inifile:
plugins: cov-2.6.0
collected 3 items

tests/test_module_c.py .                                                [ 33%]
tests/test_subpackage_a.py .                                            [ 66%]
tests/test_subpackage_b.py .                                            [100%]

----------- coverage: platform linux, python 3.7.1-final-0 -----------
Name                                 Stmts   Miss  Cover
--------------------------------------------------------
mypackage/__init__.py                    0      0   100%
mypackage/module_c.py                    2      0   100%
mypackage/subpackage_a/__init__.py       1      0   100%
mypackage/subpackage_a/module_a.py       2      0   100%
mypackage/subpackage_b/__init__.py       1      0   100%
mypackage/subpackage_b/module_b.py       2      0   100%
--------------------------------------------------------
TOTAL                                    8      0   100%


========================== 3 passed in 0.06 seconds ===========================
$ rm tests/__init__.py
```

## Testing installed code

Since `pytest` removes `$PWD` from `sys.path` by default, if you don't have a
`tests/__init__.py` file, then you're almost ready for collecting coverage on an
installed package.

```bash
$ python setup.py install
$ pytest --cov mypackage
============================= test session starts =============================
platform linux -- Python 3.7.1, pytest-4.0.2, py-1.7.0, pluggy-0.8.0
rootdir: /home/will/projects/pytest-coverage-examples/basic_layout, inifile:
plugins: cov-2.6.0
collected 3 items

tests/test_module_c.py .                                                [ 33%]
tests/test_subpackage_a.py .                                            [ 66%]
tests/test_subpackage_b.py .                                            [100%]Coverage.py warning: No data was collected. (no-data-collected)


----------- coverage: platform linux, python 3.7.1-final-0 -----------
Name                                 Stmts   Miss  Cover
--------------------------------------------------------
mypackage/__init__.py                    0      0   100%
mypackage/module_c.py                    2      2     0%
mypackage/subpackage_a/__init__.py       1      1     0%
mypackage/subpackage_a/module_a.py       2      2     0%
mypackage/subpackage_b/__init__.py       1      1     0%
mypackage/subpackage_b/module_b.py       2      2     0%
--------------------------------------------------------
TOTAL                                    8      8     0%


========================== 3 passed in 0.06 seconds ===========================
```

The reason for this behaviour is that `pytest-cov` picks up `mypackage` as a the
local in-src folder, rather than the installed package, and so installs coverage
hooks for those files, rather than the installed files. If you can run your
tests from a different directory where the in-src `mypackage` folder isn't
importable, then you can *almost* avoid this issue:

```bash
$ cd tests
$ pytest --cov mypackage
============================= test session starts =============================
platform linux -- Python 3.7.1, pytest-4.0.2, py-1.7.0, pluggy-0.8.0
rootdir: /home/will/projects/pytest-coverage-examples/basic_layout, inifile:
plugins: cov-2.6.0
collected 3 items

test_module_c.py .                                                      [ 33%]
test_subpackage_a.py .                                                  [ 66%]
test_subpackage_b.py .                                                  [100%]

----------- coverage: platform linux, python 3.7.1-final-0 -----------
Name                                                                                                                                          Stmts   Miss  Cover
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
/home/will/projects/pytest-coverage-examples/.venv/lib/python3.7/site-packages/mypackage-0.0.1-py3.7.egg/mypackage/__init__.py                    0      0   100%
/home/will/projects/pytest-coverage-examples/.venv/lib/python3.7/site-packages/mypackage-0.0.1-py3.7.egg/mypackage/module_c.py                    2      0   100%
/home/will/projects/pytest-coverage-examples/.venv/lib/python3.7/site-packages/mypackage-0.0.1-py3.7.egg/mypackage/subpackage_a/__init__.py       1      0   100%
/home/will/projects/pytest-coverage-examples/.venv/lib/python3.7/site-packages/mypackage-0.0.1-py3.7.egg/mypackage/subpackage_a/module_a.py       2      0   100%
/home/will/projects/pytest-coverage-examples/.venv/lib/python3.7/site-packages/mypackage-0.0.1-py3.7.egg/mypackage/subpackage_b/__init__.py       1      0   100%
/home/will/projects/pytest-coverage-examples/.venv/lib/python3.7/site-packages/mypackage-0.0.1-py3.7.egg/mypackage/subpackage_b/module_b.py       2      0   100%
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
TOTAL                                                                                                                                             8      0   100%


========================== 3 passed in 0.05 seconds ===========================
```

However, if you can't, and your tests rely on being run from the root folder
(e.g. use of relative paths) then you'll have to find the installed path and
then pass that to `pytest-cov` to install coverage hooks correctly

```
$ cd
$ python -c 'import mypackage, os; print(os.path.dirname(os.path.abspath(mypackage.__file__)))'
/home/will/projects/pytest-coverage-examples/.venv/lib/python3.7/site-packages/mypackage-0.0.1-py3.7.egg/mypackage
$ cd -
$ pytest --cov /home/will/projects/pytest-coverage-examples/.venv/lib/python3.7/site-packages/mypackage-0.0.1-py3.7.egg/mypackage 
============================= test session starts =============================
platform linux -- Python 3.7.1, pytest-4.0.2, py-1.7.0, pluggy-0.8.0
rootdir: /home/will/projects/pytest-coverage-examples/basic_layout, inifile:
plugins: cov-2.6.0
collected 3 items

tests/test_module_c.py .                                                [ 33%]
tests/test_subpackage_a.py .                                            [ 66%]
tests/test_subpackage_b.py .                                            [100%]
Coverage.py warning: Module /home/will/projects/pytest-coverage-examples/.venv/lib/python3.7/site-packages/mypackage-0.0.1-py3.7.egg/mypackage was never imported. (module-not-imported)
Coverage.py warning: No data was collected. (no-data-collected)
WARNING: Failed to generate report: No data to report.



============================== warnings summary ===============================
Failed to generate report: No data to report.

-- Docs: https://docs.pytest.org/en/latest/warnings.html

----------- coverage: platform linux, python 3.7.1-final-0 -----------
Name    Stmts   Miss  Cover
---------------------------

==================== 3 passed, 1 warnings in 0.05 seconds =====================
```

The issue now is that the path we've got is for an egg file, which `pytest-cov`
doesn't accept. If we use `pip install .` instead of `python setup.py install`
to install the package we'll end up with an unpacked folder which *we can* use
to collect coverage:

```bash
$ pip uninstall mypackage
$ pip install .
$ cd
$ python -c 'import mypackage, os; print(os.path.dirname(os.path.abspath(mypackage.__file__)))'
/home/will/projects/pytest-coverage-examples/.venv/lib/python3.7/site-packages/mypackage
$ cd -
$ pytest --cov /home/will/projects/pytest-coverage-examples/.venv/lib/python3.7/site-packages/mypackage
============================= test session starts =============================
platform linux -- Python 3.7.1, pytest-4.0.2, py-1.7.0, pluggy-0.8.0
rootdir: /home/will/projects/pytest-coverage-examples, inifile:
plugins: cov-2.6.0
collected 3 items

tests/test_module_c.py .                                                [ 33%]
tests/test_subpackage_a.py .                                            [ 66%]
tests/test_subpackage_b.py .                                            [100%]

----------- coverage: platform linux, python 3.7.1-final-0 -----------
Name                                                                                                                Stmts   Miss  Cover
---------------------------------------------------------------------------------------------------------------------------------------
/home/will/projects/pytest-coverage-examples/.venv/lib/python3.7/site-packages/mypackage/__init__.py                    0      0   100%
/home/will/projects/pytest-coverage-examples/.venv/lib/python3.7/site-packages/mypackage/module_c.py                    2      0   100%
/home/will/projects/pytest-coverage-examples/.venv/lib/python3.7/site-packages/mypackage/subpackage_a/__init__.py       1      0   100%
/home/will/projects/pytest-coverage-examples/.venv/lib/python3.7/site-packages/mypackage/subpackage_a/module_a.py       2      0   100%
/home/will/projects/pytest-coverage-examples/.venv/lib/python3.7/site-packages/mypackage/subpackage_b/__init__.py       1      0   100%
/home/will/projects/pytest-coverage-examples/.venv/lib/python3.7/site-packages/mypackage/subpackage_b/module_b.py       2      0   100%
---------------------------------------------------------------------------------------------------------------------------------------
TOTAL                                                                                                                   8      0   100%


========================== 3 passed in 0.07 seconds ===========================
```

We've now got ugly paths in our coverage report (which can also cause issues
with reporting tools like codecov). To mitigate this we can make use of the
path combination feature of `coverage.py` to rewrite these long paths to
relative ones:

```bash
$ cat > .coveragerc
[paths]
source =
    mypackage
    **/site-packages/mypackage
$ pytest --cov /home/will/projects/pytest-coverage-examples/.venv/lib/python3.7/site-packages/mypackage
... # long path coverage report omitted
$ coverage combine .coverage
$ coverage report
Name                                 Stmts   Miss  Cover
--------------------------------------------------------
mypackage/__init__.py                    0      0   100%
mypackage/module_c.py                    2      0   100%
mypackage/subpackage_a/__init__.py       1      0   100%
mypackage/subpackage_a/module_a.py       2      0   100%
mypackage/subpackage_b/__init__.py       1      0   100%
mypackage/subpackage_b/module_b.py       2      0   100%
--------------------------------------------------------
TOTAL                                    8      0   100%
```

## Conclusion

A lot of these issues go away if you use a `src` folder based layout instead, as
the root cause of these issues is different tools manipulating `sys.path` in
different ways causing discrepancies between each tool's location of
`mypackage`. By removing `mypackage` from `$PWD` we avoid this issue.
