# Patreon Link Downloader

A handy script to help download links from your paid for patreon content, in a fair manner.
This is not particularly advanced, but it is a starting point or solution to simple but large link repositories.

## Getting Started

### Install

On linux with python, firefox, and git installed, download this repository, and install it in a virtual environment:

```bash
git clone https://github.com/DreamingRaven/patreon-link-dl.git
cd patreon-link-dl
python -m venv venv
source venv/bin/activate # or venv/bin/activate.fish or venv/Scripts/activate.zsh
python -m ensurepip
pip install -e .
```

### Usage

With the environment already sourced, download all links from a page into the output directory.

```bash
pld login # you will have a set amount of time to login then it will save your cookies
pld download --pages https://www.patreon.com/posts/27816327 --output out/
pld logout # will delete the cookies from your chosen cookies file
```

This will by default:

- Open a special firefox session for you to login, after a set time period will close the page and save your cookies.

Then the download command will:

- Open a special firefox environment.
- Navigate to the page you have chosen.
- Find all links displayed in the html page chosen.
- Filter the links to only those that match the include and dont match the exclude regex (default "https://.*patreon.com/file.*" for include, and "$^" for exclude).
- One-by-one download each link to the output directory (default "out/"), and checks completion by checking if there are any .part files from partial downloads, and that atleast one file is in the output directory exists.
- Close the special firefox environment.

You can change the regex to match links that you want to include or exclude, or add more pages to download, along with change the output directory. For a more exhaustive list of options:

```bash
pld --help
```
