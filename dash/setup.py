from setuptools import setup, find_packages

setup(
    name="agentx-dash",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "tweepy",
        "pydantic",
        "python-dotenv",
    ],
) 