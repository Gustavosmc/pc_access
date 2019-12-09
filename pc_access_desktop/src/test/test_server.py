from src.server import *
import unittest


class TestServerTCP(unittest.TestCase):

    def test_run(self):
        #self.serverTCP.start()
        pass

    def test_get_all_ips(self):
        self.assertEqual(True, len(get_all_ips()) > 0)
        print(get_all_ips())

    def test_add_words(self):
        serverTCP = ServerTCP()
        words = ["yuna", "vaan"]
        serverTCP.add_to_received_words(words)
        self.assertEqual(words[0], serverTCP.received_words[0])

    def test_recover_words(self):
        serverTCP = ServerTCP()
        words = ["yuna", "vaan"]
        serverTCP.add_to_received_words(words)
        self.assertEqual(words[0], serverTCP.received_words[0])
        words_recovered = serverTCP.recover_received_words()
        self.assertEqual(words_recovered[1], "vaan")
        self.assertTrue(len(serverTCP.received_words) == 0)






