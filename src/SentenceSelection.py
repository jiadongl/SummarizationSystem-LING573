import nltk
import operator
import os
import string
import xml.etree.ElementTree as ET
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from xml.dom import minidom


if __name__ == "__main__":

    # TopicDir = sys.argv[1]
    TopicDir = '/Users/Jiadong/Desktop/573/SummarizationSystem/SentenceScoreData/'
    # TopicFile = sys.argv[2]
    # TopicFile = '/Users/Jiadong/Desktop/573/SummarizationSystem/PreprocessedData/D0901A.xml'
    # OutputDir = sys.argv[3]
    OutputDir = '/Users/Jiadong/Desktop/573/SummarizationSystem/SentenceSelectionData/'

    for root, dirs, files in os.walk(TopicDir):
        for file in files:
            TopicFile = os.path.join(root, file)

            Topic = ET.parse(TopicFile).getroot()
            TopicId = Topic.get('id')

            Sentences = []
            totalWords = 0

            for Content in Topic:
                if Content.tag == 'Sentences':
                    for Sentence in Content:
                        wordsCount = len(nltk.word_tokenize(Sentence.text))
                        if (totalWords + wordsCount) <= 100 :
                            Sentences.append([Sentence.get('DocIndex'), Sentence.get('Score'), Sentence.text])
                            totalWords += wordsCount
                        else:
                            break

            for sentence in Sentences:
                # print (sentence[0],sentence[1])
                sentence[1] = float(sentence[1]) - float(sentence[0])


            TopicFile = os.path.join(OutputDir, TopicId + '.xml')
            try:
                f = open(TopicFile, 'w')
                # information ordering
                for sentence in sorted(Sentences, key=operator.itemgetter(1), reverse=True):
                    f.write(sentence[2]+'\n')
                    # print (sentence[0],sentence[1])
                f.close()
            except IOError:
                print ("Wrong path provided")

            print ('Finish Sentence Selection', TopicId)

    print ('Finish')