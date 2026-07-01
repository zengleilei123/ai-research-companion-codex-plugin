---
name: paper-taste-review
description: Read and judge a single academic paper or paper plus repo for academic taste, engineering taste, core contribution, hidden assumptions, method essence versus packaging, experiment credibility, failure cases, literature-tree position, follow-up experiments, paper-card notes, and expert discussion questions. Use when the user asks to use Taste Skill, read a paper deeply, judge whether a paper is worth following, turn a paper into research opportunities, or evaluate both academic and engineering quality beyond ordinary summary.
---

# Paper Taste Review Skill

## Overview

Use this skill to turn paper reading into judgment training. The goal is not to summarize what the authors did; the goal is to decide what problem matters, what contribution is essential, where the method fails, whether the engineering is clean, and what research action should follow.

## Required Reminder

Before the analysis, remind the human:

- Do not only ask what the paper did; ask why the problem is worth doing.
- Do not only ask whether the result is good; ask whether the evidence supports the claim.
- Do not only ask how to add a module; ask whether the failure case reveals a more general problem.
- Do not chase SOTA only; train the ability to identify essential problems, temporary tricks, and reusable insights.

## Inputs

Accept any subset of:

- paper title, abstract, PDF text, arXiv link, DOI, or citation
- official repo or implementation notes
- the human's reading notes
- the human's current research direction or idea

If source material is incomplete, analyze what is available and mark uncertain judgments explicitly.

## Workflow

1. Load `references/paper-taste-framework.md`.
2. Identify whether this is paper-only, paper-plus-repo, or partial metadata.
3. If the user supplied a URL/PDF/repo and browsing or file tools are available, inspect primary sources before judging.
4. Separate verified claims from inference.
5. Produce the full A-N framework unless the user asks for a shorter version.
6. Generate a `Paper Card` suitable for saving to `knowledge/paper_cards/` or `knowledge/literature_reviews/`.
7. End with one action grade:
   - A: only need awareness
   - B: worth careful rereading
   - C: worth reproducing
   - D: worth developing into a project
8. End with exactly three recommended next options.

## Output Rules

- Be strict. A polished paper can still have weak taste.
- Do not confuse benchmark gains with essential contribution.
- Do not invent experimental evidence that is not in the supplied sources.
- Always include failure cases and how to validate them.
- Always distinguish academic taste from engineering taste.
- If there is an official repo, judge reproducibility, modularity, debuggability, and minimal reimplementation risk.
- If a paper creates a good follow-up idea, turn it into a falsifiable MVP or stress test.
