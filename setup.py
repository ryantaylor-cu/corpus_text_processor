import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="corpus_text_processor_cli", # Replace with your own username
    version="1.0.1",
    author="Ryan Taylor",
    author_email="ryan.taylor@carleton.ca",
    description="CLI corpus text processor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ResearchComputingServices/corpus_text_processor",
    packages=setuptools.find_packages(),
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "tabulate==0.8.6",
        "beautifulsoup4==4.8.0",
        "chardet==3.0.4",
        "docx2txt==0.8",
        "pdf2image==1.9.0",
        "pdfminer.six==20181108",
        "PyPDF3==1.0.1",
        "python-pptx==0.6.18",
        "six==1.12.0",
        "striprtf==0.0.8",
    ],
    scripts=['ctp'],
)
