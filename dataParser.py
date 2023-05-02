import datetime
class DataParser: 

    #takes in a string of the course title and return a dictionary
    def parse_section_information(self, section_information=""):
        
        # Split into list of words
        words = section_information.split()

        # If there is no list of words, meaning empty string was passed in
        if (not words):
            raise ValueError("Empty string passed")
        
        # If there is only one word, meaning either not the full string was passed in or the string had no
        if (len(words) <= 1):
            raise ValueError("No spaces in string passed")

        keys = ["faculty", "course_code", "section", "tut_id"]
        values = {}

        for i in range(len(words)):
            if (i == 2 and len(words[i]) >= 2):
                values["section"] = words[i][0]
                values["tut_id"] = words[i][1]
            elif (i == 2 and len(words[i]) == 1):
                values["section"] = words[i][0]
                values["tut_id"] = None
            else:
                values[keys[i]] = words[i]

        # If section or tut_id not set, set them to None
        if ("section" not in values):
            values["section"] = None 
        if ("tut_id" not in values):
            values["tut_id"] = None               
            
        return values
    
    def parse_meeting_times(self, meeting_times=""):
        months_dict = {
            "Jan": "1",
            "Feb": "2",
            "Mar": "3",
            "Apr": "4",
            "May": "5",
            "Jun": "6",
            "Jul": "7",
            "Aug": "8",
            "Sep": "9",
            "Oct": "10",
            "Nov": "11",
            "Dec":"12"
            
            }
   
        # If there is no list of words, meaning empty string was passed in
        if (len(meeting_times)==0):
            raise ValueError("Empty string passed")
        
        meeting_dates= {}
        year = meeting_times[8:13]


        start_month = months_dict[meeting_times[0:3]]
        start_day = meeting_times[4:6]
        
        end_month = months_dict[meeting_times[-6:-3]]
        end_day = meeting_times[-2:]


        if(not(start_month.isnumeric() & start_day.isnumeric() & end_month.isnumeric() & end_day.isnumeric())):
            raise  ValueError("String does not follow the proper format")

        start_date = datetime.datetime(int(year), int(start_month), int(start_day))
        end_date = datetime.datetime(int(year), int(end_month), int(end_day))
      
        meeting_dates["start_date"]=start_date
        meeting_dates["end_date"]=end_date

    
        return meeting_dates


