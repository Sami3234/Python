"""
=============================================================
  summarizer.py — Core Rule-Based Summarization Engine
  AI News Summarizer Agent
  Rule-Based AI System (No Machine Learning / No Deep Learning)
=============================================================

HOW IT WORKS (Algorithm Overview):
1. Preprocess  → Clean the raw text
2. Tokenize    → Split text into sentences and words
3. Filter      → Remove stop words (is, the, a, …)
4. Frequency   → Count remaining "important" words
5. Score       → Give each sentence a score based on word frequencies
6. Rank        → Sort sentences by score (highest = most important)
7. Summarize   → Pick top-N sentences in original order → summary
"""

import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter


# ─── STEP 0: Download required NLTK resources once ────────────────────────────
def download_nltk_data():
    """Download NLTK data files needed for tokenisation and stop words."""
    resources = ['punkt', 'stopwords', 'punkt_tab']
    for resource in resources:
        try:
            nltk.download(resource, quiet=True)
        except Exception:
            pass


download_nltk_data()


# ─── NEWS CATEGORY KEYWORDS (Rule-Based Lookup Table) ─────────────────────────
CATEGORY_KEYWORDS = {
    'Technology':  ['technology', 'software', 'computer', 'internet', 'digital',
                    'artificial intelligence', 'ai', 'robot', 'cyber', 'data',
                    'algorithm', 'smartphone', 'app', 'coding', 'machine learning'],
    'Politics':    ['government', 'election', 'president', 'minister', 'parliament',
                    'policy', 'democrat', 'republican', 'senate', 'vote',
                    'political', 'congress', 'prime minister', 'law'],
    'Sports':      ['match', 'game', 'player', 'team', 'score', 'championship',
                    'tournament', 'win', 'loss', 'football', 'cricket',
                    'basketball', 'soccer', 'olympic', 'athlete'],
    'Business':    ['market', 'stock', 'economy', 'company', 'profit', 'revenue',
                    'business', 'trade', 'investment', 'finance', 'bank',
                    'inflation', 'startup', 'merger'],
    'Health':      ['health', 'disease', 'hospital', 'doctor', 'medicine',
                    'vaccine', 'virus', 'patient', 'treatment', 'medical',
                    'cancer', 'pandemic', 'surgery', 'symptoms'],
    'Science':     ['research', 'scientist', 'discovery', 'study', 'experiment',
                    'space', 'climate', 'environment', 'biology', 'physics',
                    'chemical', 'nasa', 'planet', 'telescope'],
    'Crime':       ['police', 'arrest', 'crime', 'court', 'judge', 'sentence',
                    'murder', 'theft', 'robbery', 'investigation', 'suspect'],
    'Education':   ['school', 'university', 'student', 'teacher', 'education',
                    'degree', 'exam', 'curriculum', 'scholarship', 'college'],
}


# ─── MAIN SUMMARIZER CLASS ────────────────────────────────────────────────────
class NewsSummarizer:
    """
    Rule-Based Extractive Text Summarizer.

    Key Concept — "Extractive":
      We do NOT generate new words. We EXTRACT (pick) the most important
      existing sentences from the original article. This is the simplest
      and most transparent form of automatic summarisation.
    """

    def __init__(self):
        # Load English stop words from NLTK
        self.stop_words = set(stopwords.words('english'))
        # Add domain-specific words that carry little meaning in news
        self.stop_words.update([
            'said', 'also', 'would', 'could', 'may', 'one', 'two', 'three',
            'four', 'five', 'new', 'year', 'years', 'time', 'us', 'u.s.',
            'according', 'told', 'say', 'says', 'get', 'got', 'make'
        ])

    # ── STEP 1: Preprocess ────────────────────────────────────────────────────
    def preprocess_text(self, text: str) -> str:
        """
        Clean raw input text.
        - Collapse multiple spaces / newlines into one space
        - Remove characters that confuse the sentence tokeniser
          (but KEEP . ! ? because they mark sentence boundaries)
        """
        text = re.sub(r'\s+', ' ', text)               # multiple spaces → one space
        text = re.sub(r'[^\w\s\.\!\?\,\;\:]', ' ', text)  # keep basic punctuation
        return text.strip()

    # ── STEP 2: Sentence Tokenisation ─────────────────────────────────────────
    def split_into_sentences(self, text: str) -> list:
        """
        Split text into individual sentences using NLTK's Punkt tokeniser.
        Filters out sentences shorter than 5 words (too short to be useful).
        """
        sentences = sent_tokenize(text)
        filtered = [s.strip() for s in sentences if len(s.split()) >= 5]
        return filtered

    # ── STEP 3: Stop-Word Removal ─────────────────────────────────────────────
    def remove_stopwords(self, text: str) -> list:
        """
        Tokenise text into words, then remove:
          1. Stop words  (the, is, at, which …)
          2. Punctuation marks
          3. Non-alphabetic tokens (numbers, symbols)
        Returns a list of meaningful lowercase words.
        """
        words = word_tokenize(text.lower())
        filtered = [
            word for word in words
            if word not in self.stop_words          # not a stop word
            and word not in string.punctuation      # not punctuation
            and word.isalpha()                      # only real words
            and len(word) > 2                       # skip 1-2 letter tokens
        ]
        return filtered

    # ── STEP 4: Word Frequency Count ──────────────────────────────────────────
    def calculate_word_frequency(self, text: str) -> dict:
        """
        Count how many times each important word appears.
        Frequencies are NORMALISED to a 0.0–1.0 scale so that
        longer articles don't unfairly dominate.

        Example:
          'climate' appears 8 times, 'scientist' 4 times
          max_freq = 8  →  climate=1.0, scientist=0.5
        """
        words = self.remove_stopwords(text)
        word_freq = Counter(words)

        if word_freq:
            max_freq = max(word_freq.values())
            word_freq = {word: freq / max_freq for word, freq in word_freq.items()}

        return dict(word_freq)

    # ── STEP 5: Sentence Scoring ──────────────────────────────────────────────
    def score_sentences(self, sentences: list, word_freq: dict) -> dict:
        """
        Give every sentence a numerical importance score.

        Formula:
          sentence_score = (sum of freq of all important words in sentence)
                           ÷ (number of important words found)

        Dividing by word count prevents long sentences from always winning.
        """
        sentence_scores = {}

        for sentence in sentences:
            words = word_tokenize(sentence.lower())
            total_score = 0.0
            hit_count   = 0

            for word in words:
                if word in word_freq:
                    total_score += word_freq[word]
                    hit_count   += 1

            if hit_count > 0:
                sentence_scores[sentence] = total_score / hit_count

        return sentence_scores

    # ── STEP 6: Top-Sentence Selection ────────────────────────────────────────
    def get_top_sentences(self, sentence_scores: dict, n: int = 3) -> list:
        """
        Sort all sentences by score (descending) and return the top N.
        These are the 'most important' sentences in the article.
        """
        sorted_sentences = sorted(
            sentence_scores.items(),
            key=lambda item: item[1],
            reverse=True        # highest score first
        )
        return [sentence for sentence, score in sorted_sentences[:n]]

    # ── STEP 7: Summary Assembly ──────────────────────────────────────────────
    def assemble_summary(self, original_sentences: list, top_sentences: list) -> str:
        """
        Re-order top sentences to match their ORIGINAL position in the article.
        This makes the summary read naturally (not jump around in time).
        """
        ordered = [s for s in original_sentences if s in top_sentences]
        return ' '.join(ordered)

    # ── Category Detection (Rule-Based) ───────────────────────────────────────
    def detect_category(self, text: str) -> str:
        """
        Detect news category by checking which keyword list has the most hits.
        Pure rule-based — no model required.
        """
        text_lower = text.lower()
        scores = {
            cat: sum(1 for kw in keywords if kw in text_lower)
            for cat, keywords in CATEGORY_KEYWORDS.items()
        }
        best_score = max(scores.values())
        return max(scores, key=scores.get) if best_score > 0 else 'General'

    # ── PUBLIC API ─────────────────────────────────────────────────────────────
    def generate_summary(self, text: str, num_sentences: int = 3) -> dict:
        """
        Full pipeline: runs all 7 steps and returns a results dictionary.

        Parameters:
            text          : Raw news article string
            num_sentences : How many sentences the summary should contain

        Returns:
            dict with keys:
              original_text, sentences, word_freq, sentence_scores,
              top_sentences, summary, top_keywords, category, stats
              (or 'error' key if input is too short)
        """
        # ── Guard: article must be long enough ───────────────────────────────
        if len(text.split()) < 30:
            return {
                'error': 'Article too short. Please provide at least 30 words.',
                'sentences': []
            }

        # Step 1
        clean_text = self.preprocess_text(text)

        # Step 2
        sentences = self.split_into_sentences(clean_text)

        if len(sentences) < 2:
            return {
                'error': 'Could not detect enough sentences. Try adding more text.',
                'sentences': sentences
            }

        # Steps 3 & 4
        word_freq = self.calculate_word_frequency(clean_text)

        # Step 5
        sentence_scores = self.score_sentences(sentences, word_freq)

        # Step 6
        n = min(num_sentences, len(sentences))
        top_sentences = self.get_top_sentences(sentence_scores, n)

        # Step 7
        summary = self.assemble_summary(sentences, top_sentences)

        # Extra analytics
        top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:12]
        category = self.detect_category(clean_text)

        original_wc = len(text.split())
        summary_wc  = len(summary.split())

        return {
            'original_text':    text,
            'clean_text':       clean_text,
            'sentences':        sentences,
            'word_freq':        word_freq,
            'sentence_scores':  sentence_scores,
            'top_sentences':    top_sentences,
            'summary':          summary,
            'top_keywords':     top_keywords,
            'category':         category,
            'stats': {
                'original_word_count':   original_wc,
                'summary_word_count':    summary_wc,
                'original_sentence_count': len(sentences),
                'summary_sentence_count':  len(top_sentences),
                'compression_ratio':     round(summary_wc / original_wc * 100, 1)
            }
        }

    # ── Save to File ───────────────────────────────────────────────────────────
    def save_summary(self, result: dict, filename: str = 'summary_output.txt') -> str:
        """
        Save the full analysis report (summary + keywords + scores) to a .txt file.
        Returns the saved filename.
        """
        with open(filename, 'w', encoding='utf-8') as f:
            border = '=' * 62
            f.write(f"{border}\n")
            f.write("    AI NEWS SUMMARIZER — ANALYSIS REPORT\n")
            f.write(f"{border}\n\n")

            # Meta
            f.write(f"  Detected Category  : {result['category']}\n")
            s = result['stats']
            f.write(f"  Original Words     : {s['original_word_count']}\n")
            f.write(f"  Summary Words      : {s['summary_word_count']}\n")
            f.write(f"  Original Sentences : {s['original_sentence_count']}\n")
            f.write(f"  Summary Sentences  : {s['summary_sentence_count']}\n")
            f.write(f"  Compression Ratio  : {s['compression_ratio']}%\n\n")

            # Original
            f.write(f"{'─'*62}\nORIGINAL ARTICLE\n{'─'*62}\n")
            f.write(result['original_text'] + '\n\n')

            # Summary
            f.write(f"{'─'*62}\nGENERATED SUMMARY\n{'─'*62}\n")
            f.write(result['summary'] + '\n\n')

            # Keywords
            f.write(f"{'─'*62}\nTOP KEYWORDS (normalised frequency)\n{'─'*62}\n")
            for word, freq in result['top_keywords']:
                bar = '█' * int(freq * 25)
                f.write(f"  {word:<20} {bar:<26} {freq:.3f}\n")

            # Sentence scores
            f.write(f"\n{'─'*62}\nSENTENCE SCORES (top 5)\n{'─'*62}\n")
            ranked = sorted(
                result['sentence_scores'].items(),
                key=lambda x: x[1], reverse=True
            )
            for i, (sent, score) in enumerate(ranked[:5], 1):
                f.write(f"\n#{i}  Score: {score:.4f}\n    {sent}\n")

        return filename
