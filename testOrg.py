from Org import *

op = OrgParser()
entries = op.load("/home/cam/git/org-blog.git/org-files/entries.org")

for e in entries:
    print("title:")
    print(e.get_title())

    print("level:")
    print(e.get_level())

    print("text:")
    print(e.get_text())

    print("subheadings:")
    print(str(len(e.get_subentries())))

    print ("---------------")

