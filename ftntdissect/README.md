Help on module ftntdissect:

NAME
    ftntdissect

DESCRIPTION
    Created on Jun 16, 2021
    @author: cgustave

CLASSES
    builtins.object
        Ftntdissect
    
    class Ftntdissect(builtins.object)
     |  Ftntdissect(configfile='', debug=False)
     |  
     |  classdoc
     |  
     |  Methods defined here:
     |  
     |  __init__(self, configfile='', debug=False)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  delete(self, index=None, action='blank')
     |      Deletes a line. Per default, it is replace with a blank line (action='blank')
     |      Use action='shrink' to remove the line and shrink config by 1 line
     |  
     |  delete_all_keys_from_scope(self, key=None, scope=[1, -1], action='blank')
     |      Blank or delete any lines with a given key on the given scope
     |      Configuration is reduced if using action='shrink'
     |      otherwise block is replaced with blank lines with action='blank' (default)
     |  
     |  delete_block(self, scope=[1, -1], action='blank')
     |      Deletes an entire block of config delimited by a scope.
     |      Configuration is reduced if using action='shrink'
     |      otherwise block is replaced with blank lines with action='blank' (default)
     |  
     |  get_line(self, index=1)
     |      Returns configuration line at the provided index
     |  
     |  insert(self, index=None, content='')
     |      Inserts provided content at provided index.
     |      Configuration is expanded by 1 line
     |  
     |  load(self)
     |      Load configuration file
     |      Index starts at 1 instead of 0 so it matches the line number displayed in text editor when editing the config
     |  
     |  max_lines(self)
     |      Returns configuration size (maximum index)
     |  
     |  register_vdoms(self)
     |      Register all vdoms:
     |        - add them in a list
     |        - store for each of them their startindex and endindex
     |  
     |  set_line(self, index=None, content='')
     |      Set provided content at provided index in configuration
     |  
     |  vdom_index(self, vdom='root', type='', action='', value=None)
     |      Set or get a given vdom startindex or endindex
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)

FILE
    /home/cgustave/github/python/packages/ftntdissect/ftntdissect/ftntdissect.py


