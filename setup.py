
from setuptools import setup

setup(
    name='vackup',
    version='1.0',
    packages=['vackup'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'vackup = vackup.app:main'
        ]
    },
)
