# Description

A parallel command-line text corpus text processor.  Forked from and
retains the same functionality as writecrow's graphical Corpus Text
Processor.

Much of the code retained in the source was taken or derived from the
writecrow repository on github.

A command-line version called 'ctp' exists that replaces the
functionality of the original "Corpus Text Processor" GUI program.

The ctp command-line tool has the ability to process files in parallel
to speed things up.

# Installation

```bash
python setup.py install --user

# After install, you should be able to run the command ctp.  If not,
# then perhaps your PATH needs to be adjusted to use python packages
# in your environment.

ctp --help
```

Tested on Ubuntu 18.04 and above.

(TODO: test on Mac OS X using python3 installed via homebrew).
