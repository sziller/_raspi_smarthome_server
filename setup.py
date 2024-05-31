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
    packages=["shmc_basePackage",
              "messages",
              "shmc_routers",
              "shmc_server",
              "sql_access",
              "sql_bases"],
    include_package_data=True,
    url='shmc.sziller.eu',  # if url is used at all
    license='MIT',  # ???
    author='sziller',
    author_email='szillerke@gmail.com',
    description='ServerPackage SmartHomeMyCastle',
    install_requires=["fastapi",
                      "passlib",
                      "psycopg2-binary",
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
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',  # Specify minimum Python version requirement.
)
