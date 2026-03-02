# Python Compatibility Checks

This directory contains small Docker-based runtime checks for `src/modules/monitoring.py`
under both Python 2 and Python 3.

Run the commands below from the root of the `daro-utils` repo.

## Files

- `Dockerfile.py2`: minimal Python 2.7 image
- `Dockerfile.py3`: minimal Python 3.11 image
- `test_monitoring_py2.py`: runtime check for Python 2 behavior
- `test_monitoring_py3.py`: runtime check for Python 3 behavior

## Run

Build the images:

```sh
docker build -f tests/python_compat/Dockerfile.py2 -t daro-utils-py2-test .
docker build -f tests/python_compat/Dockerfile.py3 -t daro-utils-py3-test .
```

Run the checks:

```sh
docker run --rm -v "$PWD":/work daro-utils-py2-test python2 /work/tests/python_compat/test_monitoring_py2.py
docker run --rm -v "$PWD":/work daro-utils-py3-test python3 /work/tests/python_compat/test_monitoring_py3.py
```

Expected output:

```text
python2 monitoring test passed
python3 monitoring test passed
```
