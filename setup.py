from setuptools import setup, find_packages

setup(
    name="fastapi_gists_app",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "requests",
        "pytest",
        "httpx"
    ],
)
