import os
import sys
from PIL import Image
import imagehash


def calculate_hashes(filepath):
    # Calculate perceptual hash (phash), wavelet hash (whash), and average hash (ahash)
    phash_value = imagehash.phash(Image.open(filepath))
    whash_value = imagehash.whash(Image.open(filepath))
    ahash_value = imagehash.average_hash(Image.open(filepath))
    return phash_value, whash_value, ahash_value


def remove_duplicates(directory, label_directory, threshold=5):
    hashes = {'phash': {}, 'whash': {}, 'ahash': {}}
    duplicates = set()

    total_images = len(os.listdir(directory))
    print(f"Total images in directory: {total_images}")

    processed_images = 0

    for file in os.listdir(directory):
        filepath = os.path.join(directory, file)
        phash_value, whash_value, ahash_value = calculate_hashes(filepath)

        # Check for duplicates based on phash
        if any(abs(phash_value - h) < threshold for h in hashes['phash'].keys()):
            duplicates.add(file)
        else:
            hashes['phash'][phash_value] = filepath

        # Check for duplicates based on whash
        if any(abs(whash_value - h) < threshold for h in hashes['whash'].keys()):
            duplicates.add(file)
        else:
            hashes['whash'][whash_value] = filepath

        # Check for duplicates based on ahash
        if any(abs(ahash_value - h) < threshold for h in hashes['ahash'].keys()):
            duplicates.add(file)
        else:
            hashes['ahash'][ahash_value] = filepath

        processed_images += 1
        print(f"Processed {processed_images}/{total_images} images...", end='\r')

    print("\nRemoving duplicates and its labels...")
    labels = os.listdir(label_directory)
    labels_dic = {}
    for label in labels:
        name = label.split('.')[0]
        labels_dic[name] = label

    for duplicate in duplicates:
        os.remove(os.path.join(directory, duplicate))
        os.remove(os.path.join(label_directory, labels_dic[duplicate.split('.')[0]]))

    remaining_images = len(os.listdir(directory))
    print(f"Done! {remaining_images} images remaining after removing duplicates.")


directory = r"E:\DATA\DATA\extracted_detection_data\PolypDataset\NewTRimageDA"
label_directory = r"E:\DATA\DATA\extracted_detection_data\PolypDataset\NewTRmaskDA"
threshold = 7


remove_duplicates(directory, label_directory, threshold)
