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
    packages=["shmc_server", "shmc_basePackage", "shmc_slqAccess", "shmc_sqlBases"],
    include_package_data=True,
    url='shmc.sziller.eu',  # if url is used at all
    license='',  # ...
    author='sziller',  # well obvious
    author_email='szillerke@gmail.com',  # well obvious
    description='ServerPackage SmartHomeMyCastle',  # well obvious
    install_requires=["fastapi",
                      "passlib",
                      "psycopg2",
                      "pyaml",
                      "pydantic",
                      "pytest",
                      "python-dotenv",
                      "python-jose",
                      "python-multipart",
                      "pyzmq",
                      "requests",
                      "sqlalchemy",
                      "uvicorn"],  # ATTENTION! Wheel file needed, depending on environment
    dependency_links=[],  # if dependent on external projects
)
