python3.4 setup.py register -r pypitest
python3.4 setup.py sdist upload -r pypitest
python3.4 setup.py register -r pypi
python3.4 setup.py sdist upload -r pypi