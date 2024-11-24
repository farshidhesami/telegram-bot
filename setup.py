import setuptools

# Read the README file for the package's long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# Define package metadata
setuptools.setup(
    name="telegram_bot",  # Project name
    version="0.1.0",  # Initial version
    author="Farshid Hesami",  # Your name as the author
    author_email="farshidhesami@gmail.com",  # Your email
    description="A Telegram bot for cryptocurrency signals and real-time price updates.",  # Short project description
    long_description=long_description,  # Use README.md as the long description
    long_description_content_type="text/markdown",  # Specify Markdown format for the description
    url="https://github.com/farshidhesami/telegram-bot",  # GitHub repo URL
    project_urls={
        "Bug Tracker": "https://github.com/farshidhesami/telegram-bot/issues",  # Bug tracker URL
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="telegram-bot cryptocurrency signals bot python",
    package_dir={"": "src"},  # Source directory for packages
    packages=setuptools.find_packages(where="src"),  # Automatically find packages in `src`
    python_requires=">=3.6",  # Minimum Python version
    install_requires=[
        "requests",
        "numpy",
        "python-decouple",
        "telebot",
        "python-telegram-bot",
        "pyyaml",
    ],  # Dependencies
)
