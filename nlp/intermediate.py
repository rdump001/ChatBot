import re
from util.database import Database
from nlglib.features import TENSE, ASPECT, NUMBER
from nlglib.realisation.simplenlg.realisation import Realiser
from nlglib.microplanning import *
from nlglib.microplanning.struct import *

db = Database()
realise_en = Realiser(port=50007)


class intermediate():

    def __init__(self):
        return None
    
    def createGreeting(self):
        """ Creates Greeting Sentences """
        inputForRealisation = Clause("Hi I am AmsecBot, How can i help you..")
        answer = realise_en(inputForRealisation)
        return answer

    def createGoodBye(self):
        """ Creates Good Bye Sentences """
        subject = NP('Goob Bye...')
        inputForRealisation = Clause(subject=subject)
        answer = realise_en(inputForRealisation)
        return answer
    
    def createThankYou(self):
        """ Creates Thank You Sentences """
        subject = NP('Thank You')
        inputForRealisation = Clause(subject=subject)
        answer = realise_en(inputForRealisation)
        return answer

    def createSafeCount(self):
        """ Creates Transmiiting Data safe number Sentence """
        total_safe_count = str(db.getSafeCount())
        #print(f"Total Safes that are syncing data are ",total_safe_count)
        #answer = "safe_count"+total_safe_count

        #2133 safes are transmitting data.
        subject = NP('safe',features = {NUMBER.plural})
        subject += Adjective(total_safe_count)
        
        verb = VP('transmit')
        object = NP('data')
        inputForRealisation = Clause(subject,verb,object,features={'TENSE': 'present', 'PROGRESSIVE': 'TRUE'})
        answer = realise_en(inputForRealisation)
        return answer

    def creatSafePopulaiton(self):
        #State-8 has the highest safe population of 529 safes


        highestNumberOfSafes = db.getSafePopulaiton()
        # print(f"""{highestNumberOfSafes.get("stateName")} has the highest safe population of {highestNumberOfSafes.get("countOfState")} safes""")

        subjectNNPS = NNP(highestNumberOfSafes.get("stateName"))
        subject = NP(subjectNNPS)
        subject.premodifiers.append("the")
       
        #verb = VP('be', features = {ASPECT.perfect})
        verb = VerbPhrase(Verb('has'),features = {TENSE.PRESENT},indirect_object= NP("highest safe population of"))
        #verb = verb.indirect_object(verb,"highest safe population of")
        
        #object1 =   NP("highest safe population of")
        object1 = PP(highestNumberOfSafes.get('countOfState'), NP("safes"))
        # object2 = NP(highestNumberOfSafes.get('countOfState'))
        # object3 = NP("safes")
        # object = object1 + object2 + object3

        # c.complements += PP('in', NP('the', 'park'))
        inputForRealisation = Clause(subject,verb,object1)
        
        # inputForRealisation = Clause(subject = subject ,predicate= verb, objekt= object1)

        # inputForRealisation.complements+= PP(highestNumberOfSafes.get('countOfState'), NP("safes"))
        answer = realise_en(inputForRealisation)
        
        return answer

    def createSales(self):
        highestSold = db.getSales()
        # print(f""" {highestSold.get("brCount")} Bill Reader, {highestSold.get("lockCount")} Lock, {highestSold.get("wizardType")} is the highest sold safe model  """)

        subject1 = NP(highestSold.get("brCount")) 
        subject1.premodifiers.append("Safes with")
        subject1.postmodifiers.append("Bill Reader")
        
        subject2 = NP(highestSold.get("lockCount"))
        subject2.postmodifiers.append("Locks")

        subject3 = NP(highestSold.get("wizardType"))

        subject = CC(subject1,subject2,subject3,features={NUMBER.singular })


        verb = VP('is',features= {TENSE.present})

        object = NP("the highest sold safe model")


        inputForRealisation = Clause(subject,verb,object)
        answer =  realise_en(inputForRealisation)
        return answer

    def createFirmwareVersion(self):
       
        belowFirmwareCountVersion = db.getSafeVersion()
        subject = NP("There",features = {NUMBER.plural})
        verb = VerbPhrase(Verb('be'),features = {TENSE.PRESENT},indirect_object= NP(belowFirmwareCountVersion.get("safeBelowLatestVersion")))

        object = NP("latest version")
        object.premodifiers.append("safes below")
        object.postmodifiers.append(belowFirmwareCountVersion.get("latestVersion"))

        inputForRealisation = Clause(subject,verb,object)
        answer =  realise_en(inputForRealisation)
        
        return answer
    
    def createHighestRevenue(self):
        
        dateToBeSearched = "2019-04-11"
        highestRevenue = db.getHighestRevenue(dateValue = dateToBeSearched)
        # print(f"""Safe {highestRevenue.get("safeSerialNo")} in {highestRevenue.get('locationName')} has the highest revenue of ${highestRevenue.get("brTotal")} today""")


        subject = NP(highestRevenue.get("safeSerialNo"))
        subject.premodifiers.append("Safe")
        subject.complements.append("in")
        subject.postmodifiers.append(highestRevenue.get('locationName'))

        verb = VerbPhrase(Verb('has'),features={TENSE.present},indirect_object= NP("the highest revenue of"))

        object = NP(highestRevenue.get("brTotal"))
        object.postmodifiers.append("today")

        inputForRealisation = Clause(subject,verb,object)
        answer =  realise_en(inputForRealisation)

        return answer

    def createSafeSize(self,percentage):
        
        safeAboveCapacity = db.getSafeSize(int(re.sub(r'\%','',percentage)))

        subject = NP("safe",features={NUMBER.plural})
        subject.premodifiers.append(safeAboveCapacity)
        verb = VP('be')

        object = NP(" full above")
        # object.premodifiers.append(safeAboveCapacity)
        object.postmodifiers.append(percentage)


        inputForRealisation = Clause(subject,verb,object)
        answer =  realise_en(inputForRealisation)
        return answer

    def createCourierMissed(self):

        dateToBeSearched = "2019-04-07"
        courierMissed = db.getCourierPickup(dateValue=dateToBeSearched)
        print(f"""{courierMissed} safes have missed courier pickup this week""")
        
        subject = NP("safe",features={NUMBER.plural})
        subject.premodifiers.append(courierMissed)
        verb = VP('miss')
        
        object = NP("courier pickup this week")

        inputForRealisation = Clause(subject,verb,object,features={TENSE.PAST})
        answer = realise_en(inputForRealisation)

        return answer

    def createSafeIssue(self,safeNumber):
        # safeSerialNo = 'ABC0045271'
        
        issueReported = db.getIssueReported(safeSerialNo = safeNumber)
        # print(f"""{issueReported}, There are issue reported on {safeNumber}.""")  
        
        """
        * PreModifier      (eg, "reluctantly")
        * Verb             (eg, "gave")
        * IndirectObject   (eg, "Mary")
        * Object           (eg, "an apple")
        * PostModifier     (eg, "before school")

        """
        issueReported = 'NO'

        subject = None
        # subject = NP("There")
        if(issueReported == 'YES'):
            subject = NP("There",features={NUMBER.plural})
        elif(issueReported == 'NO'):
            subject= NP("There",features={NUMBER.singular})
            
        verb = None
        if(issueReported == 'YES'):
            verb = VerbPhrase(Verb('be'),features={TENSE.present},indirect_object=NP("issues"))
        elif(issueReported == 'NO'):
            verb = VerbPhrase(Verb('be'),features={TENSE.present},indirect_object=NP("no issue"))

        #verb.postmodifiers.append("reported")
        
        object = NP(safeNumber)
        object.premodifiers.append("reported on")

        
        inputForRealisation = Clause(subject,verb,object)
        answer = realise_en(inputForRealisation)

        return answer



    def createSafeLastSync(self,safeId):

        safeLastSync = db.getLastSync(safeSerialNo = safeId)
        # print(f"""Last sync happeded on safe {safeId} on {safeLastSunc}""")  

        #Safe aBC was last synced on time
        # subject = NP("Last Sync")

        # verb = VerbPhrase(Verb('happen'),features={TENSE.past},indirect_object=NP(safeId))
        # #verb.complements.append("on")

        # object = NP(safeLastSync)
        # object.premodifiers.append("on")


        subject  = NP(safeId)
        subject.premodifiers.append("Safe")

        verb = VP("sync",features={TENSE.past})
        verb.premodifiers.append("last")
        verb.complements.append("on")

        object = NP(safeLastSync)

        inputForRealisation = Clause(subject,verb,object)
        answer = realise_en(inputForRealisation)

        return answer
