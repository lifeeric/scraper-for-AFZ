https://github.com/lifeeric/scraper-for-AFZ/assets/28618316/d2a4a4f7-c1bc-46a0-93fe-7aa555637d2d

## Getting Started

These instructions will guide you through setting up and running the application.

### Prerequisites

- Python (3.9 or higher)

### Installation

You can install the required libraries using either `pip` or `poetry`.

#### Using Pip

Navigate to your project directory and run the following command to install the required libraries using `pip`:

```sh
pip install selenium webdriver-manager
```

#### Using Poetry

If you're using [Poetry](https://python-poetry.org/), you can navigate to your project directory and run the following commands:

```sh
poetry install
```

### Running the App

Prepare the run by copying the header.csv file to the respective outputfile. Filenames of the output have to be maintained in shell script directly 
```sh
initialize_header.sh
```

To run the `eric-bot.py` script, execute the following command in your terminal:

```sh
python3 eric-bot.py post_codes_Germany/inputfile.json scraped-data/outputfile.csv
```

and it will give you output data in realtime in `outputfile.csv`
