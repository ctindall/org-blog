import re
import string

class OrgSection:
    def __init__(self, type="regular_text"):
        self.type = type
        self.__lines = []

    def __str__(self):
        return "section type: " + self.type + "\n-----------------" + "\n".join(self.__lines)
    
    def set_type(self, type):
        self.type = type

    def get_type(self):
        return type

    def add_line(self, line):
        self.__lines.append(line)

    def add_lines(self, lines):
        self.__lines = self.__lines + lines
    
    def get_lines(self):
        return self.__lines

class OrgEntry:
    def __init__(self, title=""):
        self.__title = title
        self.__text = ""
        self.__tags = []
        self.__subentries = []
        self.__superentries = []
        self.__sections = []
        
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

    #tags
    def add_tag(self, tag):
        self.__tags.append(tag)
        
    def add_tags(self, tags):
        self.__tags = self.__tags + tags
        
    def get_tags(self):
        tags = self.__tags
        for se in self.get_superentries():
            tags = tags + se.get_tags()
            
        return tags

    #superentries
    def add_superentry(self, entry):
        self.__superentries.append(entry)

    def get_superentries(self):
        return self.__superentries
    
    #subentries
    def add_subentry(self, entry):
        self.__subentries.append(entry)
        entry.add_superentry(self)

    def get_subentries(self):
        return self.__subentries

    #sectionss
    def add_section(self, section):
        self.__sections.append(section)

    def get_sections(self):
        return self.__sections
    
    #text
    def add_line(self, line):
        self.__text = self.__text + "\n" + line

    def get_text(self):
        return self.__text
    
    def to_html(self):
        heading_tags = {
            1: "h1",
            2: "h2",
            3: "h3",
            4: "h4",
            5: "h5",
            6: "h6"
        }

        if self.get_level() > 6:
            heading_tag = "b"
        else:
            heading_tag = heading_tags[self.get_level()]
        
        html = "<div class='entry'>\n"

        if self.get_level() > 1: #don't include top-level titles as these are handled by the template
            html += "<" + heading_tag + ">" + self.get_title() + "</" + heading_tag + ">\n"
            
        html += "<p>" + self.get_text() + "\n</p>\n"
        for subentry in self.get_subentries():
            html += subentry.to_html()
        html += "</div>\n"
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
            
        return None, None
    
    def __parse_regular_line(self):
        global re
        if self.__peek():
            is_heading = re.search('^[\*]', self.__peek())
            is_option  = re.search('^(\s+)?\#\+', self.__peek())
            if not is_heading  and not is_option:
                return self.__peek()
            
        return None

    def __parse_tags(self):
        match = re.search('(\:.*\:)', self.__peek())
        if match:
        #if we're on a heading line and it has a tag portion...
        #split the tag portion on ":" characters and get rid of the empty tags
            parsed_tags = list(filter(lambda t: t != '', match.group().split(":")))
        else:
            parsed_tags = []
        return parsed_tags

    def __parse_regular_text_section(self):
        lines = []
        regular_line = self.__parse_regular_line()
        while regular_line:
            lines.append(regular_line)
            self.__eat()
            regular_line = self.__parse_regular_line()

        if lines != []:
            section = OrgSection()
            section.add_lines(lines)
        else:
            section = None
        
        return section

    def __parse_begin_src(self):
        match = re.search('^(\s)?(\#\+BEGIN_SRC)', self.__peek())
        if match:
            return True

        return None

    def __parse_end_src(self):
        match = re.search('^(\s)?(\#\+END_SRC)', self.__peek())
        if match:
            return True

        return None        
    
    def __parse_source_section(self):
        lines = []
        
        is_src = self.__parse_begin_src()
        if is_src:
            self.__eat()
            line = self.__parse_regular_line()
            while line:
                lines.append(line)
                self.__eat()
                line = self.__parse_regular_line()

            is_end = self.__parse_end_src()
            if not is_end:
                raise Exception("Was expecting END_SRC line and never found it (line " + self.get_line_number() + ")")
            self.__eat() #don't need the END_SRC line
            section = OrgSection(type="source")
            section.add_lines(lines)
            return section
        else:
            return None
    
    def __parse_section(self):
        section = self.__parse_regular_text_section() or self.__parse_source_section()
        return section
    
    def __parse_entry(self, level=1):
        my_title, my_level = self.__parse_heading_line(level=level);
        if my_title and my_level == level:
            #start a new entry
            entry = OrgEntry()

            entry.set_title(my_title)
            entry.set_level(my_level)
            entry.add_tags(self.__parse_tags())
            self.__stream.eat()             #we're done with the heading line

            #look for sections
            section = self.__parse_section()
            while section:
                entry.add_section(section)
                section = self.__parse_section()
            
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
