import datetime
import re

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
            "Jan": 1,
            "Feb": 2,
            "Mar": 3,
            "Apr": 4,
            "May": 5,
            "Jun": 6,
            "Jul": 7,
            "Aug": 8,
            "Sep": 9,
            "Oct": 10,
            "Nov": 11,
            "Dec":12
            
            }
   
        # If there is no list of words, meaning empty string was passed in
        if (len(meeting_times)==0):
            raise ValueError("Empty string passed")
        
        meeting_dates= {}

        #Extracts Months and days and year from the String
        start_year = meeting_times[8:12]
        start_month = meeting_times[0:3]
        start_day = meeting_times[4:6]
    


        end_month = meeting_times[-12:-9]
        end_day = meeting_times[-8:-6]
        end_year = meeting_times[-4:]

  

        #Chekcs if we acutally found the correct dates and months
        if(not((start_month in months_dict) & (start_day.isnumeric()) & (end_month in months_dict) & (end_day.isnumeric())& start_year.isnumeric() &end_year.isnumeric)):
            raise  ValueError("String does not follow the proper format")

        #Converts the Months string into its integer 
        start_month = months_dict[start_month]
        end_month = months_dict[end_month]

        #Sets the each start and end date to pydatetime
        start_date = datetime.datetime(int(start_year), start_month, int(start_day))
        end_date = datetime.datetime(int(end_year), end_month, int(end_day))
      
        #Puts the each date into the dictionary      
        meeting_dates["start_date"]=start_date
        meeting_dates["end_date"]=end_date

      
        return meeting_dates




    def parse_days(self,section_information=""):
        days_dict ={
            "Mon":"Monday",
            "Tue":"Tuesday",
            "Wed":"Wednesday",
            "Thu":"Thursday",
            "Fri":"Friday",
            "Sat":"Saturday",
            "Sun":"Sunday",
        }

        if(section_information==""):
            raise ValueError("No day information was found")

        days_arr = section_information.split(" ")

        #This is at most O(7) because only seven days in a week
        for x in range(len(days_arr)):
            if (not(days_arr[x] in days_dict)):
                raise ValueError(f"Could not find {days_arr[x]} inside days")
            
            days_arr[x]=days_dict[days_arr[x]]

        return days_arr

    def parse_time(self, time=""):
        
        # If there is no list of words, meaning empty string was passed in
        if (time == ""):
            raise ValueError("Empty string passed")
        
        times = time.split("-")

        # If there is an invalid amount of '-'s
        if (len(times) != 2):
            raise TypeError("Invalid format: requires one and only one '-'")
        
        times = [time.strip() for time in times]

        values = {}
        values["start_time"] = datetime.time(int(times[0].split(":")[0]), int(times[0].split(":")[1]), 0, 0)
        values["end_time"] = datetime.time(int(times[1].split(":")[0]), int(times[1].split(":")[1]), 0, 0)
        
        return values

    
    def parse_prereq_data(self, section_information=""):
        initial_index = section_information.find("Prerequisite(s):")
        if initial_index == -1:
            return None
        initial_index+=len("Prerequisite(s):")
        end_index = section_information.find(".", initial_index)
        prereqs = section_information[initial_index:end_index]
        pattern = re.compile(r"[A-Z]{4}\s\d{4}")
        course_codes = pattern.findall(section_information)
        values = {}
        values["courses"] = course_codes
        values["string"] = prereqs

        return values

