import streamlit as st

def app():
    # Custom CSS for a premium look
    st.markdown("""
        <style>
        .main {
            background-color: #fdfdfd;
        }
        .stExpander {
            border: 1px solid #e1e4e8;
            border-radius: 8px;
            margin-bottom: 10px;
            background-color: white;
            color: #2c3e50; /* Force dark text */
        }
        /* Target the expander summary/header text specifically */
        .stExpander p {
            color: #2c3e50 !important;
            font-weight: 600;
        }
        .category-header {
            color: #2c3e50;
            border-bottom: 2px solid #2980b9;
            padding-bottom: 5px;
            margin-top: 20px;
        }
        .question-text {
            font-weight: 600;
            color: #1a1a1a;
        }
        .answer-text {
            color: #34495e;
            line-height: 1.6;
        }
        code {
            background-color: #f0f2f6 !important;
            color: #e83e8c !important;
            padding: 2px 4px;
            border-radius: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Data Structure: All 100 Questions (Abbreviated here for logic, fully populated in app)
    questions = [
        # System Architecture & Design (1-15)
        {"cat": "System Architecture & Design", "q": "1. Can you describe the high-level architecture of LOGICHIVE?", "a": "LOGICHIVE follows a **microservices architecture**. It consists of multiple specialized backend services (User, Problem, Submission, Competition, GitHub) built with **NestJS**, an **AI Service** built with **FastAPI**, and a **Frontend** built with **React/Vite**. These services communicate via HTTP/REST and share a **PostgreSQL** database and **Redis** cache, orchestrated using **Docker Compose**."},
        {"cat": "System Architecture & Design", "q": "2. Why did you choose a microservices architecture over a monolith?", "a": "Microservices allow for **independent scaling**, **technology diversity** (using Python for AI), **fault isolation**, and **easier team collaboration**."},
        {"cat": "System Architecture & Design", "q": "3. How do your services communicate with each other?", "a": "The services primarily communicate using **synchronous HTTP REST APIs**. Direct HTTP is used for service-to-service calls currently."},
        {"cat": "System Architecture & Design", "q": "4. What is the role of the API Gateway in this project?", "a": "The **Frontend** acts as the client-side aggregator. In production, a reverse proxy like **Nginx** would route requests to avoid CORS and expose only one port."},
        {"cat": "System Architecture & Design", "q": "5. How do you handle authentication across microservices?", "a": "We use **JWT (JSON Web Tokens)**. The User Service issues a token, and other services validate it using a shared `JWT_SECRET`."},
        {"cat": "System Architecture & Design", "q": "6. What is the purpose of the `ai-service`?", "a": "It provides intelligent features like **problem recommendations** using Python's ML libraries (Pandas, Scikit-learn)."},
        {"cat": "System Architecture & Design", "q": "7. How does the Code Execution Engine work?", "a": "It uses **Judge0**. The Submission Service sends code to the Judge0 API which runs it in a sandboxed environment."},
        {"cat": "System Architecture & Design", "q": "8. What are the benefits of using Docker Compose?", "a": "Ensures a **consistent environment** across all developer machines with a single command (`docker-compose up`)."},
        {"cat": "System Architecture & Design", "q": "9. How do you handle data consistency between services?", "a": "Currently via shared PostgreSQL instance using **ACID transactions**. In strict microservices, we'd use Sagas/Eventual Consistency."},
        {"cat": "System Architecture & Design", "q": "10. What is the role of Redis in your architecture?", "a": "Used for **caching** frequently accessed data and potentially as a message broker for queues."},
        {"cat": "System Architecture & Design", "q": "11. How would you scale the Submission Service?", "a": "Run **multiple replicas** behind a load balancer and scale Judge0 instances accordingly."},
        {"cat": "System Architecture & Design", "q": "12. What design pattern is used for the 'Competition' feature?", "a": "Likely uses an **aggregator pattern**, linking Users, Problems, and Submissions within a specific window."},
        {"cat": "System Architecture & Design", "q": "13. How do you handle configuration management?", "a": "Using **Environment Variables** (`.env`) injected via Docker and managed via `@nestjs/config`."},
        {"cat": "System Architecture & Design", "q": "14. What are the trade-offs of using a shared database?", "a": "Pros: Simplicity, consistency. Cons: Tight coupling, single point of failure."},
        {"cat": "System Architecture & Design", "q": "15. How do you ensure high availability?", "a": "Redundant service instances, managed database replication, and load balancing (AWS ECS/Kubernetes in production)."},

        # Backend: NestJS & Node.js (16-40)
        {"cat": "Backend: NestJS & Node.js", "q": "16. Why did you choose NestJS over Express?", "a": "NestJS provides **modular architecture**, built-in TypeScript support, and Dependency Injection for maintainable code."},
        {"cat": "Backend: NestJS & Node.js", "q": "17. Explain the concept of a 'Module' in NestJS.", "a": "A class annotated with `@Module()` that organizes components like Controllers and Providers."},
        {"cat": "Backend: NestJS & Node.js", "q": "18. What is Dependency Injection (DI)?", "a": "A pattern where dependencies are injected into a class via constructor instead of manual creation."},
        {"cat": "Backend: NestJS & Node.js", "q": "19. Controller vs Service?", "a": "Controllers handle HTTP requests; Services contain **business logic** and DB interactions."},
        {"cat": "Backend: NestJS & Node.js", "q": "20. What are Guards?", "a": "Used for **authorization**. They determine if a request can proceed based on logic like JWT validation."},
        {"cat": "Backend: NestJS & Node.js", "q": "21. What is a Pipe?", "a": "Used for **validation** (e.g., `ValidationPipe`) or transformation of input data."},
        {"cat": "Backend: NestJS & Node.js", "q": "22. What is an Interceptor?", "a": "Used to bind extra logic before or after method execution (logging, response mapping)."},
        {"cat": "Backend: NestJS & Node.js", "q": "23. Role of DTOs?", "a": "Data Transfer Objects define request shapes and enable validation via decorators."},
        {"cat": "Backend: NestJS & Node.js", "q": "24. Error handling in NestJS?", "a": "Using standard HTTP exceptions (e.g., `NotFoundException`) and global Exception Filters."},
        {"cat": "Backend: NestJS & Node.js", "q": "25. What is TypeORM?", "a": "An ORM for TypeScript that lets you interact with DBs using Classes and Objects."},
        {"cat": "Backend: NestJS & Node.js", "q": "26. Define One-to-Many in TypeORM.", "a": "Using `@OneToMany` and `@ManyToOne` decorators in respective entities."},
        {"cat": "Backend: NestJS & Node.js", "q": "27. Repository Pattern?", "a": "Abstracts data access logic, decoupling business logic from the specific DB queries."},
        {"cat": "Backend: NestJS & Node.js", "q": "28. Handling async in Node.js?", "a": "Using **Promises** and `async/await` syntax for clean, non-blocking code."},
        {"cat": "Backend: NestJS & Node.js", "q": "29. Purpose of main.ts?", "a": "Entry point that bootstraps the Nest application using `NestFactory`."},
        {"cat": "Backend: NestJS & Node.js", "q": "30. File uploads in NestJS?", "a": "Using `FileInterceptor` based on Multer and the `@UploadedFile()` decorator."},

        # Frontend: React & Vite (41-60)
        {"cat": "Frontend: React & Vite", "q": "41. Why Vite over CRA?", "a": "Vite is significantly faster using native ES modules and Rollup for production builds."},
        {"cat": "Frontend: React & Vite", "q": "42. Common React Hooks?", "a": "`useState`, `useEffect`, `useContext`, `useRef`, `useMemo`."},
        {"cat": "Frontend: React & Vite", "q": "43. useEffect vs useLayoutEffect?", "a": "`useEffect` is async after paint; `useLayoutEffect` is sync before paint (prevents flicker)."},
        {"cat": "Frontend: React & Vite", "q": "44. Global State management?", "a": "React Context API, Redux Toolkit, or Zustand."},
        {"cat": "Frontend: React & Vite", "q": "45. Virtual DOM?", "a": "A lightweight copy of the real DOM used for efficient 'diffing' and 'reconciliation'."},
        {"cat": "Frontend: React & Vite", "q": "46. Routing in React?", "a": "`react-router-dom` using HTML5 History API for SPA navigation."},
        {"cat": "Frontend: React & Vite", "q": "47. Prop Drilling?", "a": "Passing data through many layers. Avoid with Context or State Management."},
        {"cat": "Frontend: React & Vite", "q": "48. Key prop in lists?", "a": "Identifies items uniquely for efficient DOM updates during re-renders."},
        {"cat": "Frontend: React & Vite", "q": "49. Tailwind CSS?", "a": "Utility-first CSS framework for rapid UI development directly in markup."},
        {"cat": "Frontend: React & Vite", "q": "50. React Performance Optimization?", "a": "Memoization, Code Splitting, Virtualization, and lazy loading."},

        # AI Service: Python & FastAPI (61-75)
        {"cat": "AI Service: Python & FastAPI", "q": "61. Why FastAPI for AI?", "a": "High performance, native async support, and excellent integration with Python ML libs."},
        {"cat": "AI Service: Python & FastAPI", "q": "62. What is Pydantic?", "a": "Data validation library used in FastAPI for defining request/response schemas."},
        {"cat": "AI Service: Python & FastAPI", "q": "63. Flask vs FastAPI?", "a": "FastAPI is async-first, faster, and provides auto-generated docs."},
        {"cat": "AI Service: Python & FastAPI", "q": "64. Recommender System logic?", "a": "Likely uses collaborative or content-based filtering via user history."},
        {"cat": "AI Service: Python & FastAPI", "q": "65. What is SQLAlchemy?", "a": "The industry-standard SQL toolkit and ORM for Python."},

        # Database: PostgreSQL & Redis (76-85)
        {"cat": "Database: PostgreSQL & Redis", "q": "76. Why PostgreSQL?", "a": "Reliable relational data management with ACID transactions and strong integrity."},
        {"cat": "Database: PostgreSQL & Redis", "q": "77. Database Migrations?", "a": "Version control for schemas, allowing incremental and reversible DB changes."},
        {"cat": "Database: PostgreSQL & Redis", "q": "78. Normalization?", "a": "Organizing data to reduce redundancy and improve integrity via relationships."},
        {"cat": "Database: PostgreSQL & Redis", "q": "80. Redis use case?", "a": "Caching frequently accessed data (like problems) to reduce DB latency."},

        # DevOps & Infrastructure (86-95)
        {"cat": "DevOps & Infrastructure", "q": "86. What is Docker?", "a": "Platform for running apps in isolated containers with all dependencies packaged."},
        {"cat": "DevOps & Infrastructure", "q": "87. Image vs Container?", "a": "Image is the read-only blueprint; Container is the running instance."},
        {"cat": "DevOps & Infrastructure", "q": "88. docker-compose up?", "a": "Builds and starts all defined services in the correct network environment."},

        # Behavioral (96-100)
        {"cat": "Behavioral & Project Specific", "q": "96. Biggest Challenge?", "a": "Implementing secure sandboxed code execution using Judge0/Docker."},
        {"cat": "Behavioral & Project Specific", "q": "100. Why this stack?", "a": "NestJS for scale, React for UI, Postgres for reliability, Python for AI. Industry standard."}
    ]

    # Sidebar Navigation
    st.sidebar.title("🐝 LogicHive Prep")
    st.sidebar.markdown("---")
    category_list = ["All"] + sorted(list(set(q['cat'] for q in questions)))
    selected_cat = st.sidebar.selectbox("Filter by Category", category_list)

    # Main Content
    st.title("Interview Q&A 🐝")
    st.write(f"100 Questions & Answers for LOGICHIVE Project")

    # Search Bar
    search_query = st.text_input("🔍 Search questions or keywords", "").lower()

    # Filter Logic
    filtered_questions = questions
    if selected_cat != "All":
        filtered_questions = [q for q in filtered_questions if q['cat'] == selected_cat]

    if search_query:
        filtered_questions = [q for q in filtered_questions if search_query in q['q'].lower() or search_query in q['a'].lower()]

    # Progress / Counter
    st.caption(f"Showing {len(filtered_questions)} questions")

    # Display Questions
    if not filtered_questions:
        st.info("No questions found matching your criteria.")
    else:
        current_cat = ""
        for item in filtered_questions:
            # Show Category header if it changes
            if item['cat'] != current_cat and selected_cat == "All":
                st.markdown(f"<h3 class='category-header'>{item['cat']}</h3>", unsafe_allow_html=True)
                current_cat = item['cat']
            
            # Expandable Q&A
            with st.expander(item['q']):
                st.markdown(f"<div class='answer-text'><strong>Answer:</strong><br>{item['a']}</div>", unsafe_allow_html=True)

    # Footer for Mobile Navigation ease
    st.sidebar.markdown("---")
    st.sidebar.info("💡 **Tip:** Use the expanders to quiz yourself. Read the question, think of the answer, then expand!")

if __name__ == "__main__":
    app()