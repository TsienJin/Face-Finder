# Database Relation Documentation

```mermaid
---
title: Entity Relation
---
erDiagram
    Image {
        int id pk
        string dir
        string filename
    }
    
    Person {
        int id pk
        string name
    }
    
    PersonWithFaceInImage {
        int id pk
        int person_id
        int face_in_image_id
    }  
    
    FaceInImage {
        int id pk
        int image_id
        int img_x_pos
        int img_y_pos
        int img_width
        int img_height
        array encoding
    }
    
    Source { 
        int id pk
        string dir
    }  
    
    
    Image ||--o{ FaceInImage : "Contains"
    FaceInImage }|--o{ PersonWithFaceInImage : "Recorded by"
    PersonWithFaceInImage }o--|| Person : ""
```

The SQLite3 implementation implements an additional adapter to handle Numpy arrays to simplify the storage of vectors (embeddings) of faces.