from setuptools import setup, find_packages

setup(
    name='Trolley',
    version='0.1.0',
    description='',
    author='Jeff Triplett',
    author_email='jeff.triplett@gmail.com',
    url='http://github.com/jefftriplett/trolley',
    packages=find_packages(),
    py_modules=['trolley'],
    entry_points={
        'console_scripts': [
            'trolley=trolley:cli',
        ]
    },
    install_requires=[
        'click',
        'click-config',
        'github3.py',
        'trello',
    ],
)
