#Author: Martin De La Cruz Valdez
#Major: Information Technology
#Due Date: December 14, 2023
#Course: CSC328
#Professor Name: Dr. Schwesinger
#Assignment: final project
#Filename: test_lib_team.py


import unittest
import lib_team


class TestLibTeam(unittest.TestCase):
    
    def test_generate_wordspackets(self):
        b = b''
        type_check = lib_team.generate_wordspackets(['Bye','Hello'])
        self.assertEqual(type(type_check), type(b))
        type_check = lib_team.generate_wordspackets(['Bye','Ä'])
        self.assertEqual(type_check, 'Unicode Error occured while encoding')
        type_check = lib_team.generate_wordspackets(['Bye','䑖'])
        self.assertEqual(type_check, 'Unicode Error occured while encoding')
        type_check = lib_team.generate_wordspackets(['Bye','😀'])

    def test_pack_message(self):
        b = b''
        type_check = lib_team.pack_message('Hello')
        self.assertEqual(type(type_check), type(b))
        type_check = lib_team.pack_message('Ä')
        self.assertEqual(type_check, 'Unicode Error occured while encoding')
        type_check = lib_team.pack_message('䑖')
        self.assertEqual(type_check, 'Unicode Error occured while encoding')
        type_check = lib_team.pack_message('😀')



if __name__ == '__main__':
    unittest.main()
