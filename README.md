# the-ci-programming-language
## Overview
Programming language with Polish syntax.

## Setup
### Normal:
To launch the shell:

```
python main.py
```

(the project is written in vanilla python, there are no external dependencies)

### Dev (CMake, stesting, static analysis):

Create a build directory for CMake trash

```
mkdir build
```

Configure the CMake project

```
cmake -B build/ -S .
```

Then, to fire up the shell (from the base of the project tree):

```
build/venv/Scripts/python.exe main.py
```

Additionally, in VSCode you can now press `Shift+F7` and run any target (tests, static analysis, etc.)

```
cmake build --target <target-name> build/
```

You can also use the environment to launch the shell

```
build/venv/Scripts/python.exe main.py
```