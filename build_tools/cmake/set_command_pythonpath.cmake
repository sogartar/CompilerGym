include(CMakeParseArguments)

function(set_command_pythonpath)
  cmake_parse_arguments(
    _ARG
    ""
    "COMMAND;RESULT_VAR"
    ""
    ${ARGN}
  )

  if(CMAKE_PYTHONPATH)
    set(${_ARG_RESULT_VAR} "\"${CMAKE_COMMAND}\" -E env \"PYTHONPATH=${CMAKE_PYTHONPATH}\" ${_ARG_COMMAND}" PARENT_SCOPE)
  else()
    set(${_ARG_RESULT_VAR} ${_ARG_COMMAND} PARENT_SCOPE)
  endif()

endfunction()
