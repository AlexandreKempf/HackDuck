import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

packages = ["HackDuck"]

setuptools.setup(
    name="HackDuck",
    version="0.1.5",
    author="Alexandre Kempf",
    author_email="alexandre.kempf@cri-paris.org",
    description="Machine learning data flow for reproducible data science",
    long_description=long_description,
    package_dir={"": "src"},
    packages=["HackDuck"],
    long_description_content_type="text/markdown",
    url="https://github.com/AlexandreKempf/HackDuck",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'prefect',
          'mlflow',
          'pyyaml',
          'numpy',
          'torch',
          'simplejson',
          'TaskBank',
      ],

    python_requires='>=3.6',
    scripts=['hackduck']

)
