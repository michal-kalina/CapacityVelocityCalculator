# Capacity Velocity Calculator
This application use python 3 to calculate Sprint Capacity and Velocity per sprint

# Setup
* Environment setup
    - Python 3.9.*
    - VS Code with:
        - Python extension by Microsoft
        - Material Icon Theme by Philip Kief
        - GitLens by Eric Amodio
        - Python Test Explorer by Little Fox Team


# Run
From root directory run this command. It will setup whole project and run main.py script
## MacOs
From root directory run command in terminal
```bash
. build/buildTrigger.sh
```
# Testing
We are using [PyTest](https://docs.pytest.org/) framework for testing

# Test coverage
We are using [coverage](https://coverage.readthedocs.io/en/coverage-5.5/install.html) framework to analyze code coverage.
Just run
```bash
coverage run -m pytest
```
And to get report run
```bash
coverage report
```

# Linting
While you are in venv active mode
```bash
black .
```

# Other
* This doc will use [GitHub formatting](https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

# Useful links
* [How to use bash](https://linuxhint.com/30_bash_script_examples/#t1).
* [A word about python virtual environment](https://www.recurse.com/blog/14-there-is-no-magic-virtualenv-edition)
## Python
* [Forward references](https://www.python.org/dev/peps/pep-0484/#forward-references)
## PyTest
* [Python testing frameworks](https://www.softwaretestinghelp.com/python-testing-frameworks/)
* [PYTHONPATH](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH)
* [How to Use Fixtures as Arguments in pytest.mark.parametrize](https://miguendes.me/how-to-use-fixtures-as-arguments-in-pytestmarkparametrize)
* [How to pass argument to a fixture](https://stackoverflow.com/a/44701916)

## Black
* [Black github repository](https://github.com/psf/black)
* [Setup black in VS Code](https://marcobelo.medium.com/setting-up-python-black-on-visual-studio-code-5318eba4cd00)
* [Setup black in VS Code 2](https://py-vscode.readthedocs.io/en/latest/files/linting.html)
* [Auto format on save](https://stackoverflow.com/questions/50606758/vscode-how-do-you-autoformat-on-save)

# Useful stuff
* [How to clear screen in terminal](https://stackoverflow.com/a/5367075)
```
alias cls='printf "\033c"'
```
Then run `cls` in terminal