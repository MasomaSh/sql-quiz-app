
import os
import re

import streamlit as st
from dotenv import load_dotenv
from rag_sql import generate_sql
from supabase import create_client
from quiz_questions import QUESTIONS
from sql_runner import run_sql

load_dotenv()

st.set_page_config(
    page_title="SQL Practice Quiz",
    page_icon="📝",
    layout="centered",
)

# --------------------------------------------------
# 1. ORIGINAL SIMPLE THEME
# --------------------------------------------------
st.markdown(
    """
    <style>
    :root {
        --page-bg: #E8EEF7;
        --card-bg: #F8FAFD;
        --input-bg: #FFFFFF;
        --text-color: #243247;
        --muted-color: #53657A;
        --navy: #234E70;
        --navy-hover: #183B56;
        --code-bg: #102A43;
        --code-text: #FFFFFF;
        --border-color: #C5D2E3;
    }

    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stHeader"] {
        background-color: var(--page-bg) !important;
        color: var(--text-color) !important;
    }

    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp p,
    .stApp label,
    .stApp li,
    .stApp [data-testid="stMarkdownContainer"] {
        color: var(--text-color);
    }

    [data-testid="stSidebar"] {
        background-color: #DCE5F1 !important;
    }

    [data-testid="stSidebar"] * {
        color: var(--text-color) !important;
    }

    [data-testid="stExpander"],
    [data-testid="stExpander"] details,
    [data-testid="stExpander"] summary {
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
        border-color: var(--border-color) !important;
    }

    [data-testid="stExpander"] {
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        margin-bottom: 12px;
    }

    [data-testid="stExpander"] summary {
        font-weight: 600;
        border-radius: 12px !important;
    }

    .stTextArea textarea,
    .stTextInput input {
        background-color: var(--input-bg) !important;
        color: var(--text-color) !important;
        -webkit-text-fill-color: var(--text-color) !important;
        border: 1px solid #AAB8CA !important;
        border-radius: 8px !important;
        caret-color: var(--text-color) !important;
    }

    .stTextArea textarea::placeholder,
    .stTextInput input::placeholder {
        color: #66768A !important;
        -webkit-text-fill-color: #66768A !important;
        opacity: 1 !important;
    }

    .stTextArea textarea:focus,
    .stTextInput input:focus {
        border: 2px solid var(--navy) !important;
        box-shadow: 0 0 0 1px #B8CBE0 !important;
    }

    .stButton > button,
    .stFormSubmitButton > button,
    [data-testid="stPopover"] button {
        background-color: var(--navy) !important;
        color: #FFFFFF !important;
        border: 1px solid var(--navy) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    .stButton > button *,
    .stFormSubmitButton > button *,
    [data-testid="stPopover"] button * {
        color: #FFFFFF !important;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover,
    [data-testid="stPopover"] button:hover {
        background-color: var(--navy-hover) !important;
        border-color: var(--navy-hover) !important;
    }

    .stButton > button:disabled,
    .stFormSubmitButton > button:disabled {
        background-color: #C8D2DF !important;
        color: #526174 !important;
        border-color: #C8D2DF !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        background-color: #DCE5F1 !important;
        border-radius: 8px !important;
        gap: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #DCE5F1 !important;
        color: var(--text-color) !important;
        border-radius: 8px !important;
    }

    .stTabs [data-baseweb="tab"] p {
        color: var(--text-color) !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: var(--navy) !important;
        color: #FFFFFF !important;
    }

    .stTabs [aria-selected="true"] p {
        color: #FFFFFF !important;
    }

    [data-testid="stForm"] {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 18px !important;
    }

    [data-testid="stDataFrame"],
    [data-testid="stTable"] {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        overflow: hidden;
    }

    [data-testid="stMetric"] {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 10px !important;
        padding: 14px !important;
    }

    [data-testid="stMetric"] label,
    [data-testid="stMetric"] [data-testid="stMetricValue"],
    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: var(--text-color) !important;
    }

    [data-testid="stProgress"] > div {
        background-color: #D1DBE8 !important;
        border-radius: 20px;
    }

    [data-testid="stProgress"] [data-testid="stProgressBar"] {
        background-color: var(--navy) !important;
    }

    [data-testid="stAlert"] {
        border-radius: 9px !important;
    }

    [data-testid="stAlert"] p {
        color: var(--text-color) !important;
    }

    [data-testid="stCaptionContainer"] {
        color: var(--muted-color) !important;
    }

    /* ----------------------------------------------
       NAVY BLUE CODE BOXES WITH WHITE TEXT
       Streamlit st.code() includes a built-in
       copy button in each code box.
    ---------------------------------------------- */

    [data-testid="stCode"],
    [data-testid="stCodeBlock"],
    [data-testid="stCode"] > div,
    [data-testid="stCodeBlock"] > div,
    .stCodeBlock,
    .stCodeBlock > div,
    [data-testid="stCode"] pre,
    [data-testid="stCodeBlock"] pre,
    .stCodeBlock pre,
    pre {
        background-color: var(--code-bg) !important;
        color: var(--code-text) !important;
        border: 1px solid #294C68 !important;
        border-radius: 8px !important;
    }

    [data-testid="stCode"] code,
    [data-testid="stCodeBlock"] code,
    .stCodeBlock code,
    pre code,
    code {
        background-color: transparent !important;
        color: var(--code-text) !important;
        -webkit-text-fill-color: var(--code-text) !important;
    }

    [data-testid="stCode"] span,
    [data-testid="stCodeBlock"] span,
    .stCodeBlock span {
        color: var(--code-text) !important;
        -webkit-text-fill-color: var(--code-text) !important;
    }

    /* Copy button styling */
    [data-testid="stCode"] button,
    [data-testid="stCodeBlock"] button,
    [data-testid="stCodeCopyButton"] {
        background-color: #234E70 !important;
        border: 1px solid #6F8FA8 !important;
        border-radius: 6px !important;
        opacity: 1 !important;
    }

    [data-testid="stCode"] button svg,
    [data-testid="stCodeBlock"] button svg,
    [data-testid="stCodeCopyButton"] svg {
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
        stroke: #FFFFFF !important;
    }

    [data-testid="stCode"] button:hover,
    [data-testid="stCodeBlock"] button:hover,
    [data-testid="stCodeCopyButton"]:hover {
        background-color: #183B56 !important;
    }

    [data-testid="stPopoverBody"],
    [data-baseweb="popover"] {
        color: var(--text-color) !important;
    }

    hr {
        border-color: var(--border-color) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("SQL Practice Quiz")
st.write(
    "Practice SQL against a live PostgreSQL database. "
    "Complete five questions worth 4 points each."
)

# --------------------------------------------------
# 2. SUPABASE CONFIGURATION
# --------------------------------------------------
try:
    secret_url = st.secrets["SUPABASE_URL"]
except Exception:
    secret_url = None

try:
    secret_key = st.secrets["SUPABASE_KEY"]
except Exception:
    secret_key = None

supabase_url = secret_url or os.getenv("SUPABASE_URL")
supabase_key = secret_key or os.getenv("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    st.error(
        "Supabase configuration is missing. "
        "Check SUPABASE_URL and SUPABASE_KEY in your .env file."
    )
    st.stop()

if "supabase_client" not in st.session_state:
    st.session_state.supabase_client = create_client(
        supabase_url,
        supabase_key,
    )

client = st.session_state.supabase_client

# --------------------------------------------------
# 3. SESSION STATE
# --------------------------------------------------
defaults = {
    "access_token": None,
    "refresh_token": None,
    "quiz_scores": {},
    "answer_feedback": {},
    "quiz_submitted": False,
    "attempt_id": 1,
    "submission_saved": False,
    "submission_errors": [],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --------------------------------------------------
# 4. SQL VALIDATION AND ANSWER CHECKING
# --------------------------------------------------
def validate_query_ending(query):
    """
    Require a semicolon at the end of a SQL query.
    The quiz intentionally enforces this requirement.
    """
    query = query.strip()

    if not query:
        return "Please enter a SQL query."

    if not query.endswith(";"):
        return (
            "Missing semicolon (;). Add a semicolon at the end "
            "of your SQL query before running or checking it."
        )

    return None


def normalize_rows(dataframe):
    """Convert query results into comparable, ordered rows."""
    return [
        tuple(str(value) for value in row)
        for row in dataframe.itertuples(index=False, name=None)
    ]


def missing_requirements(question_id, query):
    """Check required SQL operations for each quiz question."""
    normalized = re.sub(r"\s+", " ", query.lower()).strip()

    requirements = {
        "q1": [
            (r"\bwhere\b", "WHERE"),
            (r"\border\s+by\b", "ORDER BY"),
            (
                r"\border\s+by\s+customer_id\b",
                "ORDER BY customer_id",
            ),
        ],
        "q2": [
            (r"\border\s+by\b", "ORDER BY"),
            (
                r"\border\s+by\s+price\s+desc\b",
                "ORDER BY price DESC",
            ),
            (
                r"\bproduct_name\b",
                "product_name as the secondary sort",
            ),
        ],
        "q3": [
            (r"\bgroup\s+by\b", "GROUP BY"),
            (r"\bsum\s*\(", "SUM"),
            (r"\border\s+by\b", "ORDER BY"),
        ],
        "q4": [
            (r"\bjoin\b", "JOIN"),
            (r"\border\s+by\b", "ORDER BY"),
        ],
        "q5": [
            (r"\bjoin\b", "JOIN"),
            (r"\border\s+by\b", "ORDER BY"),
            (
                r"\b\w+(?:\.\w+)?\s*\*\s*\w+(?:\.\w+)?\b",
                "multiplication of price by quantity",
            ),
        ],
    }

    return [
        label
        for pattern, label in requirements.get(question_id, [])
        if not re.search(pattern, normalized)
    ]


def compare_answer(question, query):
    """
    Compare the student's output with the expected result.
    The semicolon must be validated before this function is called.
    """
    actual = run_sql(query)
    missing = missing_requirements(question["id"], query)

    if missing:
        return (
            actual,
            False,
            "Your query ran successfully, but it is missing: "
            + ", ".join(missing)
            + ".",
        )

    expected = run_sql(question["solution"])

    actual_columns = list(actual.columns)
    expected_columns = list(expected.columns)

    missing_columns = [
        column
        for column in expected_columns
        if column not in actual_columns
    ]

    extra_columns = [
        column
        for column in actual_columns
        if column not in expected_columns
    ]

    if missing_columns:
        return (
            actual,
            False,
            "Missing required column(s): "
            + ", ".join(missing_columns)
            + ". Add them to your SELECT clause.",
        )

    if extra_columns:
        return (
            actual,
            False,
            "Unexpected column(s): "
            + ", ".join(extra_columns)
            + ". Return only the columns requested in the question.",
        )

    if actual_columns != expected_columns:
        return (
            actual,
            False,
            "The columns are present but in the wrong order. "
            "Return them in this order: "
            + ", ".join(expected_columns)
            + ".",
        )

    actual_rows = normalize_rows(actual)
    expected_rows = normalize_rows(expected)

    if actual_rows == expected_rows:
        return (
            actual,
            True,
            "Correct! Your result matches the expected answer.",
        )

    if sorted(actual_rows) == sorted(expected_rows):
        return (
            actual,
            False,
            "Your rows contain the expected data, but their order "
            "is incorrect. Check the ORDER BY clause.",
        )

    feedback_by_question = {
        "q1": (
            "Your query ran, but it returned the wrong customers. "
            "Check that WHERE filters city to Boston."
        ),
        "q2": (
            "Your product results do not match the expected answer. "
            "Check that you selected the requested products and sorted "
            "by price descending, then product name alphabetically."
        ),
        "q3": (
            "Your calculated quantities are incorrect. Check that SUM "
            "adds quantity and GROUP BY groups rows by product_id."
        ),
        "q4": (
            "Your customer names or order IDs do not match. "
            "Check the JOIN condition using customer_id."
        ),
        "q5": (
            "Your order values are incorrect. Check that you multiply "
            "product price by quantity and join using product_id."
        ),
    }

    return (
        actual,
        False,
        feedback_by_question.get(
            question["id"],
            "Your query ran, but the results do not match the expected answer.",
        ),
    )


# --------------------------------------------------
# 5. SIGN IN AND ACCOUNT CREATION
# --------------------------------------------------
if not st.session_state.access_token:

    login_tab, signup_tab = st.tabs(
        ["Sign in", "Create account"]
    )

    with login_tab:
        with st.form("login_form"):

            email = st.text_input("Email")

            password = st.text_input(
                "Password",
                type="password",
            )

            login_clicked = st.form_submit_button("Sign in")

        if login_clicked:
            try:
                response = client.auth.sign_in_with_password(
                    {
                        "email": email,
                        "password": password,
                    }
                )

                st.session_state.access_token = (
                    response.session.access_token
                )

                st.session_state.refresh_token = (
                    response.session.refresh_token
                )

                st.rerun()

            except Exception:
                st.error(
                    "Sign-in failed. Check your email and password. "
                    "If email confirmation is enabled, confirm your "
                    "account before signing in."
                )

    with signup_tab:
        with st.form("signup_form"):

            new_email = st.text_input(
                "Email",
                key="signup_email",
            )

            new_password = st.text_input(
                "Password",
                type="password",
                key="signup_password",
            )

            signup_clicked = st.form_submit_button("Create account")

        if signup_clicked:

            if len(new_password) < 6:
                st.error(
                    "Use a password with at least 6 characters."
                )

            else:
                try:
                    response = client.auth.sign_up(
                        {
                            "email": new_email,
                            "password": new_password,
                        }
                    )

                    if response.session:

                        st.session_state.access_token = (
                            response.session.access_token
                        )

                        st.session_state.refresh_token = (
                            response.session.refresh_token
                        )

                        st.rerun()

                    else:
                        st.info(
                            "Your account was created. Check your "
                            "email if confirmation is required, then "
                            "sign in."
                        )

                except Exception:
                    st.error(
                        "Account creation failed. The email may "
                        "already be registered, or the password may "
                        "not meet the configured requirements."
                    )

    st.stop()


# --------------------------------------------------
# 6. RESTORE USER SESSION
# --------------------------------------------------
try:
    client.auth.set_session(
        st.session_state.access_token,
        st.session_state.refresh_token,
    )

    user = client.auth.get_user().user

except Exception:
    st.session_state.access_token = None
    st.session_state.refresh_token = None

    st.warning("Your session expired. Please sign in again.")

    st.stop()

st.success(f"Signed in as {user.email}")


# --------------------------------------------------
# AI SQL ASSISTANT (RAG)
# --------------------------------------------------
st.divider()

st.header("AI SQL Assistant")

st.write(
    "Ask a question about your database in plain English. "
    "The assistant retrieves relevant schema information from "
    "ChromaDB before generating PostgreSQL SQL with Gemini."
)

natural_language_question = st.text_area(
    "What would you like to find out?",
    placeholder="Example: Show the five most expensive products.",
    key="rag_natural_language_question",
)

if st.button("Generate SQL", key="generate_rag_sql"):

    if not natural_language_question.strip():
        st.warning("Please enter a question first.")

    else:
        try:
            with st.spinner(
                "Retrieving schema and generating SQL..."
            ):
                generated_sql, retrieved_context = generate_sql(
                    natural_language_question.strip()
                )

            st.subheader("Retrieved database context")

            for document in retrieved_context:
                # Each st.code box has its own built-in copy button.
                st.code(document, language="text")

            st.subheader("Generated SQL")

            # This box also has its own built-in copy button.
            st.code(generated_sql, language="sql")

        except Exception as exc:
            st.error(f"Could not generate SQL: {exc}")


# --------------------------------------------------
# SIGN OUT
# --------------------------------------------------
if st.button("Sign out"):

    try:
        client.auth.sign_out()

    finally:
        st.session_state.access_token = None
        st.session_state.refresh_token = None
        st.session_state.quiz_scores = {}
        st.session_state.answer_feedback = {}
        st.session_state.quiz_submitted = False
        st.session_state.submission_saved = False
        st.session_state.submission_errors = []

        st.rerun()


# --------------------------------------------------
# 7. QUIZ QUESTIONS
# --------------------------------------------------
st.divider()

st.subheader("Your SQL Quiz")

st.caption("5 questions · 4 points each · 20 points total")

scores = st.session_state.quiz_scores
feedback = st.session_state.answer_feedback
attempt_id = st.session_state.attempt_id

st.progress(
    len(scores) / len(QUESTIONS),
    text=f"{len(scores)} of {len(QUESTIONS)} questions checked",
)

st.metric(
    "Current score",
    f"{sum(scores.values())} / 20",
)

for number, question in enumerate(QUESTIONS, start=1):

    qid = question["id"]

    query_key = f"query_{attempt_id}_{qid}"
    result_key = f"result_{attempt_id}_{qid}"
    checked_key = f"checked_{attempt_id}_{qid}"

    with st.expander(
        f"Question {number}: {question['title']} "
        f"({question['points']} points)",
        expanded=not st.session_state.quiz_submitted,
    ):

        st.write(question["prompt"])

        with st.popover("Show hint"):
            st.write(question["hint"])

        student_query = st.text_area(
            "Write your SQL query",
            key=query_key,
            height=150,
            placeholder="SELECT ...;",
            disabled=st.session_state.quiz_submitted,
        )

        previous_query = st.session_state.get(checked_key)

        if (
            previous_query is not None
            and previous_query != student_query
            and not st.session_state.quiz_submitted
        ):

            scores.pop(qid, None)
            feedback.pop(qid, None)

            st.session_state.pop(checked_key, None)
            st.session_state.pop(result_key, None)

        run_col, check_col = st.columns(2)

        with run_col:

            run_clicked = st.button(
                "Run Query",
                key=f"run_{attempt_id}_{qid}",
                disabled=st.session_state.quiz_submitted,
                use_container_width=True,
            )

        with check_col:

            check_clicked = st.button(
                "Check Answer",
                key=f"check_{attempt_id}_{qid}",
                disabled=st.session_state.quiz_submitted,
                use_container_width=True,
            )

        # ------------------------------------------
        # RUN QUERY
        # ------------------------------------------
        if run_clicked:

            validation_error = validate_query_ending(
                student_query
            )

            if validation_error:

                st.error(validation_error)

                st.session_state.pop(result_key, None)

            else:

                try:
                    result = run_sql(student_query)

                    st.session_state[result_key] = result

                    missing = missing_requirements(
                        qid,
                        student_query,
                    )

                    if missing:

                        st.warning(
                            "Your query executed, but it is missing "
                            "required element(s): "
                            + ", ".join(missing)
                            + ". See the hint for guidance."
                        )

                    else:

                        expected = run_sql(question["solution"])

                        expected_columns = list(expected.columns)
                        actual_columns = list(result.columns)

                        missing_columns = [
                            column
                            for column in expected_columns
                            if column not in actual_columns
                        ]

                        extra_columns = [
                            column
                            for column in actual_columns
                            if column not in expected_columns
                        ]

                        if missing_columns:

                            st.warning(
                                "Missing required column(s): "
                                + ", ".join(missing_columns)
                                + ". Add them to your SELECT clause."
                            )

                        elif extra_columns:

                            st.warning(
                                "Unexpected column(s): "
                                + ", ".join(extra_columns)
                                + ". Return only the requested columns."
                            )

                        elif actual_columns != expected_columns:

                            st.warning(
                                "Your columns are in the wrong order. "
                                "Expected: "
                                + ", ".join(expected_columns)
                                + "."
                            )

                        elif normalize_rows(result) == normalize_rows(expected):

                            st.success(
                                "Your results match the expected answer. "
                                "Click Check Answer to receive your points."
                            )

                        elif sorted(normalize_rows(result)) == sorted(
                            normalize_rows(expected)
                        ):

                            st.warning(
                                "Your rows are correct, but their order "
                                "is incorrect. Check ORDER BY."
                            )

                        else:

                            st.warning(
                                "Your query ran, but the data is incorrect. "
                                "Check the filters, calculations, or joins "
                                "required by this question."
                            )

                except Exception as error:

                    st.session_state.pop(result_key, None)

                    st.error(
                        "SQL execution failed. Check your syntax, table "
                        "names, column names, and SQL operations. "
                        f"Database message: {error}"
                    )

        # ------------------------------------------
        # CHECK ANSWER
        # ------------------------------------------
        if check_clicked:

            validation_error = validate_query_ending(
                student_query
            )

            if validation_error:

                st.error(validation_error)

            else:

                try:
                    result, correct, message = compare_answer(
                        question,
                        student_query,
                    )

                    st.session_state[result_key] = result

                    scores[qid] = (
                        question["points"] if correct else 0
                    )

                    feedback[qid] = message

                    st.session_state[checked_key] = student_query

                    if correct:

                        st.success(
                            f"Correct! You earned "
                            f"{question['points']} points."
                        )

                    else:

                        st.warning(message)

                except Exception as error:

                    scores[qid] = 0

                    feedback[qid] = (
                        "SQL execution failed. Check the query syntax "
                        f"and database message: {error}"
                    )

                    st.session_state[checked_key] = student_query

                    st.error(feedback[qid])

        # ------------------------------------------
        # SHOW THE MOST RECENT RESULT
        # ------------------------------------------
        if result_key in st.session_state:

            st.caption("Query results")

            st.dataframe(
                st.session_state[result_key],
                use_container_width=True,
            )

        if qid in scores:

            st.caption(
                f"Points earned: {scores[qid]} / "
                f"{question['points']}"
            )


# --------------------------------------------------
# 8. SUBMIT QUIZ
# --------------------------------------------------
st.divider()

if not st.session_state.quiz_submitted:

    st.subheader("Finished answering?")

    unanswered = [
        question
        for question in QUESTIONS
        if question["id"] not in scores
    ]

    if unanswered:

        st.info(
            f"{len(unanswered)} question(s) have not been checked. "
            "Unchecked questions receive zero points."
        )

    if st.button(
        "Submit Quiz",
        type="primary",
        use_container_width=True,
    ):

        final_score = sum(scores.values())

        save_errors = []

        for question in QUESTIONS:

            qid = question["id"]

            query_key = f"query_{attempt_id}_{qid}"

            try:
                client.table("quiz_submissions").insert(
                    {
                        "user_id": str(user.id),
                        "question_id": qid,
                        "query_text": st.session_state.get(
                            query_key,
                            "",
                        ),
                    }
                ).execute()

            except Exception as error:

                save_errors.append(
                    f"{qid}: {error}"
                )

        st.session_state.final_score = final_score

        st.session_state.quiz_submitted = True

        st.session_state.submission_saved = not save_errors

        st.session_state.submission_errors = save_errors

        st.rerun()


# --------------------------------------------------
# 9. COMPLETION SCREEN
# --------------------------------------------------
if st.session_state.quiz_submitted:

    st.balloons()

    st.header("Quiz Complete!")

    st.metric(
        "Final score",
        f"{st.session_state.get('final_score', 0)} / 20",
    )

    st.write("Your results:")

    for number, question in enumerate(QUESTIONS, start=1):

        points = scores.get(question["id"], 0)

        st.write(
            f"**Question {number}: {question['title']}** — "
            f"{points} / {question['points']} points"
        )

    if st.session_state.submission_saved:

        st.success(
            "Your quiz submissions were saved to Supabase."
        )

    else:

        st.warning(
            "The quiz is complete, but one or more submissions "
            "could not be saved. Check your Supabase permissions."
        )

        for error in st.session_state.submission_errors:
            st.caption(error)

    if st.button(
        "Start a New Attempt",
        use_container_width=True,
    ):

        st.session_state.attempt_id += 1

        st.session_state.quiz_scores = {}

        st.session_state.answer_feedback = {}

        st.session_state.quiz_submitted = False

        st.session_state.submission_saved = False

        st.session_state.submission_errors = []

        st.rerun()
