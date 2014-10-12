from PIL import Image
import zipfile
import time

def step(slot):
    texSlot = slot*16
    return texSlot

textureSlots = {
    "grass_top": (step(0),step(0)),
    "stone": (step(1),step(0)),
    "dirt": (step(2),step(0)),
    "grass_side": (step(3),step(0)),
    "planks_oak": (step(4),step(0)),
    "stone_slab_side": (step(5),step(0)),
    "stone_slab_top": (step(6),step(0)),
    }

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
                    block_name = block_name.split(".")[0]
                    zfile.extract(name.filename, "textures/")
                    self.block_image[block_name] = Image.open("textures/"+name.filename)
        self.parse_terrain_png()

    # FIXME: Use a Dictionary to find out were to put the textures
    def parse_terrain_png(self):
        new_terrain = Image.new("RGB", (512, 512))
        for tex in self.block_image.keys():
            try:
                image = self.block_image[tex]
                slot = textureSlots[tex]
                new_terrain.paste(image, slot)
            except:
                pass
                

        '''
        new_terrain.paste(self.block_image["grass_top"], textureSlots["grass_top"])
        new_terrain.paste(self.block_image["stone"], textureSlots["stone"])
        new_terrain.paste(self.block_image["dirt"], textureSlots["dirt"])
        new_terrain.paste(self.block_image["grass_side"], (step(3),step(0)))
        new_terrain.paste(self.block_image["planks_oak"], (step(4),step(0)))
        new_terrain.paste(self.block_image["stone_slab_side"], (step(5),step(0)))
        new_terrain.paste(self.block_image["stone_slab_top"], (step(6),step(0)))
        '''
        
        new_terrain.save(self.pack_name.replace(" ", "_")+".png")
        
rp = ResourcePack('OCD pack 1.8.zip', "OCD Pack")
