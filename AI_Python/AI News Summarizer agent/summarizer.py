"""
AI NEWS SUMMARIZER AGENT


Methodology:
1. Text preprocessing and cleaning
2. Sentence tokenization
3. Stop-word removal
4. Word frequency analysis and normalization
5. Sentence importance scoring
6. Position-based scoring enhancement
7. Title keyword matching and boosting
8. Named-entity importance boosting
9. Length-based penalty adjustment
10. Redundancy removal using Jaccard Similarity
11. Summary generation using top-ranked sentences



"""

import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter


#  SECTION 0 — NLTK BOOTSTRAP

def _download_nltk_data() -> None:
    """Download required NLTK resources silently on first run."""
    for resource in ['punkt', 'stopwords', 'punkt_tab']:
        try:
            nltk.download(resource, quiet=True)
        except Exception:
            pass

_download_nltk_data()

#  SECTION 1 — CONFIGURATION CONSTANTS
#  Position boosting 
POSITION_FIRST_BOOST  = 0.30   # index 0  
POSITION_SECOND_BOOST = 0.20   # index 1
POSITION_EARLY_BOOST  = 0.10   # index 2–4
#Title / headline boosting
TITLE_KEYWORD_BOOST   = 0.15   # per matching title word
#  Named-entity boosting
ENTITY_BOOST          = 0.12   # per entity found (capped at 3 entities)
ENTITY_CAP            = 3      # max entities credited per sentence
#  Length penalty
LONG_SENTENCE_THRESHOLD = 45   # words; sentences above this get penalised
LONG_SENTENCE_PENALTY   = 0.08 # base penalty 
#  Redundancy filter
SIMILARITY_THRESHOLD  = 0.45
# Sentence quality gate
MIN_SENTENCE_WORDS    = 6      # sentences shorter than this are ignored


#  SECTION 2 — NAMED-ENTITY REGEX PATTERNS
# Honorifics and political / organisational titles
_TITLE_WORDS = (
    r'President|Prime\s+Minister|Minister|Senator|Governor|Chancellor|'
    r'Secretary|Ambassador|General|Admiral|Commissioner|Director|CEO|'
    r'Chairman|Chief|Mayor|Judge|Justice|Officer|Spokesperson'
)
# Well-known countries and geopolitical entities (extend as needed)
_GEOPOLITICAL = (
    r'United\s+States|United\s+Kingdom|European\s+Union|United\s+Nations|'
    r'NATO|ASEAN|G7|G20|IMF|World\s+Bank|WHO|WTO|'
    r'Pakistan|India|China|Russia|Iran|Israel|Ukraine|Afghanistan|'
    r'Germany|France|Japan|South\s+Korea|North\s+Korea|Brazil|Canada|'
    r'Saudi\s+Arabia|Turkey|Egypt|Nigeria|South\s+Africa|Australia'
)
# Organisation suffixes
_ORG_SUFFIXES = (
    r'University|Corporation|Corp\.|Inc\.|Ltd\.|'
    r'Institute|Foundation|Agency|Department|Ministry|'
    r'Committee|Council|Bureau|Authority|Commission'
)
ENTITY_PATTERNS = [
    # 1. Two consecutive Title-Case words → likely a person's name
    # Imran Khan
    re.compile(r'\b[A-Z][a-z]{1,15}\s+[A-Z][a-z]{1,15}\b'),
    # 2. Known political / professional titles 
    re.compile(rf'\b({_TITLE_WORDS})\b'),
    # 3. Known countries, regions, international bodies
    re.compile(rf'\b({_GEOPOLITICAL})\b'),
    # 4. All-caps abbreviations of 2–5 letters: NASA, FBI, CIA, WHO
    re.compile(r'\b[A-Z]{2,5}\b'),
    # 5. Title-Case word followed by an organization suffix
    re.compile(rf'\b[A-Z][a-z]+\s+({_ORG_SUFFIXES})\b'),
]


