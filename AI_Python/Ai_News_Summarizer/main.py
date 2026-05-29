"""
=============================================================
  main.py — Command-Line Interface (CLI)
  AI News Summarizer Agent
  Run with:  python main.py
=============================================================
"""

import os
from summarizer import NewsSummarizer


# ─── DISPLAY HELPERS ──────────────────────────────────────────────────────────

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    print("\n" + "=" * 62)
    print("       AI NEWS SUMMARIZER AGENT")
    print("       Rule-Based Extractive Summarization System")
    print("       University AI Lab Final Project")
    print("=" * 62)


def print_sep(char='─'):
    print('\n' + char * 62 + '\n')


def wrap_text(text: str, width: int = 58, indent: str = '  ') -> str:
    """Wrap long text to fit in terminal."""
    words  = text.split()
    lines  = []
    line   = indent
    for word in words:
        if len(line) + len(word) + 1 > width:
            lines.append(line)
            line = indent + word + ' '
        else:
            line += word + ' '
    if line.strip():
        lines.append(line)
    return '\n'.join(lines)


# ─── INPUT ────────────────────────────────────────────────────────────────────

def get_article() -> str:
    """Prompt user for news article (type directly or load from file)."""
    print("  How would you like to provide the article?\n")
    print("  [1] Type / Paste article here")
    print("  [2] Load from a .txt file")
    print("  [3] Use built-in sample article (for quick testing)")

    choice = input("\n  Enter choice (1/2/3): ").strip()

    if choice == '2':
        fname = input("  Enter file path: ").strip()
        try:
            with open(fname, 'r', encoding='utf-8') as fh:
                text = fh.read()
            print(f"\n  ✔ Loaded {len(text.split())} words from '{fname}'")
            return text
        except FileNotFoundError:
            print(f"\n  ✖ File not found: '{fname}'. Switching to manual input.\n")

    if choice == '3':
        return SAMPLE_ARTICLE

    # Manual paste
    print("\n  Paste or type your article below.")
    print("  Press Enter twice when finished.\n")
    lines = []
    empty = 0
    while empty < 2:
        line = input()
        if line == '':
            empty += 1
        else:
            empty = 0
            lines.append(line)
    return ' '.join(lines)


# ─── DISPLAY RESULTS ──────────────────────────────────────────────────────────

def display_results(result: dict):
    """Pretty-print the summarisation results."""
    stats = result['stats']

    print_sep('═')
    print(f"  📰  DETECTED CATEGORY : {result['category']}")
    print_sep()

    # Statistics table
    print("  📊  STATISTICS\n")
    print(f"  {'Original Words':<28} {stats['original_word_count']}")
    print(f"  {'Summary Words':<28} {stats['summary_word_count']}")
    print(f"  {'Original Sentences':<28} {stats['original_sentence_count']}")
    print(f"  {'Summary Sentences':<28} {stats['summary_sentence_count']}")
    print(f"  {'Compression (summary/original)':<28} {stats['compression_ratio']}%")

    print_sep()

    # Keywords bar chart
    print("  🔑  TOP KEYWORDS\n")
    for i, (word, freq) in enumerate(result['top_keywords'][:8], 1):
        bar = '█' * int(freq * 22)
        print(f"  {i:2}. {word:<18} {bar:<24} {freq:.3f}")

    print_sep()

    # Important sentences
    print("  ⭐  IMPORTANT SENTENCES (ranked by score)\n")
    ranked = sorted(
        result['sentence_scores'].items(),
        key=lambda x: x[1], reverse=True
    )
    for i, (sent, score) in enumerate(ranked[:3], 1):
        print(f"  #{i}  Score: {score:.4f}")
        print(wrap_text(sent))
        print()

    print_sep('═')
    print("  📝  GENERATED SUMMARY\n")
    print(wrap_text(result['summary']))
    print()


# ─── SAMPLE ARTICLE ───────────────────────────────────────────────────────────

SAMPLE_ARTICLE = """
Scientists at NASA have announced a groundbreaking discovery that could
change our understanding of Mars. The Mars Perseverance rover, which landed
on the red planet in February 2021, has found chemical signatures that suggest
ancient microbial life may have once existed beneath the Martian surface.

The rover collected rock samples from the Jezero Crater, an ancient lake bed
believed to have contained liquid water billions of years ago. Analysis of
these samples revealed organic molecules and mineral deposits consistent with
biological activity, according to the research team.

"This is the most significant finding in the history of Mars exploration,"
said lead scientist Dr. Sarah Chen during a press conference at NASA
headquarters in Washington D.C. "While we cannot confirm life definitively,
the evidence strongly suggests Mars had the right conditions to support it."

The discovery has sparked intense debate in the scientific community. Some
researchers argue the organic compounds could have originated from
non-biological chemical reactions. However, the pattern and concentration of
molecules found align more closely with biological processes, researchers say.

NASA plans to return the collected samples to Earth by 2033 through a joint
mission with the European Space Agency. Once on Earth, the samples will be
analyzed using advanced laboratory equipment far more sophisticated than
anything currently on Mars. This will allow scientists to determine
conclusively whether life ever existed on the neighboring planet.

The finding also has major implications for the search for life elsewhere in
the universe. If life once existed on Mars, a planet far less hospitable than
Earth, scientists believe the chances of finding life on other planets and
moons throughout the cosmos are significantly higher.
"""


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    clear_screen()
    print_header()

    summarizer = NewsSummarizer()

    while True:
        print_sep()
        article = get_article()

        if len(article.strip().split()) < 30:
            print("\n  ✖ Article too short! Need at least 30 words. Please try again.")
            continue

        # Summary length
        print_sep()
        print("  How many sentences should the summary contain?\n")
        print("  [1] Very Short  — 1 sentence")
        print("  [2] Short       — 2 sentences")
        print("  [3] Medium      — 3 sentences  ← recommended")
        print("  [4] Detailed    — 4 sentences")

        n_raw = input("\n  Enter choice (1-4) [default=3]: ").strip()
        n     = int(n_raw) if n_raw.isdigit() and 1 <= int(n_raw) <= 4 else 3

        print("\n  ⏳  Processing article …\n")
        result = summarizer.generate_summary(article, num_sentences=n)

        if 'error' in result:
            print(f"\n  ✖ {result['error']}")
            continue

        display_results(result)

        # Save prompt
        save_choice = input("  💾  Save full report to file? (y/n): ").strip().lower()
        if save_choice == 'y':
            fname = input("  Enter filename [default: summary_output.txt]: ").strip()
            fname = fname if fname else 'summary_output.txt'
            saved = summarizer.save_summary(result, fname)
            print(f"\n  ✔ Report saved → {saved}")

        # Loop
        print_sep()
        again = input("  🔄  Summarize another article? (y/n): ").strip().lower()
        if again != 'y':
            print("\n  Thank you for using AI News Summarizer!")
            print("  — AI Lab Final Project\n")
            break


if __name__ == '__main__':
    main()
