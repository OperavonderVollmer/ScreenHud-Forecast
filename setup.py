from setuptools import setup, find_packages

setup(
    name="ScreenHUD-Forecast",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "dotenv",
        "setuptools",
        "requests",
        "OperaPowerRelay @ git+https://github.com/OperavonderVollmer/OperaPowerRelay@main"
    ],
    python_requires=">=3.7",
    author="Opera von der Vollmer",
    description="Forecast plugin for Opera's ScreenHUD",
    url="https://github.com/OperavonderVollmer/ScreenHUD-Forecast", 
    license="MIT",
)
