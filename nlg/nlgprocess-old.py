import spacy
import os
import re
from sklearn.externals import joblib 
from util.database import Database
from nlglib.realisation.simplenlg.realisation import Realiser
from nlglib.microplanning import *
from nlp.intermediate import intermediate

it = intermediate()
db = Database()
realise_en = Realiser(port=50007)
   
#####----- Intent alanysis model -----#######
intent_model_path = os.path.abspath('model/Amsec_Intent_models/model_nb.pkl')
# print(intent_model_path) 
model_nb = joblib.load(intent_model_path)

#####----- Named Entity Recognization -----#######
ner_model_path  = os.path.abspath('model/NER_Model')
# print(ner_model_path)
ner_model = spacy.load(ner_model_path)

#### ----- sub intent model ----###
'''
HighestRevenue
SafeSize
Sales
context
nlg
unknown questions
'''

class nlgprocess:
    
    def removeSplChars(self,query):
        query = re.sub(r'\?|\,|\.|\\|\'',' ',query)
        return query

    #####----- Intent Classification -----#######
    def getIntent(self,query):
        clean_query = self.removeSplChars(query)
        intent = model_nb.predict([clean_query.lower()])
        return intent
   
    #####----- Named Entity Recognization -----#######
    def getEntities(self,query):
        clean_query = self.removeSplChars(query)
        doc = ner_model(clean_query)
        ent_dict = {}
        for i in doc.ents:
            if(i.label_ not in ent_dict.keys()):
                ent_dict[i.label_] = [i.text]
            else:
                ent_dict[i.label_].append(i.text)    
        # print(ent_dict.keys())
        # print(ent_dict.get(i.label_))
        return ent_dict

    #context analysis methods

    #nlg sentences
 
    def nlg_main(self,query):
        # print("Query : ",query)
        
        intent = self.getIntent(query.lower())
        
        # print(intent)
       
        answer = None
       
        if(intent == "greeting" ):
            answer = it.createGreeting()
            # answer = "Hi I am AmsecBot, how can i help you.."
            return answer

        elif(intent == 'goodbye'):    
            #answer = "Good Bye....."
            answer = it.createGoodBye()
            return answer   

        elif(intent == "thankyou"):
            # answer = "thank you" 
            subject = NP('Thank You')
            inputForRealisation = Clause(subject=subject)
            answer = realise_en(inputForRealisation)
            return answer   

        elif((intent == "safe_count") or (intent == "SafeCount")):  
            
            
            
            total_safe_count = str(db.getSafeCount())
            #print(f"Total Safes that are syncing data are ",total_safe_count)
            #answer = "safe_count"+total_safe_count

            #2133 safes are transmitting data.
            subject = NP('safe')
            subject += Adjective(total_safe_count)
            verb = VP('transmit')
            object = NP('data')
            inputForRealisation = Clause(subject,verb,object,features={'TENSE': 'present', 'PROGRESSIVE': 'TRUE'})
            answer = realise_en(inputForRealisation)

            return answer

        
        elif((intent == "safe_population") or (intent == "SafeCount")):  
            highestNumberOfSafes = db.getSafePopulaiton()
            
            answer = "safe_population"

        elif((intent == "sales") or (intent == "Sales")):    
            answer = "sales"
            highestSold = db.getSales()
            print(f""" {highestSold.get("brCount")} Bill Reader, {highestSold.get("lockCount")} Lock, {highestSold.get("wizardType")} is the highest sold safe model  """)

        
        elif((intent == "safe_version") or (intent == "SafeVersion")):    
            answer = "safe_version"
            belowFirmwareCountVersion = db.getSafeVersion()
            print(f"""There are {belowFirmwareCountVersion.get("safeBelowLatestVersion")}  below latest verison {belowFirmwareCountVersion.get("latestVersion")} """)

            #2111 safes are below firmware version'1.09.01.10'

            subject = NP('safe')
            subject.premodifiers.append(belowFirmwareCountVersion.get("safeBelowLatestVersion"))
            #subject += Adjective(belowFirmwareCountVersion.get("safeBelowLatestVersion"))
            verb = VP('be')
            object = NP('below', 'firmware vesion') + NP(belowFirmwareCountVersion.get("latestVersion"))

        elif((intent == "safe_size") or (intent == "SafeSize")):    
            answer = "safe_size"    
            entites = self.getEntities(query)
            percentage = entites.get('PERCENETAGE')
            print(percentage)
            percentage = re.sub(r'\%','',percentage[0])
            safeAboveCapacity = db.getSafeSize(percentage)
            print(f"""There are {safeAboveCapacity} safes full above {percentage}%""")

        
        elif((intent == "location") or (intent == "HighestRevenue")):    
            answer = "location"
            dateToBeSearched = "2019-04-11"
            highestRevenue = db.getHighestRevenue(dateValue = dateToBeSearched)
            print(f"""Safe {highestRevenue.get("safeSerialNo")} in {highestRevenue.get('locationName')} has the highest revenue of ${highestRevenue.get("brTotal")} today""")
            
        
        elif((intent == "courier_missed") or (intent == "CourierMissed")):    
            answer = "courier_missed"
            dateToBeSearched = "2019-04-07"
            courierMissed = db.getCourierPickup(dateValue=dateToBeSearched)
            print(f"""{courierMissed} safes have missed courier pickup this week""")
        
        elif((intent == "safe_issue") or (intent == "SafeIssue" )):    
            answer = "safe_issue" 
            entites = self.getEntities(query)
            safeNumber = entites.get('SAFE-ID')[0]
            answer = it.createSafeIssue(safeNumber)

            
            #print(entites.keys())          
        
        elif((intent == "safe_last_Sync") or (intent == "SafeLastSync")):    
            answer = "safe_last_Sync" 
            entites = self.getEntities(query)
            safeNumber = entites.get('SAFE-ID')
            safeLastSunc = db.getLastSync(safeSerialNo = safeNumber[0])
            print(f"""Last sync happeded on safe {safeNumber} on {safeLastSunc}""")  
            #print(getEntities(query))
        

        return answer