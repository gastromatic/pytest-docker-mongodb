import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytest-docker-mongodb",
    version="0.0.1",
    author="Gastromatic",
    author_email="s.singh@gastromatic.de",
    description="Pytest fixtures for mongodb in docker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gastromatic/pytest-docker-mongodb",
    packages=setuptools.find_packages(),
    package_data={"pytest_docker_mongodb": ["*.yml"]},
    python_requires=">=3.5",
    # These may be too strict, feel free to make a PR and change them
    install_requires=[
        "pytest>=5.0",
        "lovely-pytest-docker>=0.0.5",
        "motor>=2.0.0"
    ],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
    ],
    keywords="mongodb pytest docker database",
    entry_points={"pytest11": ["docker_mongodb = pytest_docker_mongodb"]},
)
