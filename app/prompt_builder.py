# app/prompt\_builder.py

from typing import Literal

TaskType = Literal\['algebra', 'geometry', 'graph']

PROMPT\_TEMPLATES: dict\[TaskType, str] = {
'algebra': (
"You are a mathematics teacher. Provide a detailed solution for the following algebra problem."
"\n\nProblem: {question}"
"\n\nAnswer format:"
"\n1) Restate the problem briefly."
"\n2) Step-by-step solution."
"\n3) Final answer."
"\n===GRAPHIC===
(Optional SVG or description for graphic solution)"
),
'geometry': (
"You are a geometry instructor. Explain the solution to the geometric problem below."
"\n\nProblem: {question}"
"\n\nAnswer format:"
"\n1) Restate problem and given data."
"\n2) Detailed construction and proof steps."
"\n3) Conclusion with result."
"\n===GRAPHIC===
(Provide SVG or step-by-step drawing instructions)"
),
'graph': (
"You are a data visualization expert. Solve and visualize the following graphing problem."
"\n\nProblem: {question}"
"\n\nAnswer format:"
"\n1) Interpret the problem."
"\n2) Show how to plot or derive the graph."
"\n3) Key insights."
"\n===GRAPHIC===
(Include plot commands or SVG)"
),
}

def build\_prompt(question: str, task\_type: TaskType = 'algebra') -> str:
"""
Build a tailored prompt for the AI based on the task type.

```
:param question: The user's problem description.
:param task_type: One of 'algebra', 'geometry', or 'graph'.
:return: Full prompt string including formatting separators.
"""
template = PROMPT_TEMPLATES.get(task_type)
if not template:
    raise ValueError(f"Unsupported task type: {task_type}")
return template.format(question=question)
```
