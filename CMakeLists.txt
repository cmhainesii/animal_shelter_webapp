cmake_minimum_required(VERSION 3.0.0)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_FLAGS "--std=c++20")
cmake_policy(SET CMP0135  NEW)
project(KSP_Station_Manager VERSION 0.1.0)

include(CTest)

include(FetchContent)

FetchContent_Declare(json URL https://github.com/nlohmann/json/releases/download/v3.11.2/json.tar.xz)
FetchContent_MakeAvailable(json)



FetchContent_Declare(fmt
    GIT_REPOSITORY https://github.com/fmtlib/fmt.git
    GIT_TAG master
)
FetchContent_MakeAvailable(fmt)

enable_testing()
FILE(GLOB CppSources *.cpp)

add_executable(KSP_Station_Manager ${CppSources})
target_link_libraries(KSP_Station_Manager
    PRIVATE
        fmt::fmt
        nlohmann_json::nlohmann_json
)


set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})

include(CPack)
