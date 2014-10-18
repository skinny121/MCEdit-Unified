"""Copyright (c) 2010-2012 David Rio Vierra

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE."""

import collections
import json
import os
from directories import dataDir

blockStatePath = os.path.join(dataDir, os.path.join("assets", "minecraft", "blockstates"))
modelPath = os.path.join(dataDir, os.path.join("assets", "minecraft", "models"))

class Variants(collections.Mapping):
    def __init__(self, name):
        with file(os.path.join(blockStatePath, name+".json"), "r") as f:
            self.json = json.load(f)["variants"]
        self.variants = {n: self._createVariant(self.json[n]) for n in self.json}

    def _createVariant(self, variant):
        if isinstance(variant, list):
            # return [self._createVariant(v) for v in variant]
            return self._createVariant(variant[0])
        else:
            return Variant(**{k: variant[k] for k in ["model", "x", "y", "uvlock"] if k in variant})

    def __getitem__(self, key):
        return self.variants[key]

    def __iter__(self):
        return self.variants.__iter__()

    def __len__(self):
        return self.variants.__len__()

class Variant(object):

    def __init__(self, model=None, x=0, y=0, uvlock=False):
        self._Model = getModel("block/"+model)
        self._XRot = x
        self._YRot = y
        self._UVLock = uvlock

    @property
    def Model(self):
        return self._Model

    @property
    def XRot(self):
        return self._XRot

    @property
    def YRot(self):
        return self._YRot

    @property
    def UVLock(self):
        return self._UVLock

_models = dict()

def getModel(name):
    if name in _models:
        return _models[name]
    else:
        model = Model(name)
        _models[name] = model
        return model

class Model(object):
    def __init__(self, name):
        with file(os.path.join(modelPath, *(name+".json").split("/")), "r") as f:
            self.json = json.load(f)
        if "parent" in self.json:
            self.parent = getModel(self.json["parent"])
            self.elements = self.Parent.Elements + self._createElements()
        else:
            self.elements = self._createElements()

    def _createElements(self):
        if "elements" in self.json:
            return [Element(j) for j in self.json["elements"]]
        else:
            return []
    @property
    def Parent(self):
        return self.parent

    @property
    def Elements(self):
        return self.elements


class Element(object):
    def __init__(self, json):
        self.json = json

    @property
    def From(self):
        return self.json["from"]

    @property
    def To(self):
        return self.json["from"]
