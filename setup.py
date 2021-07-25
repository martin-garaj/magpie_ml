import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="magpie_ml", # Replace with your own username
    version="0.9.0",
    author="Martin GARAJ",
    author_email="garaj.martin@gmail.com",
    description="Key stroke logger, visualization and analysis.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/martin3366/magpie_ml",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)