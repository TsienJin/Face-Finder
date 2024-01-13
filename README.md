# Face Finder

An intuitive Python GUI application that allows users to perform facial recognition searches against a large (and heavily nested) directory of images.

### Supported Image Formats
1. JPG/JPEG
2. PNG
3. CR2
4. DNG
5. TIFF

---

## Modes

There are two modes of operation, both utilise the [DeepFace](https://github.com/serengil/deepface?tab=readme-ov-file) library to detect and analyse faces seen in images.

### 1. Persistent Tagging

This method works best for scenarios where your images are in 'long term storage' whereby the images are kept do not change directories often. An example of this scenario is a photographer with a Network Attached Storage (NAS) to keep raw images.

Images in storage are first indexed and analyzed to identify faces. The embeddings for the faces are stored in an SQLite3 database[^1].

By going through the analyzed images using the GUI, the user will be able to set **Anchor Faces**.

> **Anchor Faces**
> 
> These refer to faces that have been manually labeled by the user. [Range Search](https://en.wikipedia.org/wiki/Range_searching) is performed on unlabeled faces to find faces that are within the euclidian range set by the user.

The intention is that over time, the identification of faces will become more refined as there would be a greater number of **Anchor Faces**.

### 2. Reference Search

This method works by searching for a face against all indexed images. After indexing the store to generate facial embeddings, the user will provide an image that contains a face of interest. The embeddings for the face will then be used as the search criteria for similar faces. 





[^1]: Vector storage in PySQLite3 by [Okpare, 2023](https://github.com/DaveOkpare/sqlite_vector/tree/main).

---

## References

1. [David Okpare (2023)](https://github.com/DaveOkpare/sqlite_vector/tree/main)
2. [Sefik Ilkin Serengil (2019)](https://github.com/serengil/deepface)