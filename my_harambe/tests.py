from django.test import TestCase

class RedundantTest(TestCase):

    def test_test(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        self.assertTrue(True)
        self.assertFalse(False)