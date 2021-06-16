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

    @unittest.skip  # quicker dev stage
    def test_attributs_validation(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.assertTrue(self.cfg.configfile == 'tests/config1.conf')

    @unittest.skip # quicker dev stage
    def test_config_loaded_ok(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.assertEqual(self.cfg._config[5], 'config system global')
        self.assertEqual(self.cfg._config_lines, 12200)

    @unittest.skip # quicker dev stage
    def test_get_line_ok(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.assertEqual(self.cfg.get_line(index=5), 'config system global')

    @unittest.skip # quicker dev stage
    def test_set_line_ok(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.cfg.set_line(index=10, content='    set hostname "MyFgt"')
        self.assertEqual(self.cfg.get_line(index=10), '    set hostname "MyFgt"')

    @unittest.skip # quicker dev stage
    def test_max_lines_ok(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.assertEqual(self.cfg.max_lines(), 12200)

    @unittest.skip # quicker dev stage
    def test_insert_line_ok(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.cfg.insert(index=12, content="__ADDED__\n")
        self.assertEqual(self.cfg.get_line(index=13), 'end')
        self.assertEqual(self.cfg.max_lines(), 12201)
        self.assertEqual(self.cfg.get_line(index=12), '__ADDED__\n')

    @unittest.skip # quicker dev stage
    def test_delete_blank_ok(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.cfg.delete(action='blank', index=5)
        self.assertEqual(self.cfg.get_line(index=5), "\n")
        self.cfg.delete(action='shrink', index=5)
        self.assertEqual(self.cfg.get_line(index=11), 'end')


    @unittest.skip # quicker dev stage
    def test_delete_block_shrink_ok(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.cfg.delete_block(scope=[5,12], action='shrink')
        self.assertEqual(self.cfg.max_lines(), 12200-8)

    @unittest.skip # quicker dev stage
    def test_delete_block_blank_ok(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.cfg.delete_block(scope=[5, 12], action='blank')
        self.assertEqual(self.cfg.get_line(index=5), "\n")
        self.assertEqual(self.cfg.get_line(index=10), "\n")
        self.assertEqual(self.cfg.get_line(index=12), "\n")
        self.assertEqual(self.cfg.max_lines(), 12200)

    @unittest.skip # quicker dev stage
    def test_delete_all_keys_from_scope_blank_ok(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.cfg.delete_all_keys_from_scope(key='uuid', scope=[7278, 7402], action='blank')
        self.assertEqual(self.cfg.get_line(index=7280), "\n")
        self.assertEqual(self.cfg.get_line(index=7398), "\n")

    @unittest.skip # quicker dev stage
    def test_delete_all_keys_from_scope_shrink_ok(self):
        self.cfg = Ftntdissect(configfile='tests/config1.conf', debug=True)
        self.cfg.delete_all_keys_from_scope(key='start-ip', scope=[7403, 7428], action='shrink')
        self.assertEqual(self.cfg.max_lines(), 12200-6)

    def test_register_vdoms_ok(self):
        self.cfg = Ftntdissect(configfile='tests/config2.conf', debug=True)
        self.cfg.register_vdoms()





if __name__ == '__main__':
    unittest.main()
