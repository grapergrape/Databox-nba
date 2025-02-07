# NBA & GitHub Stats to Databox

This project fetches NBA player statistics and GitHub commit data, then pushes this information to a Databox dashboard for visual display.

## Features

- **NBA API Fetcher**: Retrieves basic statistics for Luka Dončić from a public NBA API.
- **GitHub Commit Fetcher**: Gathers daily commit data for this specific project using GitHub's API key authorization. If OAuth is used, details are provided in the documentation.
- **Databox Integration**: Displays the fetched NBA stats and commit data on a Databox dashboard. Access it [here](https://app.databox.com/datawall/4bbfb0483949287855f6bd65405742713c71a8467a251d1). Databox user was created through Google signup: gasper.skornik@gmail.com

## Setup & Usage

1. **Environment Configuration**:
   - Rename `.envtemplate` to `.env`.
   - Replace dummy Databox and GitHub API tokens with actual values.

2. **Build & Run**:
   - Use Docker Compose to orchestrate the environment.
   - Build and run the project:
     ```bash
     docker-compose up --build
     ```

3. **Testing & Coverage**:
   - To run coverage tests, modify the `Dockerfile`:
     - Comment out: `CMD ["python3", "main.py"]`
     - Uncomment: `CMD ["sh", "-c", "coverage run test_runner.py && coverage report -m && coverage html -d /databox-service/coverage_report"]`
   - This generates a coverage report in the `coverage_report` directory, if the command fails: create empty directroy called coverage_report in projects root dir.

## Docker Setup

- **Environment**: Defined through a `Dockerfile` and orchestrated with `docker-compose`.
- **Dependencies**: The Databox Python library, required but not available via pip, is fetched through Git.

## Coverage Report

```
databox_connector.py        40      4    90%   139-140, 181-182
databox_tests.py            45      1    98%   82
github_helper.py            44      6    86%   51-52, 97-100
github_helper_tests.py      34      1    97%   59
nba_helper.py               38      2    95%   43-44
nba_helper_tests.py         41      1    98%   65
test_runner.py               6      0   100%
----------------------------------------------
```

## License
No license is included with this repository.
