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
        self.configfile = configfile
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

    def delete_block(self, scope=[1,-1], action='blank'):
        """
        Deletes an entire block of config delimited by a scope.
        Configuration is reduced if using action='shrink'
        otherwise block is replaced with blank lines with action='blank' (default)
        """
        log.info("Enter with scope={}".format(scope))
        for i in range(scope[0], scope[1]+1):
            if action == 'shrink':
                del self._config[i]
                self._config_lines = self._config_lines - 1
            elif action == 'blank':
                self._config[i]="\n"
            else:
                log.error('unknown action={}'.format(action))
                raise SystemExit

    def delete_all_keys_from_scope(self, key=None, scope=[1,-1], action='blank'):
        """
        Blank or delete any lines with a given key on the given scope
        Configuration is reduced if using action='shrink'
        otherwise block is replaced with blank lines with action='blank' (default)
        """
        log.info("Enter with scope={} key={} action={}".format(scope, key, action))
        nb = 0
        for i in range (scope[0], scope[1]+1):
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
        for i in range(1, len(self._config)):
            log.info("line={}".format(self._config[i]))
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

                    # TBD ! I am HERE

            if re.search('config vdom', self._config[i]):
                log.debug('found config vdom')
                flag = 1

    def vdom_index(self, vdom='root', type='', action='', value=None):
        """
        Set or get a given vdom startindex or endindex
        """
        log.info("Enter with vdom={} type={} action={} value={}". \
          format(vdom, type, action, value))



"""
Class sample code
"""
if __name__ == '__main__':  # pragma: no cover
    pass
