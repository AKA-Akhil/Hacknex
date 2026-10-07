def classify(query: str) -> dict:
    q_lower = query.lower()
    
    visual_keywords = ["chart", "graph", "plot", "visual", "diagram", "figure", "image", "picture"]
    table_keywords = ["table", "row", "column", "compare numbers", "data", "statistics"]
    cross_doc_keywords = ["across documents", "compare reports", "between documents"]
    
    needs_visual = any(kw in q_lower for kw in visual_keywords)
    needs_table = any(kw in q_lower for kw in table_keywords)
    needs_cross_doc = any(kw in q_lower for kw in cross_doc_keywords)
    
    return {
        "needs_text": True,  # Always true by default
        "needs_table": needs_table,
        "needs_visual": needs_visual,
        "needs_cross_doc": needs_cross_doc
    }
