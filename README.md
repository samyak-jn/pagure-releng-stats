# Pagure Releng Stats

A Python script to fetch, analyze, and visualize issue statistics from the Pagure Releng repository.

## Features

- Fetch open and closed issues from Pagure's API.
- Weekly report of opened vs. closed issues.
- Tag analysis to categorize issues.
- Story points estimation based on issue tags.
- Assign unassigned tickets to `Samyak (releng user)`.
- Data visualization with graphs for better insights.

## Setup

### Prerequisites

Ensure you have Python 3.9+ and Poetry installed:

```
curl -sSL https://install.python-poetry.org | python3 -
```

### Installation

1. Clone the repository:

   ```
   git clone https://github.com/samyak-jn/pagure-releng-stats.git
   cd pagure-releng-stats
   ```

2. Install dependencies using Poetry:

   ```
   poetry install
   ```

3. Activate the virtual environment:

   ```
   poetry shell
   ```

## Usage

Run the script using Poetry:

```
poetry run fetch-stats
```

## Project Structure

```
 pagure-releng-stats/
 ├── src/
 │   ├── main.py  # Main script for fetching and processing issues
 ├── pyproject.toml  # Poetry dependency and project configuration
 ├── README.md  # Project documentation
 ├── .gitignore  # Git ignore rules
```

## Contribution

Contributions are welcome! Please open an issue or a pull request.

## License

This project is licensed under the MIT License.

---

