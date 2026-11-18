
import streamlit as st
import requests
import pandas as pd
import sqlite3

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Predictive Maintenance Dashboard",
    page_icon="⚙️",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000/predict"


# ---------------- SQLITE DATABASE ----------------

def init_database():

    conn = sqlite3.connect("prediction_history.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_type TEXT,
            air_temperature REAL,
            process_temperature REAL,
            rotational_speed INTEGER,
            torque REAL,
            tool_wear INTEGER,
            failure_probability REAL,
            prediction TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    columns = [
        row[1] for row in
        conn.execute("PRAGMA table_info(predictions)").fetchall()
    ]

    if "air_temperature" not in columns:
        conn.execute(
            "ALTER TABLE predictions ADD COLUMN air_temperature REAL"
        )

    if "process_temperature" not in columns:
        conn.execute(
            "ALTER TABLE predictions ADD COLUMN process_temperature REAL"
        )

    conn.commit()
    conn.close()


def save_prediction(
    machine_type,
    air_temperature,
    process_temperature,
    rotational_speed,
    torque,
    tool_wear,
    probability,
    prediction
):

    conn = sqlite3.connect("prediction_history.db")

    conn.execute("""
        INSERT INTO predictions
        (
            machine_type,
            air_temperature,
            process_temperature,
            rotational_speed,
            torque,
            tool_wear,
            failure_probability,
            prediction
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        machine_type,
        air_temperature,
        process_temperature,
        rotational_speed,
        torque,
        tool_wear,
        probability,
        prediction
    ))

    conn.commit()
    conn.close()


def get_prediction_history():

    conn = sqlite3.connect("prediction_history.db")

    history = pd.read_sql_query(
        "SELECT * FROM predictions ORDER BY id DESC",
        conn
    )

    conn.close()

    return history


def clear_database_history():

    conn = sqlite3.connect("prediction_history.db")

    conn.execute("DELETE FROM predictions")

    conn.commit()
    conn.close()


# Initialize database
init_database()


# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background-color: #F3F6FA;
}

h1, h2, h3 {
    color: #17365D;
}

.block-container {
    padding-top: 2rem;
}

div[data-testid="stMetric"] {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #DCE3ED;
}

.stButton > button {
    background-color: #17365D;
    color: white;
    width: 100%;
    height: 50px;
    border-radius: 10px;
    font-size: 17px;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #24558A;
    color: white;
}
</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------

st.title("⚙️ Predictive Maintenance System")

st.write("### Machine Failure Prediction Dashboard")

st.caption(
    "An intelligent machine monitoring system powered by "
    "Machine Learning and Gradient Boosting."
)

st.divider()


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.header("📊 About the System")

    st.write(
        "This system predicts possible machine failure "
        "using operating parameters."
    )

    st.divider()

    st.subheader("Technology Stack")

    st.write("🤖 Machine Learning: Gradient Boosting")
    st.write("⚡ Backend: FastAPI")
    st.write("🎨 Frontend: Streamlit")
    st.write("🐍 Language: Python")

    st.divider()

    st.caption("Predictive Maintenance Project")


# ---------------- MACHINE INPUT SECTION ----------------

st.header("🔧 Machine Operating Parameters")

st.write(
    "Enter the machine details below to generate a prediction."
)

col1, col2 = st.columns(2)

with col1:

    machine_type = st.selectbox(
        "Machine Type",
        ["L", "M", "H"],
        help="L = Low, M = Medium, H = High"
    )

    air_temperature = st.number_input(
        "Air Temperature (K)",
        min_value=250.0,
        max_value=350.0,
        value=300.0
    )

    process_temperature = st.number_input(
        "Process Temperature (K)",
        min_value=250.0,
        max_value=400.0,
        value=310.0
    )

with col2:

    rotational_speed = st.number_input(
        "Rotational Speed (rpm)",
        min_value=0,
        max_value=5000,
        value=1500
    )

    torque = st.number_input(
        "Torque (Nm)",
        min_value=0.0,
        max_value=100.0,
        value=40.0
    )

    tool_wear = st.number_input(
        "Tool Wear (minutes)",
        min_value=0,
        max_value=300,
        value=100
    )

st.divider()


# ---------------- PREDICTION ----------------

if st.button("🔍 ANALYZE MACHINE CONDITION"):

    input_data = {
        "Type": machine_type,
        "air_temperature": air_temperature,
        "process_temperature": process_temperature,
        "rotational_speed": rotational_speed,
        "torque": torque,
        "tool_wear": tool_wear
    }

    try:

        with st.spinner("Analyzing machine parameters..."):

            response = requests.post(
                API_URL,
                json=input_data,
                timeout=30
            )

        if response.status_code == 200:

            result = response.json()

            prediction = result["prediction"]

            probability = float(
                result["failure_probability"]
            )

            # Keep probability between 0 and 100
            probability = max(
                0.0,
                min(100.0, probability)
            )

            # Save prediction permanently in SQLite
            save_prediction(
                machine_type,
                air_temperature,
                process_temperature,
                rotational_speed,
                torque,
                tool_wear,
                probability,
                prediction
            )

            # Save prediction details in session history
            st.session_state.history = (
                st.session_state.history
                if "history" in st.session_state
                else []
            )

            st.session_state.history.append({
                "Machine Type": machine_type,
                "Air Temperature": air_temperature,
                "Process Temperature": process_temperature,
                "Rotational Speed": rotational_speed,
                "Torque": torque,
                "Tool Wear": tool_wear,
                "Failure Probability (%)": round(probability, 2),
                "Prediction": prediction
            })

            # ---------------- ANALYSIS RESULTS ----------------

            st.header("📊 Machine Analysis Results")

            result_col1, result_col2 = st.columns(2)

            with result_col1:

                st.metric(
                    "Machine Status",
                    prediction
                )

            with result_col2:

                st.metric(
                    "Failure Probability",
                    f"{probability:.2f}%"
                )

            st.subheader("Failure Probability Indicator")

            st.progress(probability / 100)

            if prediction == "No Machine Failure":

                st.success(
                    "✅ Machine is predicted to operate normally."
                )

            else:

                st.error(
                    "⚠️ Machine failure is predicted. "
                    "Inspection is recommended."
                )

            st.info(
                "Note: This is a Machine Learning prediction. "
                "It does not guarantee actual machine performance."
            )

            # ---------------- MACHINE HEALTH OVERVIEW ----------------

            st.divider()

            st.subheader("🏭 Machine Health Overview")

            st.write("Operating condition summary")

            health_col1, health_col2, health_col3 = st.columns(3)

            with health_col1:

                st.metric("Machine Type", machine_type)

                st.metric(
                    "Air Temperature",
                    f"{air_temperature:.1f} K"
                )

            with health_col2:

                st.metric(
                    "Process Temperature",
                    f"{process_temperature:.1f} K"
                )

                st.metric(
                    "Rotational Speed",
                    f"{rotational_speed} rpm"
                )

            with health_col3:

                st.metric(
                    "Torque",
                    f"{torque:.1f} Nm"
                )

                st.metric(
                    "Tool Wear",
                    f"{tool_wear} minutes"
                )

            st.caption(
                "These values represent the machine parameters "
                "submitted for the current prediction."
            )

        else:

            st.error(
                f"Backend Error: {response.status_code}"
            )

            st.write(response.text)

    except requests.exceptions.ConnectionError:

        st.error(
            "Cannot connect to FastAPI. "
            "Please start the backend server."
        )

    except requests.exceptions.Timeout:

        st.error(
            "The backend took too long to respond. "
            "Please try again."
        )

    except Exception as e:

        st.error(f"Unexpected Error: {e}")


# ---------------- PREDICTION HISTORY ----------------

st.divider()

st.header("📈 Prediction Analytics")

history_df = get_prediction_history()

if not history_df.empty:

    st.subheader("Prediction Overview")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Predictions",
            len(history_df)
        )

    with col2:

        failure_count = (
            history_df["prediction"] != "No Machine Failure"
        ).sum()

        st.metric(
            "Failure Predictions",
            int(failure_count)
        )

    with col3:

        average_probability = (
            history_df["failure_probability"].mean()
        )

        st.metric(
            "Average Failure Probability",
            f"{average_probability:.2f}%"
        )

    st.subheader("Failure Probability Trend")

    chart_data = history_df[
        ["failure_probability"]
    ].copy()

    chart_data.index = range(1, len(chart_data) + 1)

    st.line_chart(chart_data)

    st.subheader("Previous Predictions")

    st.dataframe(
        history_df,
        width="stretch",
        hide_index=True
    )

    if st.button("🗑️ Clear Prediction History"):

        clear_database_history()

        st.success("Prediction history cleared!")

        st.rerun()

else:

    st.info(
        "No prediction history available. "
        "Analyze a machine to start building your history."
    )


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "Predictive Maintenance System | "
    "Gradient Boosting | FastAPI | Streamlit"
)
