from main import main
import unittest

class TestEmotions(unittest.TestCase):

    def test_analyze_emotion_correct(self):
        self.assertEqual(
            main(
                {"name": "edgar.jpg", "bucket": "sentimentproject-362601-input"}, 0),
                "edgar esta feliz, " )
if __name__ == '__main__':
    unittest.main()