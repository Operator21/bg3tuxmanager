import xml.etree.ElementTree as ET
from app.model.mod import Mod
from app.model.nodetype import NodeType

path = "/mnt/nvme_ssd/SteamLibrary/steamapps/compatdata/1086940/pfx/drive_c/users/steamuser/AppData/Local/Larian Studios/Baldur's Gate 3/PlayerProfiles/Public/test.lsx"

class XmlUtil:
    """
    Class for manipulating modsettings.lsx file
    """
    root: ET.Element = None

    def __init__(self, path):
        self.path = path

    # get root of the xml
    def get_root_of_xml(self):
        # if the root is already set, return it
        if self.root is not None:
            return self.root

        # parse the XML file
        tree = ET.parse(self.path)
        self.root = tree.getroot()
        
        return self.root

    # get node with id "Mods"
    def get_mods_node(self):
        return self.get_root_of_xml().find(".//node[@id='Mods']")

    # get node with id "ModOrder"
    def get_mod_order_node(self):
        return self.get_root_of_xml().find(".//node[@id='ModOrder']")

    # get children node of "Mods"
    def get_mods_children(self):
        return self.get_mods_node().find("children")

    # get children node of "ModOrder"
    def get_mod_order_children(self):
        return self.get_mod_order_node().find("children")


    # create node in xml file, can be used for mod definitions aswell for mod order
    def add_node(self, folder: str, md5: str, name: str, uuid: str, version64: str, nodetype: str = NodeType.DEFINITION):
        node = ET.Element('node', id=nodetype.value)
        
        # if adding to mod definitions then add all required attributes
        if nodetype == NodeType.DEFINITION:
            folder_attribute = ET.SubElement(node, 'attribute', id="Folder", type="LSString", value=folder)
            md5_attribute = ET.SubElement(node, 'attribute', id="MD5", type="LSString", value=md5)
            name_attribute = ET.SubElement(node, 'attribute', id="Name", type="LSString", value=name)
            version64_attribute = ET.SubElement(node, 'attribute', id="Version64", type="int64", value=version64)

        uuid_attribute = ET.SubElement(node, 'attribute', id="UUID", type="FixedString", value=uuid)
        
        if nodetype == NodeType.DEFINITION:
            self.get_mods_children().append(node)
        else:
            # NodeType.ORDER
            self.get_mod_order_children().append(node)     

    def add_default_node(self):
        self.add_node("GustavDev", "", "GustavDev", "28ac9ce2-2aba-8cda-b3b5-6e922f71b6b8", "36028797018963968", NodeType.DEFINITION)
        self.add_node("GustavDev", "", "GustavDev", "28ac9ce2-2aba-8cda-b3b5-6e922f71b6b8", "36028797018963968", NodeType.ORDER)

    def add_nodes(self, nodes: list[Mod], nodetype: str = NodeType.DEFINITION):
        for node in nodes:
            self.add_node(node.Folder, "", node.Name, node.UUID, node.Version, nodetype)
        self.save_xml()

    # clear children of node with id "Mods" and "ModOrder", but keep node itself given root element
    def clear_mods(self):
        self.create_children_node_if_not_exist()
        self.get_mods_children().clear() 
        self.get_mod_order_children().clear()    
        self.add_default_node()
        self.save_xml()

    # if "children" node does not exist for "Mods" or "ModOrder", create it
    def create_children_node_if_not_exist(self):
        mods_children = self.get_mods_children()
        mod_order_children = self.get_mod_order_children()

        if mods_children is None:
            mods_children = ET.SubElement(self.get_mods_node(), "children")

        if mod_order_children is None:
            mod_order_children = ET.SubElement(self.get_mod_order_node(), "children")
    

    # save root changes back to xml
    def save_xml(self):
        tree = ET.ElementTree(self.get_root_of_xml())
        tree.write(self.path, encoding="utf-8")