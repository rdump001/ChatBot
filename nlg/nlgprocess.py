import os
import re
import sys
import spacy
import logging
from sklearn.externals import joblib 
from vo.context import contextPojo
from nlp.intermediate import intermediate

# Logging Module

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)

# Intent alanysis model 
intent_model_path = os.path.abspath('model/Amsec_Intent_models/model_nb_3.pkl')
log.debug("From Logger : %(intent_model_path)s ")
print(intent_model_path) 
model_nb = joblib.load(intent_model_path)

# Named Entity Recognization Model
ner_model_path  = os.path.abspath('model/NER_Model')
print(ner_model_path)
ner_model = spacy.load(ner_model_path)

#### ----- sub intent model ----###
###### Threshold setting #######


context = contextPojo()
it = intermediate()

class nlgprocess:

    answer = None
    
    #Method for Removing Special Charactors
    def removeSplChars(self,query):
        query = re.sub(r'\?|\,|\.|\\|\'',' ',query)
        return query

    # Method for Intent Classification 
    def queryIntent(self,query):
        clean_query = self.removeSplChars(query)
        intent = model_nb.predict([clean_query.lower()])
        return intent
   
    # Method for Named Entity Recognization 
    def getEntities(self,query):
        
        clean_query = self.removeSplChars(query)
        doc = ner_model(clean_query)
        ent_dict = {}
        for i in doc.ents:
            if(i.label_ not in ent_dict.keys()):
                ent_dict[i.label_] = [i.text]
            else:
                ent_dict[i.label_].append(i.text)    

        #entites = self.getEntities(query) 
        # if('SAFE-ID' in ent_dict.keys()):
        #     context.setsafe_id(ent_dict.get('SAFE-ID')[0])
        #     context.setpercentage(0)   
            
        # elif(context.getsafe_id() != 0):
        #     context.getsafe_id() 
            

        # if('PERCENETAGE' in ent_dict.keys()):
        #         context.setpercentage(ent_dict.get('PERCENETAGE')[0])  
        #         context.setsafe_id(0)
        #         print(ent_dict.get('PERCENETAGE')[0]) 
        #         print(context.showall())     

        return ent_dict

    #Method for Getting SafeId and setting context for safeid
    def methodSafeID(self, query): 
        
        entites = self.getEntities(query) 
        if('SAFE-ID' in entites.keys()):
            context.setsafeId(entites.get('SAFE-ID')[0])
            context.setpercentage(0)   
            safeId = context.getsafeId()
            print(context.showall())
        elif(context.getsafeId() != 0):
            safeId = context.getsafeId()

        return safeId
 
    #Main NLG Method
    def nlg_main(self,query):    
        intent = self.queryIntent(query.lower())
        print(intent)
       
        if(intent == "greeting" ):
            context.setIntent("greeting")
            answer = it.createGreeting()
            print(context.showall()) 

        elif(intent == 'goodbye'):   
            context.setIntent("goodbye") 
            answer = it.createGoodBye()
            print(context.showall()) 
        
        elif(intent == "thankyou"):
            context.setIntent("thankyou")
            answer = it.createThankYou()
            print(context.showall()) 

        elif(intent == "safe_count"):  
            context.setIntent("safe_count")
            answer = it.createSafeCount()
            print(context.showall()) 
        
        elif(intent == "safe_population"): 
            context.setIntent("safe_population") 
            answer = it.creatSafePopulaiton()
            print(answer)
            print(context.showall()) 
        
        elif(intent == "sales"): 
            context.setIntent("sales")    
            answer = it.createSales()
            print(answer)
            # answer = "sales"
            print(context.showall()) 
        
        elif((intent == "safe_version")):    
            context.setIntent("safe_version") 
            answer = it.createFirmwareVersion()
            print(answer)
            print(context.showall())  
        
        elif((intent == "location") or (intent == "HighestRevenue")):   
            context.setIntent("location")  
            answer  = it.createHighestRevenue()

        elif((intent == "safe_size")):  
            context.setIntent("safe_size")   
            # answer = "safe_size" 
            self.getEntities(query)  
            # print(context.getpercentage())   
            entites = self.getEntities(query)           
            
            if('PERCENETAGE' in entites.keys()):
                context.setpercentage(entites.get('PERCENETAGE')[0])
                context.setsafeId(0) 
                print(context.getpercentage())
                answer = it.createSafeSize(context.getpercentage())
        
        elif((intent == "courier_missed") or (intent == "CourierMissed")):   
            context.setIntent("courier_missed")   
            answer = it.createCourierMissed()
        
        elif((intent == "safe_issue") or (intent == "SafeIssue" )):
            context.setIntent("safe_issue") 
            safeID = self.methodSafeID(query)
            answer = it.createSafeIssue(safeID)
  
        elif((intent == "safe_last_Sync") or (intent == "SafeLastSync")): 
            context.setIntent("safe_last_Sync")  
            safeID = self.methodSafeID(query)
            answer = it.createSafeLastSync(safeID)
        
        elif((intent == "what")):
            if(context.getIntent()!= 0):
                if((context.getIntent() == "safe_issue") or (context.getIntent() == "SafeIssue" )):
                    answer =   self.method_safe_issue(query)
                elif((context.getIntent() == "safe_last_Sync") or (context.getIntent() == "safe_last_Sync" )):
                    answer = self.method_safe_last_sync(query)
                else :
                    answer = "Sorry I Could not understand, can you be more specific"    
            else:
                answer =  "Sorry I Could not understand, can you be more specific"

        return answer