### What is Cosine similarity

Imagine every embedding (vector) as an arrow in space.
- The direction of the arrow = meaning
- The length of the arrow = intensity or magnitude
Cosine similarity asks:
“How similar are the directions of these two arrows?”

It ignores the length and focuses only on the angle.

- Angle = 0° → vectors point the same way → similarity = 1
- Angle = 90° → vectors are unrelated → similarity = 0
- Angle = 180° → opposite meaning → similarity = -1

This is why cosine similarity is so good for text.. MEANING MATTERS MORE THAN MAGNITUDE. 

## Why Cosine Is Better Than L2 for Text
L2 distance (Euclidean) measures:
“How far apart are these points?”

But embeddings can have different magnitudes even if they mean the same thing.

Example:
"CSK won IPL 2023"
"Chennai Super Kings won the 2023 IPL"


- Their vectors may have different lengths but point in the same direction.
- Cosine similarity sees them as very similar. L2 distance might not.

*This is why most modern RAG systems prefer cosine.*


### How Cosine Search Works in Practice

To use cosine similarity in FAISS, you must:
- Normalize all embeddings
(turn them into unit vectors)
- Use IndexFlatIP
(inner product = cosine similarity when vectors are normalized)



