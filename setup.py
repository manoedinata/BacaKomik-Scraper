import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bacakomikscraper",
    version="0.1",
    author="manoedinata",
    author_email="manoedinata@gmail.com",
    description="BacaKomik.co Scraper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
        "beautifulsoup4",
    ],
    python_requires='>=3.6',
)
