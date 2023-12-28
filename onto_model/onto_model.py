import owlready2 as owl
import os

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
        range = [int]
    class hasY(owl.DataProperty, owl.FunctionalProperty):
        domain = [onto.Terrene]
        range = [int]
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

class SPARQL:

    prefix: str = """          
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX eco: <C:/Users/1milo/Desktop/EcoOntology/envo.owl#>"""
    
    @classmethod
    def get_individuals_by_condition(cls, 
                                     image_name: str,
                                     class_name: str = "Terrene",
                                     x1: int = 0,
                                     y1: int = 0,
                                     x2: int = 1e6,
                                     y2: int = 1e6,
                                     min_percentage: float = 0,
                                     max_percentage: float = 100) -> list:
        query:str = f"""
        {cls.prefix}
        SELECT ?class ?x ?y ?p ?image
        WHERE {{
            ?class rdf:type/rdfs:subClassOf* eco:{class_name} .
            ?class eco:hasX ?x .
            ?class eco:hasY ?y .
            ?class eco:hasPercentage ?p .
            ?class eco:hasImage ?image.
            ?image eco:hasImageUri ?imageUri.
            FILTER (?x >= {x1} && ?x <= {x2} && ?y >= {y1} && ?y <= {y2} && ?p >= {min_percentage} && ?p <= {max_percentage})
            FILTER (STRENDS(STR(?imageUri), "{image_name}"))
        }}
    """
        return list(owl.default_world.sparql(query))


class IndividualGenerator():
    class_map: dict = {
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
    def create_terrene_individual(cls, x: int, y: int, percentage: float, class_label: int, image_name: str) -> None:
        individual_class: object = cls.class_map[class_label]
        individual_name: str = f"{image_name}_{x}_{y}_{individual_class[1]}"
        individual: object = individual_class[0](individual_name)
        individual.hasX = x
        individual.hasY = y
        individual.hasPercentage = float(percentage)
        individual.hasImage = onto[image_name]
        onto.save()

    @classmethod
    def create_image_individual(cls, image_uri: str, longitude: float, lantitude:float) -> None:
        image: Image = Image(os.path.basename(image_uri))
        image.hasImageUri = image_uri
        image.hasLongitude = longitude
        image.hasLatitude = lantitude
        onto.save()