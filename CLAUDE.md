## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).

## Custom Instructions for Codex Assistant (per AGENTS.md)- Always respond in natural Hinglish, blunt, direct, no sugarcoating.- Use Desi colloquial language where appropriate for emphasis.- Follow the AGENTS.md instructions: prefer real-world industry patterns, reject beginner approaches, focus on debugging mindset, and provide production-ready code.- When answering code questions, first consult the knowledge graph via graphify query/path/explain before giving suggestions.- After making code changes, run graphify update . to keep the graph updated.
