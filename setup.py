from setuptools import setup

setup(
    name = 'highspot',
    version = '0.1.0',
    packages = ['highspot'],
    author="Deb Jones",
    author_email="debjones513@gmail.com",
    #install_requires=['docutils>=0.3'],
    entry_points = {
        'console_scripts': [
            'highspot = highspot.__main__:main'
        ]
    })