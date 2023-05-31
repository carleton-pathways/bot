import datetime
import re

class DataParser: 

    def parse(self, term="", info="", **kwargs):
        
        if (term == ""):
            raise ValueError("Empty term passed")
        
        parse_n = ["subject", "course_description", "meeting_date", "days", "time", "instructor", 'year_in_program', 'level_restriction', 'degree_restriction', 
                   'major_restriction', 'program_restrictions', 'department_restriction', 'faculty_restriction']
        
        if (term not in parse_n):
            return [info]
        elif (term == "subject"):
            return self.parse_subject(info)
        elif (term == "course_description"):
            return [info] + self.parse_additional_credit_data(info) + self.parse_prereq_data(info)
        elif (term == "meeting_date"):
            return self.parse_meeting_times(info)
        elif (term == "days"):
            return self.parse_days(info)
        elif (term == "time"):
            return self.parse_time(info)
        elif (term == "instructor"):
            return self.parse_instructor(info)
        elif (term in ['year_in_program', 'level_restriction', 'degree_restriction', 'major_restriction', 'program_restrictions', 'department_restriction', 'faculty_restriction']):
            return self.parse_restriction_exclusion(info)
        
    # takes in a string of the course title and return a dictionary
    def parse_subject(self, section_information=""):

        # Split into list of words
        words = section_information.split()

        # If there is no list of words, meaning empty string was passed in
        if (not words):
            return [None, None, None, None, ]

        # If there is only one word, meaning either not the full string was passed in or the string had no
        if (len(words) <= 1):
            raise ValueError("No spaces in string passed")
        
        values = [None, None, None, None, ]

        for i in range(len(words)):
            if (i == 2 and len(words[i]) >= 2):
                values[2] = words[i][0]
                values[3] = words[i][1]
            elif (i == 2 and len(words[i]) == 1):
                values[2] = words[i][0]
                values[3] = None
            else:
                values[i] = words[i]

        return values

    # takes in a string which would represent a data containing an exlusion or inclusion
    # array contains the subject and whether it is excluded or included

    def parse_restriction_exclusion(self, dataString=""):
        if (dataString == ""):
            return [None]

        if ("{None}" in dataString):
            return [None]

        data = dataString.split("\n")
        result = []
        for x in data:

            bracketIndex = x.index("(")
            result.append([(x[:bracketIndex]).strip(), x[bracketIndex+1:-1]])

        return [result]

    def parse_instructor(self, instructor=""):
        if (instructor == ""):
            return [None, None]

        if ("{None}" in instructor):
            return [None, None]
        
        result = [None, None]

        bracketIndex = instructor.index("(")
        result[0] = ((instructor[:bracketIndex]).strip())
        result[1] = (instructor[bracketIndex+1:-1])

        return result

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
            "Dec":12,
            }
   
        # If there is no list of words, meaning empty string was passed in
        if (len(meeting_times)==0):
            return [None, None]
        
        meeting_dates= [None, None]

        #Extracts Months and days and year from the String
        start_year = meeting_times[8:12]
        start_month = meeting_times[0:3]
        start_day = meeting_times[4:6]

        end_month = meeting_times[-12:-9]
        end_day = meeting_times[-8:-6]
        end_year = meeting_times[-4:]

        #Chekcs if we acutally found the correct dates and months
        if(not((start_month in months_dict) and (start_day.isnumeric()) and (end_month in months_dict) and (end_day.isnumeric()) and (start_year.isnumeric()) and (end_year.isnumeric))):
            raise  ValueError("String does not follow the proper format")

        #Converts the Months string into its integer 
        start_month = months_dict[start_month]
        end_month = months_dict[end_month]

        #Sets the each start and end date to pydatetime
        start_date = datetime.datetime(int(start_year), start_month, int(start_day))
        end_date = datetime.datetime(int(end_year), end_month, int(end_day))
      
        #Puts the each date into the dictionary      
        meeting_dates[0]=start_date
        meeting_dates[1]=end_date

        return meeting_dates

    def parse_days(self,section_information=""):

        if(section_information==""):
            return [[]]
        
        days_dict = {
            "Mon":"Monday",
            "Tue":"Tuesday",
            "Wed":"Wednesday",
            "Thu":"Thursday",
            "Fri":"Friday",
            "Sat":"Saturday",
            "Sun":"Sunday",
        }

        days_arr = section_information.split(" ")

        #This is at most O(7) because only seven days in a week
        for x in range(len(days_arr)):
            if (not(days_arr[x] in days_dict)):
                raise ValueError(f"Could not find {days_arr[x]} inside days")
            
            days_arr[x]=days_dict[days_arr[x]]

        return [days_arr]

    def parse_time(self, time=""):
        
        # If there is no list of words, meaning empty string was passed in
        if (time == ""):
            return [None, None]
        
        times = time.split("-")

        # If there is an invalid amount of '-'s
        if (len(times) != 2):
            raise TypeError("Invalid format: requires one and only one '-'")
        
        times = [time.strip() for time in times]

        values = [None, None]
        values[0] = datetime.time(int(times[0].split(":")[0]), int(times[0].split(":")[1]), 0, 0)
        values[1] = datetime.time(int(times[1].split(":")[0]), int(times[1].split(":")[1]), 0, 0)
        
        return values
    
    def parse_additional_credit_data(self, section_information=""):

        if section_information=="":
            return [None, None]
        
        initial_index = section_information.find("Precludes additional credit for ")

        if initial_index == -1:
            return [None, None]
        
        initial_index+=len("Precludes additional credit for ")
        end_index = section_information.find(".", initial_index)
        prereqs = section_information[initial_index:end_index]

        pattern = re.compile(r"[A-Z]{4}\s\d{4}")
        
        course_codes = pattern.findall(prereqs)
      
        values = [None, None]
        values[0] = "Precludes additional credit for " + prereqs
        values[1] = course_codes

        return values
    
    def parse_prereq_data(self, section_information=""):

        if (section_information == ""):
            return [None, None]
        
        initial_index = section_information.find("Prerequisite(s): ")

        if initial_index == -1:
            return [None, None]
        
        initial_index+=len("Prerequisite(s): ")
        end_index = section_information.find(".", initial_index)

        prereqs = section_information[initial_index:end_index]

        pattern = re.compile(r"[A-Z]{4}\s\d{4}")

        course_codes = pattern.findall(prereqs)
        values = [None, None]
        values[0] = "Prerequisite(s): " + prereqs
        values[1] = course_codes
        
        return values
