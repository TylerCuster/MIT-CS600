# -*- coding: cp1252 -*-
# 6.00 Problem Set 5
# RSS Feed Filter
##
import feedparser
import string
import time
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

# TODO: NewsStory

class NewsStory(object):
    """
    Creates object with:
    globally unique identifier (guid) - a string that serves as a unique name for this entry
    title - string
    subject - string
    summary - string
    link to more content - string
    """
    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_subject(self):
        return self.subject
    def get_summary(self):
        return self.summary
    def get_link(self):
        return self.link

#======================
# Part 2
# Triggers
#======================

# Whole Word Triggers
# Problems 2-5

# TODO: WordTrigger

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

class WordTrigger(Trigger):
    def __init__(self, word):
        self.word = word
    def is_word_in(self, text):
        test_word = string.lower(self.word)
        test_text = string.lower(text)
        for punc in string.punctuation:
            if punc+test_word in test_text:
                return True
            if test_word+punc in test_text:
                return True
        if " "+test_word+" " in test_text:
            return True
        if test_word == test_text[0:len(test_word)]:
            return True
        return False
    
##fucks = WordTrigger("soft")
##print fucks.is_word_in("Koala bears are soft and cuddly.")
##print fucks.is_word_in("I prefer pillows that are soft.")
##print fucks.is_word_in("Soft drinks are great.")
##print fucks.is_word_in("Soft’s the new pink!")
##print fucks.is_word_in("'Soft!' he exclaimed as he threw the football.")
##print fucks.is_word_in("Microsoft announced today that pillows are bad.")

# TODO: TitleTrigger
class TitleTrigger(WordTrigger):
    def __init__(self, word):
        self.word = word
    def evaluate(self, story):
        title = story.get_title()
        if self.is_word_in(title) == True:
            return True
        return False

# TODO: SubjectTrigger

class SubjectTrigger(WordTrigger):
    def __init__(self, word):
        self.word = word
    def evaluate(self, story):
        subject = story.get_subject()
        if self.is_word_in(subject) == True:
            return True
        return False

# TODO: SummaryTrigger

class SummaryTrigger(WordTrigger):
    def __init__(self, word):
        self.word = word
    def evaluate(self, story):
        summary = story.get_summary()
        if self.is_word_in(summary) == True:
            return True
        return False

# Composite Triggers
# Problems 6-8

# TODO: NotTrigger

class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger
    def evaluate(self, story):
        return not self.trigger.evaluate(story)

# TODO: AndTrigger

class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def evaluate(self, story):
        if (self.trigger1.evaluate(story) == True and self.trigger2.evaluate(story) == True):
            return True
        else:
            return False

# TODO: OrTrigger

class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def evaluate(self, story):
        if self.trigger1.evaluate(story) == True:
            return True
        elif self.trigger2.evaluate(story) == True:
            return True
        else:
            return False

# Phrase Trigger
# Question 9

# TODO: PhraseTrigger

class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase
    def evaluate(self, story):
        if self.phrase in story.subject:
            return True
        elif self.phrase in story.title:
            return True
        elif self.phrase in story.summary:
            return True
        else:
            return False

#======================
# Part 3
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    story_list = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story) == True:
                story_list.append(story)
    return story_list

#======================
# Part 4
# User-Specified Triggers
#======================

def triggerDictionary(triggerdict, triggertype, params, name):
    if triggertype == "TITLE":
        trigger = TitleTrigger(params[0])
    elif triggertype == "SUBJECT":
        trigger = SubjectTrigger(params[0])
    elif triggertype == "SUMMARY":
        trigger = SummaryTrigger(params[0])
    elif triggertype == "NOT":
        trigger = NotTrigger(triggerdict[params[0]])
    elif triggertype == "AND":
        trigger = AndTrigger(triggerdict[params[0]], triggerdict[params[1]])
    elif triggertype == "OR":
        trigger = OrTrigger(triggerdict[params[0]], triggerdict[params[1]])
    elif triggertype == "PHRASE":
        param = ""
        for word in params:
            param = param + " " + word
        trigger = PhraseTrigger(param)
    else:
        return None
    triggerdict[name] = trigger

def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)
    trigger_list = []
    triggerdict = {}
    for line in lines:
        split_list = string.split(line)
        if split_list[0] != "ADD":
            trigger = triggerDictionary(triggerdict, split_list[1], split_list[2:], split_list[0])
        else:
            for name in split_list[1:]:
                trigger_list.append(triggerdict[name])
    return trigger_list

    # TODO: Problem 11
    # 'lines' has a list of lines you need to parse
    # Build a set of triggers from it and
    # return the appropriate ones
    
import thread

def main_thread(p):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    t1 = SummaryTrigger("Obama")
    t2 = SummaryTrigger("Anarchists")
    t3 = PhraseTrigger("Bomb")
    t4 = OrTrigger(t2, t3)
    triggerlist = [t1, t4]
    
    # TODO: Problem 11
    # After implementing readTriggerConfig, uncomment this line 
    triggerlist = readTriggerConfig("triggers.txt")

    guidShown = []
    
    while True:
        print "Polling..."

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)
    
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)
        
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)

SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()

