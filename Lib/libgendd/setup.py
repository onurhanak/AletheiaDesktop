import setuptools

with open("README.md", "r", errors="replace") as fh:
    long_description = fh.read()

setuptools.setup(
    name="libgen_api_dd",
    packages=["libgen_api_dd"],
    version="1.0.1",
    description="Search Library genesis by Title or Author with direct download links",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/onurhanak/libgen-api-dd",
    author="OA",
    author_email="onurhanak@protonmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords=["libgen search", "libgen api", "search libgen", "search library genesis"],
    install_requires=["bs4", "requests", "lxml"],
)
