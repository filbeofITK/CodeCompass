include_directories(
  include
  ${PROJECT_SOURCE_DIR}/model/include
  ${PROJECT_SOURCE_DIR}/util/include
  ${PROJECT_SOURCE_DIR}/parser/include
  ${PLUGIN_DIR}/model/include)

add_library(metricsparser SHARED
  src/metricsparser.cpp)

target_link_libraries(metricsparser
  metricsmodel
  util
  ${Boost_LIBRARIES})

install(TARGETS metricsparser
  LIBRARY DESTINATION ${INSTALL_LIB_DIR}
  DESTINATION ${INSTALL_PARSER_DIR})
