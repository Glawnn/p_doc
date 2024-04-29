from setuptools import setup, find_packages

files = {
    "long_description": "README.md",
    "requirements": "requirements.txt",
    "version": "VERSION",
}

param = {}

for key in files:
    try:
        with open(files[key], "r", encoding="utf-8") as file:
            param[key] = file.read()
    except(OSError, IOError) as exc:
        param[key] = ""

setup(
    name="p_doc",
    version=param["version"],
    description="A Python package for generate documentation from python files.",
    author="Gael",
    author_email="",
    packages=find_packages(include=["p_doc", "p_doc.*"]),
    install_requires=param["requirements"].split("\n"),
    long_description=param["long_description"],
    long_description_content_type="text/markdown",
    url="https://github.com/Glawnn/p_doc",
    project_urls={
        'Source': 'https://github.com/Glawnn/p_doc',
    },
    entry_points={
        "console_scripts": [
            "p-doc = p_doc.app:main",
        ]
    },
)