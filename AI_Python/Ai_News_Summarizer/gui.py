"""
=============================================================
  gui.py — Graphical User Interface (Tkinter)
  AI News Summarizer Agent
  Run with:  python gui.py
=============================================================
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
from summarizer import NewsSummarizer

# ─── COLOR PALETTE ────────────────────────────────────────────────────────────
BG_DARK    = "#1e1e2e"   # main background
BG_PANEL   = "#2a2a3e"   # panel / frame background
BG_INPUT   = "#12121f"   # text input background
ACCENT     = "#7c6af7"   # purple accent
ACCENT2    = "#56cfb2"   # teal accent
TEXT_MAIN  = "#cdd6f4"   # primary text
TEXT_DIM   = "#6c7086"   # dimmed text
TEXT_WARN  = "#f38ba8"   # warning / error
TEXT_OK    = "#a6e3a1"   # success
CARD_BG    = "#313244"   # card background
BORDER     = "#45475a"   # border colour

FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_HEAD  = ("Segoe UI", 11, "bold")
FONT_BODY  = ("Segoe UI", 10)
FONT_MONO  = ("Consolas", 10)
FONT_SMALL = ("Segoe UI", 9)


# ─── MAIN APPLICATION ─────────────────────────────────────────────────────────

class NewsApp(tk.Tk):
    """Root window — holds the full GUI."""

    def __init__(self):
        super().__init__()
        self.summarizer = NewsSummarizer()
        self.result = None

        self.title("AI News Summarizer — Rule-Based AI System")
        self.geometry("1200x800")
        self.minsize(900, 600)
        self.configure(bg=BG_DARK)

        self._build_ui()
        self._load_sample()

    # ── UI construction ────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Top header bar ──────────────────────────────────────────────────
        header = tk.Frame(self, bg=ACCENT, height=60)
        header.pack(fill='x')
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🧠  AI News Summarizer Agent",
            font=FONT_TITLE, bg=ACCENT, fg="white"
        ).pack(side='left', padx=20, pady=12)

        tk.Label(
            header,
            text="Rule-Based NLP  |  Extractive Summarization",
            font=FONT_SMALL, bg=ACCENT, fg="#ddd"
        ).pack(side='right', padx=20)

        # ── Main body (left + right panes) ────────────────────────────────
        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill='both', expand=True, padx=12, pady=10)

        # Left panel — input
        left = tk.Frame(body, bg=BG_DARK)
        left.pack(side='left', fill='both', expand=True, padx=(0, 6))
        self._build_input_panel(left)

        # Right panel — output
        right = tk.Frame(body, bg=BG_DARK)
        right.pack(side='right', fill='both', expand=True, padx=(6, 0))
        self._build_output_panel(right)

        # ── Status bar ──────────────────────────────────────────────────────
        self.status_var = tk.StringVar(value="Ready — paste an article and click Summarize")
        status_bar = tk.Frame(self, bg=BG_PANEL, height=28)
        status_bar.pack(fill='x', side='bottom')
        tk.Label(
            status_bar,
            textvariable=self.status_var,
            bg=BG_PANEL, fg=TEXT_DIM, font=FONT_SMALL
        ).pack(side='left', padx=10, pady=4)

    # ── Left (input) panel ─────────────────────────────────────────────────────

    def _build_input_panel(self, parent):
        self._section_label(parent, "📄  Input News Article")

        # Options row
        opts = tk.Frame(parent, bg=BG_DARK)
        opts.pack(fill='x', pady=(0, 6))

        tk.Label(opts, text="Summary sentences:", bg=BG_DARK,
                 fg=TEXT_MAIN, font=FONT_BODY).pack(side='left', padx=(0, 6))

        self.n_var = tk.IntVar(value=3)
        for n in range(1, 6):
            tk.Radiobutton(
                opts, text=str(n), variable=self.n_var, value=n,
                bg=BG_DARK, fg=TEXT_MAIN, selectcolor=ACCENT,
                activebackground=BG_DARK, activeforeground=ACCENT,
                font=FONT_BODY
            ).pack(side='left', padx=2)

        # Input text area
        self.input_text = scrolledtext.ScrolledText(
            parent, wrap='word', font=FONT_BODY,
            bg=BG_INPUT, fg=TEXT_MAIN, insertbackground=ACCENT,
            relief='flat', padx=10, pady=10,
            selectbackground=ACCENT, selectforeground='white'
        )
        self.input_text.pack(fill='both', expand=True)

        # Button row
        btn_row = tk.Frame(parent, bg=BG_DARK)
        btn_row.pack(fill='x', pady=(8, 0))

        self._btn(btn_row, "🗒  Load File",   self._load_file,    CARD_BG).pack(side='left', padx=(0, 6))
        self._btn(btn_row, "📋  Sample",      self._load_sample,  CARD_BG).pack(side='left', padx=(0, 6))
        self._btn(btn_row, "🗑  Clear",        self._clear_input,  CARD_BG).pack(side='left')

        self._btn(
            btn_row, "▶  SUMMARIZE",
            self._run_summarize, ACCENT
        ).pack(side='right')

        # Word count label
        self.wc_var = tk.StringVar(value="0 words")
        tk.Label(parent, textvariable=self.wc_var,
                 bg=BG_DARK, fg=TEXT_DIM, font=FONT_SMALL).pack(anchor='e')

        self.input_text.bind('<KeyRelease>', self._update_word_count)

    # ── Right (output) panel ───────────────────────────────────────────────────

    def _build_output_panel(self, parent):
        self._section_label(parent, "📝  Results")

        # Notebook (tabs)
        style = ttk.Style(self)
        style.theme_use('default')
        style.configure(
            'Custom.TNotebook',
            background=BG_PANEL, tabmargins=[2, 2, 2, 0]
        )
        style.configure(
            'Custom.TNotebook.Tab',
            background=CARD_BG, foreground=TEXT_MAIN,
            padding=[12, 5], font=FONT_BODY
        )
        style.map(
            'Custom.TNotebook.Tab',
            background=[('selected', ACCENT)],
            foreground=[('selected', 'white')]
        )

        nb = ttk.Notebook(parent, style='Custom.TNotebook')
        nb.pack(fill='both', expand=True)

        # Tab 1: Summary
        t1 = tk.Frame(nb, bg=BG_PANEL)
        nb.add(t1, text='  Summary  ')
        self._build_summary_tab(t1)

        # Tab 2: Keywords
        t2 = tk.Frame(nb, bg=BG_PANEL)
        nb.add(t2, text='  Keywords  ')
        self._build_keywords_tab(t2)

        # Tab 3: Sentences
        t3 = tk.Frame(nb, bg=BG_PANEL)
        nb.add(t3, text='  Sentences  ')
        self._build_sentences_tab(t3)

        # Tab 4: Stats
        t4 = tk.Frame(nb, bg=BG_PANEL)
        nb.add(t4, text='  Statistics  ')
        self._build_stats_tab(t4)

        # Save button
        self._btn(parent, "💾  Save Report", self._save_report, ACCENT2).pack(
            anchor='e', pady=(8, 0)
        )

    def _build_summary_tab(self, parent):
        # Category badge
        info_row = tk.Frame(parent, bg=BG_PANEL)
        info_row.pack(fill='x', padx=10, pady=(10, 4))

        tk.Label(info_row, text="Category:", bg=BG_PANEL,
                 fg=TEXT_DIM, font=FONT_SMALL).pack(side='left')

        self.cat_var = tk.StringVar(value="—")
        tk.Label(info_row, textvariable=self.cat_var, bg=ACCENT,
                 fg='white', font=FONT_SMALL, padx=8, pady=2).pack(side='left', padx=6)

        # Summary text
        self.summary_text = scrolledtext.ScrolledText(
            parent, wrap='word', font=("Segoe UI", 11),
            bg=CARD_BG, fg=TEXT_MAIN, relief='flat',
            padx=14, pady=14, height=8,
            selectbackground=ACCENT, selectforeground='white'
        )
        self.summary_text.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        self.summary_text.config(state='disabled')

    def _build_keywords_tab(self, parent):
        self.kw_canvas = tk.Canvas(parent, bg=BG_PANEL, highlightthickness=0)
        kw_scroll = ttk.Scrollbar(parent, orient='vertical',
                                  command=self.kw_canvas.yview)
        self.kw_canvas.configure(yscrollcommand=kw_scroll.set)
        kw_scroll.pack(side='right', fill='y')
        self.kw_canvas.pack(fill='both', expand=True, padx=10, pady=10)
        self.kw_frame = tk.Frame(self.kw_canvas, bg=BG_PANEL)
        self.kw_canvas.create_window((0, 0), window=self.kw_frame, anchor='nw')
        self.kw_frame.bind('<Configure>',
                           lambda e: self.kw_canvas.configure(
                               scrollregion=self.kw_canvas.bbox('all')))

    def _build_sentences_tab(self, parent):
        self.sent_text = scrolledtext.ScrolledText(
            parent, wrap='word', font=FONT_BODY,
            bg=CARD_BG, fg=TEXT_MAIN, relief='flat',
            padx=14, pady=14,
            selectbackground=ACCENT, selectforeground='white'
        )
        self.sent_text.pack(fill='both', expand=True, padx=10, pady=10)
        self.sent_text.tag_config('highlight', background='#2d3250', foreground=ACCENT2)
        self.sent_text.tag_config('rank',      foreground=ACCENT, font=FONT_HEAD)
        self.sent_text.tag_config('score',     foreground=TEXT_DIM, font=FONT_SMALL)
        self.sent_text.config(state='disabled')

    def _build_stats_tab(self, parent):
        self.stats_frame = tk.Frame(parent, bg=BG_PANEL)
        self.stats_frame.pack(fill='both', expand=True, padx=16, pady=16)

    # ── Widget helpers ─────────────────────────────────────────────────────────

    def _section_label(self, parent, text: str):
        tk.Label(parent, text=text, bg=BG_DARK, fg=ACCENT,
                 font=FONT_HEAD).pack(anchor='w', pady=(0, 6))

    def _btn(self, parent, text, command, color):
        return tk.Button(
            parent, text=text, command=command,
            bg=color, fg='white', relief='flat',
            font=FONT_BODY, padx=12, pady=6,
            activebackground=ACCENT, activeforeground='white',
            cursor='hand2'
        )

    # ── Actions ────────────────────────────────────────────────────────────────

    def _load_file(self):
        path = filedialog.askopenfilename(
            title="Open Article File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if path:
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
            self.input_text.delete('1.0', 'end')
            self.input_text.insert('1.0', text)
            self._update_word_count()
            self.status_var.set(f"Loaded: {path}")

    def _load_sample(self, _=None):
        sample = (
            "Scientists at NASA have announced a groundbreaking discovery that could change our "
            "understanding of Mars. The Mars Perseverance rover, which landed on the red planet "
            "in February 2021, has found chemical signatures that suggest ancient microbial life "
            "may have once existed beneath the Martian surface.\n\n"
            "The rover collected rock samples from the Jezero Crater, an ancient lake bed believed "
            "to have contained liquid water billions of years ago. Analysis of these samples "
            "revealed organic molecules and mineral deposits consistent with biological activity, "
            "according to the research team.\n\n"
            "'This is the most significant finding in the history of Mars exploration,' said lead "
            "scientist Dr. Sarah Chen. 'While we cannot confirm life definitively, the evidence "
            "strongly suggests Mars had the right conditions to support it.'\n\n"
            "NASA plans to return the collected samples to Earth by 2033 through a joint mission "
            "with the European Space Agency. Once on Earth, the samples will be analyzed using "
            "advanced laboratory equipment far more sophisticated than anything currently on Mars. "
            "The finding also has major implications for the search for life elsewhere in the "
            "universe. If life once existed on Mars, scientists believe the chances of finding "
            "life on other planets are significantly higher."
        )
        self.input_text.delete('1.0', 'end')
        self.input_text.insert('1.0', sample)
        self._update_word_count()

    def _clear_input(self):
        self.input_text.delete('1.0', 'end')
        self.wc_var.set("0 words")

    def _update_word_count(self, _=None):
        text = self.input_text.get('1.0', 'end')
        count = len(text.split())
        self.wc_var.set(f"{count} words")

    def _run_summarize(self):
        article = self.input_text.get('1.0', 'end').strip()
        if len(article.split()) < 30:
            messagebox.showwarning(
                "Too Short",
                "Please provide an article with at least 30 words."
            )
            return
        self.status_var.set("⏳ Processing …")
        threading.Thread(target=self._do_summarize, args=(article,), daemon=True).start()

    def _do_summarize(self, article: str):
        result = self.summarizer.generate_summary(article, num_sentences=self.n_var.get())
        self.after(0, self._show_results, result)

    def _show_results(self, result: dict):
        if 'error' in result:
            messagebox.showerror("Error", result['error'])
            self.status_var.set("Error — see message")
            return

        self.result = result

        # ── Summary tab ──────────────────────────────────────────────────────
        self.cat_var.set(f"  {result['category']}  ")
        self.summary_text.config(state='normal')
        self.summary_text.delete('1.0', 'end')
        self.summary_text.insert('1.0', result['summary'])
        self.summary_text.config(state='disabled')

        # ── Keywords tab ─────────────────────────────────────────────────────
        for w in self.kw_frame.winfo_children():
            w.destroy()

        tk.Label(
            self.kw_frame, text="Important Keywords (normalised frequency)",
            bg=BG_PANEL, fg=TEXT_DIM, font=FONT_SMALL
        ).grid(row=0, columnspan=3, sticky='w', pady=(0, 8))

        for i, (word, freq) in enumerate(result['top_keywords'], 1):
            bar_len = max(int(freq * 200), 4)
            tk.Label(self.kw_frame, text=f"{i:2}. {word}",
                     bg=BG_PANEL, fg=TEXT_MAIN, font=FONT_BODY,
                     width=18, anchor='w').grid(row=i, column=0, sticky='w', pady=2)
            tk.Frame(self.kw_frame, bg=ACCENT, height=18,
                     width=bar_len).grid(row=i, column=1, sticky='w', padx=6)
            tk.Label(self.kw_frame, text=f"{freq:.3f}",
                     bg=BG_PANEL, fg=TEXT_DIM, font=FONT_SMALL).grid(row=i, column=2)

        # ── Sentences tab ────────────────────────────────────────────────────
        self.sent_text.config(state='normal')
        self.sent_text.delete('1.0', 'end')

        ranked = sorted(
            result['sentence_scores'].items(),
            key=lambda x: x[1], reverse=True
        )
        for i, (sent, score) in enumerate(ranked[:5], 1):
            is_in_summary = sent in result['top_sentences']
            self.sent_text.insert('end', f"#{i}  ", 'rank')
            self.sent_text.insert('end', f"(score: {score:.4f})  ", 'score')
            flag = " ← IN SUMMARY" if is_in_summary else ""
            self.sent_text.insert('end', flag + '\n', 'highlight' if is_in_summary else 'score')
            tag = 'highlight' if is_in_summary else None
            if tag:
                self.sent_text.insert('end', sent + '\n\n', tag)
            else:
                self.sent_text.insert('end', sent + '\n\n')

        self.sent_text.config(state='disabled')

        # ── Stats tab ────────────────────────────────────────────────────────
        for w in self.stats_frame.winfo_children():
            w.destroy()

        stats_data = [
            ("Original Word Count",       result['stats']['original_word_count'],   TEXT_MAIN),
            ("Summary Word Count",         result['stats']['summary_word_count'],     ACCENT2),
            ("Original Sentence Count",    result['stats']['original_sentence_count'],TEXT_MAIN),
            ("Summary Sentence Count",     result['stats']['summary_sentence_count'], ACCENT2),
            ("Compression Ratio",          f"{result['stats']['compression_ratio']}%",ACCENT),
            ("Detected Category",          result['category'],                         TEXT_OK),
            ("Unique Important Words",     len(result['word_freq']),                   TEXT_MAIN),
        ]

        for r, (label, value, color) in enumerate(stats_data):
            tk.Label(self.stats_frame, text=label, bg=BG_PANEL,
                     fg=TEXT_DIM, font=FONT_BODY, anchor='w', width=28
                     ).grid(row=r, column=0, sticky='w', pady=6)
            tk.Label(self.stats_frame, text=str(value), bg=BG_PANEL,
                     fg=color, font=FONT_HEAD
                     ).grid(row=r, column=1, sticky='w', padx=14)

        s = result['stats']
        self.status_var.set(
            f"Done — {s['original_word_count']} words → {s['summary_word_count']} words "
            f"({s['compression_ratio']}% of original)"
        )

    def _save_report(self):
        if not self.result:
            messagebox.showinfo("Nothing to save", "Please summarize an article first.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension='.txt',
            filetypes=[("Text file", "*.txt")],
            initialfile='summary_report.txt',
            title="Save Report"
        )
        if path:
            self.summarizer.save_summary(self.result, path)
            messagebox.showinfo("Saved", f"Report saved to:\n{path}")
            self.status_var.set(f"Saved → {path}")


# ─── ENTRY POINT ─────────────────────────────────────────────────────────────

def main():
    app = NewsApp()
    app.mainloop()


if __name__ == '__main__':
    main()
