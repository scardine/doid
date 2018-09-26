import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="doid",
    version="0.0.1",
    author="Paulo Scardine",
    author_email="paulo@xtend.com.br",
    description="Generic container with complex filter/sorting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scardine/doid",
    test_suite='nose.collector',
    tests_require=['nose'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License""",
        "Operating System :: OS Independent",
    ]
)