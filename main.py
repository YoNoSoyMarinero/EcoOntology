import cv2
import numpy as np
from onto_model.onto_model import IndividualGenerator, SPARQL


def image_statistics(image_mask: np.array) -> zip:
    flat_image: np.array = image_mask[:,:,0].flatten()
    unique_values, counts = np.unique(flat_image, return_counts=True)
    counts = [round(el, 2) for el in 100*counts/flat_image.shape[0]]
    return zip(unique_values, counts)

def create_terrene_individuals(image: np.array, image_name: str, x: int, y: int) -> None:
    image_statistics: zip = image_statistics(image)
    for key, value in image_statistics:
        IndividualGenerator.create_terrene_individual(x, y, value, key, image_name)



