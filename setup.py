from setuptools import setup


setup(
    name='trolley',
    version='0.1.6',
    description='Trolley syncs issues between CSV, Github, and Trello.',
    author='Jeff Triplett',
    author_email='jeff.triplett@gmail.com',
    url='http://github.com/jefftriplett/trolley',
    packages=[
        'trolley',
        'trolley.commands',
    ],
    py_modules=[
        'trolley',
    ],
    entry_points={
        'console_scripts': [
            'trolley=trolley.cli:cli',
        ]
    },
    install_requires=[
        'click',
        'github3.py',
        'dynaconf',
        # 'git+ssh://git@github.com/sarumont/py-trello.git@0.2.3',
    ],
)
