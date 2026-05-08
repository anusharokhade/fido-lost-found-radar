# matcher.py
import os
import pandas as pd

# Try to use sklearn TF-IDF + cosine (best). If not available, fall back to fuzzy ratio.
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except Exception:
    SKLEARN_AVAILABLE = False

from difflib import SequenceMatcher

def _fuzzy_sim(a, b):
    """Simple fallback similarity (0..1)"""
    return SequenceMatcher(None, a, b).ratio()

def find_matches(new_item_img, new_item_desc, dataset, top_k=3, min_score=0.30):
    """
    Args:
        new_item_img: path or file-like (ignored by this text-only matcher)
        new_item_desc: string
        dataset: pandas DataFrame OR path to CSV
        top_k: how many results to return
        min_score: minimal similarity (0..1) to consider a match
    Returns:
        list of dicts with keys: item_id, description, image_path, score
        (returns [] if no items meet min_score)
    """

    # load dataset if path
    if isinstance(dataset, str):
        df = pd.read_csv(dataset)
    else:
        df = dataset.copy()

    if df.empty:
        return []

    # Normalize descriptions
    df['clean_description'] = df['description'].fillna('').astype(str).str.lower().str.strip()
    query = (new_item_desc or "").strip().lower()

    # If there's no text (empty description) we don't attempt text matching here.
    # You can implement image-based matching later (CLIP, ResNet) if needed.
    if not query:
        return []

    scores = []
    if SKLEARN_AVAILABLE:
        # Fit TF-IDF on dataset descriptions + query (small data so fitting on the fly is OK)
        try:
            vec = TfidfVectorizer().fit(df['clean_description'].tolist() + [query])
            desc_vecs = vec.transform(df['clean_description'].tolist())
            q_vec = vec.transform([query])
            sims = cosine_similarity(q_vec, desc_vecs).flatten()
            scores = sims.tolist()
        except Exception as e:
            # fallback
            scores = [ _fuzzy_sim(query, d) for d in df['clean_description'].tolist() ]
    else:
        # fallback fuzzy matching
        scores = [ _fuzzy_sim(query, d) for d in df['clean_description'].tolist() ]

    # Build result list
    results = []
    for idx, row in df.iterrows():
        score = float(scores[idx]) if idx < len(scores) else 0.0
        results.append({
            'item_id': row.get('item_id', '-'),
            'description': row.get('description', ''),
            'image_path': row.get('image_path', ''),
            'score': score
        })

    # Sort by score desc
    results = sorted(results, key=lambda x: x['score'], reverse=True)

    # Debug print (optional; visible in terminal)
    print("DEBUG matcher: query=", query, " top scores:", [(r['description'], round(r['score'],3)) for r in results[:6]])

    # Filter by threshold
    filtered = [r for r in results if r['score'] >= float(min_score)]

    # Return top_k
    return filtered[:int(top_k)]