class DataParser:

    # takes in a string of the course title and return a dictionary
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

    # takes in a string which would represent a data containing an exlusion or inclusion
    # array contains the subject and whether it is excluded or included

    def parseRestrictionExclusion(self, dataString=""):
        if (dataString == ""):
            raise ValueError("Empty string passed")

        if ("{None}" in dataString):
            return None

        data = dataString.split("\n")
        result = []
        for x in data:

            bracketIndex = x.index("(")
            result.append([x[:bracketIndex], x[bracketIndex+1:-1]])

        return result

    def parseInstructor(self, instructor=""):
        if (instructor == ""):
            raise ValueError("Empty string passed")

        result = []
        if ("{None}" in instructor):
            return None

        bracketIndex = instructor.index("(")
        result.append(instructor[:bracketIndex])
        result.append(instructor[bracketIndex+1:-1])
        return result


p = DataParser()
print(p.parseRestrictionExclusion("""First Year Undergraduate (Exclude)
Second Year Undergraduate (Exclude)"""))
