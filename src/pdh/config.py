'''Configure Folder Paths'''
import configparser
import os


__path_pdh__ = os.path.realpath(os.path.join(__file__, '..', '..', '..'))
__path_config__ = os.path.join(__path_pdh__, 'pdh.cfg')

config = configparser.RawConfigParser()
config.read(__path_config__)


__path_user__ = os.path.join(__path_pdh__, config.get('PDH', 'path_user'))

if os.path.isdir(__path_user__):
    print('USER Path: ' + __path_user__)
else:
    print('**Missing** USER Path: ' + __path_user__)

__path_system__ = os.path.join(__path_pdh__, config.get('PDH', 'path_system'))
if os.path.isdir(__path_system__):
    print('SYSTEM Path: ' + __path_system__)
else:
    print('**Missing** SYSTEM Path: ' + __path_system__)

__path_data__ = os.path.join(__path_pdh__, config.get('PDH', 'path_data'))
if os.path.isdir(__path_data__):
    print('DATA Path: ' + __path_data__)
else:
    print('**Missing** USER Path: ' + __path_data__)
