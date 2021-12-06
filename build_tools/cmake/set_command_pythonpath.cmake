include(CMakeParseArguments)

function(set_command_pythonpath)
  cmake_parse_arguments(
    _ARG
    ""
    "COMMAND;RESULT"
    ""
    ${ARGN}
  )

  if(COMPILER_GYM_PYTHONPATH)
    set(${_ARG_RESULT} "\"${CMAKE_COMMAND}\" -E env \"PYTHONPATH=${COMPILER_GYM_PYTHONPATH}\" ${_ARG_COMMAND}" PARENT_SCOPE)
  else()
    set(${_ARG_RESULT} ${_ARG_COMMAND} PARENT_SCOPE)
  endif()

endfunction()
