import letterstats
import sys
from peaklistener import PeakListener, RATE
from time import sleep
import time
import speech
prev_phrase = ''

if __name__ == "__main__":
    # Handle a specific set of heard phrases with a callback.
    def response(phrase, listener):
        print("You said %s" % phrase)
        if phrase == 'turn off':
            #print prev_phrase
            listener.stoplistening()
        #prev_phrase = phrase    
        """
        http://www.renuncln.com/blog/2012/05/28/python-speech-recognition-and-tts-part-i-pyspeech/
        
        spoken = speech.input("Processing input", ['ABC', 'AWL', 'TJC2', 'turn off'])
        print "I think you said '%s'." % spoken
        if spoken == "turn off":
            listener.stoplistening()"""
        #print "Processing input"
        #best_match = letterstats.get_best_match(samples, RATE, stats)
        #print "I think you said '%s'." % best_match
    listener = speech.listenfor(
    ['Stefan Kopieczek', 'EA','MKA','DLA','JJA','SA5','BSA','EA2','DA2','LA','FMA','JPA','MA','RMB','KAB','SHB','JPB','TDMB','GHB','CB2','SB3','GB','MJB2','JSB','PAB','DB','SHB2','JEB','DRB','CAB','NDB','SBL','AMC','OJC','TJC2','GJC','DC4','IMC','BAC','CC','AJC2','EC2','NC2','HNC','PD2','SGD','RKD','MJD','CRD','JAD','RND','CNE','ME','VCE','TME','ISF','JAF','GJF','MJF','JAG2','JHJG','RG3','PCG','BCG','JKG2','MSG','KG1','SG6','AG','DG','FJH','SJH','IRH','EPH','GWH','REH','JPH','SEH','MRH','KH2','CH','AJH','ENH','SH','DCH','ASCH','NH','JH3','RH2','SI1','AJ','CLJ','TDBJ','SK','AK','HK','DL','SL5','JL','AL','JJL','SL2','CJL','DJLY','SJL','MDL','NL','CDL','JAL','ML','DHM','REM','CM','CMM','RM3','RGM','JMcL','EMcS','EM','MLM','BMM','MSM','MAM','AM','CJM','MM3','KM3','MGN','BEN','WAN','ATN','AO2','PPON','SO','KOR','SO2','WRO','MEO','SP3','DCP','JDP','CP','GAP','CJP','ACP','LP1','MRR','BR1','LAR','RER','DR','DGR','KMR','JR','AJR','LR2','MWR','OR','JTR','BJR','CAS2','MS1','NJS','PDS','TLS','GMS','SJS','AFS','MNS','TJCS','SS','CNS','NT1','MT','PT','GRT','MBT','CJT','ELNT','CTD','RU','RBW','CW','CW2','PW','DJW','TPW','MIRW','TSW1','DW','JSW2','CEW', "Ernesto Abad", "Malcolm Ackland", "Doris Adade", "Josie Adkin", "Suliman Ahmad", "Bilen Ahmet", "Ed Allberry", "Duncan Archer", "Laura Arutjunane", "Faisal Ashraf", "Jamie Ashton", "Milly Ashwell", "Robyn Ballin", "Kelly Barker", "Simon Bate", "John Batty", "Tim Bellis", "Gill Belshaw", "Cory Benfield", "Steve Biggs", "Ginney Birch", "Mike Bird", "Jo Brittain", "Peter Brittain", "Derek Brooker", "Sam Broster", "James Broughton", "Daniel Buller", "Claire Butcher", "Nick Butcher", "Sean Butler-Lee", "Andy Caldwell", "Oliver Carter", "Thomas Chambers", "Guy Chapman", "Derek Cheong", "Ian Clarkson", "Becca Condon", "Carol Copland", "Andrew Craigie", "Esther Craythorn", "Nick Critchell", "Helen Curtis", "Pam Daniels", "Sam Davies", "Rob Day", "Mike Dell", "Chris Dickens", "Jian Dong", "Rob Dover", "Chris Elford", "Mike Evans", "Vicky Evans", "Tim Eyre", "Ian Ferguson", "James Fletcher", "Gary Fordham", "Mike Forster", "James Giblin", "Julia Gilbert", "Rolandas Glotnis", "Peter Goodhew", "Beth Gorman", "Jalaj Gothi", "Matt Graham", "Kelly Gray", "Susan Greenwood", "Andy Guest", "Dawn Guest", "Fiona Hall", "Stephen Halstead", "Ian Hanahoe", "Ed Harrison", "Gemma Harrison", "Rob Hart", "Joshua Haslam", "Sandra Haste", "Mark Hazell", "Kellie Henderson", "Clare Hill", "Alex Hockey", "Ed Holland", "Steve Hoole", "David Hotham", "Andrew Huang", "Nigel Hubbard", "Josie Huddleston", "Rachel Hummerston", "Simon Inman", "Alison Jackson", "Chris Jones", "Tim Joseph", "Steven Kennedy", "Andy Kilpatrick", "Hemal Kothari", "Dave Langridge", "Sue Layzell", "John Lazar", "Alistair Lee", "James Lee", "Simon Lee", "Carolyn Leonard", "Daniel Liu Yin", "Sarah Lofting", "Matt Lowe", "Ned Lowe", "Chris Lund", "Jenny Lynch", "Mark Lynch", "Diarmid Mackenzie", "Rich Maclannan", "Chris Mairs", "Christine Martin", "Rachel Martin", "Robert Mathews", "Justine McLennan", "Elaine McSherry", "Eleanor Merry", "Mia Miles", "Ben Miller", "Malcolm Milne", "Mark Mitchell", "Alex Moore", "Caroline Moss", "Meyrem Muhdi", "Katherine Murphy", "Martin Nelson", "Ben Noakes", "Will Normand", "Andrew Nubbert", "Anthony Obi", "Peter O'Neill", "Steve Orbell", "Kara O'Riordan", "Sue Osman", "Will Ouldridge", "Mark Overton", "Sandra Page", "David Parker", "Jamie Parsons", "Clive Partridge", "Gill Paschalis", "Chris Paterson", "Adam Pilcher", "Lewis Proudlove", "Mike Ramage", "Ben Ramsden", "Lisa Raven", "Ruth Reed", "Dave Reekie", "David Reid", "Kelly Reynolds", "Jane Richards", "Andrew Robinson", "Lance Robson", "Murray Rogers", "Olivia Rogers", "Jon Rowland", "Ben Russell", "Claire Sargent", "Michael Siuda", "Nina Skillett", "Paul D Smith", "Tracey Smith", "Graham Sparrey", "Sam Spicer", "Austin Spreadbury", "Mark Stewart", "Terry Streeter", "Salih Suavi", "Chris Swindle", "Neil Tarrant", "Martin Taylor", "Paul Theobald", "Geoff Thomas", "Mark Thomas", "Chris Tozer", "Emma Tozer", "Colin Tregenza Dancer", "Richard Underwood", "Robert Wallace", "Caroline Ward", "Caroline Ward (2)", "Peter Waters", "Dave Watts", "Thomas Whiteway", "Matt Williams", "Toni Williams", "Doreen Willis", "Jesse Wong", "Colin Wright", 'turn off'],
    response)
    try:
        while listener.islistening():
            time.sleep(1)
    except KeyboardInterrupt:
        answer = raw_input("OK, just type your answer: ")

        
