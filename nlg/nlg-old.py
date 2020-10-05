from util.database import Database
db = Database()
class nlgprocess:
    #intent alanysis model
    
    # classified_intent = "Heloo"
    # answer = ""

    # if(classified_intent == "greeting"):
    #       #context analysis methods
    #       #getting data from DB
    #       #nlg sentences
    #     answer = ""
    # elif(classified_intent == "thankyou"):
    #     answer = ""
    # elif(classified_intent == "goodbye"):
    #     answer=""
    # elif(classified_intent == "howmany"):
    #     answer=""
    # elif(classified_intent == "dpds" or classified_intent =="what"):
    #     answer = "" 
        
    #context analysis methods

    #nlg sentences

    #return responses
    
    
    
    def nlg_main(self,query):
        
        #What is the count of safes which are transmitting data?
        total_safe_count = str(db.getSafeCount())
        print(f"Total Safes that are syncing data are ",total_safe_count)
        
        #Which state in North America has the highest population of Safes, and how much?
        highestNumberOfSafes = db.getSafePopulaiton()
        print(f"""{highestNumberOfSafes.get("stateName")} has the highest safe population of {highestNumberOfSafes.get("countOfState")} safes""")
        
        #Which is the highest sold safe model ?
        #Method to be implemented.

        #How many Safes are there with firmware below latest version?
        belowFirmwareCountVersion = db.getSafeVersion()
        print(f"""There are {belowFirmwareCountVersion.get("safeBelowLatestVersion")}  below latest verison {belowFirmwareCountVersion.get("latestVersion")} """)

        #Which location has the highest revenue today?
        dateToBeSearched = "2019-04-11"
        highestRevenue = db.getHighestRevenue(dateValue = dateToBeSearched)
        print(f"""Safe {highestRevenue.get("safeSerialNo")} in {highestRevenue.get('locationName')} has the highest revenue of ${highestRevenue.get("brTotal")} today""")
        
        #How many safes are above 80% full?
        percentage = 80
        safeAboveCapacity = db.getSafeSize(percentage)
        print(f"""There are {safeAboveCapacity} full above {percentage}%""")

        #Is there any courier pickup missed this week?
        
        courierMissed = db.getCourierPickup(dateValue=dateToBeSearched)
        print(f"""{courierMissed} safes have missed courier pickup this week""")

        #is there any issue reported on safe ABC0045271 before?
        safeNumber = "ABC0045271"
        issueReported = db.getIssueReported(safeSerialNo = safeNumber)
        print(f"""{issueReported}, There are issue reported on {safeNumber}.""")

        safeLastSunc = db.getLastSync(safeSerialNo = safeNumber)
        print(f"""Last sync happeded on safe {safeNumber} on {safeLastSunc}""")
        
        return total_safe_count

