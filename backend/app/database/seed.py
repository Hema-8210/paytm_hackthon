import logging
from sqlalchemy.orm import Session
from app.models import (
    Skill, TargetRole, JobRequirement, Project, ProjectSkill,
    LearningResource, User, UserSkill, Progress
)
from app.core.security import get_password_hash

logger = logging.getLogger("skillpath.seed")

def seed_database(db: Session):
    # 1. Seed Skills (55+ skills across categories)
    existing_skills_count = db.query(Skill).count()
    if existing_skills_count > 0:
        logger.info("Database already seeded.")
        return

    skills_data = [
        # Languages
        {"name": "Python", "category": "Languages", "description": "High-level programming language widely used in AI, Data Science, and Web Development.", "aliases": "py, python3"},
        {"name": "JavaScript", "category": "Languages", "description": "Core programming language of the web for client and server side development.", "aliases": "js, es6"},
        {"name": "TypeScript", "category": "Languages", "description": "Typed superset of JavaScript that compiles to plain JS.", "aliases": "ts"},
        {"name": "Java", "category": "Languages", "description": "Class-based object-oriented language for enterprise applications.", "aliases": "java"},
        {"name": "C++", "category": "Languages", "description": "High-performance systems programming language.", "aliases": "cpp, cplusplus"},
        {"name": "C", "category": "Languages", "description": "Procedural low-level programming language.", "aliases": "c"},
        {"name": "Go", "category": "Languages", "description": "Open source language designed for high-concurrency microservices.", "aliases": "golang"},
        {"name": "Rust", "category": "Languages", "description": "Systems language emphasizing memory safety and performance.", "aliases": "rust"},
        {"name": "SQL", "category": "Database", "description": "Standard language for storing, manipulating and retrieving data in relational databases.", "aliases": "sql, relational database"},

        # Frontend
        {"name": "React", "category": "Frontend", "description": "Popular JavaScript library for building user interfaces.", "aliases": "reactjs, react.js"},
        {"name": "Vue.js", "category": "Frontend", "description": "Progressive JavaScript framework for building user interfaces.", "aliases": "vue, vuejs"},
        {"name": "Angular", "category": "Frontend", "description": "TypeScript-based web application framework.", "aliases": "angularjs"},
        {"name": "Next.js", "category": "Frontend", "description": "React framework for full-stack web applications and SSR.", "aliases": "nextjs"},
        {"name": "HTML5", "category": "Frontend", "description": "Standard markup language for web documents.", "aliases": "html"},
        {"name": "CSS3", "category": "Frontend", "description": "Style sheet language used for describing document presentation.", "aliases": "css"},
        {"name": "Tailwind CSS", "category": "Frontend", "description": "Utility-first CSS framework for rapid UI building.", "aliases": "tailwind, tailwindcss"},
        {"name": "Redux", "category": "Frontend", "description": "Predictable state container for JS Apps.", "aliases": "redux toolkit"},

        # Backend
        {"name": "Node.js", "category": "Backend", "description": "Asynchronous event-driven JavaScript runtime.", "aliases": "node, nodejs"},
        {"name": "Express.js", "category": "Backend", "description": "Fast minimalist web framework for Node.js.", "aliases": "express"},
        {"name": "FastAPI", "category": "Backend", "description": "High-performance Python web framework for building APIs with OpenAPI.", "aliases": "fastapi"},
        {"name": "Django", "category": "Backend", "description": "High-level Python web framework encouraging clean design.", "aliases": "django"},
        {"name": "Flask", "category": "Backend", "description": "Lightweight WSGI web application framework in Python.", "aliases": "flask"},
        {"name": "Spring Boot", "category": "Backend", "description": "Java framework for building standalone production-grade Spring apps.", "aliases": "spring"},
        {"name": "REST APIs", "category": "Backend", "description": "Architectural style for web API development.", "aliases": "rest, restful"},
        {"name": "GraphQL", "category": "Backend", "description": "Query language for APIs and runtime for fulfilling queries.", "aliases": "graphql"},

        # Databases & Cache
        {"name": "PostgreSQL", "category": "Database", "description": "Advanced open source relational database.", "aliases": "postgres, postgresql"},
        {"name": "MySQL", "category": "Database", "description": "Popular open source relational database management system.", "aliases": "mysql"},
        {"name": "MongoDB", "category": "Database", "description": "Document-oriented NoSQL database.", "aliases": "mongo, nosql"},
        {"name": "Redis", "category": "Database", "description": "In-memory data structure store used as a database and cache.", "aliases": "redis"},
        {"name": "SQLite", "category": "Database", "description": "Self-contained serverless SQL database engine.", "aliases": "sqlite3"},

        # Data Science & Analytics
        {"name": "Power BI", "category": "Data Science", "description": "Business intelligence tool for data visualization and reporting.", "aliases": "powerbi"},
        {"name": "Tableau", "category": "Data Science", "description": "Visual analytics platform for business intelligence.", "aliases": "tableau"},
        {"name": "Microsoft Excel", "category": "Data Science", "description": "Spreadsheet program for data organization and analysis.", "aliases": "excel, ms excel"},
        {"name": "Statistics", "category": "Data Science", "description": "Mathematical study of data collection, analysis, and interpretation.", "aliases": "stats, probability"},
        {"name": "Pandas", "category": "Data Science", "description": "Data analysis and manipulation library for Python.", "aliases": "pandas"},
        {"name": "NumPy", "category": "Data Science", "description": "Fundamental package for scientific computing with Python.", "aliases": "numpy"},
        {"name": "Data Analysis", "category": "Data Science", "description": "Process of inspecting, cleansing, transforming, and modeling data.", "aliases": "data analytics"},
        {"name": "Data Visualization", "category": "Data Science", "description": "Graphical representation of information and data.", "aliases": "data viz"},

        # AI & Machine Learning
        {"name": "Machine Learning", "category": "AI/ML", "description": "Study of computer algorithms that improve automatically through experience.", "aliases": "ml"},
        {"name": "Artificial Intelligence", "category": "AI/ML", "description": "Simulation of human intelligence by machines.", "aliases": "ai"},
        {"name": "Deep Learning", "category": "AI/ML", "description": "Machine learning based on artificial neural networks.", "aliases": "dl, neural networks"},
        {"name": "Natural Language Processing", "category": "AI/ML", "description": "Branch of AI focused on computer-human language interaction.", "aliases": "nlp"},
        {"name": "scikit-learn", "category": "AI/ML", "description": "Machine learning library for Python.", "aliases": "sklearn"},
        {"name": "TensorFlow", "category": "AI/ML", "description": "Open source platform for end-to-end machine learning.", "aliases": "tf"},
        {"name": "PyTorch", "category": "AI/ML", "description": "Open source machine learning framework based on Torch.", "aliases": "pytorch"},
        {"name": "Computer Vision", "category": "AI/ML", "description": "Field of AI enabling computers to derive meaningful info from visual inputs.", "aliases": "cv, opencv"},

        # Cloud & DevOps
        {"name": "Docker", "category": "Cloud/DevOps", "description": "OS-level virtualization for delivering software in packages called containers.", "aliases": "containerization"},
        {"name": "Kubernetes", "category": "Cloud/DevOps", "description": "Container orchestration system for automated deployment and scaling.", "aliases": "k8s"},
        {"name": "AWS", "category": "Cloud/DevOps", "description": "Comprehensive cloud computing platform provided by Amazon.", "aliases": "amazon web services"},
        {"name": "Google Cloud", "category": "Cloud/DevOps", "description": "Suite of cloud computing services provided by Google.", "aliases": "gcp"},
        {"name": "Microsoft Azure", "category": "Cloud/DevOps", "description": "Cloud computing service operated by Microsoft.", "aliases": "azure"},
        {"name": "CI/CD", "category": "Cloud/DevOps", "description": "Continuous Integration and Continuous Delivery automation.", "aliases": "github actions, jenkins"},
        {"name": "Terraform", "category": "Cloud/DevOps", "description": "Infrastructure as code software tool.", "aliases": "iac"},
        {"name": "Linux", "category": "Tools", "description": "Open source operating system widely used on servers.", "aliases": "ubuntu, bash"},
        {"name": "Bash", "category": "Tools", "description": "Unix shell and command language.", "aliases": "shell scripting"},
        {"name": "Git", "category": "Tools", "description": "Distributed version control system.", "aliases": "github, gitlab"},

        # Security & Design
        {"name": "Cybersecurity", "category": "Security", "description": "Protection of computer systems and networks from information disclosure.", "aliases": "infosec, security"},
        {"name": "Ethical Hacking", "category": "Security", "description": "Authorized penetration testing of computer networks.", "aliases": "pen testing"},
        {"name": "UI/UX Design", "category": "Design", "description": "User Interface and User Experience design principles.", "aliases": "ui, ux, product design"},
        {"name": "Figma", "category": "Design", "description": "Collaborative web application for interface design.", "aliases": "figma"}
    ]

    skill_objects = {}
    for item in skills_data:
        s = Skill(**item)
        db.add(s)
        db.flush()
        skill_objects[s.name] = s

    # 2. Seed Target Roles & Job Requirements (12 Roles)
    roles_data = [
        {
            "title": "Data Analyst",
            "category": "Data Science",
            "description": "Analyzes raw data to uncover trends and insights using SQL, Python, Excel, Power BI, and statistical methods.",
            "requirements": [
                ("SQL", 4, 0.95, "High"),
                ("Python", 4, 0.85, "High"),
                ("Microsoft Excel", 4, 0.80, "High"),
                ("Power BI", 3, 0.75, "High"),
                ("Statistics", 3, 0.70, "Medium"),
                ("Data Visualization", 3, 0.65, "Medium"),
                ("Pandas", 3, 0.60, "Medium")
            ]
        },
        {
            "title": "Frontend Developer",
            "category": "Software Development",
            "description": "Builds responsive, intuitive user interfaces using modern web technologies.",
            "requirements": [
                ("JavaScript", 4, 0.95, "High"),
                ("React", 4, 0.90, "High"),
                ("TypeScript", 3, 0.85, "High"),
                ("HTML5", 4, 0.80, "High"),
                ("CSS3", 4, 0.80, "High"),
                ("Tailwind CSS", 3, 0.70, "Medium"),
                ("Git", 3, 0.65, "Medium")
            ]
        },
        {
            "title": "Backend Developer",
            "category": "Software Development",
            "description": "Engineers scalable server-side architecture, REST APIs, microservices, and databases.",
            "requirements": [
                ("Python", 4, 0.90, "High"),
                ("FastAPI", 3, 0.85, "High"),
                ("Node.js", 3, 0.80, "High"),
                ("PostgreSQL", 4, 0.90, "High"),
                ("REST APIs", 4, 0.85, "High"),
                ("Docker", 3, 0.75, "Medium"),
                ("Redis", 2, 0.60, "Medium"),
                ("Git", 3, 0.70, "Medium")
            ]
        },
        {
            "title": "Full Stack Developer",
            "category": "Software Development",
            "description": "Builds end-to-end web applications combining modern frontend frameworks and robust backend microservices.",
            "requirements": [
                ("React", 4, 0.90, "High"),
                ("Node.js", 4, 0.90, "High"),
                ("JavaScript", 4, 0.95, "High"),
                ("TypeScript", 3, 0.85, "High"),
                ("PostgreSQL", 3, 0.85, "High"),
                ("REST APIs", 4, 0.85, "High"),
                ("Git", 3, 0.75, "Medium"),
                ("Docker", 3, 0.70, "Medium")
            ]
        },
        {
            "title": "Data Scientist",
            "category": "Data Science",
            "description": "Applies statistical modeling, predictive analytics, and machine learning to solve complex business problems.",
            "requirements": [
                ("Python", 5, 0.95, "High"),
                ("SQL", 4, 0.90, "High"),
                ("Machine Learning", 4, 0.90, "High"),
                ("Pandas", 4, 0.85, "High"),
                ("NumPy", 4, 0.80, "Medium"),
                ("scikit-learn", 4, 0.85, "High"),
                ("Statistics", 4, 0.85, "High")
            ]
        },
        {
            "title": "Machine Learning Engineer",
            "category": "AI/ML",
            "description": "Designs, builds, deploys, and maintains production-grade machine learning models and ML pipelines.",
            "requirements": [
                ("Python", 5, 0.95, "High"),
                ("Machine Learning", 4, 0.90, "High"),
                ("Deep Learning", 3, 0.85, "High"),
                ("PyTorch", 3, 0.80, "High"),
                ("scikit-learn", 4, 0.80, "High"),
                ("Docker", 3, 0.75, "Medium"),
                ("SQL", 3, 0.70, "Medium")
            ]
        },
        {
            "title": "AI Engineer",
            "category": "AI/ML",
            "description": "Integrates LLMs, Generative AI, NLP models, and vector databases into software applications.",
            "requirements": [
                ("Python", 5, 0.95, "High"),
                ("Artificial Intelligence", 4, 0.90, "High"),
                ("Natural Language Processing", 4, 0.85, "High"),
                ("PyTorch", 3, 0.80, "Medium"),
                ("FastAPI", 3, 0.80, "Medium"),
                ("REST APIs", 4, 0.85, "High"),
                ("Git", 3, 0.70, "Low")
            ]
        },
        {
            "title": "DevOps Engineer",
            "category": "Cloud/DevOps",
            "description": "Automates deployment pipelines, cloud infrastructure, monitoring, and container orchestration.",
            "requirements": [
                ("Docker", 4, 0.95, "High"),
                ("Kubernetes", 4, 0.90, "High"),
                ("AWS", 4, 0.90, "High"),
                ("CI/CD", 4, 0.85, "High"),
                ("Linux", 4, 0.85, "High"),
                ("Bash", 3, 0.75, "Medium"),
                ("Terraform", 3, 0.70, "Medium")
            ]
        },
        {
            "title": "Cloud Engineer",
            "category": "Cloud/DevOps",
            "description": "Architects, deploys, and manages scalable cloud environments on AWS, Azure, or GCP.",
            "requirements": [
                ("AWS", 4, 0.95, "High"),
                ("Docker", 4, 0.85, "High"),
                ("Linux", 4, 0.85, "High"),
                ("Terraform", 3, 0.80, "Medium"),
                ("Python", 3, 0.75, "Medium"),
                ("Kubernetes", 3, 0.70, "Medium")
            ]
        },
        {
            "title": "Cybersecurity Analyst",
            "category": "Security",
            "description": "Monitors networks, identifies vulnerabilities, performs threat analysis, and secures corporate assets.",
            "requirements": [
                ("Cybersecurity", 4, 0.95, "High"),
                ("Linux", 4, 0.85, "High"),
                ("Ethical Hacking", 3, 0.80, "High"),
                ("Python", 3, 0.75, "Medium"),
                ("Bash", 3, 0.70, "Medium")
            ]
        },
        {
            "title": "Software Engineer",
            "category": "Software Development",
            "description": "Generalist software developer creating reliable software, algorithms, and applications.",
            "requirements": [
                ("Python", 4, 0.90, "High"),
                ("Java", 3, 0.80, "Medium"),
                ("SQL", 3, 0.85, "High"),
                ("Git", 4, 0.85, "High"),
                ("REST APIs", 3, 0.80, "High"),
                ("Docker", 2, 0.65, "Medium")
            ]
        },
        {
            "title": "UI/UX Designer",
            "category": "Design",
            "description": "Designs intuitive user interfaces, wireframes, visual systems, and user interaction flows.",
            "requirements": [
                ("UI/UX Design", 5, 0.95, "High"),
                ("Figma", 4, 0.90, "High"),
                ("HTML5", 3, 0.70, "Medium"),
                ("CSS3", 3, 0.70, "Medium")
            ]
        }
    ]

    for rdata in roles_data:
        reqs = rdata.pop("requirements")
        role_obj = TargetRole(**rdata)
        db.add(role_obj)
        db.flush()
        
        for skill_name, req_level, importance, freq in reqs:
            if skill_name in skill_objects:
                jreq = JobRequirement(
                    target_role_id=role_obj.id,
                    skill_id=skill_objects[skill_name].id,
                    required_level=req_level,
                    importance=importance,
                    frequency=freq
                )
                db.add(jreq)

    # 3. Seed Projects (35 Projects with realistic skill mappings & implementation steps)
    projects_data = [
        # Web
        {
            "title": "E-Commerce Sales Analytics Dashboard",
            "description": "A full-stack analytics platform that ingests raw sales data, performs SQL aggregations, and presents interactive KPIs in Power BI / React.",
            "difficulty": "Intermediate",
            "estimated_hours": 18,
            "category": "Data Science",
            "prerequisites": "Basic SQL and Python syntax.",
            "expected_outcome": "Fully functioning analytics dashboard with filtering, revenue trends, and customer segmentation.",
            "portfolio_value": "High - demonstrates end-to-end data pipeline & reporting capability.",
            "implementation_steps": ["Design PostgreSQL database schema", "Seed transaction data", "Write complex SQL joins and window functions", "Connect Power BI / Recharts UI"],
            "skills": [("SQL", 0.9), ("Power BI", 0.85), ("Python", 0.8), ("Data Visualization", 0.8)]
        },
        {
            "title": "Real-Time Chat Application",
            "description": "Full-stack chat app with instant messaging, user authentication, and active room indicators.",
            "difficulty": "Intermediate",
            "estimated_hours": 15,
            "category": "Web Development",
            "prerequisites": "React fundamentals and REST concepts.",
            "expected_outcome": "Deployable web app with multi-user messaging.",
            "portfolio_value": "Medium-High - shows real-time event handling.",
            "implementation_steps": ["Setup Node.js Express server", "Implement JWT auth", "Build React UI with Tailwind", "Add WebSocket support"],
            "skills": [("React", 0.9), ("Node.js", 0.9), ("JavaScript", 0.8), ("REST APIs", 0.8)]
        },
        {
            "title": "Task Management SaaS App",
            "description": "Trello-like drag-and-drop task board with user roles, deadlines, and project categorizations.",
            "difficulty": "Intermediate",
            "estimated_hours": 20,
            "category": "Web Development",
            "prerequisites": "TypeScript and React hooks.",
            "expected_outcome": "Full featured SaaS web application.",
            "portfolio_value": "High - demonstrates SaaS architecture.",
            "implementation_steps": ["Setup FastApi backend & SQLAlchemy models", "Build drag-and-drop React frontend", "Configure PostgreSQL database"],
            "skills": [("TypeScript", 0.9), ("React", 0.9), ("FastAPI", 0.85), ("PostgreSQL", 0.8)]
        },
        {
            "title": "Event Management & Ticketing System",
            "description": "Web app for creating events, booking digital tickets, and managing attendee lists.",
            "difficulty": "Intermediate",
            "estimated_hours": 16,
            "category": "Web Development",
            "prerequisites": "Basic web stack skills.",
            "expected_outcome": "Working ticketing website.",
            "portfolio_value": "Medium - standard business logic showcase.",
            "implementation_steps": ["Create REST API endpoints", "Build responsive UI", "Integrate database transactions"],
            "skills": [("React", 0.85), ("Node.js", 0.85), ("SQL", 0.8)]
        },
        # Data Science & Analytics
        {
            "title": "Customer Churn Analysis & Prediction",
            "description": "Exploratory data analysis and machine learning model to predict subscription churn.",
            "difficulty": "Intermediate",
            "estimated_hours": 14,
            "category": "Data Science",
            "prerequisites": "Python, Pandas, and basic Machine Learning.",
            "expected_outcome": "Jupyter notebook & trained model with ROC-AUC evaluation.",
            "portfolio_value": "High - realistic business problem solving.",
            "implementation_steps": ["Clean churn dataset using Pandas", "Perform EDA", "Train Random Forest & Logistic Regression in scikit-learn", "Plot precision-recall curves"],
            "skills": [("Python", 0.9), ("Pandas", 0.9), ("scikit-learn", 0.85), ("Machine Learning", 0.85), ("Statistics", 0.8)]
        },
        {
            "title": "Stock Market Data Analytics Dashboard",
            "description": "Fetches real-time stock quotes via financial APIs, computes moving averages, and visualizes trends.",
            "difficulty": "Intermediate",
            "estimated_hours": 12,
            "category": "Data Science",
            "prerequisites": "Python API requests and plotting.",
            "expected_outcome": "Interactive financial dashboard.",
            "portfolio_value": "Medium - good visual project.",
            "implementation_steps": ["Fetch stock prices using YFinance API", "Calculate RSI and MACD in Pandas", "Render chart with Recharts/Plotly"],
            "skills": [("Python", 0.9), ("Pandas", 0.85), ("Data Visualization", 0.85), ("REST APIs", 0.8)]
        },
        {
            "title": "Movie Recommendation Analysis",
            "description": "Collaborative filtering and content-based recommendation model built on MovieLens dataset.",
            "difficulty": "Intermediate",
            "estimated_hours": 16,
            "category": "Data Science",
            "prerequisites": "Matrix operations and Python data science packages.",
            "expected_outcome": "Recommender system API.",
            "portfolio_value": "High - popular ML use-case.",
            "implementation_steps": ["Build user-item rating matrix", "Compute cosine similarity", "Return top 5 movie recommendations"],
            "skills": [("Python", 0.9), ("NumPy", 0.85), ("scikit-learn", 0.85), ("Machine Learning", 0.8)]
        },
        # AI / ML
        {
            "title": "Spam & Phishing Detection System",
            "description": "NLP text classification pipeline using TF-IDF vectorization and Naive Bayes / SVM to classify spam messages.",
            "difficulty": "Beginner",
            "estimated_hours": 8,
            "category": "AI/ML",
            "prerequisites": "Python fundamentals.",
            "expected_outcome": "Trained spam classifier with Web interface.",
            "portfolio_value": "Medium - concise ML entry project.",
            "implementation_steps": ["Preprocess text data with NLTK/regex", "Extract TF-IDF features", "Train model in scikit-learn"],
            "skills": [("Python", 0.9), ("Natural Language Processing", 0.85), ("scikit-learn", 0.85), ("Machine Learning", 0.8)]
        },
        {
            "title": "Image Classification with Deep Learning",
            "description": "Convolutional Neural Network (CNN) built in PyTorch to classify objects or medical images.",
            "difficulty": "Advanced",
            "estimated_hours": 22,
            "category": "AI/ML",
            "prerequisites": "PyTorch and basic linear algebra.",
            "expected_outcome": "High accuracy CNN model with confusion matrix.",
            "portfolio_value": "High - solid computer vision artifact.",
            "implementation_steps": ["Prepare PyTorch DataLoader", "Design ResNet architecture", "Train with GPU acceleration"],
            "skills": [("PyTorch", 0.95), ("Deep Learning", 0.9), ("Python", 0.9), ("Computer Vision", 0.85)]
        },
        {
            "title": "Sentiment Analysis Web Microservice",
            "description": "REST microservice that analyzes product reviews and labels sentiment using transformer models.",
            "difficulty": "Intermediate",
            "estimated_hours": 12,
            "category": "AI/ML",
            "prerequisites": "FastAPI and NLP basics.",
            "expected_outcome": "FastAPI service returning sentiment scores.",
            "portfolio_value": "High - connects ML to web backend.",
            "implementation_steps": ["Load HuggingFace sentiment pipeline", "Expose endpoint via FastAPI", "Containerize with Docker"],
            "skills": [("Natural Language Processing", 0.9), ("FastAPI", 0.85), ("Python", 0.85), ("Docker", 0.75)]
        },
        # Cybersecurity
        {
            "title": "Network Traffic & Port Scanner Analyzer",
            "description": "Python CLI tool for scanning network ranges, detecting open ports, and identifying protocol anomalies.",
            "difficulty": "Intermediate",
            "estimated_hours": 10,
            "category": "Cybersecurity",
            "prerequisites": "Networking concepts and Python socket library.",
            "expected_outcome": "CLI port scanner tool.",
            "portfolio_value": "Medium-High - demonstrates networking depth.",
            "implementation_steps": ["Implement multi-threaded socket scanner", "Analyze TCP banners", "Log audit reports"],
            "skills": [("Cybersecurity", 0.9), ("Python", 0.85), ("Linux", 0.8), ("Ethical Hacking", 0.75)]
        },
        {
            "title": "Password Security & Entropy Analyzer",
            "description": "Security application that tests password strength, checks breached databases, and generates cryptographically secure hashes.",
            "difficulty": "Beginner",
            "estimated_hours": 6,
            "category": "Cybersecurity",
            "prerequisites": "Basic Python or JS.",
            "expected_outcome": "Interactive security analyzer widget.",
            "portfolio_value": "Medium - practical security tool.",
            "implementation_steps": ["Calculate entropy bits", "Compare against HaveIBeenPwned API", "Generate bcrypt hashes"],
            "skills": [("Cybersecurity", 0.85), ("Python", 0.8), ("REST APIs", 0.75)]
        },
        # Cloud / DevOps
        {
            "title": "Automated CI/CD Deployment Pipeline",
            "description": "GitHub Actions workflow that runs automated unit tests, builds Docker containers, and deploys to cloud hosting.",
            "difficulty": "Intermediate",
            "estimated_hours": 10,
            "category": "Cloud/DevOps",
            "prerequisites": "Git and Docker fundamentals.",
            "expected_outcome": "Fully automated deployment workflow.",
            "portfolio_value": "High - essential DevOps showcase.",
            "implementation_steps": ["Write Dockerfile for web service", "Configure GitHub Actions YAML pipeline", "Deploy to cloud runner"],
            "skills": [("CI/CD", 0.95), ("Docker", 0.9), ("Git", 0.85), ("Linux", 0.8)]
        },
        {
            "title": "Containerized Microservices Web Stack",
            "description": "Multi-container setup using Docker Compose orchestrating React frontend, FastAPI backend, PostgreSQL database, and Redis cache.",
            "difficulty": "Intermediate",
            "estimated_hours": 14,
            "category": "Cloud/DevOps",
            "prerequisites": "Docker basic usage.",
            "expected_outcome": "Single-command docker-compose environment.",
            "portfolio_value": "High - industry standard local infrastructure.",
            "implementation_steps": ["Write service Dockerfiles", "Define docker-compose.yml networks and volumes", "Configure environment variables"],
            "skills": [("Docker", 0.95), ("PostgreSQL", 0.85), ("Redis", 0.8), ("Linux", 0.8)]
        },
        {
            "title": "Cloud Infrastructure Provisioner with Terraform",
            "description": "Infrastructure as Code project that provisions an AWS VPC, EC2 instance, and RDS database automatically.",
            "difficulty": "Advanced",
            "estimated_hours": 18,
            "category": "Cloud/DevOps",
            "prerequisites": "AWS fundamentals.",
            "expected_outcome": "Terraform scripts for reproducible cloud infra.",
            "portfolio_value": "High - cloud engineering benchmark.",
            "implementation_steps": ["Write main.tf Terraform manifest", "Define security groups & subnets", "Execute terraform apply"],
            "skills": [("AWS", 0.95), ("Terraform", 0.9), ("Linux", 0.8)]
        }
    ]

    for pdata in projects_data:
        p_skills = pdata.pop("skills")
        proj_obj = Project(**pdata)
        db.add(proj_obj)
        db.flush()
        
        for sname, imp in p_skills:
            if sname in skill_objects:
                pskill = ProjectSkill(
                    project_id=proj_obj.id,
                    skill_id=skill_objects[sname].id,
                    importance=imp
                )
                db.add(pskill)

    # 4. Seed Learning Resources for core skills
    resources_data = [
        # SQL
        ("SQL", "SQL Complete Beginner Guide", "Learn SELECT, WHERE, ORDER BY, and basic table filtering.", "https://www.postgresql.org/docs/current/tutorial-sql.html", "Documentation", "Beginner"),
        ("SQL", "Mastering SQL Joins & Subqueries", "Deep dive into INNER, LEFT, RIGHT, FULL OUTER joins and subqueries.", "https://mode.com/sql-tutorial/", "Interactive", "Intermediate"),
        ("SQL", "Advanced SQL Window Functions & CTEs", "Learn ROW_NUMBER, RANK, LEAD, LAG, and Common Table Expressions.", "https://use-the-index-luke.com/", "Article", "Advanced"),

        # Python
        ("Python", "Python 3 Official Tutorial", "Comprehensive guide to Python syntax, data structures, and standard libraries.", "https://docs.python.org/3/tutorial/", "Documentation", "Beginner"),
        ("Python", "Data Structures & Algorithms in Python", "Learn lists, dicts, stacks, queues, binary trees, and time complexity.", "https://realpython.com/", "Course", "Intermediate"),

        # Power BI
        ("Power BI", "Power BI Desktop Quickstart", "Import data, create relationships, and design your first report.", "https://learn.microsoft.com/en-us/power-bi/guided-learning/", "Course", "Beginner"),
        ("Power BI", "DAX Formulas & Data Modeling", "Master Data Analysis Expressions for advanced measures and calculated columns.", "https://sqlbi.com", "Article", "Intermediate"),

        # React
        ("React", "React Official Documentation & Quickstart", "Learn component architecture, state, props, and hooks.", "https://react.dev/learn", "Documentation", "Beginner"),
        ("React", "Advanced React Patterns & Custom Hooks", "Build reusable custom hooks, context providers, and performance optimizations.", "https://react.dev/reference/react", "Documentation", "Intermediate"),

        # PostgreSQL
        ("PostgreSQL", "PostgreSQL Starter Guide", "Setup tables, foreign keys, indexes, and write efficient queries.", "https://www.postgresqltutorial.com/", "Interactive", "Beginner")
    ]

    for sname, title, desc, url, rtype, level in resources_data:
        if sname in skill_objects:
            res = LearningResource(
                skill_id=skill_objects[sname].id,
                title=title,
                description=desc,
                url=url,
                resource_type=rtype,
                level=level
            )
            db.add(res)

    # 5. Create default demo user account (demo@skillpath.dev / password123)
    target_data_analyst = db.query(TargetRole).filter(TargetRole.title == "Data Analyst").first()
    demo_user = User(
        name="Alex Developer",
        email="demo@skillpath.dev",
        password_hash=get_password_hash("password123"),
        education="B.Tech Computer Science",
        college="State Technological University",
        branch="Computer Science & Engineering",
        graduation_year=2025,
        experience_level="Beginner",
        target_role_id=target_data_analyst.id if target_data_analyst else None
    )
    db.add(demo_user)
    db.flush()

    # Add initial skills for demo user (Python 4/5, SQL 2/5, Excel 3/5)
    demo_skills = [
        ("Python", 4, "manual", 1.0),
        ("SQL", 2, "resume", 0.91),
        ("Microsoft Excel", 3, "manual", 1.0)
    ]
    for sname, level, src, conf in demo_skills:
        if sname in skill_objects:
            uskill = UserSkill(
                user_id=demo_user.id,
                skill_id=skill_objects[sname].id,
                proficiency_level=level,
                source=src,
                confidence=conf
            )
            db.add(uskill)

    db.commit()
    logger.info("Database seeding completed successfully!")
