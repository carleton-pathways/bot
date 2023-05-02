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

        days_arr = section_information.split(" ")

        #This is at most O(7) because only seven days in a week
        for x in range(len(days_arr)):
            if (not(days_arr[x] in days_dict)):
                raise ValueError(f"Could not find {days_arr[x]} inside days")
            days_arr[x]=days_dict[days_arr[x]]

        return days_arr
