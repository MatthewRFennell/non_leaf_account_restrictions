from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name = 'non_leaf_account_restrictions',
    packages = find_packages(),
    python_requires = '>=3.3',
    version = '0.0.1',
    license = 'MIT',
    description = 'Disallow transactions to non-leaf accounts in Beancount',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    author = 'Matthew Fennell',
    author_email = 'matthew.robert.fennell@gmail.com',
    url = 'https://github.com/MatthewRFennell/non_leaf_account_restrictions',
    keywords = [ 'beancount' ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
