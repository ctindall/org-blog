from Org import *

op = OrgParser()
entries = op.load("/home/cam/git/org-blog.git/org-files/posts.org")

def show_entry(e,level):
    indent = ""
    for n in range(1,level):
        indent += "\t"
        
    print(indent + "title:")
    print(indent + e.get_title())

    print(indent + "level:")
    print(indent + str(e.get_level()))

    print(indent + "tags:")
    print(indent + str(e.get_tags()))

    # for s in e.get_sections():
    #     print(indent + "------------------------")
    #     print(indent + str(s))

    print(indent + "subheadings:")
    for entry in e.get_subentries():
        show_entry(entry,level + 1)

    print(indent + "html:")
    print(indent + e.to_html())

    print (indent + "---------------")


for e in entries:
    show_entry(e,1)
