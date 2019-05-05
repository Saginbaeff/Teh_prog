import unittest
import review
import time
import random
import string
import subprocess


class UnitTest(unittest.TestCase):
    def test_caesar_encode(self):
        self.assertEqual(review.caesar_encode('Python', 0, 1), 'Qzuipo')
        self.assertEqual(review.caesar_encode('Python', 0, 2), 'Ravjqp')
        self.assertEqual(review.caesar_encode('Python', 0, 3), 'Sbwkrq')
        self.assertEqual(review.caesar_encode('Python', 0, 4), 'Tcxlsr')
        self.assertEqual(review.caesar_encode('Python', 0, 5), 'Udymts')
        self.assertEqual(review.caesar_encode('Python', 0, 6), 'Veznut')
        self.assertEqual(review.caesar_encode('Python', 0, 7), 'Wfaovu')
        self.assertEqual(review.caesar_encode('Python', 0, 8), 'Xgbpwv')
        self.assertEqual(review.caesar_encode('Python', 0, 9), 'Yhcqxw')

    def test_caesar_decode(self):
        self.assertEqual(review.caesar_encode('Qzuipo', 1, 0), 'Python')
        self.assertEqual(review.caesar_encode('Ravjqp', 2, 0), 'Python')
        self.assertEqual(review.caesar_encode('Sbwkrq', 3, 0), 'Python')
        self.assertEqual(review.caesar_encode('Tcxlsr', 4, 0), 'Python')
        self.assertEqual(review.caesar_encode('Udymts', 5, 0), 'Python')
        self.assertEqual(review.caesar_encode('Veznut', 6, 0), 'Python')
        self.assertEqual(review.caesar_encode('Wfaovu', 7, 0), 'Python')
        self.assertEqual(review.caesar_encode('Xgbpwv', 8, 0), 'Python')
        self.assertEqual(review.caesar_encode('Yhcqxw', 9, 0), 'Python')

    def test_vigenere_encode(self):
        self.assertEqual(review.vigenere_encode('attackatdawn', 'A', 'lemon'), 'lxfopvefrnhr')
        self.assertEqual(review.vigenere_encode('python', 'A', 'lemon'), 'acfvby')

    def test_vigenere_decode(self):
        self.assertEqual(review.vigenere_encode('lxfopvefrnhr', 'lemon', 'A'), 'attackatdawn')
        self.assertEqual(review.vigenere_encode('acfvby', 'lemon', 'A'), 'python')

    def test_vernam_encode(self):
        self.assertEqual(review.vernam_encode('abcdef', 'abcdef'), '111111')
        self.assertEqual(review.vernam_encode('python', 'vbasic'), 'APJTUN')

    def test_vernam_decode(self):
        self.assertEqual(review.vernam_encode('111111', 'abcdef'), 'abcdef')
        self.assertEqual(review.vernam_encode('APJTUN', 'vbasic'), 'python')

    def test_hack(self):
        with open('input.txt', 'r') as file:
            text = file.read()
        new_text = review.vigenere_encode(text, 'A', 'python')
        self.assertEqual(review.hack(new_text, 'model.txt'), text)


class LoadTest(unittest.TestCase):
    def test_many_words_caesar_encode(self):
        with open('Shakespire.txt', 'r') as file:
            text = file.read()
        text = text.split('\n')
        time_start = time.time()
        for i in text:
            review.caesar_encode(i, 0, random.randrange(1, 20))
        self.assertTrue(time.time() - time_start < 1.0)

        with open('Vocabulary.txt', 'r') as file:
            text = file.read()
        text = text.split('\n-')
        time_start = time.time()
        for i in text:
            review.caesar_encode(i, 0, random.randrange(1, 20))
        self.assertTrue(time.time() - time_start < 2.0)

    def test_many_words_vigenere_encode(self):
        with open('Shakespire.txt', 'r') as file:
            text = file.read()
        text = text.split('\n')
        time_start = time.time()
        for i in text:
            review.vigenere_encode(i, 'A', ''.join(random.choices(string.ascii_lowercase, k=10)))
        self.assertTrue(time.time() - time_start < 2.0)

        with open('Vocabulary.txt', 'r') as file:
            text = file.read()
        text = text.split('\n-')
        time_start = time.time()
        for i in text:
            review.vigenere_encode(i, 'A', ''.join(random.choices(string.ascii_lowercase, k=10)))
        self.assertTrue(time.time() - time_start < 5.0)

    def test_many_words_vernam_encode(self):
        with open('Shakespire.txt', 'r') as file:
            text = file.read()
        text = text.split('\n-')
        time_start = time.time()
        for i in text:
            review.vernam_encode(i, ''.join(random.choices(string.ascii_lowercase, k=len(i))))
        self.assertTrue(time.time() - time_start < 1.0)

        with open('Vocabulary.txt', 'r') as file:
            text = file.read()
        text = text.split('\n-')
        time_start = time.time()
        for i in text:
            review.vernam_encode(i, ''.join(random.choices(string.ascii_lowercase, k=len(i))))
        self.assertTrue(time.time() - time_start < 3.0)

    def test_small_text_caesar_encode(self):
        with open('Shakespire.txt', 'r') as file:
            text = file.read()
        time_start = time.time()
        review.caesar_encode(text, 0, 10)
        self.assertTrue(time.time() - time_start < 0.5)

    def test_medium_text_caesar_encode(self):
        with open('Jerome_-_Three_men_in_a_boat.txt', 'r') as file:
            text = file.read()
        time_start = time.time()
        review.caesar_encode(text, 0, 10)
        self.assertTrue(time.time() - time_start < 1.0)

    def test_small_text_vigenere_encode(self):
        with open('Shakespire.txt', 'r') as file:
            text = file.read()
        time_start = time.time()
        review.vigenere_encode(text, 'A', 'python')
        self.assertTrue(time.time() - time_start < 1.0)

    def test_medium_text_vigenere_encode(self):
        with open('Jerome_-_Three_men_in_a_boat.txt', 'r') as file:
            text = file.read()
        time_start = time.time()
        review.vigenere_encode(text, 'A', 'python')
        self.assertTrue(time.time() - time_start < 2.0)

    def test_small_text_vernam_encode(self):
        with open('Shakespire.txt', 'r') as file:
            text = file.read()
        time_start = time.time()
        review.vernam_encode(text, ''.join(random.choices(string.ascii_lowercase, k=len(text))))
        self.assertTrue(time.time() - time_start < 1.0)

    def test_medium_text_vernam_encode(self):
        with open('Jerome_-_Three_men_in_a_boat.txt', 'r') as file:
            text = file.read()
        time_start = time.time()
        review.vernam_encode(text, ''.join(random.choices(string.ascii_lowercase, k=len(text))))
        self.assertTrue(time.time() - time_start < 2.0)


