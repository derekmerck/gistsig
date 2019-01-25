import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

metadata = {
    'name': "gistsig",
    'version': "1.1.1",
    'author': "Derek Merck",
    'author_email': "derek_merck@brown.edu"
}

setuptools.setup(
    name=metadata.get("name"),
    version=metadata.get("version"),
    author=metadata.get("author"),
    author_email=metadata.get("author_email"),
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/derekmerck/gistsig",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=(
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    license='MIT',
    entry_points='''
      [console_scripts]
      gistsig=gs_cli:_cli
    ''',
)