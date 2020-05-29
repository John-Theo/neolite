import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="neolite",
    version="0.7.2",
    author="John Theo",
    author_email="xinhaozhuang.work@gmail.com",
    description="Super light weight neo4j python driver with multi-graph support.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/John-Theo/neolite",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests'
    ],
    python_requires='>=3.6'
)
