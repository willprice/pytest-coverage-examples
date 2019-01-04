# src layout coverage example

`src` project layouts put your root package under a `src` folder so tools can't
directly import your package from in-src unless you explicitly set
`PYTHONPATH=src`, whilst this may seem cumbersome it prevents many of the issues
outlined in the [basic layout coverage example](../basic_layout).

If you switch to a `src` based layout, take note of the changes in `setup.py`,
you'll need to set `package_dir={'': 'src'}` and pass `where='src'` to
`find_packages`.

## Testing in-src code

```bash
$ pytest --cov mypackage
============================= test session starts =============================
platform linux -- Python 3.7.1, pytest-4.0.2, py-1.7.0, pluggy-0.8.0
rootdir: /home/will/projects/pytest-coverage-examples/src_layout, inifile:
plugins: cov-2.6.0
collected 0 items / 3 errors
Coverage.py warning: Module mypackage was never imported. (module-not-imported)
Coverage.py warning: No data was collected. (no-data-collected)
WARNING: Failed to generate report: No data to report.


=================================== ERRORS ====================================
___________________ ERROR collecting tests/test_module_c.py ___________________
ImportError while importing test module '/home/will/projects/pytest-coverage-examples/src_layout/tests/test_module_c.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
tests/test_module_c.py:1: in <module>
    from mypackage.module_c import c
E   ModuleNotFoundError: No module named 'mypackage'
_________________ ERROR collecting tests/test_subpackage_a.py _________________
ImportError while importing test module '/home/will/projects/pytest-coverage-examples/src_layout/tests/test_subpackage_a.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
tests/test_subpackage_a.py:1: in <module>
    from mypackage.subpackage_a import a
E   ModuleNotFoundError: No module named 'mypackage'
_________________ ERROR collecting tests/test_subpackage_b.py _________________
ImportError while importing test module '/home/will/projects/pytest-coverage-examples/src_layout/tests/test_subpackage_b.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
tests/test_subpackage_b.py:1: in <module>
    from mypackage.subpackage_b import b
E   ModuleNotFoundError: No module named 'mypackage'
============================== warnings summary ===============================
Failed to generate report: No data to report.

-- Docs: https://docs.pytest.org/en/latest/warnings.html

----------- coverage: platform linux, python 3.7.1-final-0 -----------
Name    Stmts   Miss  Cover
---------------------------

!!!!!!!!!!!!!!!!!!! Interrupted: 3 errors during collection !!!!!!!!!!!!!!!!!!!
===================== 1 warnings, 3 error in 0.18 seconds =====================
```

Understandably `pytest` cannot find `mypackage` as it has not been installed,
nor is present on `sys.path`. We can simply resolve this by setting
`PYTHONPATH=src`:

```bash
$ PYTHONPATH=src pytest --cov mypackage
============================= test session starts =============================
platform linux -- Python 3.7.1, pytest-4.0.2, py-1.7.0, pluggy-0.8.0
rootdir: /home/will/projects/pytest-coverage-examples/src_layout, inifile:
plugins: cov-2.6.0
collected 3 items

tests/test_module_c.py .                                                [ 33%]
tests/test_subpackage_a.py .                                            [ 66%]
tests/test_subpackage_b.py .                                            [100%]

----------- coverage: platform linux, python 3.7.1-final-0 -----------
Name                                     Stmts   Miss  Cover
------------------------------------------------------------
src/mypackage/__init__.py                    0      0   100%
src/mypackage/module_c.py                    2      0   100%
src/mypackage/subpackage_a/__init__.py       1      0   100%
src/mypackage/subpackage_a/module_a.py       2      0   100%
src/mypackage/subpackage_b/__init__.py       1      0   100%
src/mypackage/subpackage_b/module_b.py       2      0   100%
------------------------------------------------------------
TOTAL                                        8      0   100%


========================== 3 passed in 0.07 seconds ===========================
```

and coverage collection just works.


## Testing installed code

Testing installed code is much easier than with a basic layout. Note we still
have to use `pip install .` instead of `python setup.py install` to avoid
installing a compressed egg.

```bash
$ pip install .
$ pytest --cov mypackage
============================= test session starts =============================
platform linux -- Python 3.7.1, pytest-4.0.2, py-1.7.0, pluggy-0.8.0
rootdir: /home/will/projects/pytest-coverage-examples/src_layout, inifile:
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

We can rewrite long paths to short paths by using the path combination feature
of `coverage.py`:

```bash
$ cat > .coveragerc
[paths]
source =
    src/mypackage
    **/site-packages/mypackage
$ pytest --cov mypackage
$ coverage combine .coverage
$ coverage report
Name                                     Stmts   Miss  Cover
------------------------------------------------------------
src/mypackage/__init__.py                    0      0   100%
src/mypackage/module_c.py                    2      0   100%
src/mypackage/subpackage_a/__init__.py       1      0   100%
src/mypackage/subpackage_a/module_a.py       2      0   100%
src/mypackage/subpackage_b/__init__.py       1      0   100%
src/mypackage/subpackage_b/module_b.py       2      0   100%
------------------------------------------------------------
TOTAL                                        8      0   100%
```

## Conclusion

A lot of the faff present in a basic layout coverage set up is avoided. You
explicitly control which version of your code you're testing against, without
the risk of accidentally confusing an installed version with a local in-src
version.

Cristin Maries has a good post [extolling other virtues of a src layout](https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure).
