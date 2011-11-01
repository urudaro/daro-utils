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
        {'from': 'src/scripts/pyze.py', 'to': '.', 'chmod': '0744'},
        {'from': '$xmod/setup.py', 'to': '.', 'chmod': '0744'}
      ]
      }
    ]
}