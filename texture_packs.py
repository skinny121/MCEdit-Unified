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
    "brick": (step(7),step(0)),
    "tnt_side": (step(8),step(0)),
    "tnt_top": (step(9),step(0)),
    "tnt_bottom": (step(10),step(0)),
    "web": (step(11),step(0)),
    "flower_rose": (step(12),step(0)),
    "flower_dandelion": (step(13),step(0)),
    "sapling_oak": (step(15),step(0)),
    "flower_blue_orchid": (step(16),step(0)),
    "flower_allium": (step(17),step(0)),
    
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
        new_terrain = Image.new("RGBA", (512, 512), None)
        for tex in self.block_image.keys():
            try:
                image = self.block_image[tex]
                slot = textureSlots[tex]
                new_terrain.paste(image, slot, image)
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
        new_terrain.show()
        
rp = ResourcePack('OCD pack 1.8.zip', "OCD Pack")
