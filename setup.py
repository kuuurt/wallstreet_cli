import setuptools

setuptools.setup(
    version="0.0.1",
    install_requires=[
           'wallstreet==0.3',
           'forex-python==1.5'

    ],
    description="Wall street cli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points = {
        'console_scripts': ['wallstreet_cli=wallstreet_cli.main:main'],
    }
)
