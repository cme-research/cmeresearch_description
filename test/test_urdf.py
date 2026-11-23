"""Every robot model must expand with xacro into a consistent URDF.

xacro resolves $(find cmeresearch_description) through the ament index, so these
tests run against the *installed* package and also catch missing install rules.
"""

import pathlib
import xml.etree.ElementTree as ET

import pytest
import xacro
from ament_index_python.packages import get_package_share_directory

PKG = 'cmeresearch_description'
SHARE = pathlib.Path(get_package_share_directory(PKG))

# Top-level robot models (the files launch files hand to xacro).
ROBOTS = {
    'cmexa': 'urdf/cmexa/robot.urdf.xacro',
    'cmexaiii': 'urdf/cmexaiii/robot.urdf.xacro',
    'cmexamini': 'urdf/cmexamini/robot.urdf.xacro',
    'diffbot': 'urdf/diffbot/diffbot.urdf.xacro',
}

# Hardware parameters CmexaBaseBotSystemHardware::on_init() refuses to start without.
CMEXA_BASE_PLUGIN = 'cmexa_base/CmexaBaseBotSystemHardware'
CMEXA_BASE_REQUIRED = {
    'example_param_hw_start_duration_sec', 'example_param_hw_stop_duration_sec',
    'gear_ratio', 'wheel_radius', 'wheel_separation_x', 'wheel_separation_y',
    'steps_per_revolution',
}
CMEXA_BASE_OPTIONAL_NUMERIC = {'step_resolution', 'max_step_vel'}
CMEXA_BASE_JOINTS = {'front_left_wheel_joint', 'front_right_wheel_joint',
                     'rear_left_wheel_joint', 'rear_right_wheel_joint'}

# Real hardware configurations that cmexa_base would currently reject.
KNOWN_BROKEN_HARDWARE = {
    'cmexamini': 'passes only 3 of the 7 hardware parameters cmexa_base requires',
    'diffbot': 'demo model: passes only 3 of the 7 hardware parameters cmexa_base requires',
}


def expand(robot, use_mock_hardware):
    path = SHARE / ROBOTS[robot]
    doc = xacro.process_file(
        str(path), mappings={'use_mock_hardware': str(use_mock_hardware).lower()})
    return ET.fromstring(doc.toxml())


CASES = [(r, m) for r in sorted(ROBOTS) for m in (True, False)]


def case_id(case):
    robot, mock = case
    return f'{robot}-{"mock" if mock else "hardware"}'


@pytest.fixture(scope='module', params=CASES, ids=case_id)
def urdf(request):
    robot, mock = request.param
    return robot, mock, expand(robot, mock)


def test_installed_models_exist():
    for robot, rel in ROBOTS.items():
        assert (SHARE / rel).is_file(), f'{robot}: {rel} is not installed'


def test_link_and_joint_tree(urdf):
    robot, _, root = urdf
    assert root.tag == 'robot'
    links = [link.get('name') for link in root.findall('link')]
    joints = root.findall('joint')
    assert links, f'{robot}: no links'
    assert len(links) == len(set(links)), f'{robot}: duplicate link names'
    names = [j.get('name') for j in joints]
    assert len(names) == len(set(names)), f'{robot}: duplicate joint names'
    children = set()
    for j in joints:
        parent = j.find('parent').get('link')
        child = j.find('child').get('link')
        assert parent in links, f'{robot}: joint {j.get("name")} parent {parent} missing'
        assert child in links, f'{robot}: joint {j.get("name")} child {child} missing'
        assert child not in children, f'{robot}: link {child} has two parents'
        children.add(child)
    roots = set(links) - children
    assert len(roots) == 1, f'{robot}: expected exactly one root link, got {sorted(roots)}'


def test_meshes_resolve(urdf):
    robot, _, root = urdf
    for mesh in root.iter('mesh'):
        uri = mesh.get('filename')
        if uri.startswith('package://'):
            pkg, _, rest = uri[len('package://'):].partition('/')
            base = pathlib.Path(get_package_share_directory(pkg))
            assert (base / rest).is_file(), f'{robot}: mesh {uri} not installed'
        elif uri.startswith('file://'):
            assert pathlib.Path(uri[len('file://'):]).is_file(), f'{robot}: {uri} missing'


def test_wheel_geometry_is_positive(urdf):
    robot, _, root = urdf
    for cyl in root.iter('cylinder'):
        assert float(cyl.get('radius')) > 0 and float(cyl.get('length')) > 0, robot
    for link in root.findall('link'):
        mass = link.find('inertial/mass')
        if mass is not None:
            assert float(mass.get('value')) > 0, f'{robot}: link {link.get("name")} mass'


def test_ros2_control_block(urdf):
    robot, mock, root = urdf
    blocks = root.findall('ros2_control')
    assert len(blocks) == 1, f'{robot}: expected one ros2_control block'
    block = blocks[0]
    urdf_joints = {j.get('name') for j in root.findall('joint')}
    plugin = block.find('hardware/plugin').text.strip()
    if mock:
        assert plugin == 'mock_components/GenericSystem'
    else:
        assert plugin == CMEXA_BASE_PLUGIN
    for joint in block.findall('joint'):
        name = joint.get('name')
        assert name in urdf_joints, f'{robot}: ros2_control joint {name} not in URDF'
        assert [c.get('name') for c in joint.findall('command_interface')] == ['velocity']
        assert [s.get('name') for s in joint.findall('state_interface')] == [
            'position', 'velocity'], f'{robot}: {name} state interfaces'


def cmexa_base_case(robot):
    marks = []
    if robot in KNOWN_BROKEN_HARDWARE:
        marks = [pytest.mark.xfail(strict=True, reason=KNOWN_BROKEN_HARDWARE[robot])]
    return pytest.param(robot, id=robot, marks=marks)


@pytest.mark.parametrize('robot', [cmexa_base_case(r) for r in sorted(ROBOTS)])
def test_cmexa_base_hardware_parameters(robot):
    """The real-hardware model must give cmexa_base everything on_init() needs."""
    block = expand(robot, False).find('ros2_control')
    params = {p.get('name'): p.text.strip() for p in block.findall('hardware/param')}
    missing = CMEXA_BASE_REQUIRED - set(params)
    assert not missing, f'{robot}: missing cmexa_base parameters {sorted(missing)}'
    for key in CMEXA_BASE_REQUIRED | (CMEXA_BASE_OPTIONAL_NUMERIC & set(params)):
        value = float(params[key])
        if not key.startswith('example_param'):
            assert value > 0, f'{robot}: {key} = {value}'
    if 'step_resolution' in params:
        assert int(float(params['step_resolution'])) in [2 ** i for i in range(9)]
    joints = {j.get('name') for j in block.findall('joint')}
    assert CMEXA_BASE_JOINTS <= joints, f'{robot}: cmexa_base needs {sorted(CMEXA_BASE_JOINTS)}'
