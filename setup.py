import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="pubmlst_client",
    version="0.3.0",
    description="Find and download schemes from pubmlst.org",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Public-Health-Bioinformatics/pubmlst_client",
    author="Dan Fornika",
    author_email="dan.fornika@bccdc.ca",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["pubmlst_client"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pubmlst_list=pubmlst_client.list:main",
            "pubmlst_download=pubmlst_client.download:main",
        ]
    },
)
