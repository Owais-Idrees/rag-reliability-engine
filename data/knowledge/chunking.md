# Chunking for retrieval

Chunking divides documents into units that can be independently retrieved. Very large chunks may mix unrelated ideas and waste context. Very small chunks may lose definitions or conditions needed to interpret a sentence.

Overlap repeats a small boundary region between adjacent chunks. It can preserve ideas that cross a boundary, but excessive overlap creates duplicate results and increases index size. Chunk size and overlap should be selected with retrieval evaluation rather than intuition alone.

Paragraph-aware splitting preserves natural topic boundaries better than blindly cutting every fixed number of characters. Stable chunk identifiers are useful for citations and regression testing.
