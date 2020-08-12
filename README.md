[![Build Status](https://travis-ci.com/nl2go/ansible-role-hetzner_installimage.svg?branch=master)](https://travis-ci.com/nl2go/ansible-role-hetzner_installimage)
[![Codecov](https://img.shields.io/codecov/c/github/nl2go/ansible-role-hetzner_installimage)](https://codecov.io/gh/nl2go/ansible-role-hetzner_installimage)
[![Ansible Galaxy](https://img.shields.io/badge/role-nl2go.hetzner_installimage-blue.svg)](https://galaxy.ansible.com/nl2go/hetzner_installimage/)
[![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/nl2go/ansible-role-hetzner_installimage)](https://galaxy.ansible.com/nl2go/hetzner_installimage)
[![Ansible Galaxy Downloads](https://img.shields.io/ansible/role/d/44642.svg?color=blue)](https://galaxy.ansible.com/nl2go/hetzner_installimage/)

# Ansible Role: Hetzner Installimage

An Ansible Role that manages the OS image installation lifecycle of [Hetzner servers](https://robot.your-server.de/server) using [Hetzner Robot API](https://robot.your-server.de/doc/webservice/en.html#preface).

## Prerequisites

- Existing [Hetzner Online GmbH Account](https://accounts.hetzner.com).
- Configured [Hetzner Robot Webservice Account](https://robot.your-server.de/preferences).
- Present SSH public key within [Hetzner Robot Key Management](https://robot.your-server.de/key/index).

## Requirements

| Name | Type | Version | Location |
|---|---|---|---|
| [ansible-filter](https://github.com/nl2go/ansible-filter) | Python package | 1.0.1 | Control node |

## Config Variables

The following variables are suggested to be set within your ansible.cfg file

    [defaults]
    inventory = __YOUR_INVENTORY__
    forks = 1
    host_key_checking = false
    private_key_file = __YOUR_HETZNER_PROVISIONING_KEY__
    remote_user = root
    roles_path = __PATH_TO_YOUR_GALAXY_ROLES__
    [ssh_connection]
    pipelining = True
    scp_if_ssh = True
    control_path = %(directory)s/%%h-%%r

## Role Variables

The default set of variables defines the installimage and needs at best to be overwritten in group_vars/host_vars

    hetzner_installimage_install_bootloader: grub
    hetzner_installimage_install_hostname: your-server-name-here
    hetzner_installimage_install_partitions:
    - PART swap swap 32G
    - PART /boot ext4 1G
    - PART / ext4 all
    hetzner_installimage_install_image: Ubuntu-1604-xenial-64-minimal.tar.gz

The role includes an autodetection of RAID values and setup. It will configure no RAID if one disk is found and
RAID1 if 2 disks are found. The automatic RAID config can be overwritten with the following variables:

    hetzner_installimage_install_drives:
    - DRIVE1 /dev/sda
    - DRIVE2 /dev/sdb
    hetzner_installimage_install_raid:
    - SWRAID 1
    - SWRAIDLEVEL 0

It is also possible to just set `hetzner_installimage_install_raid` and let the autodetection find the respective disks.

The following mandatory variables need to be set in group_vars/host_vars or as extra vars to allow communication with 
the webservice and deployment of the public key:

    hetzner_installimage_webservice_username: username
    hetzner_installimage_webservice_password: password

The following variable can be set optionally, to set the hostname within the hetzner robot

    hetzner_installimage_server_name: __YOUR_SERVER_NAME__

If `hetzner_installimage_key_fingerprints`is set, only the selected keys will be installed during the image installation
process from the [Hetzner Robot Key Management](https://robot.your-server.de/key/index). Otherwise all existing
keys will be provisioned.

    hetzner_installimage_key_fingerprints:
        - 00:11:22:33:44:55:66:77:88:99:aa:bb:cc:dd:ee:ff

When executing the playbook successfully the role creates a flag file on the respective server under 
`/etc/hetzner_installimage_provisioned.flag`. In the beginning of the role it checks if that file exists on the host and skips the further
tasks. This behaviour can be avoided by using the variable `hetzner_installimage_ignore_provisioned_flag`:

    --extra-vars "{ hetzner_installimage_ignore_provisioned_flag: yes }"
    
Setting this variable to `true` will skip checking the flag file.

## Example Playbook

    - hosts: hetzner
      gather_facts: no
      roles:
         - nl2go.hetzner_installimage
      vars:
        hetzner_installimage_webservice_username: "{{ hetzner_robot_api_user}}"
        hetzner_installimage_webservice_password: "{{ hetzner_robot_api_pass}}"
        hetzner_installimage_server_name: "{{ inventory_hostname }}"

**Important note:** The role must be executed with `gather_facts: no` as the hosts where you want to install a new 
operating system usually have no ssh access configured and `gather_facts` will directly try to access the host. 

See more examples in the playbooks of the different test scenarios inside the test folder.

The role will ask for a confirmation from the user to wipe all data for all hosts in the play. This can be overwritten
by using the variable `hetzner_installimage_skip_confirmation` set to `yes`.

An example for the extra vars would look like this:

    --extra-vars "{ hetzner_installimage_skip_confirmation : yes }"
 
## Installation Steps

  * Install a new machine
    1. Enter your hetzner robot (robot.your-server.de)
    2. Order a new server
    3. Select your operating system
    4. Select your provisioning key
    5. Run the hetzner_installimage role
  * Install an existing machine
    1. Add your provisioning key to hetzner robot via robot.your-server.de
    2. Run the hetzner_installimage role
  * Install an already provisioned machine
    1. Enter the machine
    2. Delete /etc/hetzner_installimage_provisioned.flag or set 
    3. Run the hetzner_installimage role

If you are sure, you will not accidentally purge a running machine which is already in use, you can directly run the 
role with the extra variable `hetzner_installimage_ignore_provisioned_flag`:

    --extra-vars "{ hetzner_installimage_ignore_provisioned_flag: yes }"

This way the role will not check the machine for an existing `/etc/hetzner_installimage_provisioned.flag` file but will also not prevent the machine from 
being purged accidentally!

## Available images

The OS images are located in the folder `/root/.oldroot/nfs/images/` inside the rescue system. The
following images are available at 25 Mar 2020:

* Archlinux-2017-64-minimal.tar.gz
* archlinux-latest-64-minimal.tar.gz
* CentOS-76-64-minimal.tar.gz
* CentOS-77-64-minimal.tar.gz
* CentOS-80-64-minimal.tar.gz
* CentOS-81-64-minimal.tar.gz
* CoreOS-1298-64-production.bin.bz2
* Debian-103-buster-64-LAMP.tar.gz
* Debian-103-buster-64-minimal.tar.gz
* Debian-811-jessie-64-minimal.tar.gz
* Debian-911-stretch-64-minimal.tar.gz
* Debian-912-stretch-64-minimal.tar.gz
* Ubuntu-1604-xenial-64-minimal-no-hwe.tar.gz
* Ubuntu-1604-xenial-64-minimal.tar.gz
* Ubuntu-1804-bionic-64-minimal.tar.gz
* Ubuntu-1804-bionic-64-nextcloud.tar.gz
* Ubuntu-1910-eoan-64-minimal.tar.gz

Older images are located in the `/root/.oldroot/nfs/images.old/` inside the rescue system. The role
will check if an image exists in the folder with the current images first and afterwards check if
an image exists in the folder with the older images and use it from the place where it was found first.
This way it is possible to keep the operating system consistent amongst hosts even if the latest image
of an operating system is updated at some point.

If none of these images work for you it is possible to use a custom image by leveraging
the `hetzner_installimage_custom_image_url` variable. The image will be downloaded from
the given url and used during the installation process.

## Maintainers

- [dirkaholic](https://github.com/dirkaholic)
- [build-failure](https://github.com/build-failure)

## License

See the [LICENSE.md](LICENSE.md) file for details

## Author Information

This role was initially created by/forked from [andrelohmann](https://github.com/andrelohmann).
