import sys
import unittest

import appletrailers


class test_appletrailer(unittest.TestCase):
    all_trailers = None
    def setUp(self):
        if self.all_trailers is None:
            # Only initialise all_trailers once
            self.__class__.all_trailers = appletrailers.Trailers(res = "720")
    
    def test_has_trailers(self):
        self.failUnless(len(self.all_trailers) > 1)
    
    def test_get_poster(self):
        first_poster = self.all_trailers[0].poster.location
        self.failUnless(first_poster.startswith("http://trailers.apple.com/trailers/"))
    
    def test_trailer(self):
        first_trailer_preview = self.all_trailers[0].preview.large
        self.failUnless(first_trailer_preview.startswith("http://trailers.apple.com/movies/"))


def main():
    """Runs unittests, or simply lists title/poster URL/actors/trailer link for all trailers"""
    suite = unittest.TestSuite()
    suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(
            test_appletrailer
        )
    )
    runner = unittest.TextTestRunner(verbosity = 2)
    results = runner.run(suite)
    if len(results.failures) > 0 or len(results.errors) > 0:
        sys.exit(1)
    else:
        sys.exit(0)

    
if __name__ == '__main__':
    main()
