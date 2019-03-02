class Image:
    def __init__(self, desc):
        parts = desc.split(" ")
        self.desc = desc
        self.id = parts[0]
        self.type = parts[1]
        self.num_tags = int(parts[2])
        self.tags = set(parts[3:])
        self.used = False

    def get_type(self):
        return self.type

    def is_horizontal(self):
        return self.type == "H"

    def is_vertical(self):
        return self.type == "V"

    def get_tags(self):
        return self.tags

    def get_tags_count(self):
        return self.num_tags

    def get_id(self):
        return self.id

    def __str__(self):
        return self.desc

    def is_used(self):
        return self.used
    
    def set_used(self):
        self.used = True


class Slide:
    def __init__(self, img1, img2=None):
        self.used = False
        if img1.is_horizontal():
            self.s_type = "H"
            self.id1 = img1.get_id()
            self.id2 = None
            self.tags = img1.get_tags()
        else:
            self.s_type = "V"
            self.id1 = img1.get_id()
            self.id2 = img2.get_id()
            self.tags = self.combine_tags(img1, img2)

    def combine_tags(self, img1, img2):
        tags1 = img1.get_tags()
        tags2 = img2.get_tags()
        tags = tags1.union(tags2)
        return tags

    def get_ids(self):
        if self.is_horizontal():
            return self.id1
        else:
            return self.id1 + " " + self.id2

    def is_horizontal(self):
        return self.s_type == "H"

    def get_type(self):
        return self.s_type

    def get_tags(self):
        return self.tags

    def __str__(self):
        return self.get_ids() + " " + self.get_type() + " " + str(self.get_tags())

    def get_if(self, slide):
        tags1 = self.get_tags()
        tags2 = slide.get_tags()
        intersection = tags1.intersection(tags2)
        tags_l = tags1 - intersection
        tags_r = tags2 - intersection
        # print("Tags left: " + str(tags_l) +  " intersection: " +
        #     str(intersection) + " Tags right: " + str(tags_r))
        return min(len(intersection), len(tags_l), len(tags_r))

    def set_used(self):
        self.used = True

    def is_used(self):
        return self.used