import unittest
from final import *

class TestDatabase(unittest.TestCase):
	def test_player_table(self):
		conn = sqlite3.connect("final.sqlite")
		cur = conn.cursor()
		statement = '''
			SELECT PLAYER, PTS FROM  Players
		'''
		cur.execute(statement)
		tups = cur.fetchall()
		conn.close()
		self.assertIsInstance(tups[0],tuple)
		self.assertIn(('Kevin Durant', 30), tups)
		self.assertEqual('Joel Embiid', tups[7][0])
		self.assertEqual(23, tups[15][1])
		self.assertEqual(453, len(tups))

	def test_team_table(self):
		conn = sqlite3.connect("final.sqlite")
		cur = conn.cursor()
		statement = '''
			SELECT TEAM, W, PTS  FROM  Teams
		'''
		cur.execute(statement)
		tups = cur.fetchall()
		conn.close()
		self.assertIsInstance(tups[0],tuple)
		self.assertIn(('Boston Celtics', 13, 108.5), tups)
		self.assertEqual(15, tups[3][1])
		self.assertEqual('Houston Rockets', tups[19][0])
		self.assertEqual(30, len(tups))

	def test_all_time_table(self):
		conn = sqlite3.connect("all_time.sqlite")
		cur = conn.cursor()
		statement = '''
			SELECT Player, GP, PTS FROM  Players
		'''
		cur.execute(statement)
		tups = cur.fetchall()
		conn.close()
		self.assertIsInstance(tups[0],tuple)
		self.assertIn(('Kobe Bryant', '1,346', 33643), tups)
		self.assertEqual('Wilt Chamberlain', tups[5][0])
		self.assertEqual(38387, tups[0][2])
		self.assertEqual(1249, len(tups))

	def test_json(self):
		fr = open('cache_comment.json','r')
		diction = json.loads(fr.read())
		fr.close()
		self.assertIsInstance(diction, dict)
		self.assertIsInstance(diction['Stephen Curry'], list)
		self.assertEqual(diction['Chris Paul'][58], 'All of that may be true,\n\nBut you still spit bruh.')

if __name__ == '__main__':
	unittest.main(verbosity = 2)