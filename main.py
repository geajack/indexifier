from re import match
from sys import argv, stdout
from pathlib import Path

class Index:

    def __init__(self, title=None, page_number=None):
        self.title = title
        self.page_number = page_number
        self.offset = 0
        self.children = []

    def set_offset(self, offset):
        self.offset = offset
        for child in self.children:
            child.set_offset(offset)

    def add_child(self, index):
        self.children.append(index)

    def as_pdftk_index(self, level=0):
        output = ""
        if level > 0:
            output += "BookmarkBegin\n"
            output += "BookmarkTitle:" + self.title + "\n"
            output += "BookmarkLevel:" + str(level) + "\n"
            output += "BookmarkPageNumber:" + str(self.page_number + self.offset) + "\n"
        for child in self.children:
            output += child.as_pdftk_index(level + 1)
        return output
    
    def as_djvu_index(self, is_root):
        output = ""
        for child in self.children:
            output += child.as_djvu_index(False)

        if is_root:
            output = "(bookmarks " + output + ")"
        else:
            output = f'("{self.title}" "#{self.page_number + self.offset}" ' + output + ") "

        return output

    def __repr__(self):
        return f"{self.title} ({self.page_number})" if self.title is not None else "ROOT"

def index_from_file(filepath):
    with open(filepath, "r") as file:
        lines = file.readlines()

    ancestors = [Index()]
    margins = [""]

    for line in lines:
        margin = match(r"\s*", line).group(0)
        parent = None
        for i in range(len(margins) - 1, -1, -1):
            if margin.startswith(margins[i]):
                if margin == margins[i]:
                    parent = ancestors[i]
                    ancestors = ancestors[:i+1]
                    margins = margins[:i+1]
                    break
                else:
                    parent = ancestors[i].children[-1]
                    ancestors.append(parent)      
                    margins.append(margin)
                    break
        
        if parent is None:
            raise Exception()

        reversed_line = str.join("", reversed(line.strip()))
        reversed_page_number, reversed_title = reversed_line.split(" ", 1)
        page_number = str.join("", reversed(reversed_page_number))
        title = str.join("", reversed(reversed_title))
        subindex = Index(title, int(page_number))
        parent.add_child(subindex)

    return ancestors[0]

if __name__ == "__main__":
    book_file = argv[1]
    index_file = argv[2]
    try:
        offset = int(argv[3])
    except:
        offset = 0
    index = index_from_file(index_file)
    index.set_offset(offset)
    if book_file == "djvu":
        djvu_index = index.as_djvu_index(True)
        print(djvu_index)
    elif book_file == "pdf":
        pdf_index = index.as_pdftk_index()
        print(pdf_index)