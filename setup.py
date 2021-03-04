import setuptools

with open("README.md", "rb") as fh:
    long_description = fh.read().decode("utf-8")

setuptools.setup(
    name='coursesical',
    version='0.0.1',
    url='https://github.com/cdfmlr/coursesical',
    license='MIT',
    author='CDFMLR',
    author_email='cdfmlr@outlook.com',
    description='Courses to iCalendar.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
    python_requires='>=3.6',
    install_requires=['selenium', 'lxml', 'beautifulsoup4', 'icalendar'],
)