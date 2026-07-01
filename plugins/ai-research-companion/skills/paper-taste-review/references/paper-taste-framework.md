# Paper Taste Review Framework

Use this framework for deep paper reading. The output should train academic taste, engineering taste, failure-case thinking, research opportunity design, and expert communication.

## A. One-Sentence Summary

Format:

```text
This paper proposes ____ to solve ____. The core idea is ____, and its main value is ____.
```

Requirements:

- Include problem, method, and value.
- Avoid jargon stacking.
- Do not merely paraphrase the title.
- Make it understandable to an AI/CS reader outside the exact subfield.

## B. What Problem Is the Paper Really Solving?

Answer:

```text
Surface problem:
Deep technical challenge:
Why it matters:
Long-term problem or short-term benchmark problem:
Generality:
Worth long-term following:
```

Good problems usually affect a class of tasks, come from real failure cases, and can generate follow-up research.

## C. Core Assumptions

Find the key assumptions:

- Data assumptions
- Model assumptions
- Task/environment assumptions
- Evaluation assumptions
- Engineering assumptions

Format:

```text
Key assumption 1:
Key assumption 2:
Key assumption 3:

Most fragile assumption:
If this assumption fails, the method may:
```

## D. Method Decomposition: Essence vs Packaging

Use this table:

| Component | Role | Essential? | Alternative | Possible issue |
| --- | --- | --- | --- | --- |
| Component A |  | High / Medium / Low |  |  |
| Component B |  | High / Medium / Low |  |  |

Then answer:

```text
The real core insight is:
The part most likely to be engineering packaging or empirical trick is:
If I could keep only one design, I would keep:
```

Definitions:

- Essential contribution: removing it makes the method fail conceptually.
- Engineering packaging: improves results but is not the root reason.
- Tuning trick: may only work in a narrow setting.
- Expression packaging: sounds new but is close to prior work.

## E. Are the Experiments Convincing?

Evaluate evidence quality, not only result quality.

Check:

- Are baselines strong?
- Do ablations answer the core question?
- Are metrics appropriate?
- Are failure examples analyzed?
- Are there cross-dataset, cross-setting, or cross-scale tests?
- Could results come from tuning, leakage, implementation differences, or compute advantage?
- Does the paper explain why it works, not only that it works?

Format:

```text
Most convincing experiment:
Weakest experiment:
Missing key ablation:
Experiment I most want to add:
Experiment credibility score: __/5
```

## F. Failure Case Analysis

This is mandatory and central.

Analyze possible failures under:

- data distribution shift
- longer or more complex tasks
- noisy inputs
- metric changes
- model scale changes
- real deployment
- adversarial or edge cases
- resource constraints
- human interaction or multi-turn settings
- composition with other systems

Format:

```text
Possible failure case 1:
Why it fails:
How to validate:

Possible failure case 2:
Why it fails:
How to validate:

Possible failure case 3:
Why it fails:
How to validate:

Shared technical challenge behind these failures:
Can this challenge become my research question:
```

## G. Academic Taste Score

Use 1-5 scores:

| Dimension | Score | Reason |
| --- | --- | --- |
| Problem importance | /5 |  |
| Problem generality | /5 |  |
| Core insight clarity | /5 |  |
| Method simplicity | /5 |  |
| Evidence strength | /5 |  |
| Follow-up inspiration | /5 |  |
| Long-term value | /5 |  |

Classify:

- A. Direction-level contribution
- B. Method-level contribution
- C. Engineering-level contribution
- D. Benchmark / dataset contribution
- E. Incremental improvement
- F. Mostly packaging existing ideas

## H. Engineering Taste Score

Use 1-5 scores:

| Dimension | Score | Reason |
| --- | --- | --- |
| Simplicity | /5 |  |
| Reproducibility | /5 |  |
| Modularity | /5 |  |
| Debuggability | /5 |  |
| Scalability | /5 |  |
| Resource friendliness | /5 |  |
| Reusability | /5 |  |

Then answer:

```text
Engineering taste highlight:
Least clean engineering part:
Biggest reproduction risk:
For a minimal reimplementation, I would keep:
```

## I. What Can I Learn?

Academic taste:

```text
Selection taste this paper teaches:
Argument style this paper teaches:
Research trap this paper warns against:
```

Engineering taste:

```text
System design habit this paper teaches:
Implementation pattern worth copying:
Engineering complexity not worth copying:
```

Expression taste:

```text
Storyline:
How it argues the problem is important:
How it explains the method:
Writing move I can imitate:
```

## J. Literature Tree Position

Output:

```text
Research direction:
Subproblem:
Inherited ideas:
Assumptions it challenges or revises:
Difference from classic methods:
Difference from recent methods:
```

Then give a simplified tree:

```text
Direction:
  - Subdirection 1:
    - Representative papers:
    - Current challenge:
  - Subdirection 2:
    - Representative papers:
    - Current challenge:
  - This paper's position:
```

## K. Follow-Up Work

Give three levels.

1. Minimal reproduction:

```text
What I should reproduce first:
Minimum components:
Most likely bug:
Success criterion:
```

2. Stress test / failure-case experiment:

```text
Stress test:
Purpose:
Expected exposed issue:
If the result holds, it means:
```

3. Project ideas:

```text
Project idea 1:
Core problem:
Why it matters:
Minimum validation:
Possible contribution form: analysis / benchmark / method / system / paper / repo

Project idea 2:
Core problem:
Why it matters:
Minimum validation:
Possible contribution form:
```

## L. Expert Communication Prep

Generate concrete questions:

```text
Question for the author 1:
Why this is worth asking:

Question for the author 2:
Why this is worth asking:

Question for a field expert:
Research value behind this question:
```

Then generate an opener:

```text
Hello, I recently read your work on ____. My understanding is that the core idea is ____.
While reproducing / thinking about it, I noticed a possible failure case: ____.
My question is: ____.
I would like to further test ____. Do you think this direction is valuable?
```

## M. Paper Card

Generate a card suitable for the research notebook:

```text
# Paper Card

## Paper
Title:
Authors:
Year:
Area:

## One-Sentence Contribution

## Core Problem

## Core Method

## Real Insight

## Most Important Experimental Result

## Most Fragile Assumption

## Possible Failure Cases
1.
2.
3.

## Academic Taste
Problem importance:
Method simplicity:
Experiment credibility:
Long-term value:

## Engineering Taste
Reproduction difficulty:
Engineering complexity:
Scalability:
Reusability:

## Taste I Learned

## Follow-Up I Can Do
1.
2.
3.

## Expert Question

## Worth Following Deeply
Yes / No / Watch

Reason:
```

## N. Action Grade

Do not end at summary. Choose one:

- A. Awareness only: know its position, no deep follow-up.
- B. Worth careful rereading: method and experiments deserve another pass.
- C. Worth reproducing: important baseline or engineering artifact.
- D. Worth developing: failure case or setting can become a project.

Output:

```text
Recommended action grade: A / B / C / D
Reason:
Minimum next action:
```

At the end, provide exactly three next options:

```text
Option A - conservative:
Option B - recommended:
Option C - ambitious:
```
