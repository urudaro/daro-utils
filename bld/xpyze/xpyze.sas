#
# -*- coding: iso-8859-1 -*-
# Description: System assembly file for xpyze
# Authors: Daniel Rodriguez
# Copyright: Copyright (c) 2009, Seibo Software Studios AB
# $Date:  $
# $Revision: $
# $HeadURL:  $
# $LastChangedBy: $

{
   'src_root': '../..',
   'symbols': {'xmod': 'src/modules'},
   'components': [
      {'name': 'xpyze',
      'files': [
        {'from': '$xmod/xpyze.py', 'to': '.'},
        {'from': '$xmod/simplegit.py', 'to': '.'},
        {'from': '$xmod/monitoring.py', 'to': '.'},
        {'from': 'src/scripts/pyze.py', 'to-file': 'pyze', 'chmod': '0744'},
        {'from': 'src/scripts/xpyze.sh', 'to-file': 'xpyze', 'chmod': '0744'},
        {'from': '$xmod/setup.py', 'to': '.', 'chmod': '0744'}
      ]
      }
    ]
}
