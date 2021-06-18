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
     |  delete_all_keys_from_scope(self, key=None, action='blank')
     |      Blank or delete any lines with a given key on a scope
     |      Configuration is reduced if using action='shrink'
     |      otherwise block is replaced with blank lines with action='blank' (default)
     |  
     |  delete_block(self, action='blank')
     |      Deletes an entire block of config delimited by scope.
     |      Configuration is reduced if using action='shrink'
     |      otherwise block is replaced with blank lines with action='blank' (default)
     |  
     |  dump(self)
     |      Dump current scope on STDOUT
     |  
     |  get_key(self, key='', nested=False, default='')
     |      Search the given key in the current scope.
     |        - key: the key to search
     |        - nested: False(default) or True
     |          If nested = False the key is not searched in netsted config/end or edit/next blocks
     |        - default: A default key value to return if the key is not found (not seen in the config)
     |        - found: True/False if key is found
     |       Limitation: can't extract a key value that is a list with brackets
     |        Feedback attribut is updated:
     |        - index: if found, the index of the key
     |        - key: the key itself
     |        - value: its value
     |      Returns the key value (or its default if not found)
     |  
     |  get_line(self, index=1)
     |      Returns configuration line at the provided index
     |  
     |  get_nb_vdoms(self)
     |      Returns the number of vdoms
     |  
     |  get_vdom_list(self)
     |      Resturns the vdom list sorted alphabetically with management vdom first
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
     |  parse(self)
     |      Parses the loaded configuration to set information
     |  
     |  register_vdoms(self)
     |      Register all vdoms:
     |        - add them in a list
     |        - store for each of them their startindex and endindex
     |  
     |  scope_config(self, statement='', partial=False)
     |      Search for config statement from current scope.
     |      Upon search success, the scope is updated
     |      Feedback attribut is updated on success
     |      return True if statement is found
     |  
     |  scope_edit(self, statement='', partial=True)
     |      Search for edit statement from current scope.
     |      Upon search success, the scope is updated,
     |      Feedback attribut is updated:
     |        - found: True/False if key is found
     |        - startindex: edit section starting index
     |        - endindex: edit section ending index
     |        - id: the edit <id>
     |      Returns True if statement is found
     |  
     |  scope_init(self)
     |      Reset scope to the full size of the configuration file
     |  
     |  scope_vdom(self, vdom='root')
     |      Set scope corresponding to the given vdom
     |      Vdoms should have been registered before use.
     |  
     |  set_key(self, key='', value='', index_increment=1, nb_spaces=0, nested=False)
     |      Insert of update a configuration key
     |      The key is first searched on the current scope, if found, it is updated (no new line)
     |      If the key is not found, a new configuration statement is applied (increase config by 1 line)
     |      Parameters:
     |        - key: the key to set or udpate
     |        - value: the value to apply for the key
     |        - index_increment: increment of position for the key to add from scope start (if key not found)
     |        - nb_spaces: nb of spaces to add on left indentation befor the 'set'
     |        - nested: True/False : Do we need to search for the key in nested blocks ?
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


