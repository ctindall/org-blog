import re
import string

class OrgParseError(Exception):
    pass

class OrgSection:
    def __init__(self, type="regular_text"):
        self.__type = type
        self.__lines = []

    def __str__(self):
        return "section type: " + self.__type + "\n-----------------" + "\n".join(self.__lines)
    
    def set_type(self, type):
        self.__type = type

    def get_type(self):
        return self.__type

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
        self.__todo_status = ""
        
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

    #TODO status
    def set_todo_status(self, status):
        self.__todo_status = status

    def get_todo_status(self):
        return self.__todo_status
    
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

    #sections
    def add_section(self, section):
        self.__sections.append(section)

    def get_sections(self):
        return self.__sections
    
    #text
    def add_line(self, line):
        self.__text = self.__text + "\n" + line

    def get_text(self):
        return self.__text

    def __inline_quotify(self, line):
        regex = '\=(.*?)\='

        match = re.search(regex, line)
        while match:
            text = match.group(1)
            html = "<code>" + text + "</code>"
            line = line.replace(match.group(), html)
            match = re.search(regex, line)

        return line

    def __boldify(self, line):
        regex = '\*(.*?)\*'

        match = re.search(regex, line)
        while match:
            text = match.group(1)
            html = "<b>" + text + "</b>"
            line = line.replace(match.group(), html)
            match = re.search(regex, line)

        return line
    
    def __linkify(self, line):
        #return the same line, but with org-mode link syntax turned into HTML links
        with_link_text_regex = '(\[\[)(https|http|ftps|ftp)(://)(.*?)(\]\[)(.*?)(\]\])'
        without_link_text_regex = '(\[\[)(https|http|ftps|ftp)(://)(.*?)(\]\[)(.*?)'
        
        match_with_link_text = re.search(with_link_text_regex, line)
        match_without_link_text = re.search(without_link_text_regex, line)
        while match_with_link_text or match_without_link_text:
            if match_with_link_text:
                match = match_with_link_text
            else:
                match = match_without_link_text
            
            proto = match.group(2)
            url = match.group(4)
            if match.group(6):
                link_text = match.group(6)
            else:
                link_text = url
                                    
            link = "<a href='" + proto + "://" + url + "'>" + link_text + "</a>"
            line = line.replace(match.group(), link)
            match_with_link_text = re.search(with_link_text_regex, line)
            match_without_link_text = re.search(without_link_text_regex, line)


        return line
    
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

        for section in self.get_sections():
            html += "<div class='section-" + section.get_type() + "'>\n"
            for line in section.get_lines():
                line = self.__inline_quotify(line)
                line = self.__boldify(line)
#                line = self.__italicize(line)
                line = self.__linkify(line)
                    
                html += line + "\n"
            html += "</div>"
            
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
            return False

    def finished(self):
        if self.__position >= len(self.__lines):
            return True
        else:
            return False

        
    def eat(self): #advance the tape to the next line
        self.__position = self.__position + 1

    def get_line_number(self):
        return self.__position + 1
    
class OrgParser:

    def __init__(self):
        self.__settings = {}
        self.set_setting("TODO", "TODO | DONE") #default TODO states

    def get_valid_todo_statuses(self):
        words = self.get_setting("TODO").split()
        return [word for word in words if word != "|"]
        
    def get_setting(self, setting_name):
        return self.__settings[setting_name]

    def get_all_settings(self):
        return self.__settings
    
    def set_setting(self, setting_name, setting_value):
        self.__settings[setting_name] = setting_value

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
        if self.__peek():
            line_without_tags = re.sub('(\s+)?(\:.*\:)(\s+)?$', "", self.__peek())
            match = re.search('^(\*+)(\s)([A-Z]+)?(\s+)?(.*)(\:.*\:)?', line_without_tags)
            if not match:
                raise OrgParseError("trouble parsing heading at line " + str(self.__stream.get_line_number()))

            todo_status = match.group(3)
            parsed_level = len(match.group(1))
            title = match.group(5)

            if todo_status not in self.get_valid_todo_statuses():
                # If the parsed TODO status is not actually a valid
                # status, then we were mistaken and the todo_status is
                # really part of the title. Add it back, along with
                # the white space that we thought separated them.
                title = todo_status + match.group(4) + title
                todo_status = ""

            if match and parsed_level == level:
                return title, level, todo_status
            
        return None, None, None
    
    def __parse_regular_line(self):
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
            return section
        else:
            return None
        
    def __parse_source_section(self):
        lines = []
        
        is_src = self.__parse_begin_src()
        if is_src:
            self.__eat() #down with the BEGIN_SRC line
            
            while not self.__parse_end_src():
                lines.append(self.__peek())
                self.__eat()

            self.__eat() #done with the END_SRC line

            #we're done, create a section and return it
            section = OrgSection(type="source")
            section.add_lines(lines)
            return section
        else:
            return None
    
    def __parse_begin_src(self):
        if self.__peek():
            match = re.search('^(\s+)?(\#\+BEGIN_SRC)', self.__peek())
            if match:
                return True

        return None

    def __parse_end_src(self):
        if self.__peek():
            match = re.search('^(\s+)?(\#\+END_SRC)', self.__peek())
            if match:
                return True

        return None        

    def __parse_blank_line(self):
        if not self.__stream.finished(): #if there are lines left
            match = re.search('^\s*$', self.__peek())
            if match: #...and the line is blank
                return True
            
        return False
                            
    def __eat_blank_lines(self):
        blank_line = self.__parse_blank_line()
        while blank_line:
            self.__eat()
            blank_line = self.__parse_blank_line()
        
    def __parse_section(self):
        self.__eat_blank_lines()
        section = self.__parse_regular_text_section() or self.__parse_source_section()
        return section

    def __parse_settings_line(self):
        if self.__peek():
            match = re.search('^\#\+([^\:]+)\:(.*)$', self.__peek())
            if match:
                option = match.group(1)
                value = match.group(2)

                #we're not looking for #+BEGIN_* and #+END_* lines, since those are handled elsewhere 
                if re.search('^(BEGIN|END)_', option):
                    return False, False
                
                return option, value

        return False, False
    
    def __parse_settings_lines(self):
        option, value = self.__parse_settings_line()
        while option and value:
            self.set_setting(option, value)
            self.__eat()
            self.__eat_blank_lines()
            option, value = self.__parse_settings_line()
            
    def __parse_entry(self, level=1):
        self.__eat_blank_lines()

        self.__parse_settings_lines()
        
        my_title, my_level, my_todo_status = self.__parse_heading_line(level=level);
        if my_title and my_level == level:
            #start a new entry
            entry = OrgEntry()

            entry.set_title(my_title)
            entry.set_level(my_level)
            entry.set_todo_status(my_todo_status)
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
