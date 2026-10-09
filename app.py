import requests
import pandas as pd
import streamlit as st

st.set_page_config(page_title="AI Code Review Assistant", page_icon="🔍", layout="wide")

HEADERS = {"ngrok-skip-browser-warning": "true"}
ICONS = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}
ORDER = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}

st.title("🔍 AI Code Review Assistant")
st.caption("Paste or upload Python code to get issues, severity, explanations and suggested fixes.")

# ---------- Sidebar: connection to the Kaggle backend ----------
with st.sidebar:
    st.header("Settings")
    api_url = st.text_input("Backend URL (from Kaggle)", placeholder="https://xxxx.ngrok-free.app")
    api_url = api_url.strip().rstrip("/")

    if st.button("Check connection"):
        if not api_url:
            st.warning("Paste the URL first.")
        else:
            try:
                r = requests.get(api_url + "/health", headers=HEADERS, timeout=15)
                if r.status_code == 200:
                    st.success("Connected ✅")
                else:
                    st.error(f"Server answered with status {r.status_code}")
            except Exception as e:
                st.error(f"Could not connect: {e}")

    st.markdown("---")
    st.markdown(
        "**How to use**\n"
        "1. Run the Kaggle notebook\n"
        "2. Copy the public URL it prints\n"
        "3. Paste it above\n"
        "4. Add your code and click **Review**"
    )

# ---------- Input ----------
uploaded = st.file_uploader("Upload a Python file", type=["py"])

if uploaded is not None:
    code = uploaded.read().decode("utf-8", errors="ignore")
    file_name = uploaded.name
    st.code(code, language="python")
else:
    file_name = st.text_input("File name", value="main.py")
    code = st.text_area("...or paste your code here", height=300)

# ---------- Review ----------
if st.button("Review code", type="primary"):
    if not api_url:
        st.error("Paste the backend URL in the sidebar first.")
    elif not code.strip():
        st.error("Please add some code.")
    else:
        with st.spinner("Reviewing... this can take a few minutes."):
            try:
                r = requests.post(
                    api_url + "/review",
                    json={"code": code, "file_name": file_name},
                    headers=HEADERS,
                    timeout=900,
                )
                if r.status_code == 200:
                    st.session_state["result"] = r.json()
                else:
                    st.error(f"Server error {r.status_code}: {r.text[:300]}")
            except Exception as e:
                st.error(f"Request failed: {e}")

# ---------- Output ----------
result = st.session_state.get("result")
if result:
    st.markdown("---")
    st.subheader("Code summary")
    st.write(result["summary"])

    issues = sorted(result["issues"], key=lambda i: ORDER.get(i.get("severity"), 9))

    st.subheader(f"Issues found: {len(issues)}")
    if not issues:
        st.success("No issues found.")
    else:
        cols = st.columns(4)
        for col, level in zip(cols, ["Critical", "High", "Medium", "Low"]):
            count = sum(1 for i in issues if i.get("severity") == level)
            col.metric(f"{ICONS[level]} {level}", count)

        for i in issues:
            sev = i.get("severity", "")
            with st.expander(f"{ICONS.get(sev, '⚪')} {i.get('issue', '')}  |  {sev}"):
                st.markdown(f"**File:** `{i.get('file', '')}`")
                st.markdown(f"**Explanation:** {i.get('explanation', '')}")
                st.markdown("**Suggested fix:**")
                st.code(str(i.get("suggested_fix", "")).replace("\\n", "\n"), language="python")

        df = pd.DataFrame(issues)[["file", "issue", "severity", "explanation", "suggested_fix"]]
        st.download_button("Download results (CSV)", df.to_csv(index=False),
                           file_name="code_review.csv", mime="text/csv")