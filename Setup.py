from setuptools import setup
import setuptools

# setup(
#     name='BindingPredictor',
#     version='0.1',
#     scripts=['BindingPredictor']
# )

setup(
    name="BindingPredictor",
    version="0.1",
    #author="Example Author",
    #author_email="author@example.com",
    #description="A small example package",
    #long_description=long_description,
    #long_description_content_type="text/markdown",
    #url="https://github.com/pypa/example-project",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)