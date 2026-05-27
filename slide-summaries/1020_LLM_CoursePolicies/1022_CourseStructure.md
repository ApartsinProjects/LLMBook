# 1022_CourseStructure — Per-Slide Summary

**Source file:** `1022_CourseStructure.pptx`
**Source folder:** `SlidesPool/1020_LLM_CoursePolicies/`
**Drive link:** https://drive.google.com/file/d/1fFfQATurtuOYkydYvSlWxduY-oTeqlH9/view
**Slide count (exact, via python-pptx):** 11
**Extraction:** Local parse + slide PNG render. Slides 8, 10, and 11 were inspected visually because the python-pptx body was empty yet they carry the main pedagogical content.

---

## Slide 1 — About this Course
Title slide announcing that the deck covers the course structure and requirements.

## Slide 2 — Recent Graduate: Market Expectations
A five-row "Past vs. Current" table contrasts the old graduate profile (gradual on-the-job learning, reliance on study-era knowledge, basic interview puzzles, narrow specialization, customized standard solutions) with what employers now demand (value from day one, continuous tech adaptation, a complex portfolio project on modern stacks, integrating multiple technologies via AI, and solving genuinely new problems using AI-built blocks). The shift motivates the course's emphasis on portfolio-grade work.

## Slide 3 — This course is different
A five-row "Conventional vs. This course" table positions the course against typical instruction: rather than teaching standard individual tasks with tool-agnostic notation in a sequential order with an unguided end-of-course project, this course focuses on novel multi-component solutions, emerging concepts presented through modern libraries and code, guided project development with in-class checkpoints, and early exposure to advanced topics that are revisited in depth.

## Slide 4 — Progressive introduction of concepts
Lays out the five questions used to introduce each concept in the course: what does it do in terms of inputs and outputs, what is its API or library, how is it used to solve problems, how is it constructed and trained, and how can it be extended.

## Slide 5 — Code-first learning
The slide commits to presenting code fragments alongside concepts using state-of-the-art libraries (HuggingFace, PyTorch, others) for both model implementation and application. Objectives are to ground theory, give a starting point for the project, and build the skill of reading code (including AI-generated). Expectations are high-level understanding and the ability to sketch a solution skeleton, with technical details available on demand rather than memorized.

## Slide 6 — Course Project: In teams
Defines the team project scope: define a novel task or research question, generate synthetic training and evaluation data, train or fine-tune models, and compare with off-the-shelf pretrained models. The timeline lists Week 5 proposal, Week 9 interim with implemented baseline, Week 13 final presentation, in-class discussion sessions throughout, and a GitHub submission two weeks after the last class.

## Slide 7 — Focus: A valuable project in your portfolio
Warns against two failure modes: an exercise-like project (standard task with standard tools, which AI can do alone) and an over-ambitious long project (infeasible in course settings). The "smart project" sweet spot has technical depth, multiple components, and non-trivial design decisions, achieved with reasonable effort by reusing libraries, tools, and AI to demonstrate fast new-thing-building.

## Slide 8 — Project Objectives
Visual inspection shows three columns. "Fulfill coursework requirements" asks the student to demonstrate depth and breadth of knowledge in methods and models, attention to formal project requirements, and reasonable effort to achieve good performance. "Acquire knowledge and skills" asks for hands-on proficiency with software libraries, practice in innovative idea development by recombining and adapting building blocks, and opening one's mind to what is truly possible with AI. "Advance your career" asks the student to build a tangible demonstrable project that adds value to the resume, gain presentation and discussion confidence, and lay the ground for graduate studies or a research paper.

## Slide 9 — AI Tool Usage Policy
A single emphatic instruction: focus on project novelty.

## Slide 10 — Project is NOT
Visual inspection shows three icon-labeled negatives. The project is NOT a software-engineering exercise (code organization is not graded, though good organization helps iteration). It is NOT a re-implementation or code-googling exercise (reuse every available component or model and concentrate on the novelty element). It is NOT a perfect-model exercise (focus on methodology, scope, and novelty, while showing reasonable effort for good accuracy).

## Slide 11 — Common Pitfalls
Visual inspection reveals an eight-tile grid of pitfalls: obsessing over accuracy while neglecting data quality, ML methodology, scope, and methods; avoiding newly studied concepts in favor of prior knowledge; skipping iterative improvements to code, slides, or narrative; not reviewing class material on models, tools, and applications; deferring most coding to the end of the semester; ignoring formal requirements like slide and repo formats and due dates; neglecting presentation quality (slides, README, repo files, figures, diagrams); and black-box magical thinking, with no debugging, no inspection of failure cases, no preprocessing, and no hyperparameter tuning.

---

## Deck-level takeaway
The deck frames the course's structural philosophy and the rubric for student judgment. Two contrast tables (graduate market expectations, conventional teaching) justify a portfolio-first, code-first, project-guided approach. The middle slides specify how each concept is introduced (five-question lens), how code is used in lectures, and how the team project is scheduled and scoped. The closing trio of "Objectives", "Project is NOT", and "Common Pitfalls" gives students an explicit success criterion plus a list of anti-patterns to avoid, all centered on the theme that novelty and methodology matter more than engineering polish or accuracy chasing.
