#encoding: utf-8

from setuptools import setup, find_packages


setup(
    name='zstat',
    version='0.0.6',
    packages=find_packages(),
    entry_points={
            'console_scripts': [
                'zstat = zstat.main:main',
            ]
    },
    install_requires=["MySQL-python==1.2.5", "pyrabbit==1.0.1"],
    url='https://github.com/sievetech/zstat',
    license='3-BSD',
    author='Sievetech',
    author_email='sievetech@sieve.com.br',
    description='A set of metrics to be sent to the Zabbix monitoring system',
)
