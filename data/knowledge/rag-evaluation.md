# Evaluating retrieval systems

Retrieval evaluation isolates whether the system found the right evidence before generation begins. If the expected source is absent, changing the prompt or language model cannot repair the missing context. Teams should maintain a representative set of questions with expected sources and run it whenever indexing changes.

Hit rate reports how often at least one expected document appears in the top results. Mean reciprocal rank rewards systems that place the first relevant result near the top. Precision at k estimates how much of the retrieved context is relevant. These metrics should be paired with qualitative error analysis because a small benchmark cannot represent every user question.

Citation coverage measures whether an answer points to an expected source. It does not prove that every claim is supported. Faithfulness evaluation should compare individual claims with their cited evidence.