class StressTest(unittest.TestCase):
    def test_big_text_caesar_encode(self):
        with open('WarAndPeace.txt', 'r', encoding='utf-8') as file:
            text = file.read()
        time_start = time.time()
        new_text = review.caesar_encode(text, 0, 10)
        self.assertTrue(time.time() - time_start < 2.0)
        with open('WarAndPeaceCipherCaesar.txt', 'r', encoding='utf-8') as file:
            text = file.read()
        self.assertEqual(new_text + '\n', text)

    def test_big_text_vigenere_encode(self):
        with open('WarAndPeace.txt', 'r', encoding='utf-8') as file:
            text = file.read()
        time_start = time.time()
        new_text = review.vigenere_encode(text, 'A', 'python')
        self.assertTrue(time.time() - time_start < 20.0)
        with open('WarAndPeaceCipherVigenere.txt', 'r', encoding='utf-8') as file:
            text = file.read()
        self.assertEqual(new_text + '\n', text)

    def test_big_text_vernam_encode(self):
        with open('WarAndPeace.txt', 'r', encoding='utf-8') as file:
            text = file.read()
        with open('key.txt', 'r', encoding='utf-8') as file:
            key = file.read()
        time_start = time.time()
        new_text = review.vernam_encode(text, key)
        self.assertTrue(time.time() - time_start < 10.0)
        with open('WarAndPeaceCipherVernam.txt', 'r', encoding='utf-8') as file:
            text = file.read()
        self.assertEqual(new_text + '\n', text)

    def test_big_text_caesar_decode(self):
        with open('WarAndPeaceCipherCaesar.txt', 'r', encoding='utf-8') as file:
            text = file.read()
        time_start = time.time()
        new_text = review.caesar_encode(text, 10, 0)
        self.assertTrue(time.time() - time_start < 2.0)
        with open('WarAndPeace.txt', 'r', encoding='utf-8') as file:
            text = file.read()
        self.assertEqual(new_text, text + '\n')

    def test_big_text_vigenere_decode(self):
        with open('WarAndPeaceCipherVigenere.txt', 'r', encoding='utf-8') as file:
            text = file.read()
        time_start = time.time()
        new_text = review.vigenere_encode(text, 'python', 'A')
        self.assertTrue(time.time() - time_start < 20.0)
        with open('WarAndPeace.txt', 'r', encoding='utf-8') as file:
            text = file.read()
        self.assertEqual(new_text, text + '\n')


class UsabilityTest(unittest.TestCase):
    def test_scenario_1(self):
        self.assertEqual(subprocess.check_output(["python", "review.py", "encode", "--cipher", "caesar", "--key", "20", "--input-file", "input_sc1.txt"]), b'Jsnbihcw\r\n')

    def test_scenario_2(self):
        self.assertEqual(subprocess.check_output(["python", "review.py", "encode", "--cipher", "vigenere", "--key", "python", "--input-file", "input_sc2.txt"]), b'hcx fch aymlf najbnogdp\r\n')

    def test_scenario_3(self):
        self.assertEqual(subprocess.check_output(["python", "review.py", "decode", "--cipher", "caesar", "--key", "20", "--input-file", "input_sc3.txt"]), b'Pythonic\r\n')

    def test_scenario_4(self):
        self.assertEqual(subprocess.check_output(["python", "review.py", "decode", "--cipher", "vigenere", "--key", "python", "--input-file", "input_sc4.txt"]), b'see you later alligator\r\n')

    def test_scenario_5(self):
        with open('input.txt', 'r') as file:
            text = file.read()
        self.assertEqual(subprocess.check_output(["python", "review.py", "hack", "--input-file", "output.txt", "--model-file", "model.txt"], encoding='utf-8'), text + "\n")

    def test_scenario_6(self):
        subprocess.run(
            ["python", "review.py", "decode", "--cipher", "vigenere", "--key", "python", "--input-file",
             "input_sc4.txt", "--output-file", "output_sc6.txt"])
        with open('output_sc6.txt', 'r') as file:
            text = file.read()
        self.assertEqual(text, "see you later alligator\n")

    def test_scenario_7(self):
        subprocess.run(
            ["python", "review.py", "decode", "--cipher", "caesar", "--key", "20", "--input-file", "input_sc3.txt", "--output-file", "output_sc7.txt"])
        with open('output_sc7.txt', 'r') as file:
            text = file.read()
        self.assertEqual(text, "Pythonic\n")


unittest.main()
