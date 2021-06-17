"""
Created on Jun 16, 2021
@author: cgustave
"""
import logging as log
import os
import re


class Ftntdissect(object):
    """
    classdoc
    """
    def __init__(self, configfile='', debug=False):
        log.basicConfig(
           format='%(asctime)s,%(msecs)3.3d %(levelname)-8s[%(module)-7.7s.%(funcName)-30.30s:%(lineno)5d] %(message)s',
           datefmt='%Y%m%d:%H:%M:%S',
           filename='debug.log',
           level=log.NOTSET)
        if debug:
            self.debug = True
            log.basicConfig(level='DEBUG')
        log.info("Constructor configfile={} debug={}".format(configfile, debug))
        # Public Attributs
        self.configfile = configfile    # FortiGate configuration file
        self.vdom_enable = False        # Tell if config has vdom enabled or not
        self.scope = [1,9999999999]     # scope array made of start and end indexes
        self.mgmt_vdom = None
        self.feedback = {}              # Feedback dict after search
        self.debug = debug
        # Private Attributs
        self._config = []
        self._config_lines = 0
        self._vdom_list = []
        self._vdom = dict()
        self.load()

    def load(self):
        """
        Load configuration file
        Index starts at 1 instead of 0 so it matches the line number displayed in text editor when editing the config
        """
        log.info("Enter")
        if not (os.path.exists(self.configfile)):
            print("configfile is required\n")
            raise SystemExit
        try:
            with open(self.configfile)as file_in:
                # add an empty line so array index starts at 1 for config file
                self._config.append("# Empty line:# WARNING: ")
                index = 1
                for line in file_in:
                    line = line.strip()
                    log.debug("index={} read line={}".format(index, line))
                    self._config.append(line)
                    index = index + 1
        except IOError as e:
            log.debug("I/O error filename={} error={}".format(filename,e.strerror))
        self._config_lines = index
        log.debug("Loaded {} line".format(self._config_lines))

    def scope_init(self):
        """
        Reset scope to the full size of the configuration file
        """
        log.info("Enter")
        self.scope = [ 0 , self._config_lines ]

    def get_line(self, index=1):
        """
        Returns configuration line at the provided index
        """
        return(self._config[index])

    def set_line(self, index=None, content=''):
        """
        Set provided content at provided index in configuration
        """
        log.info("Enter with index={} content={}".format(index, content))
        self._config[index] = content

    def max_lines(self):
        """
        Returns configuration size (maximum index)
        """
        return self._config_lines

    def insert(self, index=None, content=''):
        """
        Inserts provided content at provided index.
        Configuration is expanded by 1 line
        """
        log.info("Enter with index={} content={}".format(index, content))
        self._config.insert(index, content)
        self._config_lines = self._config_lines + 1

    def delete(self, index=None, action='blank'):
        """
        Deletes a line. Per default, it is replace with a blank line (action='blank')
        Use action='shrink' to remove the line and shrink config by 1 line
        """
        log.info("Enter with index={} action={}".format(index, action))
        if action == 'shrink':
            del self._config[index]
            self._config_lines = self._config_lines - 1
        elif action == 'blank':
            self._config[index]="\n"
        else:
            log.error('unknown action={}'.format(action))
            raise SystemExit

    def delete_block(self, action='blank'):
        """
        Deletes an entire block of config delimited by scope.
        Configuration is reduced if using action='shrink'
        otherwise block is replaced with blank lines with action='blank' (default)
        """
        log.info("Enter having scope={}".format(self.scope))
        self._check_scope()
        for i in range(self.scope[0], self.scope[1]+1):
            if action == 'shrink':
                del self._config[i]
                self._config_lines = self._config_lines - 1
            elif action == 'blank':
                self._config[i]="\n"
            else:
                log.error('unknown action={}'.format(action))
                raise SystemExit

    def delete_all_keys_from_scope(self, key=None, action='blank'):
        """
        Blank or delete any lines with a given key on a scope
        Configuration is reduced if using action='shrink'
        otherwise block is replaced with blank lines with action='blank' (default)
        """
        log.info("Enter with key={} action={}".format(key, action))
        self._check_scope()
        nb = 0
        for i in range (self.scope[0], self.scope[1]+1):
            log.debug("checking line={}".format(self._config[i]))
            search_pattern = '^(?:\s|\t)*(?:set\s)'+key+'(?:\s|\t)'
            if re.search(search_pattern, self._config[i]):
                nb = nb + 1
                log.debug("found key={} at index={} nb={}".format(key, i, nb))
                if action == 'shrink':
                    del self._config[i]
                    self._config_lines = self._config_lines - 1
                elif action == 'blank':
                    self._config[i]="\n"
                else:
                    log.error('unknown action={}'.format(action))
                    raise SystemExit

    def parse(self):
        """
        Parses the loaded configuration to set information
        """
        log.info("Enter")
        if self._config_lines == 0:
            log.error("configuration file is not loaded")
            raise SystemExit
        self.register_vdoms()
        self._update_mgmt_vdom()

    def register_vdoms(self):
        """
        Register all vdoms:
          - add them in a list
          - store for each of them their startindex and endindex
        """
        log.info("Enter")
        self._vdom_list = []
        self._vdom = dict()
        flag = 0
        vdom = ""
        previous_vdom = ""
        for i in range(1, len(self._config)):
            log.info("line={}  (flag={})".format(self._config[i], flag))
            if flag == 1: #line is config vdom
                match = re.search('edit\s(?P<vdom>(\w|-)*)', self._config[i])
                if match:
                    vdom = match.group('vdom')
                    log.debug("found start of vdom={}".format(vdom))
                    if vdom != '':
                        flag = 2 # got vdom name
                    else:
                        log.error("config error")
                        raise SystemExit
            elif flag == 2:
                # first vdom definition should be ignored
                if not re.search('^(end|next)', self._config[i]):
                    self.vdom_index(vdom=vdom, action='set', type='startindex', value=i)
                    log.debug('registering vdom={}'.format(vdom))
                    self._vdom_list.append(vdom)
                    previous_vdom_index = i - 4
                    log.debug("updating vdom {} endindex={}".format(previous_vdom, previous_vdom_index))
                    self.vdom_index(vdom=previous_vdom, action='set', type='endindex', value=previous_vdom_index)
                    previous_vdom = vdom
                flag = 0
            # reset flag
            if flag == 1:
                flag = 0
            # set flag = 1 when reaching config vdom
            if re.search('config vdom', self._config[i]):
                log.debug("found config vdom at index={}".format(i))
                flag = 1
        # In case there was no vdom found, we only have root vdom
        if vdom == "":
            log.debug("no vdoms")
            vdom = 'root'
            self._vdom_list.append(vdom)
            self.vdom_index(vdom=vdom, action='set', type='startindex', value=4)
        else:
            self.vdom_enable = True
        # Terminates the last vdom
        self.vdom_index(vdom=vdom, action='set', type='endindex', value= i)



    def vdom_index(self, vdom='root', type='', action='', value=None):
        """
        Set or get a given vdom startindex or endindex
        """
        log.info("Enter with vdom={} type={} action={} value={}". \
          format(vdom, type, action, value))
        if vdom == '':
            return
        if action == 'set':
            if not re.search('\d+', str(value)):
                log.error("unexpected value")
                raise SystemExit
            if (vdom not in self._vdom):
                self._vdom[vdom] = {'startindex': None , 'endindex': None}
            if type == 'startindex':
                self._vdom[vdom]['startindex'] = value
            elif type == 'endindex':
                 self._vdom[vdom]['endindex'] = value

        elif action == 'get':
            return self._vdom[vdom][type]
        else:
            log.error("unexpected type")

    def get_nb_vdoms(self):
        """
        Returns the number of vdoms
        """
        log.info("Enter")
        return len (self._vdom_list)

    def get_vdom_list(self):
        """
        Resturns the vdom list sorted alphabetically with management vdom first
        """
        log.info("Enter")
        # TBD requires _update_mgmt_vdom that requires scope_config

    def scope_vdom(self, vdom='root'):
        """
        Set scope corresponding to the given vdom
        Vdoms should have been registered before use.
        """
        log.info("Enter with vdom={}".format(vdom))
        if not self._vdom_list:
            log.error("vdoms are not registered")
        start = self.vdom_index(vdom=vdom, type='startindex', action='get')
        end = self.vdom_index(vdom=vdom, type='endindex', action='get')
        log.debug("result={}".format([start, end]))
        return [start, end]

    def scope_config(self, statement='', partial=False):
        """
        Search for config statement from current scope.
        Upon search success, the scope is updated
        Feedback attribut is updated on success
        return True if statement is found
        """
        log.info("Enter with statement={} partial={}".format(statement, partial))
        log.debug("Initial scope={}".format(self.scope))
        self._clear_feedback()
        result = self._config_seek(startindex = self.scope[0],
                                   endindex = self.scope[1],
                                   starting_statement = statement,
                                   ending_statement = 'end',
                                   key = 'config',
                                   partial_flag = partial)
        self.scope = [ result[1], result[2] ]
        self.feedback['found'] = result[0]
        self.feedback['startindex'] = result[1]
        self.feedback['endindex'] = result[2]
        return result[0]

    def scope_edit(self, statement='', partial=True):
        """
        Search for edit statement from current scope.
        Upon search success, the scope is updated,
        Feedback attribut is updated on success.
        It is possible to get the <id> from an "edit <id>" from feedback 'id'
        return True if statement is found
        """
        log.info("Enter with statement={} partial={}".format(statement, partial))
        log.debug("Initial scope={}".format(self.scope))
        self._clear_feedback()
        result = self._config_seek(startindex = self.scope[0],
                                   endindex = self.scope[1],
                                   starting_statement = statement,
                                   ending_statement = 'next',
                                   key = 'edit',
                                   partial_flag = partial)
        self.scope = [ result[1], result[2] ]
        self.feedback['found'] = result[0]
        self.feedback['startindex'] = result[1]
        self.feedback['endindex'] = result[2]
        self.feedback['id'] = result[3]
        return result[0]

    def get_key(self, key='', nested=False, default=''):
        """
        TBD
        """
        log.info("Enter with key={} nested={} defaut={}".format(key, nested, default))
        log.debug("Initial scope={}".format(self.scope))
        self._clear_feedback()
        # TBD : work in progress

    def _update_mgmt_vdom(self):
        """
        Update management vdoms
        """
        log.info("Enter")
        # TBD: requires scope_config

    def _check_scope(self):
        """
        Check scope attribut is good to be used
        Die if no good
        """
        log.info("Enter having self.scope={}".format(self.scope))
        valid = True
        if not self.scope:
            log.error("scope is not defined")
            valid = False
        if not re.search('\d+',str(self.scope[0])):
            log.error("scope startindex is not a number")
        if not re.search('\d+',str(self.scope[1])):
            log.error("scope endindex is not a number")
        if self.scope[0] > self.scope[1]:
            log.error("scope startindex > endindex")
        if not valid:
            raise SystemExit

    def _clear_feedback(self):
        """
        Resets feedback attribut
        """
        log.info("Enter")
        self.feedback = {}
        self.feedback['found'] = False

    def _config_seek(self, startindex=0, endindex=999999999, starting_statement='', ending_statement='', key='', partial_flag=False):
        """
        Generic seak for config/end and edit/next
        Use self.scope as search entry point. self.scope is refined during the search
        inputs:
           - startindex
           - endindex
           - starting_statement : ex: config
           - ending_statement   : ex: end
           - key : 'edit' or 'config' to count nested element
           - partial_flag : True if the statement by anywhere in the line

        returns an array of 3 values :
           - first  value : True for success (statement found), False for failure
           - second value : start index of the config_statement provided  "config xxxx"
           - third  value : end   index of the end statement corresponding to the config statement
           - fourth value : in case partial_flag is set, retrieves the key in edit <key>
        """
        log.info("Enter with startindex={} endindex={} starting_statement={} ending_statement={} key={} partial_flag={}".\
          format(startindex, endindex, starting_statement, ending_statement, key, partial_flag))
        result = [False, startindex, endindex]
        flag_found = False
        nested_config = 0
        start_return = startindex
        end_return = endindex
        edit_key = None
        for i in range(startindex, endindex):
            line = self._config[i]
            # If we see some other config/edit statement once we have found ours, they are nested so we have to ignore them
            if (re.search('^(\s|\t)*'+key, line) and flag_found):
                nested_config = nested_config + 1
                log.debug("found nested {} at #{}".format(key, i))
            # Find the config statement
            if not flag_found:
                regexp = '(\s|\t)*'+starting_statement
                if not partial_flag:
                    regexp = regexp+'$'
                if re.search(regexp, line):
                    log.debug("found {} at #{}".format(starting_statement, i))
                    flag_found = True
                    start_return = i
                    # Retrieve the key, it could be the name in edit <NAME> or config <name>
                    match = re.search('^(?:\s|\t)*(?:edit|config)(?:\s|\t)*(?:")?(?P<key>[A-Za-z0-9_-]*)(?:")?(?:\r|\n)*', line)
                    if match:
                        edit_key = match.group('key')
                        log.debug('found config/edit key={} at #{}'.format(edit_key, i))
            # Exit if we have found the corresponding end statement
            # but don't catch nested_config end statement
            if re.search('^(\s|\t)*'+ending_statement+'$', line) and flag_found:
                if nested_config > 0:
                    nested_config = nested_config - 1
                    log.debug('seen end of a nested {} at #{}'.format(key, i))
                else:
                    log.debug('end of the {} statement we are looking for at #{}'.format(key,i))
                    end_return = i
                    break
        result = [ flag_found, start_return, end_return, edit_key ]
        log.debug('returning result={}'.format(result))
        return result


"""
Class sample code
"""
if __name__ == '__main__':  # pragma: no cover
    pass
