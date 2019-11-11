import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_autosetupfile_exists(host):
    f = host.file('/autosetup')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'

    assert f.contains('SWRAID 0')
    assert f.contains('DRIVE1')
    assert not f.contains('DRIVE2')
