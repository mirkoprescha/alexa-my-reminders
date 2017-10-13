# coding: utf-8
import unittest
import read_reminders
import config


class ReadRemindersTest(unittest.TestCase):
    def test_read_reminders(self):
        under_test = read_reminders.getTextFromS3(config.S3_BUCKET, config.S3_KEY)
        print under_test

    def clean_text(self):
        sample = open ("sample.txt").read()
        print "raw text:" + sample
        under_test = read_reminders.clean_text(sample)

        print "reminder#1: " + under_test[0]
        print "reminder#2: " + under_test[1]
        print "reminder#3: " + under_test[2]
        print "reminder#4: " + under_test[3]
        print "reminder#5: " + under_test[4]
        self.assertEqual(len(under_test),5, msg="expected number of reminders is wrong")

        #self.assertEqual(under_test[3], "X5zpabc.", msg="expected only speakable characters")
        self.assertEqual(under_test[4], "ÄÖÜYYY.", msg="expected correct umlauts")