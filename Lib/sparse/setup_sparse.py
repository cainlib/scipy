#!/usr/bin/env python

import os, sys
from glob import glob
from scipy_distutils.core import Extension
from scipy_distutils.misc_util import get_path, default_config_dict, dot_join
from scipy_distutils.system_info import get_info,dict_append
import shutil

def configuration(parent_package=''):
    package = 'sparse'
    config = default_config_dict(package,parent_package)
    local_path = get_path(__name__)

    atlas_info = get_info('atlas')

    superlu = glob(os.path.join(local_path,'SuperLU2.0','SRC','*.c'))
    superlu.append(os.path.join(local_path,'_superlu_utils.c'))
    myblas = glob(os.path.join(local_path,'SuperLU2.0','CBLAS','*.c'))
    sparsekit = glob(os.path.join(local_path,'sparsekit','*.f'))
    #mach = glob(os.path.join(local_path,'mach','*.f'))

    head = [os.path.join(sys.prefix,'include','python%d.%d' %sys.version_info[:2])]

    #SuperLU2.0/SRC/util.h  has been modifed to use these by default
    #macs = [('USER_ABORT','superlu_python_module_abort'),
    #        ('USER_MALLOC','superlu_python_module_malloc'),
    #        ('USER_FREE','superlu_python_module_free')]
    
    # C libraries
    config['libraries'].append(('superlu',{'sources':superlu,
                                           'include_dirs':head}))
    config['libraries'].append(('myblas',{'sources':myblas}))
    
    # Fortran libraries
    config['fortran_libraries'].append(('sparsekit',{'sources':sparsekit}))
    
    # Extension
    sources = ['_zsuperlumodule.c']
    ext_args = {'name':dot_join(parent_package,package,'_zsuperlu'),
                'sources':[os.path.join(local_path,x) for x in sources],
                'libraries': ['superlu','myblas']
                }
    dict_append(ext_args,**atlas_info)
    ext = Extension(**ext_args)
    config['ext_modules'].append(ext)

    sources = ['_dsuperlumodule.c']
    ext_args = {'name':dot_join(parent_package,package,'_dsuperlu'),
                'sources':[os.path.join(local_path,x) for x in sources],
                'libraries': ['superlu','myblas']
                }
    dict_append(ext_args,**atlas_info)
    ext = Extension(**ext_args)
    config['ext_modules'].append(ext)

    sources = ['_csuperlumodule.c']
    ext_args = {'name':dot_join(parent_package,package,'_csuperlu'),
                'sources':[os.path.join(local_path,x) for x in sources],
                'libraries': ['superlu','myblas']
                }
    dict_append(ext_args,**atlas_info)
    ext = Extension(**ext_args)
    config['ext_modules'].append(ext)

    sources = ['_ssuperlumodule.c']
    ext_args = {'name':dot_join(parent_package,package,'_ssuperlu'),
                'sources':[os.path.join(local_path,x) for x in sources],
                'libraries': ['superlu','myblas']
                }
    dict_append(ext_args,**atlas_info)
    ext = Extension(**ext_args)
    config['ext_modules'].append(ext)

    ext_args = {'name':dot_join(parent_package,package,'_sparsekit'),
                'sources':[os.path.join(local_path,'_sparsekit.pyf')],
                #'f2py_options':['--no-wrap-functions'],
                #'define_macros':[('F2PY_REPORT_ATEXIT_DISABLE',None)],
                'libraries' : ['sparsekit']
                }
    dict_append(ext_args,**atlas_info)
    ext = Extension(**ext_args)
    ext.need_fcompiler_opts = 1
    config['ext_modules'].append(ext)

    return config

if __name__ == '__main__':
    from scipy_distutils.core import setup
    setup(**configuration())
