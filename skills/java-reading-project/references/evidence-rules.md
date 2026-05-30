# Evidence Rules

## Mission

Define what counts as evidence in Java Reading Project. This file is the single source of truth for mastery evidence, transfer evidence, equipment evidence, ask-data limitations, passive-reading limitations, and precise mastery percentage eligibility.

Other references may cite this file, but they must not redefine mastery evidence.

## Evidence Categories

### Mastery Evidence

Mastery evidence means recorded learner interaction that demonstrates understanding, misconception, correction, or transfer.

Counts as mastery evidence:

- completed post-project assessment answers;
- user-initiated explanations that clearly show understanding;
- user questions that clearly reveal understanding or confusion and are recorded with evidence references;
- transfer evidence where the learner applies a boundary, concept, or equipment item to a different domain, input shape, failure mode, or review context;
- equipment transfer where the learner explicitly uses or explains a previously unlocked equipment item in a later slice, project, discussion, or post-project assessment.

Does not count as mastery evidence:

- `jr ask` perceived-difficulty ratings;
- adaptive level, adaptive confidence, or ask-data profile;
- equipment unlocks by themselves;
- build success;
- demo success;
- passive reading completion;
- Slice Gate confirmation;
- Slice Completion continuation replies;
- zero-friction continuation replies;
- story hooks, curiosity, learner enthusiasm, or narrative engagement;
- incident-first orientation responses unless they contain explicit technical reasoning;
- code being shown through `follow` or `micro-follow` mode;
- AI-written project code quality by itself.

## Post-Project Assessment

Post-project assessment is the default required source of active evidence after a runnable project is complete.

Assessment evidence may include:

- main-flow reconstruction;
- boundary ownership explanation;
- failure classification;
- bad-design diagnosis;
- transfer check;
- correction followed by improved explanation.

If a project is built and read but assessment is missing, report the project as `assessment_pending` or evidence-limited. Do not claim mastery.

## User Questions And Volunteered Explanations

User questions can become evidence only when they clearly expose understanding or confusion.

Record evidence only when all conditions hold:

1. The user message contains a technical claim, diagnosis, comparison, or confusion signal.
2. The relevant boundary, concept, FM ID, or project artifact can be identified.
3. The evidence is written to the correct artifact, usually `TEACHING_LOG.md` or a progress update derived from it.

Do not record ordinary continuation messages, curiosity, preferences, or confirmations as mastery evidence.

## Transfer Evidence

Transfer evidence means the learner applies a boundary, concept, failure-mode distinction, or equipment item outside the original slice context.

Examples that may count:

- applying parse-vs-validate separation from CSV import to third-party API payload handling;
- applying cause-chain preservation from a payment SDK to object storage client errors;
- using a previously unlocked review sentence to critique a new design.

Examples that do not count:

- the learner reads a transfer example written by the AI;
- the AI shows an equipment callback;
- a project contains code that could transfer, but the learner does not explain or apply it.

## Equipment Evidence

Equipment is a reusable review, debugging, or design tool. It is not a badge, score, rank, or mastery proof.

An equipment unlock may be stored in progress when it has:

- a name;
- source slice or project;
- one concrete use sentence;
- two or three transfer contexts;
- code evidence that made the equipment useful.

Equipment unlock does not count as mastery evidence. Equipment transfer counts only when the learner later explicitly applies or explains that equipment item.

## `jr ask` Evidence Boundary

`jr ask` collects perceived difficulty only. It supports adaptive delivery.

`jr ask` data may influence:

- explanation density;
- clue exposure;
- JDK8-to-modern-Java bridge notes;
- equipment callback directness;
- post-project assessment follow-up depth;
- next project pacing.

`jr ask` data must not create:

- mastery evidence;
- weakpoint evidence;
- transfer evidence;
- assessment completion;
- precise mastery percentages;
- learner ability labels.

If post-project assessment contradicts `jr ask` data, assessment evidence wins.

## Build And Demo Boundary

Build and demo success show that the AI-built project is runnable. They do not prove learner understanding.

Use build/demo results for:

- project completion readiness;
- candidate project quality;
- progress project-practice fields;
- confidence that the artifact is readable and executable.

Do not use build/demo success as user interaction evidence.

## Precise Mastery Percentage

Only produce a precise mastery percentage after at least one completed post-project assessment for the node or equivalent explicit transfer evidence.

When active evidence is missing:

- report assessment as `pending`, `partial`, or evidence-limited;
- use a broad confidence-limited range or omit the percentage;
- explain that reading and build completion are not mastery evidence.

## Artifact Rules

- `TEACHING_LOG.md` stores project-level teaching and learner evidence.
- `progress-state.yaml` stores lightweight state and summarized evidence.
- `progress.md` is regenerated from `progress-state.yaml`.
- Do not copy full `TEACHING_LOG.md` content into workspace-level progress files.
- Do not record story hooks, curiosity, or learner enthusiasm as understanding evidence.

## Anti-Patterns

- Calling equipment a reward, badge, rank, or mastery proof.
- Treating adaptive difficulty as a grade or ability label.
- Inferring mastery from `jr ask`.
- Inferring mastery from build/demo success.
- Inferring transfer from AI-provided examples.
- Using confirmation words as evidence.
- Producing a precise mastery percentage when assessment evidence is missing.
