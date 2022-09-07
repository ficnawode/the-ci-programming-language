
add_custom_target(static_analysis.flake8
    COMMAND ${Python3_venv_EXECUTABLE} -m flake8 --config=${CMAKE_SOURCE_DIR}/.flake8 ${CMAKE_SOURCE_DIR}/src
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    DEPENDS tooling.install_requirements
    JOB_POOL ${TOOLING_ANALYSIS_POOL}
)

add_custom_target(static_analysis.mypy
    COMMAND ${Python3_venv_EXECUTABLE} -m mypy
        --namespace-packages
        --explicit-package-bases
        --no-incremental
        --strict
        --warn-unused-configs
        --python-executable=${Python3_venv_EXECUTABLE}
        --config-file=${CMAKE_SOURCE_DIR}/.mypy
        --cache-dir=${CMAKE_BINARY_DIR}/.mypy_cache
        ${CMAKE_SOURCE_DIR}/src
    DEPENDS tooling.install_requirements
    JOB_POOL ${TOOLING_ANALYSIS_POOL}
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
)


add_custom_target(tests
    COMMAND ${Python3_venv_EXECUTABLE} -m pytest tests/
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR})

add_custom_target(run
    COMMAND ${Python3_venv_EXECUTABLE} src/main.py
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR})