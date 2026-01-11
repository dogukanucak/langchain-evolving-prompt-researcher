"""
Source Quality Assessment for SCOPE Learning

Evaluates the trustworthiness and academic credibility of sources
so SCOPE can learn to prioritize high-quality references.
"""

import re
from typing import Dict, List
from urllib.parse import urlparse


# Academic and trusted domains (expandable)
ACADEMIC_DOMAINS = {
    # Academic publishers
    'springer.com', 'sciencedirect.com', 'elsevier.com', 'wiley.com',
    'tandfonline.com', 'sagepub.com', 'cambridge.org', 'oxfordjournals.org',
    
    # Research databases
    'jstor.org', 'researchgate.net', 'academia.edu', 'arxiv.org',
    
    # Academic institutions
    '.edu', '.ac.uk', '.edu.au',
    
    # Government and official sources
    '.gov', 'nih.gov', 'ncbi.nlm.nih.gov', 'pmc.ncbi.nlm.nih.gov',
    
    # Encyclopedias and references
    'wikipedia.org', 'britannica.com',
    
    # Professional organizations
    'ieee.org', 'acm.org', 'aaas.org',
}

NEWS_DOMAINS = {
    'nytimes.com', 'washingtonpost.com', 'bbc.com', 'bbc.co.uk',
    'reuters.com', 'apnews.com', 'theguardian.com', 'wsj.com',
    'economist.com', 'npr.org', 'ft.com'
}

# Indicators of lower quality
BLOG_INDICATORS = ['blog', 'wordpress', 'medium.com', 'tumblr', 'blogspot']
LOW_QUALITY_INDICATORS = ['listicle', 'top-10', 'you-wont-believe']


def classify_source(url: str) -> Dict[str, any]:
    """
    Classify a source by its URL and return quality metrics.
    
    Returns:
        dict with keys: type, authority, score, reasoning
    """
    if not url:
        return {
            'type': 'unknown',
            'authority': 'unknown',
            'score': 0,
            'reasoning': 'No URL provided'
        }
    
    domain = urlparse(url).netloc.lower()
    path = urlparse(url).path.lower()
    
    # Check for academic sources (highest quality)
    if any(academic_domain in domain for academic_domain in ACADEMIC_DOMAINS):
        # Extra points for peer-reviewed indicators
        if 'journal' in path or 'article' in path or 'doi' in path:
            return {
                'type': 'academic_journal',
                'authority': 'high',
                'score': 10,
                'reasoning': 'Peer-reviewed academic journal'
            }
        elif '.edu' in domain or '.ac.' in domain:
            return {
                'type': 'academic_institution',
                'authority': 'high',
                'score': 9,
                'reasoning': 'Academic institution'
            }
        elif 'pmc.ncbi' in domain or 'pubmed' in domain:
            return {
                'type': 'medical_database',
                'authority': 'high',
                'score': 10,
                'reasoning': 'Medical research database (NIH)'
            }
        elif '.gov' in domain:
            return {
                'type': 'government',
                'authority': 'high',
                'score': 9,
                'reasoning': 'Government/official source'
            }
        else:
            return {
                'type': 'academic',
                'authority': 'high',
                'score': 8,
                'reasoning': 'Academic or research source'
            }
    
    # Check for reputable news sources (medium-high quality)
    if any(news_domain in domain for news_domain in NEWS_DOMAINS):
        return {
            'type': 'news_reputable',
            'authority': 'medium-high',
            'score': 7,
            'reasoning': 'Reputable news organization'
        }
    
    # Check for blogs (lower quality for academic research)
    if any(indicator in domain or indicator in path for indicator in BLOG_INDICATORS):
        return {
            'type': 'blog',
            'authority': 'low',
            'score': 3,
            'reasoning': 'Blog or personal website'
        }
    
    # Check for low-quality indicators
    if any(indicator in path for indicator in LOW_QUALITY_INDICATORS):
        return {
            'type': 'content_farm',
            'authority': 'very_low',
            'score': 2,
            'reasoning': 'Low-quality content (listicle/clickbait)'
        }
    
    # Default: professional website (medium quality)
    return {
        'type': 'professional',
        'authority': 'medium',
        'score': 5,
        'reasoning': 'Professional website or organization'
    }


def assess_sources_quality(sources: List[Dict]) -> Dict[str, any]:
    """
    Assess the overall quality of a list of sources.
    
    Args:
        sources: List of source dicts with 'url' keys
    
    Returns:
        dict with quality metrics for SCOPE observations
    """
    if not sources:
        return {
            'avg_score': 0,
            'high_quality_count': 0,
            'low_quality_count': 0,
            'quality_summary': 'No sources found'
        }
    
    classifications = []
    scores = []
    
    for source in sources:
        url = source.get('url', '')
        classification = classify_source(url)
        classifications.append(classification)
        scores.append(classification['score'])
    
    avg_score = sum(scores) / len(scores) if scores else 0
    high_quality = sum(1 for c in classifications if c['score'] >= 8)
    medium_quality = sum(1 for c in classifications if 5 <= c['score'] < 8)
    low_quality = sum(1 for c in classifications if c['score'] < 5)
    
    # Build detailed summary
    quality_breakdown = []
    if high_quality > 0:
        quality_breakdown.append(f"{high_quality} academic/high-authority")
    if medium_quality > 0:
        quality_breakdown.append(f"{medium_quality} medium-authority")
    if low_quality > 0:
        quality_breakdown.append(f"{low_quality} low-authority")
    
    quality_summary = f"Quality: {', '.join(quality_breakdown)} (avg: {avg_score:.1f}/10)"
    
    return {
        'avg_score': round(avg_score, 1),
        'high_quality_count': high_quality,
        'medium_quality_count': medium_quality,
        'low_quality_count': low_quality,
        'quality_summary': quality_summary,
        'classifications': classifications
    }


def get_quality_observation(sources: List[Dict], query: str = "") -> str:
    """
    Generate a quality-focused observation string for SCOPE.
    
    This is what SCOPE will see and learn from.
    """
    quality = assess_sources_quality(sources)
    
    observation = f"""Found {len(sources)} results
✓ Source quality: {quality['quality_summary']}
✓ High-authority sources: {quality['high_quality_count']}/{len(sources)}
✓ Low-authority sources: {quality['low_quality_count']}/{len(sources)}"""
    
    # Add recommendation context for SCOPE to learn from
    if quality['avg_score'] >= 8:
        observation += "\n✓ Excellent source quality - strong academic foundation"
    elif quality['avg_score'] >= 6:
        observation += "\n⚠ Acceptable source quality - could improve with more academic sources"
    else:
        observation += "\n⚠ Low source quality - needs more authoritative/academic sources"
    
    return observation


# Example usage and testing
if __name__ == "__main__":
    # Test different source types
    test_sources = [
        {'url': 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC123456/'},
        {'url': 'https://www.proof-reading-service.com/blog/writing-tips'},
        {'url': 'https://en.wikipedia.org/wiki/Academic_writing'},
        {'url': 'https://www.nytimes.com/article/academic-publishing'},
        {'url': 'https://harvard.edu/research/writing-guide'},
    ]
    
    print("Source Quality Assessment Examples:")
    print("=" * 70)
    
    for source in test_sources:
        classification = classify_source(source['url'])
        print(f"\nURL: {source['url']}")
        print(f"Type: {classification['type']}")
        print(f"Authority: {classification['authority']}")
        print(f"Score: {classification['score']}/10")
        print(f"Reasoning: {classification['reasoning']}")
    
    print("\n" + "=" * 70)
    print("\nOverall Quality Assessment:")
    quality = assess_sources_quality(test_sources)
    print(get_quality_observation(test_sources))
