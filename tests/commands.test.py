# Standard packages
import unittest


class StartUpCase(unittest.TestCase):
    def on_guild_join(self):
        self.assertEqual(True, False)


if __name__ == "__main__":
    unittest.main()
