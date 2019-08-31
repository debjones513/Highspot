from setuptools import setup

setup(
    name = 'highspot',
    version = '0.1.0',
    packages = ['highspot'],
    entry_points = {
        'console_scripts': [
            'highspot = highspot.__main__:main'
        ]
    })