#
# DevVM provision Data Base.
#
# Author: Dongsheng Mu, 11/7/2013
#

"""
DevVM provision table.
"""


this_db = {
    'cougar-evl02': {'pci-ixgbe' : ('09:10.0', '09:1f.5')},

    '': # the sunnyvale DevVM template
    {   'name'         : 'srxbuild06-DevVM',
        'IP'           : '10.159.16.215',
        'img_file'     : '/home/VMs/cougar-kvm03-centos-dev-dmu.snapshot_kvm03_dmu-clone',
        'xml_file'     : '/etc/libvirt/qemu/srxbuild06-DevVM.xml',
        'hostname'     : 'srxbuild06',
        'server'       : 'cougar-evl02',
        'location'     : 'svl',
        'user'         : 'dmu',
        # the PCI device numbers from "lspci | grep 82599"
        'ixgbevf'      : [('0x09', '0x10', '0x0'),
                          ('0x09', '0x10', '0x2'),
                          ('0x09', '0x10', '0x4'),
                          ('0x09', '0x10', '0x6'),
                          ('0x09', '0x11', '0x0'),
                          ('0x09', '0x11', '0x2'),
                          ('0x09', '0x11', '0x4'),
                          ('0x09', '0x11', '0x6')],
    },

    'srxbuild07-DevVM02':
    {   'name'         : 'srxbuild07-DevVM02',
        'IP'           : '10.159.16.216',
        'img_file'     : '/home/localVMs/srxbuild07-DevVM02',
        'xml_file'     : '/etc/libvirt/qemu/srxbuild07-DevVM02.xml',
        'hostname'     : 'srxbuild07',
        'server'       : 'cougar-evl02',
        'location'     : 'svl',
        'user'         : 'jwag',
        'ixgbevf'      : [('0x09', '0x12', '0x0'),
                          ('0x09', '0x12', '0x2'),
                          ('0x09', '0x12', '0x4'),
                          ('0x09', '0x12', '0x6'),
                          ('0x09', '0x13', '0x0'),
                          ('0x09', '0x13', '0x2'),
                          ('0x09', '0x13', '0x4'),
                          ('0x09', '0x13', '0x6')],
    },

    'srxbuild08-DevVM03':
    {   'name'         : 'srxbuild08-DevVM03',
        'IP'           : '10.159.16.217',
        'img_file'     : '/home/localVMs/srxbuild08-DevVM03',
        'xml_file'     : '/etc/libvirt/qemu/srxbuild08-DevVM03.xml',
        'hostname'     : 'srxbuild08',
        'server'       : 'cougar-evl02',
        'location'     : 'svl',
        'user'         : 'jiama',
        'ixgbevf'      : [('0x09', '0x14', '0x0'),
                          ('0x09', '0x14', '0x2'),
                          ('0x09', '0x14', '0x4'),
                          ('0x09', '0x14', '0x6'),
                          ('0x09', '0x15', '0x0'),
                          ('0x09', '0x15', '0x2'),
                          ('0x09', '0x15', '0x4'),
                          ('0x09', '0x15', '0x6')],
    },

    'srxbuild05-DevVM04':
    {   'name'         : 'srxbuild05-DevVM04',
        'IP'           : '10.159.16.214',
        'img_file'     : '/home/localVMs/srxbuild05-DevVM04',
        'xml_file'     : '/etc/libvirt/qemu/srxbuild05-DevVM04.xml',
        'hostname'     : 'srxbuild05',
        'server'       : 'cougar-evl02',
        'location'     : 'svl',
        'user'         : '',
        'ixgbevf'      : [('0x09', '0x16', '0x0'),
                          ('0x09', '0x16', '0x2'),
                          ('0x09', '0x16', '0x4'),
                          ('0x09', '0x16', '0x6'),
                          ('0x09', '0x17', '0x0'),
                          ('0x09', '0x17', '0x2'),
                          ('0x09', '0x17', '0x4'),
                          ('0x09', '0x17', '0x6')],
    },

    'cougar-lnx'  : {'pci-ixgbe' : ('07:10.0', '07:1f.5')},

    'cougar-kvm02-DevVM05':
    {   'name'         : 'cougar-kvm02-DevVM05',
        'IP'           : '10.159.16.222',
        'img_file'     : '/home/localVMs/cougar-kvm02-DevVM05',
        'xml_file'     : '/etc/libvirt/qemu/cougar-kvm02-DevVM05.xml',
        'hostname'     : 'cougar-kvm02',
        'server'       : 'cougar-lnx',
        'location'     : 'svl',
        'user'         : 'dmu',
        'ixgbevf'      : [('0x07', '0x10', '0x0'),
                          ('0x07', '0x10', '0x2'),
                          ('0x07', '0x10', '0x4'),
                          ('0x07', '0x10', '0x6'),
                          ('0x07', '0x11', '0x0'),
                          ('0x07', '0x11', '0x2'),
                          ('0x07', '0x11', '0x4'),
                          ('0x07', '0x11', '0x6')],
    },

    'cougar-kvm03-DevVM06':
    {   'name'         : 'cougar-kvm03-DevVM06',
        'IP'           : '10.159.16.223',
        'img_file'     : '/home/localVMs/cougar-kvm03-DevVM06',
        'xml_file'     : '/etc/libvirt/qemu/cougar-kvm03-DevVM06.xml',
        'hostname'     : 'cougar-kvm03',
        'server'       : 'cougar-lnx',
        'location'     : 'svl',
        'user'         : 'dmu',
        'ixgbevf'      : [('0x07', '0x12', '0x0'),
                          ('0x07', '0x12', '0x2'),
                          ('0x07', '0x12', '0x4'),
                          ('0x07', '0x12', '0x6'),
                          ('0x07', '0x13', '0x0'),
                          ('0x07', '0x13', '0x2'),
                          ('0x07', '0x13', '0x4'),
                          ('0x07', '0x13', '0x6')],
    },

    '?-DevVM07':
    {   'name'         : 'srxbuild08-DevVM03',
        'IP'           : '10.159.16.?',
        'img_file'     : '/home/localVMs/srxbuild08-DevVM03',
        'xml_file'     : '/etc/libvirt/qemu/srxbuild08-DevVM03.xml',
        'hostname'     : 'srxbuild08',
        'server'       : 'cougar-lnx',
        'location'     : 'svl',
        'user'         : 'dmu',
        'ixgbevf'      : [('0x07', '0x14', '0x0'),
                          ('0x07', '0x14', '0x2'),
                          ('0x07', '0x14', '0x4'),
                          ('0x07', '0x14', '0x6'),
                          ('0x07', '0x15', '0x0'),
                          ('0x07', '0x15', '0x2'),
                          ('0x07', '0x15', '0x4'),
                          ('0x07', '0x15', '0x6')],
    },

    '?-DevVM08':
    {   'name'         : '?-DevVM08',
        'IP'           : '10.159.16.?',
        'img_file'     : '/home/localVMs/srxbuild05-DevVM04',
        'xml_file'     : '/etc/libvirt/qemu/srxbuild05-DevVM04.xml',
        'hostname'     : 'srxbuild05',
        'server'       : 'cougar-lnx',
        'location'     : 'svl',
        'user'         : 'dmu',
        'ixgbevf'      : [('0x07', '0x16', '0x0'),
                          ('0x07', '0x16', '0x2'),
                          ('0x07', '0x16', '0x4'),
                          ('0x07', '0x16', '0x6'),
                          ('0x07', '0x17', '0x0'),
                          ('0x07', '0x17', '0x2'),
                          ('0x07', '0x17', '0x4'),
                          ('0x07', '0x17', '0x6')],
    },
}


## test
if __name__ == '__main__':
    import rlcompleter, readline
    readline.parse_and_bind('tab: complete')
