
find_package(Python3 COMPONENTS Interpreter)

set(USER_MANAGED_VENV ON)

if(NOT PY_VENV_DIR)
    set(USER_MANAGED_VENV OFF)
    set(PY_VENV_DIR ${CMAKE_BINARY_DIR}/venv)
endif()

if (NOT EXISTS ${PY_VENV_DIR})
    execute_process(COMMAND ${Python3_EXECUTABLE} -m pip -q install virtualenv)
    execute_process(COMMAND ${Python3_EXECUTABLE} -m virtualenv ${PY_VENV_DIR})
endif()

find_program(Python3_venv_EXECUTABLE
        NAMES python
        PATHS ${PY_VENV_DIR}
        PATH_SUFFIXES bin Scripts
        NO_DEFAULT_PATH
)

execute_process(COMMAND ${Python3_venv_EXECUTABLE} -m pip install -r requirements-dev.txt
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR})

