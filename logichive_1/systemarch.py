import streamlit as st

def app():
    # Custom Styles
    st.markdown("""
        <style>
    .reportview-container {
        background: #f8f9fa;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px;
        color: #2c3e50; /* Force dark text */
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #e3f2fd;
        border-bottom: 3px solid #1976d2;
    }
    .flow-card {
        background-color: white;
        color: #2c3e50; /* Force dark text */
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1976d2;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .highlight {
        color: #d32f2f;
        font-weight: bold;
    }
    /* Ensure markdown text is visible if theme fails */
    p, li, h1, h2, h3, h4, h5, h6 {
        color: #2c3e50;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("🏗️ LOGICHIVE System Deep Dive")
    st.write("A comprehensive reverse-engineering guide to the platform's architecture and critical workflows.")

    # Tabs for Organization
    tab1, tab2, tab3, tab4 = st.tabs([
        "📍 High-Level Architecture", 
        "🔄 Critical Workflows", 
        "💻 Code Logic Analysis", 
        "🎯 Interview Readiness"
    ])

    with tab1:
        st.header("1. High-Level Architecture")
        st.write("LOGICHIVE uses a **Microservices Architecture** to ensure independent scaling and technology diversity.")
        
        # Updated Mermaid Diagram based on user provided structure
        st.markdown("""
        ### System Architecture Diagram
        ```mermaid
        graph TD
            subgraph Client_Layer [Frontend Layer]
                User((User)) -->|HTTPS| React[Frontend - React/Vite]
            end

            subgraph Backend_Services [Backend Services - Docker Network]
                React -->|REST API| US[:3001 User Service]
                React -->|REST API| PS[:3002 Problem Service]
                React -->|REST API| SS[:3003 Submission Service]
                React -->|REST API| GS[:3004 GitHub Service]
                React -->|REST API| CS[:3005 Competition Service]
                React -->|REST API| AS[:8000 AI Service - Python]

                SS -->|Queue| Redis[(Redis Cache/Queue)]
                Redis -->|Process| Worker[Submission Processor]
                Worker -->|HTTP| Judge[Judge0 API - Code Execution]
            end

            subgraph Data_Layer [Data Layer]
                US ---|Read/Write| DB[(PostgreSQL)]
                PS ---|Read/Write| DB
                SS ---|Read/Write| DB
                CS ---|Read/Write| DB
            end

            style Client_Layer fill:#f9f,stroke:#333,stroke-width:2px
            style Backend_Services fill:#e1f5fe,stroke:#01579b,stroke-width:2px
            style Data_Layer fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
        ```
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Key Components:**
            - **Frontend:** React application that serves as the UI. It talks directly to backend services via REST APIs.
            - **User Service (:3001):** Handles Registration, Login, and JWT generation.
            - **Problem Service (:3002):** Manages coding problems and test cases.
            - **Submission Service (:3003):** The core engine handling code execution flow.
            """)
        with col2:
            st.markdown("""
            - **GitHub Service (:3004):** Handles auto-pushing code to user repositories.
            - **Competition Service (:3005):** Manages contests, leaderboards, and real-time updates.
            - **AI Service (:8000):** Python-based service for problem recommendations.
            - **Redis/PostgreSQL:** Shared infrastructure for messaging, queuing, and persistent storage.
            """)

    with tab2:
        st.header("2. Life of a Request")
        
        st.subheader("A. Authentication Flow (Stateless)")
        st.markdown("""
        <div class="flow-card">
        1. <b>Credential Entry:</b> User submits email/password.<br>
        2. <b>Validation:</b> User service verifies against DB.<br>
        3. <b>Token Issuance:</b> Service signs a <b>JWT</b> with a secret key.<br>
        4. <b>Storage:</b> Frontend saves JWT in <i>localStorage</i>.<br>
        5. <b>Verification:</b> Other services use a <b>Passport Strategy</b> to verify tokens without DB lookups.
        </div>
        """, unsafe_allow_html=True)

        st.subheader("B. The Submission Engine (Asynchronous)")
        st.markdown("""
        <div class="flow-card">
        1. <b>Submission:</b> User clicks Submit. Controller creates a DB record as <span class="highlight">Pending</span>.<br>
        2. <b>Enqueuing:</b> Job is pushed to <b>Redis</b>. Controller returns ID immediately.<br>
        3. <b>Worker:</b> <i>Submission Processor</i> picks up the job.<br>
        4. <b>Judge0 Integration:</b> Code is sent to the remote sandbox. Processor polls for results.<br>
        5. <b>Update:</b> DB status is updated (Accepted/Wrong/TLE).<br>
        6. <b>Side Effects:</b> Trigger GitHub push or Leaderboard update.
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.header("3. Critical Code Breakdown")
        
        with st.expander("The Submission Processor (submissions.processor.ts)"):
            st.write("This file is the heart of the system. It handles background jobs.")
            st.code("""
    @Process('execute')
    async handleExecution(job: Job) {
    // 1. Inject Boilerplate
    const fullCode = this.injectBoilerplate(job.data.code);
    
    // 2. Call Judge0
    const result = await this.executeInSandbox(fullCode);
    
    // 3. Sanitize (Handle Null Bytes for Postgres)
    const safeOutput = result.stdout.replace(/\\u0000/g, '');
    
    // 4. Finalize
    await this.updateStatus(job.id, safeOutput);
    }
            """, language="typescript")
            st.info("💡 **Key Fact:** We use base64 encoding when talking to Judge0 to handle non-ASCII characters in code safely.")

        with st.expander("The JWT Strategy (jwt.strategy.ts)"):
            st.write("Ensures services can verify users independently.")
            st.code("""
    export class JwtStrategy extends PassportStrategy(Strategy) {
    constructor() {
        super({
        jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
        secretOrKey: process.env.JWT_SECRET,
        });
    }
    
    async validate(payload: any) {
        return { userId: payload.sub, username: payload.username };
    }
    }
            """, language="typescript")

    with tab4:
        st.header("4. Interview Cheat Sheet")
        
        st.markdown("""
        | Question | Strategic Answer |
        | :--- | :--- |
        | **Shared DB?** | Shared DB simplifies consistency and joins during the 'build' phase, though we move to DB-per-service for extreme scale. |
        | **Service Failure?** | If the Submission service crashes, jobs persist in **Redis**. On restart, the worker picks up exactly where it left off. |
        | **Real-time?** | Current UI polls the status. Future improvement: **WebSockets** for a 'push' notification when the judge is done. |
        | **Why Python?** | Python is used for the AI service specifically for **Scikit-learn** and **Pandas** support which is superior to Node for ML. |
        """)
        
        st.success("🎯 **Final Summary:** LogicHive is a polyglot system (Node/Python) that balances synchronous user management with heavy asynchronous processing for code execution.")

    # Sidebar for Navigation Help
    st.sidebar.title("🏗️ System Manual")
    st.sidebar.info("Use this app to walkthrough the technical architecture during your interview.")
    st.sidebar.warning("⚠️ Remember: The 'Submission Processor' is the most technically complex part. Be ready to explain the Redis/BullMQ flow.")

if __name__ == "__main__":
    app()