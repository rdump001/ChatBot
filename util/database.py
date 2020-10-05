import pyodbc 

class Database():
    
    def __init__(self):
        """ Initialsation of Database with connection properties. """
        
        server = 'amsectestdb.cvlivyahvos9.us-east-1.rds.amazonaws.com'
        database = 'AmsecDummyDB' 
        username = 'admin' 
        password = 'Quest1234$'
        driver = '/usr/local/lib/libmsodbcsql.17.dylib'
        self.conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        print(self.conn)
    
    def getSafeCount(self):
        """ 
        This method is used to get count of active safes which are transmitting data. 
        
        Returns :
            Number of Safes (int)
        """
       
        cursor = self.conn.cursor()

        sql = "Select count(safeid) safeid from AmsecDummyDB.dbo.Safes where isEnrolled = 1 and isDeleted = 0"
        with self.conn:
            cursor.execute(sql)
            row = cursor.fetchone()
        
        total_num_of_Safes = row.safeid
        
        return total_num_of_Safes

    def getSafePopulaiton(self):
        """
        Use this method to get which state has highest number of safes 
        
        Returns:
            It returns a dictonary with below two keys and their values. 

            stateName (str) : Name of state which has highest number of safes
            countofState (int) : Number of safes in the perticular state.

        """
        
        cursor = self.conn.cursor()
        
        sql = """Select ST.StateName stateName ,count(ST.StateName) countOfState
                    from        AmsecDummyDB.dbo.Safes S
                    inner join  AmsecDummyDB.dbo.Location L on L.LocationId = S.LocationId
                    inner join  AmsecDummyDB.dbo.State ST on ST.StateId =L.StateId
                    where       isEnrolled = 1 and isDeleted= 0 and CountryId = 1
                    group by    ST.StateName
                    order by    count(ST.StateName) desc"""
 
        with self.conn:
            cursor.execute(sql)
            row = cursor.fetchone()
        
        
        total_num_of_Safes = 0
        
        result = {
            "stateName" : row.stateName,
            "countOfState" : row.countOfState
        }
        # print(result.get("stateName"))
        return result

    def getSales(self):
        """
        Use this method to get highest revenue details. 

        Returns:
             It returns a dictonary with below three keys and their values. 
             
            "brCount" : BRCount,
            "lockCount" : LockCount,
            "count" : Count
        """
        cursor = self.conn.cursor()
        sql1 = """Select Top 1 S.SafeType safetype
                    from AmsecDummyDB.dbo.Safes S
                    where isEnrolled = 1 and isDeleted= 0
                    group by S.SafeType
                """

        sql2 = """
                    Select S.SafeId, Count(*) as BRCount 
                    into ##TempBRCount 
                    from AmsecDummyDB.dbo.Safes S
                    inner join AmsecDummyDB.dbo.SafeComponents SC on SC.SafeId = S.SafeId and SC.IsEnrolled = 1 and SC.IsEnabled = 1
                    where S.isEnrolled = 1 and isDeleted = 0 and S.SafeType = ? and ComponentTypeId = 1
                    group by S.SafeId
                    order by Count(*) desc
                """


        sql3 = """Select S.SafeId, Count(*) as LockCount 
                    into ##TempLockCount 
                    from AmsecDummyDB.dbo.Safes S
                    inner join AmsecDummyDB.dbo.SafeComponents SC on SC.SafeId = S.SafeId and SC.IsEnrolled = 1 and SC.IsEnabled = 1
                    where S.isEnrolled = 1 and isDeleted = 0 and S.SafeType = 0and ComponentTypeId = 3
                    group by S.SafeId
                    order by Count(*) desc
                """
        
        sql4 = """select L.SafeId, SUM(BRCount) as BRCount, SUM(LockCount) as LockCount 
                    into ##TempModels 
                    from ##TempLockCount L
                    left join ##TempBRCount BR on BR.SafeId = L.SafeId
                    group by L.SafeId 
                """
        sql5 = """select Top 1 BRCount, LockCount,count(*) as Count 
                    from ##TempModels
                    group by BRCount, LockCount
                    order by count(*) desc 
                """

        with self.conn:
            cursor.execute(sql1)
            _row1 = cursor.fetchone()
            cursor.execute(sql2,_row1.safetype)
            cursor.execute(sql3)
            cursor.execute(sql4)
            cursor.execute(sql5)
            _row2 = cursor.fetchone()

        safetype = ""
        
        print("Before")
        if(_row1.safetype == 0):
            print("Inside 0")
            safetype = "Cash Wizard"
        elif(_row1.safetype == 1):
            print("Inside 1")
            safetype = "Safe Wizard"
        print("After")

        result = {
            "brCount" : _row2.BRCount,
            "lockCount" : _row2.LockCount,
            "wizardType" : safetype
        }

        sql6 = """ drop table ##TempLockCount """
        sql7 = """ drop table ##TempModels"""
        sql8 = """ drop table ##TempBRCount """

        with self.conn:
            cursor.execute(sql6)
            cursor.execute(sql7)
            cursor.execute(sql8)
            

        return result
       

    
    def getSafeVersion(self):
        """
        Use this method to get how many safes are below latest verison. 

        Returns:
            It returns a dictonary with below two keys and their values. 

            latestVersion (str) : latest firmware version.
            safeBelowLatestVersion (int) : count of safes below latest version. 

        """

        cursor = self.conn.cursor()
        sql1 = """
                select substring(FirmwareVersion,4,14) version
                from (
                    select top 1 FirmwareVersion 
                    from AmsecDummyDB.dbo.FirmwareVersions 
                    where ComponentTypeId = 2 and FWType= 1 
                    order by FirmwareVersionId desc) a"""
        with self.conn:
            cursor.execute(sql1)
            _row1 = cursor.fetchone()
        
        sql2  = """
                Select Count(*) as LockCount 
                from AmsecDummyDB.dbo.Safes S
                inner join AmsecDummyDB.dbo.SafeComponents SC on SC.SafeId = S.SafeId and SC.IsEnrolled = 1 and SC.IsEnabled = 1
                where S.isEnrolled = 1 and isDeleted = 0 and ComponentTypeId = 2 and FWVersion < ?
                """
                    
        with self.conn:
            cursor.execute(sql2,_row1.version)
            _row2 = cursor.fetchone()
        
        result = {
            "latestVersion" :   _row1.version,
            "safeBelowLatestVersion" :   _row2.LockCount,
        }
        return result


    def getHighestRevenue(self,**kwargs):
        """
        This methid is to check which location has highest revenue for given date.
        
        Parameters:
            dateValue (YYYY-MM-DD) : date to be searched. 
                    If not given default value of "2019-04-07" will be taken

        Returns:
            It returns a dictonary with below two keys and their values. 

            safeSerialNo (str) : Serial Number of Safe.
            locationName (int) : Location of Safe.
            brTotal (str) : Revenue for today.
        """

        cursor = self.conn.cursor()
        dateValue = kwargs.get('dateValue', "2019-04-07")
        sql = """select Top 1 SafeSerialNo safeSerialNo ,LocationName locationName, convert(float,BRTotal) BrTotal from SafeEODSummary E
                    inner join Safes S on S.SafeId =E.SafeId
                    inner join Location L on L.LocationId = S.LocationId
                    where Convert(date,BusinessDayStart) = Convert(date,?) order by BRTotal desc"""

        
        with self.conn:
            cursor.execute(sql,dateValue)
            row = cursor.fetchone()
            #print(row)

    
        result = {
                    'safeSerialNo' : row.safeSerialNo,
                    'locationName' : row.locationName,
                    'brTotal' : row.BrTotal,
                }
        
        return result
    
    def getSafeSize(self,percentage):
        """
        This method is used to get the safe capacity. 

        Parameters : 
        percentage : capacity to check for. 

        Returns: 
            count of safes (int)
        """
        cursor = self.conn.cursor()
        sql = """select count(DISTINCT safeid) safeNumber from AmsecDummyDB.dbo.Aggr_CassettePercentageDetailsTbl where BillTotalPercent > ?"""
        with self.conn:
            cursor.execute(sql,percentage)
            row = cursor.fetchone()
            #print(row)
        result = row.safeNumber
        # print(result)
        return result

    def getCourierPickup(self,**kwargs):
        """ 
        This methid is to check how many courier pickup is missed for given date. 

        Parameters:
            dateValue (YYYY-MM-DD) : date to be searched. 
                    If not given default value of "2019-04-07" will be taken

        Returns:
            count of missed couries (int)

        """
        cursor = self.conn.cursor()
        dateValue = kwargs.get('dateValue', "2019-04-07")
        #dateValue = "2019-04-11"
        sql = """select count(*) coruierMiss from AmsecDummyDB.dbo.Aggr_MissedCourierPickupTbl 
                    where IsCourierPickupDay = 1 and IsCourierPickupDone = 0 and Convert(date,ScheduledCourierPickupDate) >=Convert(date, ?)"""

        
        with self.conn:
            cursor.execute(sql,dateValue)
            row = cursor.fetchone()
            #print(row)

    
        result = row.coruierMiss
        # print(result)
        return result

    def getIssueReported(self,**kwargs):
        """ 
        This methid is to check if safe has previous issue reported. 

        Parameters:
            safeSerialNo (str) : Serial Number of safe to be searched.


        Returns:
           Boolean value, Yes or No

        """

        cursor = self.conn.cursor()
        safeSerialNo = kwargs.get('safeSerialNo', "ABC0045271")
        #dateValue = "2019-04-11"
        sql = """select (CASE when count(*) > 0then 'YES' else 'NO' end) resultFromDB from AmsecDummyDB.dbo.Aggr_HealthMonitoring H
                    inner join AmsecDummyDB.dbo.Safes S on S.SafeId =H.SafeId
                    where EventSeverity = 2 and S.isEnrolled = 1 and isDeleted = 0and SafeSerialNo =  ?"""

        with self.conn:
            cursor.execute(sql,safeSerialNo)
            row = cursor.fetchone()
           
        result = row.resultFromDB
        # print(result)
        return result
        
    
    def getLastSync(self,**kwargs):
        """
        This method is to get last sync time of given safe serial number .
        If no argyment is spacified default ABC0045271 serial number will be taken

        Parameters:
                safeSerialNo (str) : Serial Number of safe to be searched.


        Returns:
           lastsync (str) : Last sync time of given safe.

        """
        cursor = self.conn.cursor()
        safeSerialNo = kwargs.get('safeSerialNo', "ABC0045271")
        #dateValue = "2019-04-11"
        sql = """select SafeLastSyncTime lastsync from AmsecDummyDB.dbo.Safes where SafeSerialNo =?"""

        with self.conn:
            cursor.execute(sql,safeSerialNo)
            row = cursor.fetchone()
           
        result = row.lastsync
        # print(result)
        return result
        

