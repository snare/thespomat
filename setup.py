from setuptools import setup, find_packages

setup(
    name="thespomat",
    version="0.1",
    author="snare",
    author_email="snare@ho.ax",
    description=("A movie subtitle Twitter bot"),
    license="Buy snare a beer",
    keywords="movie subtitle twitter bot",
    url="https://github.com/snare/thespomat",
    packages=find_packages(),
    package_data={'thespomat': ['config/*']},
    install_package_data=True,
    install_requires=['scruffington', 'python-twitter', 'requests', 'pysrt'],
    entry_points={
        'console_scripts': ['thespomat=thespomat:main']
    },
    zip_safe=False
)
