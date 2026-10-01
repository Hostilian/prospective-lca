# Questions for Mara / AWAM

These are the smallest questions that materially change the build. The synthetic demo can continue without answers; the real pilot cannot.

## Must answer before a real pilot

1. What exact process or technology should be the first pilot?
2. When you said “Project LIFE”, did you mean a named EU LIFE project, or project life/prospective LCA generally?
3. What decision should the first comparison support?
4. What is the functional unit and reference flow?
5. What is the system boundary and modelling type: attributional, consequential, or another approved approach?
6. Which openLCA version and operating system does AWAM use?
7. Which baseline database, version, and ecoinvent system model are approved?
8. Which LCIA method, version, and impact categories are required?
9. Which target years, geographies, and pathway labels matter?
10. Should the foreground, background, or both change over time?
11. Should future background scenarios come from premise/IAM, AWAM-defined scenarios, or another approved source?
12. What scale-up assumptions already exist, and who owns their scientific review?
13. Which files/data may Eren access, where may they be stored, and what must never leave AWAM systems?
14. What must the tool return to openLCA, if anything?
15. What single acceptance test proves that the first usable version helps AWAM?
16. Who besides Mara reviews modelling assumptions and software outputs?
17. What is the formal route: paid student project, internship, research support, grant, or another arrangement?
18. What are the time allocation, IP ownership, publication, confidentiality, and handover rules?

## Can answer during the pilot

- Which repeated import/cleaning/report task is most painful?
- Which fields, units, sources, and timestamps are most error-prone?
- Which foreground transformations should be parameterised first?
- Which results need contribution analysis?
- Which sensitivity variables should be reviewer-selected?
- Does the review package need PDF/XLSX in addition to HTML/CSV/JSON?
- Does AWAM want a CLI, a browser UI, or both?

## Nice to know later

- Whether a Brightway/Activity Browser route is already used internally.
- Whether a scenario catalogue or internal template already exists.
- Whether a second AWAM process should be used as the portability test.
- Whether an institutional Git repository, packaging convention, or CI runner is required.

## Suggested short message

> I built a small synthetic prototype around the reusable prospective-LCA workflow we discussed. Before connecting it to a real AWAM case, could you confirm the first process, functional unit/boundary, openLCA/database/method versions, future years/pathways, and what acceptance test would make the tool genuinely useful? The prototype keeps all real-data and scientific choices behind review gates.

