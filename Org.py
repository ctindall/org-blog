import re

class OrgEntry:
    def __init__(self, title="")
        self.__title = title

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
        
    def add_line(self, line):
        self.__text = self.__text + "\n" + line
        
    def to_html(self):
        return "<pre>" + self.__text + "</pre>"

class LineStream:
    def __init__(self, string):
        self.__lines = string.splitlines()
        self.__position = 0

    def peek(self): #look at current line in stream
        return self.__lines[self.__position]

    def eat(self): #advance the tape to the next line
        self.__position = self.__position + 1
    
class OrgParser:

    def load(self, filename):
        self.loads(open(filename).read())

    def loads(self, string):
        self.__stream = LineStream(string)
        return self.__parse_entry_list()

    def __eat(self):
        self.__stream.eat()

    def __peek(self):
        return self.__stream.peek()
    

    def __parse_heading_line(self, greater_than=0):
        global re
        match = re.search('^(\*+)(\s)(.*)', self.__peek())
        level = len(match.group(1))
        title = match.group(3)

        if match and level > greater_than:
            return level, title
        else:
            return None

    def __parse_non_heading_line(self):
        global re
        match = re.search('', self.__peek())
        if match:
            return match.string
        else:
            return None

    def __parse_entry(self, greater_than=0):
        
        if self.__parse_heading_line():
            entry = OrgEntry()
            title, level = self.__parse_heading_line();
            entry.set_title(title)
            entry.set_level(level)
            text = ""
            self.__stream.eat()

            # look for any text directly under this heading
            while self.__parse_non_heading_line():
                text = text + "\n" + self.__peek();
                self.__eat()

            #look for any subheadings
            while self.__parse_entry(greater_than=level):

            return 
        else:
             return None       

        
    def __parse_entry_list(self):
        global re
        out = []
        
                
            
                
            
                
        for line in string.splitlines():
            match = re.search('^(\*+)(\s)(.*)', line)
            level = len(match.group(1))
            
            if match and level == 1: #this is a top-level heading line
                #we're done with the last entry
                entries.append(entry)

                #...and we start on the next one
                entry = OrgEntry(title=match.group(3))
            elif match and level > 1: #this is a sub-entry
                
            else # this is just another line
                entry.add_line(line)
                #TODO add tags and TODO states
                
