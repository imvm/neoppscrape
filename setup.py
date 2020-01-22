from setuptools import setup, find_packages

setup(
    name         = 'bestppscraper',
    version      = '1.0',
    packages     = find_packages(),
    scripts      = ['bin/run.sh'],
    entry_points = {'scrapy': ['settings = bestppscraper.settings']},
)
