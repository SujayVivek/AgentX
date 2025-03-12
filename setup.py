from setuptools import setup, find_packages

setup(
    name="flare-ai-social",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "google-generativeai",
        "tweepy",
        "python-dotenv",
    ],
)