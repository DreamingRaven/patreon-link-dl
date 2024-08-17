# Patreon Link Downloader

A handy script to help download links from your paid for patreon content, in a fair manner.
This is not particularly advanced, but it is a starting point or solution to simple but large link repositories.

This was created out of the sheer insanity from the mish mash of methods that patreon creators usually use to deliver their content to paid members. I recentley subscribed for 1500 DnD maps, and there was no way I was clicking that many links.

## Getting Started

### Install

On linux with python, and git installed, download this repository, and install it in a virtual environment:

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
pld download --pages https://www.patreon.com/posts/master-master-27816327 --output out/
```
