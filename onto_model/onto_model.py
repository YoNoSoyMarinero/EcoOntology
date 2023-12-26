import owlready2 as owl
import os
import cv2

owl.onto_path.append(r"C:\Users\1milo\Desktop\EcoOntology\envo.owl")
onto = owl.get_ontology(r"C:\Users\1milo\Desktop\EcoOntology\envo.owl")
onto.load()

with onto:
    class Willow(onto.TreeCanopy):
        pass
    class Poplar(onto.TreeCanopy):
        pass
    class Maple(onto.TreeCanopy):
        pass
    class Marsh(onto.Liquid):
        pass
    class Stream(onto.Liquid):
        pass
    class Road(onto.HumanBuildings):
        pass
    class Oak(onto.TreeCanopy):
        pass
    class Ash(onto.TreeCanopy):
        pass
    class Grass(onto.Vegetation):
        pass
    class Sand(onto.Soil):
        pass
    class Rocks(onto.Soil):
        pass
    class River(onto.Liquid):
        pass
    class Image(owl.Thing):
        pass
    class Empty(owl.Nothing):
        pass
    class hasX(owl.DataProperty, owl.FunctionalProperty):
        domain = [onto.Terrene]
        range = [float]
    class hasY(owl.DataProperty, owl.FunctionalProperty):
        domain = [onto.Terrene]
        range = [float]
    class hasPercentage(owl.DataProperty, owl.FunctionalProperty):
        domain = [onto.Terrene]
        range = [float]
    class hasImage(owl.ObjectProperty, owl.FunctionalProperty):
        domain = [onto.Terrene]
        range = [Image]
    class hasImageUri(owl.DataProperty, owl.FunctionalProperty):
        domain = [Image]
        range = [str]
    class hasLongitude(owl.DataProperty, owl.FunctionalProperty):
        domain = [Image]
        range = [float]
    class hasLatitude(owl.DataProperty, owl.FunctionalProperty):
        domain = [Image]
        range = [float]

onto.save()

class IndividualGenerator():
    class_map = {
        0: (Empty, "empty"),
        1: (Willow,"willow"),
        2: (Poplar,"poplar"),
        3: (Maple,"maple"),
        4: (Marsh,"marsh"),
        5: (Stream,"stream"),
        6: (Road,"road"),
        7: (Oak,"oak"),
        8: (Ash,"ash"),
        9: (Grass,"grass"),
        10: (Sand,"sand"),
        11: (Rocks,"rocks"),
        12: (River, "river")
    }

    @classmethod
    def create_terrene_individual(cls, x, y, percentage, class_label, image_name):
        individual_class = cls.class_map[class_label]
        individual_name = f"{image_name}_{x}_{y}_{individual_class[1]}"
        individual = individual_class[0](individual_name)
        individual.hasX = x
        individual.hasY = y
        individual.hasPercentage = float(percentage)
        individual.hasImage = onto[image_name]
        onto.save()

    @classmethod
    def create_image_individual(cls, image_uri, longitude, lantitude):
        image = Image(os.path.basename(image_uri))
        image.hasImageUri = image_uri
        image.hasLongitude = longitude
        image.hasLatitude = lantitude
        onto.save()