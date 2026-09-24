# Safety and governance for RAG

Retrieved documents are untrusted input. A document can contain misleading instructions that attempt to redirect the application or reveal protected data. Systems should separate document text from system instructions and restrict tools through explicit authorization rules.

Access control must be enforced before retrieval so users cannot discover documents they are not allowed to read. Logs should avoid storing secrets and sensitive document content. High-impact decisions require suitable human review, audit trails, and domain-specific evaluation.

Document freshness matters. An answer grounded in an obsolete policy can still be well cited and wrong. Production indexes need ownership, update schedules, and a way to remove revoked content.
