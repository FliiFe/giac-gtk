import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="giac-gtk-fliife",
    version="0.0.3",
    author="Théophile Cailliau",
    author_email="theophile.cailliau@gmail.com",
    description="A graphical frontend for giac",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FliiFe/giac-gtk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Environment :: X11 Applications :: GTK",
        "Operating System :: POSIX :: Linux",
    ],
)