#  SECTION 3 — WEIGHTED CATEGORY KEYWORD TABLE
CATEGORY_KEYWORDS: dict[str, dict[str, list]] = {

    'Technology': {
        'high':   ['artificial intelligence', 'machine learning', 'cybersecurity',
                   'blockchain', 'quantum computing', 'deep learning'],
        'medium': ['technology', 'software', 'computer', 'internet', 'digital',
                   'robot', 'data', 'algorithm', 'cyber', 'automation'],
        'low':    ['app', 'smartphone', 'coding', 'startup', 'platform', 'cloud'],
    },

    'Politics': {
        'high':   ['prime minister', 'general election', 'presidential', 'parliament',
                   'senate hearing', 'congress', 'legislation'],
        'medium': ['government', 'election', 'president', 'minister', 'policy',
                   'democrat', 'republican', 'vote', 'political', 'opposition'],
        'low':    ['law', 'bill', 'party', 'campaign', 'official', 'reform'],
    },

    'Sports': {
        'high':   ['world cup', 'championship', 'olympic games', 'grand slam',
                   'super bowl', 'premier league', 'test match'],
        'medium': ['match', 'tournament', 'player', 'team', 'score', 'coach',
                   'football', 'cricket', 'basketball', 'soccer', 'athlete'],
        'low':    ['game', 'win', 'loss', 'league', 'stadium', 'season'],
    },

    'Business': {
        'high':   ['stock market', 'initial public offering', 'merger', 'acquisition',
                   'central bank', 'interest rate', 'gdp'],
        'medium': ['economy', 'company', 'profit', 'revenue', 'investment',
                   'finance', 'bank', 'inflation', 'trade', 'market'],
        'low':    ['startup', 'shares', 'fund', 'deal', 'quarter', 'fiscal'],
    },

    'Health': {
        'high':   ['pandemic', 'outbreak', 'clinical trial', 'vaccine efficacy',
                   'cancer treatment', 'public health emergency'],
        'medium': ['health', 'disease', 'hospital', 'doctor', 'medicine',
                   'vaccine', 'virus', 'patient', 'treatment', 'medical'],
        'low':    ['surgery', 'symptoms', 'study', 'drug', 'therapy', 'diet'],
    },

    'Science': {
        'high':   ['nasa', 'space station', 'climate change', 'peer-reviewed',
                   'scientific breakthrough', 'genome', 'black hole'],
        'medium': ['research', 'scientist', 'discovery', 'experiment', 'space',
                   'climate', 'environment', 'biology', 'physics', 'chemical'],
        'low':    ['study', 'planet', 'telescope', 'laboratory', 'species', 'data'],
    },

    'World': {
        'high':   ['united nations', 'diplomatic crisis', 'ceasefire', 'sanctions',
                   'international summit', 'foreign minister', 'bilateral talks'],
        'medium': ['international', 'foreign', 'treaty', 'global', 'conflict',
                   'refugee', 'humanitarian', 'embassy', 'nuclear'],
        'low':    ['world', 'overseas', 'abroad', 'region', 'border', 'alliance'],
    },

    'Crime': {
        'high':   ['murder', 'terrorism', 'drug trafficking', 'money laundering',
                   'sexual assault', 'corruption charges'],
        'medium': ['police', 'arrest', 'crime', 'court', 'judge', 'sentence',
                   'investigation', 'suspect', 'robbery', 'verdict'],
        'low':    ['case', 'charges', 'lawyer', 'trial', 'witness', 'evidence'],
    },

    'Education': {
        'high':   ['academic year', 'university admission', 'scholarship programme',
                   'literacy rate', 'higher education reform'],
        'medium': ['school', 'university', 'student', 'teacher', 'education',
                   'degree', 'exam', 'curriculum', 'scholarship', 'college'],
        'low':    ['class', 'course', 'campus', 'learning', 'faculty', 'grade'],
    },
}

_CATEGORY_PRIORITY = [
    'Crime', 'Health', 'Science', 'Technology',
    'Sports', 'Business', 'World', 'Politics', 'Education'
]

#  SECTION 4 — NEWS SUMMARIZER CLASS

class NewsSummarizer:

    def __init__(self):
        # ── Stop words ─────────────────────────────────────────
        self.stop_words = set(stopwords.words('english'))
        self.stop_words.update([
            'said', 'says', 'say', 'told', 'added', 'noted', 'stated',
            'announced', 'confirmed', 'reported', 'according',
            'also', 'would', 'could', 'may', 'might', 'shall',
            'one', 'two', 'three', 'four', 'five',
            'new', 'year', 'years', 'time', 'day', 'week', 'month',
            'us', 'u.s.', 'get', 'got', 'make', 'made', 'take', 'taken',
            'first', 'second', 'last', 'next', 'many', 'much',
        ])
        
    #  STEP 1 — PREPROCESSING
    def preprocess_text(self, text: str) -> str:
        text = text.replace('\u2018', "'").replace('\u2019', "'")   # ' '
        text = text.replace('\u201c', '"').replace('\u201d', '"')   # " "
        text = text.replace('\u2032', "'")                          # prime ′

        text = text.replace('\u2014', ' ').replace('\u2013', ' ')   # — –
        text = text.replace('--', ' ')

        text = re.sub(r'https?://\S+|www\.\S+', '', text)

        text = re.sub(r'\S+@\S+\.\S+', '', text)
        
        text = re.sub(r"(\w)'s\b", r'\1s', text)
        text = re.sub(r"(\w)'(\w)", r'\1\2', text)  # don't → dont

        text = re.sub(r'[^\w\s\.\!\?\,\;\:\-]', ' ', text)

        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    #  STEP 2 — SENTENCE TOKENISATION
    def split_into_sentences(self, text: str) -> list:
        raw = sent_tokenize(text)
        return [s.strip() for s in raw if len(s.split()) >= MIN_SENTENCE_WORDS]

    #  STEP 3 — STOP-WORD REMOVAL  (unchanged logic, wider list)
    def remove_stopwords(self, text: str) -> list:
        words = word_tokenize(text.lower())
        return [
            w for w in words
            if w not in self.stop_words
            and w not in string.punctuation
            and w.isalpha()
            and len(w) > 1
        ]

    #  STEP 4 — WORD FREQUENCY CALCULATION
    def calculate_word_frequency(self, text: str) -> dict:
        words = self.remove_stopwords(text)
        freq  = Counter(words)
        if freq:
            max_f = max(freq.values())
            freq  = {w: c / max_f for w, c in freq.items()}
            #new_freq = {}
            #for w, c in freq.items():
            #   new_freq[w] = c / max_f
        return dict(freq)

    #  STEP 5 — BASE SENTENCE SCORING  (frequency-density)
    def score_sentences(self, sentences: list, word_freq: dict) -> dict:
        scores = {}
        for sentence in sentences:
            words     = word_tokenize(sentence.lower())
            total     = sum(word_freq.get(w, 0.0) for w in words)
            hit_count = sum(1 for w in words if w in word_freq)
            if hit_count > 0:
                scores[sentence] = total / hit_count   # density score
        return scores
 
    #  STEP 6 — POSITION-BASED BOOST
    #  Boost values (configurable above):
    #    Index 0      → +POSITION_FIRST_BOOST  (0.30)
    #    Index 1      → +POSITION_SECOND_BOOST (0.20)
    #    Index 2–4    → +POSITION_EARLY_BOOST  (0.10)
    #    Index 5+     → no boost
    def apply_position_boost(self, scores: dict, sentences: list) -> dict:
        for i, sentence in enumerate(sentences):
            if sentence not in scores:
                continue
            if i == 0:
                scores[sentence] += POSITION_FIRST_BOOST
            elif i == 1:
                scores[sentence] += POSITION_SECOND_BOOST
            elif i <= 4:
                scores[sentence] += POSITION_EARLY_BOOST
        return scores

    #  STEP 7 — TITLE / HEADLINE KEYWORD BOOST

    def apply_title_boost(self, scores: dict, sentences: list,
                          title: str) -> dict:
        if not title or not title.strip():
            return scores   # nothing to do

        title_words = set(self.remove_stopwords(title))
        if not title_words:
            return scores

        for sentence in sentences:
            if sentence not in scores:
                continue
            sent_lower = set(word_tokenize(sentence.lower()))
            # Count how many title keywords appear in this sentence
            matches = len(title_words & sent_lower)
            if matches > 0:
                scores[sentence] += TITLE_KEYWORD_BOOST * matches

        return scores


    #  STEP 8 — NAMED-ENTITY BOOST  (pure regex, no ML)

    def count_entities(self, sentence: str) -> int:
        total = 0
        for pattern in ENTITY_PATTERNS:
            total += len(pattern.findall(sentence))
        return min(total, ENTITY_CAP)

    def apply_entity_boost(self, scores: dict, sentences: list) -> dict:
        for sentence in sentences:
            if sentence not in scores:
                continue
            entity_count = self.count_entities(sentence)
            if entity_count > 0:
                scores[sentence] += ENTITY_BOOST * entity_count
        return scores


    #  STEP 9 — LENGTH PENALTY
    def apply_length_penalty(self, scores: dict, sentences: list) -> dict:
        for sentence in sentences:
            if sentence not in scores:
                continue
            word_count = len(sentence.split())
            if word_count > LONG_SENTENCE_THRESHOLD:
                excess  = word_count - LONG_SENTENCE_THRESHOLD
                penalty = LONG_SENTENCE_PENALTY * (excess / LONG_SENTENCE_THRESHOLD)
                scores[sentence] = max(0.0, scores[sentence] - penalty)
        return scores


    #  STEP 10 — REDUNDANCY REDUCTION  (Jaccard Similarity)
    @staticmethod
    def jaccard_similarity(set_a: set, set_b: set) -> float:
        if not set_a or not set_b:
            return 0.0
        intersection = len(set_a & set_b)
        union        = len(set_a | set_b)
        return intersection / union if union > 0 else 0.0

    def select_diverse_sentences(self, scores: dict, sentences: list,
                                  n: int) -> list:
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        selected            = []   # chosen sentences (text)
        selected_word_sets  = []   # word sets of chosen sentences (for Jaccard)

        for sentence, _score in ranked:
            if len(selected) >= n:
                break
            candidate_words = set(self.remove_stopwords(sentence))
            too_similar = any(
                self.jaccard_similarity(candidate_words, existing) > SIMILARITY_THRESHOLD
                for existing in selected_word_sets
            )

            if not too_similar:
                selected.append(sentence)
                selected_word_sets.append(candidate_words)

        return selected

    #  STEP 11 — SUMMARY ASSEMBLY

    def assemble_summary(self, sentences: list, selected: list) -> str:

        # Preserve original order using a set for O(1) lookup
        selected_set = set(selected)
        ordered = [s for s in sentences if s in selected_set]
        return ' '.join(ordered)


    #  IMPROVED CATEGORY DETECTION
    def detect_category(self, text: str) -> tuple:
        text_lower = text.lower()
        scores = {}

        for cat, tiers in CATEGORY_KEYWORDS.items():
            score  = 0
            score += sum(3 for kw in tiers.get('high',   []) if kw in text_lower)
            score += sum(2 for kw in tiers.get('medium', []) if kw in text_lower)
            score += sum(1 for kw in tiers.get('low',    []) if kw in text_lower)
            scores[cat] = score

        best_score = max(scores.values())

        if best_score == 0:
            return ('General', 0)

        # Collect all categories tied at the highest score
        top_cats = [c for c, s in scores.items() if s == best_score]

        if len(top_cats) == 1:
            return (top_cats[0], best_score)

        # Tie-break: prefer more specific category
        for cat in _CATEGORY_PRIORITY:
            if cat in top_cats:
                return (cat, best_score)

        return (top_cats[0], best_score)

 
    #  PUBLIC API — generate_summary()
    def generate_summary(self, text: str, num_sentences: int = 3,
                          title: str = '') -> dict:

        # ── Input validation ────────────────────────────────────
        if len(text.split()) < 30:
            return {'error': 'Article too short. Please provide at least 30 words.',
                    'sentences': []}

        # ── Step 1: Preprocess ──────────────────────────────────
        clean_text = self.preprocess_text(text)

        # ── Step 2: Tokenize ────────────────────────────────────
        sentences = self.split_into_sentences(clean_text)
        if len(sentences) < 2:
            return {'error': 'Could not detect enough sentences. Try adding more text.',
                    'sentences': sentences}

        # ── Steps 3 & 4: Frequencies ────────────────────────────
        word_freq = self.calculate_word_frequency(clean_text)

        # ── Step 5: Base sentence scores ────────────────────────
        scores = self.score_sentences(sentences, word_freq)

        # ── Step 6: Position boost ──────────────────────────────
        scores = self.apply_position_boost(scores, sentences)

        # ── Step 7: Title keyword boost ─────────────────────────
        scores = self.apply_title_boost(scores, sentences, title)

        # ── Step 8: Named-entity boost ──────────────────────────
        scores = self.apply_entity_boost(scores, sentences)

        # ── Step 9: Length penalty ──────────────────────────────
        scores = self.apply_length_penalty(scores, sentences)

        # ── Step 10: Diverse sentence selection ─────────────────
        n= min(num_sentences, len(sentences))
        top_sentences  = self.select_diverse_sentences(scores, sentences, n)

        # ── Step 11: Assemble in original order ─────────────────
        summary = self.assemble_summary(sentences, top_sentences)

        # ── Category detection ──────────────────────────────────
        category, confidence = self.detect_category(clean_text)

        # ── Analytics ───────────────────────────────────────────
        top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:12]
        original_wc  = len(text.split())
        summary_wc   = len(summary.split())

        return {
            'original_text':       text,
            'clean_text':          clean_text,
            'sentences':           sentences,
            'word_freq':           word_freq,
            'sentence_scores':     scores,
            'top_sentences':       top_sentences,
            'summary':             summary,
            'top_keywords':        top_keywords,
            'category':            category,
            'category_confidence': confidence,
            'stats': {
                'original_word_count':     original_wc,
                'summary_word_count':      summary_wc,
                'original_sentence_count': len(sentences),
                'summary_sentence_count':  len(top_sentences),
                'compression_ratio':       round(summary_wc / original_wc * 100, 1),
            }
        }


