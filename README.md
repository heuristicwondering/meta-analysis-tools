# Meta-analysis Tools
Some basic Python-based scripts for making life easier when doing a meta-analysis

:warning: **Code currently undergoing upgrades**

Code originally developed in Python 3.5. Project is in the process of being updated to Python 3.11.5 as well as upgrading package dependencies. Not everything may work as expected during this process.

## Prerequisites, Dependencies, and Version Notes
1. Requires the gecko driver to be installed on system path. Gecko version TK was used in the creation of these scripts.

2. These scripts were developed and tested using Python 3.11.5 running on Ubuntu 20.04.6 LTS.

3. A requirements.txt file has been included for installing needed Python package dependencies. See Getting started section below for how to use this.

## Getting Started
Steps for using these tools will be included after ongoing updates are complete.

If you intend to use this but run into install problems,
please contact the author.

**Section in Progress:**
1. Install the gecko driver following instructions found here (link TK).
2. We also recommend creating a virtual environment with a tool like conda (link TK). At minimum, the environment should have both Python and pip.
3. Once gecko is installed and your virtual environment is active, use the requirements.txt file to install additional Python modules needed. This can be done with the command `pip install -r requirements.txt`
4. See individual README files associated with each tool described below for detailed usage instructions.

## Tools available
### **Generating Search Terms**
A tool that takes a folder of plain text files and generates a simple word frequency count. Useful for guiding creation of targeted search terms when there is a representative sample of manuscripts that is already known to meet inclusion criteria.

### Collecting Results
Description TK.

### Removing Duplicates
Description TK.