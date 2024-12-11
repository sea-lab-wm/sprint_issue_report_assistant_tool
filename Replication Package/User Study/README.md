## SPRINT's User Study

We conducted an user-study to evaluate SPRINT's usability and usefulness with 5 professonal developers from Samsung R&D Institute Bangladesh who are experienced in Issue management tasks with GitHub. The survey questionnaire is available at **SPRINT_User_Study_survey_msr25.pdf**.

We are including our survey responses in the SPRINT_User_Study.Responses.xlsx file.


# User Study Data Selection Methodology

## Duplicate Detection

For this task, we first selected **2 issues** as queries from the OpenOffice project that had multiple duplicates (first one had 3 duplicates and second one had 2 duplicates). Then we randomly chose 8 issues from this project that had no duplicates. In this way, we created a corpus of a total of **15 issues**. 

- Among them, we keep **13 issues** in the user study repository and **2 issues** as queries for users to input.
  
### Input Issues (Queries):
- **Issue 1**: Has **3 duplicates** among the 13 existing issues in the repository.
- **Issue 2**: Has **2 duplicates** among the 13 existing issues in the repository.

The remaining **8 issues** of the 13 are **non-duplicates** to all the issues.

---

## Severity Prediction

For this task, we randomly chose **2 issues**:
1. One issue where the model predicts the severity class accurately.
2. One issue where the model fails to predict the correct severity class.

---

## Bug Localization

For this task, we ran all the test issues of a specific repository. Since LLM outputs can slightly vary each time:
1. We performed this task **3 times**.
2. We accepted the common suggestions that occurred in all 3 runs.

### Grouping the Issues:
- **Good Performing Group**: If the model suggests **1 or more accurate buggy code files** in its first **5** suggestions.
- **Bad Performing Group**: If the model cannot suggest **even one accurate buggy code file** in its first **5** suggestions.

### Final Selection:
- Selected **1 issue** from the good-performing group.
- Selected **1 issue** from the bad-performing group for the user study.
