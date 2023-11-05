class Mod:
    path: str = ""

    def __init__(self, Author = "", Name = "", Folder = "", Version = "", Description = "", UUID = "", Created = "", Dependencies = "", Group = ""):
        self.Author = Author
        self.Name = Name
        self.Folder = Folder
        self.Version = Version
        self.Description = Description
        self.UUID = UUID
        self.Created = Created
        self.Dependencies = Dependencies
        self.Group = Group