"""
Setup configuration for IntelliReport package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="intellireport",
    version="0.1.0",
    author="IntelliReport Team",
    author_email="team@intellireport.com",
    description="Intelligent Report Processing with AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/intellireport",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Text Processing",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "anthropic>=0.7.0",
        "pydantic>=2.0.0",
        "PyYAML>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "demo": [
            "streamlit>=1.28.0",
        ],
        "all": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "streamlit>=1.28.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "intellireport=intellireport.cli:main",
        ],
    },
    keywords="ai report processing nlp claude anthropic analysis",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/intellireport/issues",
        "Source": "https://github.com/yourusername/intellireport",
        "Documentation": "https://intellireport.readthedocs.io/",
    },
)