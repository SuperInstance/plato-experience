from setuptools import setup, find_packages

setup(
    name="plato-experience",
    version="0.1.0",
    description="The breeding farm for AI agents",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Cocapn Fleet",
    url="https://github.com/SuperInstance/plato-experience",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: AI :: Agents",
        "License :: OSI Approved :: MIT License",
    ],
)
