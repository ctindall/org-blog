import re

class OrgEntry:
    def __init__(self, title=""):
        self.__title = title
        self.__text = ""
        self.__subentries = []

    #title
    def set_title(self, title):
        self.__title = title

    def get_title(self):
        return self.__title

    #level
    def set_level(self, level):
        self.__level = level

    def get_level(self):
        return self.__level

    #subentries
    def add_subentry(self, entry):
        self.__subentries.append(entry)

    def get_subentries(self):
        return self.__subentries

    #text
    def add_line(self, line):
        self.__text = self.__text + "\n" + line

    def get_text(self):
        return self.__text
    
    def to_html(self):
        html = "<pre>"
        for subentry in self.get_subentries():
            html += subentry.to_html()
        html += "</pre>"
        return html

class LineStream:
    def __init__(self, string):
        self.__lines = string.splitlines()
        self.__position = 0

    def peek(self): #look at current line in stream
        if self.__position < len(self.__lines):
            return self.__lines[self.__position]
        else:
            return None

    def eat(self): #advance the tape to the next line
        self.__position = self.__position + 1

    def get_line_number(self):
        return self.__position + 1
    
class OrgParser:

    def load(self, filename):
        return self.loads(open(filename).read())

    def loads(self, string):
        self.__stream = LineStream(string)
        return self.__parse_entry_list()

    def __eat(self):
        self.__stream.eat()

    def __peek(self):
        return self.__stream.peek()
    

    def __parse_heading_line(self, level=1):
        global re
        if self.__peek():
            match = re.search('^(\*+)(\s)(.*)', self.__peek())
            parsed_level = len(match.group(1))
            title = match.group(3)
            
            if match and parsed_level == level:
                return title, level
        else:
            print("peek is empty at line " + str(self.__stream.get_line_number()))
        return None, None
    
    def __parse_regular_line(self):
        global re
        print ("looking for regular line at line " + str(self.__stream.get_line_number()))
        if self.__peek():
            match = re.search('^[^\*]', self.__peek())
            if match:
                return match.string
        return None
    
    def __parse_entry(self, level=1):
        my_title, my_level = self.__parse_heading_line(level=level);
        if my_title and my_level == level:
            #start a new entry
            entry = OrgEntry()

            entry.set_title(my_title)
            entry.set_level(my_level)

            #we're done with the heading line
            self.__stream.eat()

            # look for any text directly under this heading
            regular_line = self.__parse_regular_line()
            while regular_line:
                entry.add_line(regular_line)
                self.__eat()
                regular_line = self.__parse_regular_line()

            #recursively look for any subheadings of the next higher level
            subentry = self.__parse_entry(level=my_level + 1)
            while subentry:
                entry.add_subentry(subentry)
                subentry = self.__parse_entry(level=my_level + 1)

            return entry
        else:
            return None    

        
    def __parse_entry_list(self):
        global re
        entries = []

        entry = self.__parse_entry()
        while entry:
            entries.append(entry)
            entry = self.__parse_entry()

        return entries
