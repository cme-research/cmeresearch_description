cmake_minimum_required(VERSION 3.8)
project(cmeresearch_description)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
find_package(rosidl_default_generators REQUIRED)

if(BUILD_TESTING)
    find_package(ament_lint_auto REQUIRED)
    # the following line skips the linter which checks for copyrights
    # comment the line when a copyright and license is added to all source files
    set(ament_cmake_copyright_FOUND TRUE)
    # the following line skips cpplint (only works in a git repo)
    # comment the line when this package is in a git repo and when
    # a copyright and license is added to all source files
    set(ament_cmake_cpplint_FOUND TRUE)
    ament_lint_auto_find_test_dependencies()
endif()

## Mark other files for installation (e.g. launch and bag files, etc.)
install(FILES
 urdf/ash/ash_properties.urdf.xacro
 urdf/ash/ash.gazebo
 urdf/ash/ash.urdf.xacro

 DESTINATION share/${PROJECT_NAME}/urdf/ash/
)

install(FILES
 urdf/unicomini/unicomini.gazebo
 urdf/unicomini/unicomini.urdf.xacro
 urdf/unicomini/unicomini_properties.urdf.xacro

 DESTINATION share/${PROJECT_NAME}/urdf/unicomini/
)

install(FILES
 urdf/cmexa/cmexa.gazebo
 urdf/cmexa/cmexa.urdf.xacro
 urdf/cmexa/cmexa_properties.urdf.xacro
 urdf/cmexa/cmexa_description.urdf.xacro
 urdf/cmexa/cmexa_mecanum.ros2_control.xacro

 DESTINATION share/${PROJECT_NAME}/urdf/cmexa/
)
install(FILES
        urdf/cmexa/diffbot.urdf.xacro
        urdf/cmexa/diffbot.materials.xacro
        urdf/cmexa/diffbot_description.urdf.xacro
        urdf/cmexa/diffbot.ros2_control.xacro

        DESTINATION share/${PROJECT_NAME}/urdf/cmexa/
)
install(FILES
 urdf/cmexaiii/cmexaiii.gazebo
 urdf/cmexaiii/cmexaiii.urdf.xacro
 urdf/cmexaiii/cmexaiii_properties.urdf.xacro
 urdf/cmexaiii/cmexaiii_description.urdf.xacro
 urdf/cmexaiii/cmexaiii_mecanum.ros2_control.xacro

 DESTINATION share/${PROJECT_NAME}/urdf/cmexaiii/
)


## Mark other files for installation (e.g. launch and bag files, etc.)
install(FILES
 urdf/materials.xacro

 DESTINATION share/${PROJECT_NAME}/urdf/
)

install(FILES
 meshes/ash/ash-base.stl
 meshes/ash/ash-wheel.stl

 DESTINATION share/${PROJECT_NAME}/meshes/ash/
)

install(FILES
 meshes/unicomini/unicomini-base.stl
 meshes/unicomini/unicomini-wheel.stl

 DESTINATION share/${PROJECT_NAME}/meshes/unicomini/
)

install(FILES
 meshes/cmexa/cmexa-base.stl
 meshes/cmexa/cmexa-wheel.stl

 DESTINATION share/${PROJECT_NAME}/meshes/cmexa/
)

install(FILES
 meshes/cmexaiii/cmexaiii-base.stl
 meshes/cmexaiii/cmexaiii-wheel.stl

 DESTINATION share/${PROJECT_NAME}/meshes/cmexaiii/
)

install(FILES
 launch/description.launch
 launch/cmexa_mecanum.launch.py
 launch/cmexa_mecanum_description.launch.py

 DESTINATION share/${PROJECT_NAME}/launch/
)

ament_package()
