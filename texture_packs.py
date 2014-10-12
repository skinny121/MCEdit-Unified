from PIL import Image
import zipfile
import time

def step(slot):
    texSlot = slot*16
    return texSlot

class ResourcePack:

    def __init__(self, zipfile, name):
        self.zipfile = zipfile
        self.pack_name = name
        self.block_image = {}

        self.open_pack()

    def open_pack(self):
        zfile = zipfile.ZipFile(self.zipfile)
        for name in zfile.infolist():
            if name.filename.endswith(".png"):
                #print name.filename
                if name.filename.startswith("assets/minecraft/textures/blocks"):
                    #print "Block Texture!"
                    print name.filename.split("/")[-1]
                    block_name = name.filename.split("/")[-1]
                    zfile.extract(name.filename, "textures/")
                    self.block_image[block_name] = Image.open("textures/"+name.filename)
        self.parse_terrain_png()

    def parse_terrain_png(self):
        new_terrain = Image.new("RGB", (512, 512))
        new_terrain.paste(self.block_image["grass_top.png"], (step(0),step(0)))
        new_terrain.paste(self.block_image["stone.png"], (step(1),step(0)))
        new_terrain.paste(self.block_image["dirt.png"], (step(2),step(0)))
        new_terrain.save(self.pack_name.replace(" ", "_")+".png")
        
rp = ResourcePack('OCD pack 1.8.zip', "OCD Pack")
