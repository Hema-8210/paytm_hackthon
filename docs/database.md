# SkillPath Database Schema

The database model is designed using SQLAlchemy ORM and supports PostgreSQL and SQLite.

## Database Tables

1. `users`: Stores user credentials, education details, and target role reference.
2. `skills`: Stores standardized technical skills, categories, and alias mappings.
3. `user_skills`: Joins users and skills with proficiency level (1-5), source, and confidence score.
4. `target_roles`: Career job roles (e.g. Data Analyst, Full Stack Developer, Machine Learning Engineer).
5. `job_requirements`: Required skills per role with required level (1-5), importance (0.1-1.0), and frequency.
6. `resumes`: Uploaded PDF resume records with extracted text and section JSON.
7. `projects`: Portfolio project library with difficulty, hours, outcome, and step-by-step implementation lists.
8. `project_skills`: Skills developed per project.
9. `learning_resources`: External documentation, tutorials, and course links per skill level.
10. `recommendations`: Priority recommendations generated per user.
11. `roadmaps`: Personalized 5-phase learning roadmaps.
12. `roadmap_steps`: Steps linked to skills or projects with status tracking (`not_started`, `in_progress`, `completed`).
13. `progress`: Tracks individual skill completion percentages and streak updates.
