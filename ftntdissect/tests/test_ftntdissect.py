# -*- coding: utf-8 -*-
'''
Created on Jun 16, 2021
@author: cgustave
'''
import logging as log
import unittest
from ftntdissect import Ftntdissect

# create logger
log.basicConfig(
    format='%(asctime)s,%(msecs)3.3d %(levelname)-8s[%(module)-7.7s.\
    %(funcName)-30.30s:%(lineno)5d]%(message)s',
    datefmt='%Y%m%d:%H:%M:%S',
    filename='debug.log',
    level=log.DEBUG)
log.debug("Start unittest")

class FtntdissectTestCase(unittest.TestCase):

    def setUp(self):
        pass

    #@unittest.skip  # quicker dev stage
    def test_attributs_validation(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.assertTrue(self.cfg.configfile == 'tests/config1.conf')

    #@unittest.skip # quicker dev stage
    def test_config_loaded_ok(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.assertEqual(self.cfg._config[5], 'config system global')
        self.assertEqual(self.cfg._config_lines, 12200)

    #@unittest.skip # quicker dev stage
    def test_get_line_ok(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.assertEqual(self.cfg.get_line(index=5), 'config system global')

    #@unittest.skip # quicker dev stage
    def test_set_line_ok(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.cfg.set_line(index=10, content='    set hostname "MyFgt"')
        self.assertEqual(self.cfg.get_line(index=10), '    set hostname "MyFgt"')

    #@unittest.skip # quicker dev stage
    def test_max_lines_ok(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.assertEqual(self.cfg.max_lines(), 12200)

    #@unittest.skip # quicker dev stage
    def test_insert_line_ok(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.cfg.insert(index=12, content="__ADDED__\n")
        self.assertEqual(self.cfg.get_line(index=13), 'end')
        self.assertEqual(self.cfg.max_lines(), 12201)
        self.assertEqual(self.cfg.get_line(index=12), '__ADDED__\n')

    #@unittest.skip # quicker dev stage
    def test_delete_blank_ok(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.cfg.delete(action='blank', index=5)
        self.assertEqual(self.cfg.get_line(index=5), "\n")
        self.cfg.delete(action='shrink', index=5)
        self.assertEqual(self.cfg.get_line(index=11), 'end')

    #@unittest.skip # quicker dev stage
    def test_delete_block_shrink_ok(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.cfg.scope = [5,12]
        self.cfg.delete_block(action='shrink')
        self.assertEqual(self.cfg.max_lines(), 12200-8)

    #@unittest.skip # quicker dev stage
    def test_delete_block_blank_ok(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.cfg.scope = [5,12]
        self.cfg.delete_block(action='blank')
        self.assertEqual(self.cfg.get_line(index=5), "\n")
        self.assertEqual(self.cfg.get_line(index=10), "\n")
        self.assertEqual(self.cfg.get_line(index=12), "\n")
        self.assertEqual(self.cfg.max_lines(), 12200)

    #@unittest.skip # quicker dev stage
    def test_delete_all_keys_from_scope_blank_ok(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.cfg.scope = [7278, 7402]
        self.cfg.delete_all_keys_from_scope(key='uuid', action='blank')
        self.assertEqual(self.cfg.get_line(index=7280), "\n")
        self.assertEqual(self.cfg.get_line(index=7398), "\n")

    #@unittest.skip # quicker dev stage
    def test_delete_all_keys_from_scope_shrink_ok(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.cfg.scope = [7403, 7428]
        self.cfg.delete_all_keys_from_scope(key='start-ip', action='shrink')
        self.assertEqual(self.cfg.max_lines(), 12200-6)

    #@unittest.skip # quicker dev stage
    def test_register_vdoms_ok_1vdom(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.cfg.register_vdoms()
        #print ("vdom={}".format(self.cfg._vdom))
        self.assertEqual(self.cfg._vdom_list, ['root'])
        self.assertEqual(self.cfg._vdom['root']['startindex'], 4)
        self.assertEqual(self.cfg._vdom['root']['endindex'], 12199)
        self.assertEqual(self.cfg.vdom_enable, False)

    #@unittest.skip # quicker dev stage
    def test_scope_init_ok(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.cfg.scope_init()
        self.assertEqual(self.cfg.scope[0], 0)
        self.assertEqual(self.cfg.scope[1], 12200)

    #@unittest.skip # quicker dev stage
    def test_register_vdoms_ok_4vdoms(self):
        self.cfg = Ftntdissect(configfile='tests/config2.conf', debug=True)
        self.cfg.register_vdoms()
        self.assertEqual(self.cfg._vdom_list, ['root', 'vdom_one', 'vdom_two', 'vdom_three'])
        #print ("vdom={}".format(self.cfg._vdom))
        self.assertEqual(self.cfg._vdom['root']['startindex'], 8331)
        self.assertEqual(self.cfg._vdom['root']['endindex'], 11574)
        self.assertEqual(self.cfg._vdom['vdom_one']['startindex'], 11578)
        self.assertEqual(self.cfg._vdom['vdom_one']['endindex'], 14071)
        self.assertEqual(self.cfg._vdom['vdom_two']['startindex'], 14075)
        self.assertEqual(self.cfg._vdom['vdom_two']['endindex'], 16548)
        self.assertEqual(self.cfg._vdom['vdom_three']['startindex'], 16552)
        self.assertEqual(self.cfg._vdom['vdom_three']['endindex'], 19025)
        self.assertEqual(self.cfg.vdom_enable, True)

    #@unittest.skip # quicker dev stage
    def test_nb_vdom_ok_1vdoms(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.cfg.register_vdoms()
        self.assertEqual(self.cfg.get_nb_vdoms(), 1)

    #@unittest.skip # quicker dev stage
    def test_nb_vdom_ok_4vdoms(self):
        self.cfg = Ftntdissect(configfile='tests/config2.conf', debug=True)
        self.cfg.register_vdoms()
        self.assertEqual(self.cfg.get_nb_vdoms(), 4)

    #@unittest.skip # quicker dev stage
    def test_scope_vdom_ok(self):
        self.cfg = Ftntdissect(configfile='tests/config2.conf', debug=True)
        self.cfg.register_vdoms()
        result = self.cfg.scope_vdom(vdom='vdom_one')
        self.assertEqual(result, [ 11578, 14071 ])

    #@unittest.skip # quicker dev stage
    def test_get_vdom_list(self):
        self.cfg = Ftntdissect(configfile='tests/config2.conf', debug=True)
        self.cfg.parse()
        self.assertEqual(self.cfg.get_vdom_list(), ['root', 'vdom_one', 'vdom_three', 'vdom_two'])

    #@unittest.skip # quicker dev stage
    def test_config_seek_1(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        result = self.cfg._config_seek( startindex = 1,
                                        endindex = self.cfg._config_lines,
                                        starting_statement = 'config system global',
                                        ending_statement = 'end',
                                        key = 'config',
                                        partial_flag = False)
        self.assertEqual(result[0], True)
        self.assertEqual(result[1], 5)
        self.assertEqual(result[2], 12)

    #@unittest.skip
    def test_scope_config_1(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.cfg.parse()
        result = self.cfg.scope_config(statement='config system global')
        self.assertTrue(result)
        self.assertTrue(self.cfg.feedback['found'])
        self.assertEqual(self.cfg.feedback['startindex'], 5)
        self.assertEqual(self.cfg.feedback['endindex'], 12)
        self.assertEqual(self.cfg.scope[0], 5)
        self.assertEqual(self.cfg.scope[1], 12)

    #@unittest.skip
    def test_scope_config_multi_1(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.cfg.parse()
        result = self.cfg.scope_config(statement='config router bgp')
        if result:
            self.cfg.scope_config(statement='config neighbor')
            self.assertTrue(self.cfg.feedback['found'])
            self.assertEqual(self.cfg.feedback['startindex'], 12112)
            self.assertEqual(self.cfg.feedback['endindex'], 12149)

    #@unittest.skip
    def test_scope_edit_get_id(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.cfg.parse()
        result = self.cfg.scope_config(statement='config system interface')
        if result:
            result = self.cfg.scope_edit(statement='edit')
            #print("result={}".format(result))
            self.assertTrue(self.cfg.feedback['found'])
            self.assertEqual(self.cfg.feedback['startindex'], 29)
            self.assertEqual(self.cfg.feedback['endindex'], 37)
            self.assertEqual(self.cfg.feedback['id'], 'port1')

    #@unittest.skip
    def test_scope_edit_specific(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.cfg.parse()
        result = self.cfg.scope_config(statement='config system interface')
        if result:
            result = self.cfg.scope_edit(statement='edit "port2"')
            #print("result={} feedback={}".format(result, self.cfg.feedback))
            self.assertTrue(self.cfg.feedback['found'])
            self.assertEqual(self.cfg.feedback['startindex'], 38)
            self.assertEqual(self.cfg.feedback['endindex'], 46)
            self.assertEqual(self.cfg.feedback['id'], 'port2')

    #@unittest.skip
    def test_get_key_ok_1(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.cfg.parse()
        if self.cfg.scope_config(statement='config system interface'):
            if self.cfg.scope_edit(statement='edit "port2"'):
                result = self.cfg.get_key(key='alias', nested=False, default='')
                self.assertTrue(self.cfg.feedback['found'])
                self.assertEqual(self.cfg.feedback['index'], 43)
                self.assertEqual(self.cfg.feedback['key'], 'alias')
                self.assertEqual(self.cfg.feedback['value'], 'Internet-2')
                #print("result={} feedback={}".format(result, self.cfg.feedback))

    #@unittest.skip
    def test_get_key_nok_1(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.cfg.parse()
        if self.cfg.scope_config(statement='config system interface'):
            if self.cfg.scope_edit(statement='edit "port2"'):
                result = self.cfg.get_key(key='whatever', nested=False, default='hoho')
                self.assertFalse(self.cfg.feedback['found'])
                self.assertEqual(self.cfg.feedback['index'], 0)
                self.assertEqual(self.cfg.feedback['key'], 'whatever')
                self.assertEqual(self.cfg.feedback['value'], 'hoho')
                print("result={} feedback={}".format(result, self.cfg.feedback))

    #@unittest.skip
    def test_udpate_mgmt_vdom(self):
        self.cfg = Ftntdissect(configfile='tests/config2.conf', debug=True)
        self.cfg.parse()
        self.assertEqual(self.cfg.mgmt_vdom, 'root')

    #@unittest.skip
    def test_set_key_update(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        if self.cfg.scope_config(statement='config system admin'):
            if self.cfg.scope_edit(statement='edit "admin"'):
                self.cfg.set_key(key='password', value='fortinet')
                result = self.cfg.get_key(key="password")
                self.assertTrue(self.cfg.feedback['found'])
                self.assertEqual(self.cfg.feedback['value'], 'fortinet')

    #@unittest.skip
    def test_set_key_add(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        if self.cfg.scope_config(statement='config system global'):
            saved_scope =self.cfg.scope
            self.cfg.set_key(key='fortiextender-vlan-mode', value='enable')
            self.cfg.scope = saved_scope
            result = self.cfg.get_key(key="fortiextender-vlan-mode")
            self.cfg.dump()
            self.assertTrue(self.cfg.feedback['found'])
            self.assertEqual(self.cfg.feedback['value'], 'enable')


if __name__ == '__main__':
    unittest.main()
