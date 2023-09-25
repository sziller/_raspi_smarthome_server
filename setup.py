#!/usr/bin/python3.10
"""
setup function to be run when creating packages for ChainRecorder Engine
command to be typed in:
python setup.py sdist # bdist_wheel
"""

from setuptools import setup

setup(
    name='smarthome_server',  # package name, used at pip or tar.
    version='0.0.0',  # version Nr.... whatever
    packages=["SmartHomeServer"],  # string list of packages to be translated
    include_package_data=True,
    url='',  # if url is used at all
    license='',  # ...
    author='sziller',  # well obvious
    author_email='szillerke@gmail.com',  # well obvious
    description='ServerPackage SmartHome',  # well obvious
    install_requires=["pydantic", "bitcoinlib", "requests", "psycopg2", "sqlalchemy", "pyqrcode", "base58", "ecdsa", "pytest", "pyaml"], # ATTENTION! Wheel file needed, depending on environment
    dependency_links=[],  # if dependent on external projects
)
