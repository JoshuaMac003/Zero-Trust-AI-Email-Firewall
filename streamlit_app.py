"""
Streamlit Frontend - Zero-Trust AI Email Firewall
Interactive web interface for email scanning and firewall management
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Page configuration
st.set_page_config(
    page_title="Zero-Trust AI Email Firewall",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-box {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .safe {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
    }
    .suspicious {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
    }
    .phishing {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
    }
    .metric-box {
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 5px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)


# Helper Functions
@st.cache_data(ttl=60)
def check_api_health():
    """Check API health status"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200, response.json()
    except:
        return False, None


def scan_email(email_text: str, sender: str = "", recipient: str = "", subject: str = ""):
    """Scan email using API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/scan-email",
            json={
                "email_text": email_text,
                "sender": sender,
                "recipient": recipient,
                "subject": subject
            },
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return None


def get_analytics():
    """Get analytics from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/analytics", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None


def get_logs(limit: int = 100, decision: str = None):
    """Get email logs from API"""
    try:
        params = {"limit": limit}
        if decision:
            params["decision"] = decision
        response = requests.get(f"{API_BASE_URL}/logs", params=params, timeout=5)
        if response.status_code == 200:
            return response.json().get("logs", [])
        else:
            return []
    except:
        return []


def get_trusted_domains():
    """Get trusted domains from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/trusted-domains", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("trusted_domains", [])
        else:
            return []
    except:
        return []


def add_trusted_domain(domain: str):
    """Add trusted domain via API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/add-trusted-domain",
            json={"domain": domain, "added_by": "admin"},
            timeout=5
        )
        return response.status_code == 200
    except:
        return False


def remove_trusted_domain(domain: str):
    """Remove trusted domain via API"""
    try:
        response = requests.delete(
            f"{API_BASE_URL}/remove-trusted-domain/{domain}",
            timeout=5
        )
        return response.status_code == 200
    except:
        return False


# Sidebar
with st.sidebar:
    st.header("🛡️ Zero-Trust AI Email Firewall")
    st.markdown("---")
    
    # API Health Check
    api_healthy, health_data = check_api_health()
    if api_healthy and health_data:
        if health_data.get("model_loaded") and health_data.get("database_initialized"):
            st.success("✅ API Connected")
            st.success("✅ Model Loaded")
            st.success("✅ Database Initialized")
        else:
            st.warning("⚠️ API Connected (Model or DB not ready)")
    else:
        st.error("❌ API Not Connected")
        st.info(f"Ensure API is running at: {API_BASE_URL}")
    
    st.markdown("---")
    
    # Navigation
    page = st.selectbox(
        "Navigation",
        ["Dashboard", "Email Scanner", "Analytics", "Logs", "Admin Panel"]
    )


# Main Content
if page == "Dashboard":
    st.markdown('<h1 class="main-header">🛡️ Zero-Trust AI Email Firewall</h1>', unsafe_allow_html=True)
    
    # Get analytics
    analytics = get_analytics()
    
    if analytics:
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Emails", analytics.get("total_emails", 0))
        
        with col2:
            st.metric("Phishing Emails", analytics.get("phishing_emails", 0),
                     f"{analytics.get('phishing_percentage', 0):.1f}%")
        
        with col3:
            st.metric("Blocked", analytics.get("blocked_emails", 0))
        
        with col4:
            st.metric("Quarantined", analytics.get("quarantined_emails", 0))
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Email Distribution
            fig = px.pie(
                values=[
                    analytics.get("safe_emails", 0),
                    analytics.get("suspicious_emails", 0),
                    analytics.get("phishing_emails", 0)
                ],
                names=["Safe", "Suspicious", "Phishing"],
                title="Email Distribution",
                color_discrete_map={
                    "Safe": "#4caf50",
                    "Suspicious": "#ff9800",
                    "Phishing": "#f44336"
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Metrics Bar Chart
            fig = go.Figure(data=[
                go.Bar(
                    x=["Safe", "Suspicious", "Phishing", "Blocked", "Quarantined"],
                    y=[
                        analytics.get("safe_emails", 0),
                        analytics.get("suspicious_emails", 0),
                        analytics.get("phishing_emails", 0),
                        analytics.get("blocked_emails", 0),
                        analytics.get("quarantined_emails", 0)
                    ],
                    marker_color=["#4caf50", "#ff9800", "#f44336", "#f44336", "#ff9800"]
                )
            ])
            fig.update_layout(title="Email Statistics", xaxis_title="Category", yaxis_title="Count")
            st.plotly_chart(fig, use_container_width=True)
        
        # Average Scores
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Average AI Confidence", f"{analytics.get('avg_confidence', 0):.2%}")
        with col2:
            st.metric("Average Trust Score", f"{analytics.get('avg_trust_score', 0):.2%}")
    
    else:
        st.warning("Unable to load analytics. Ensure API is running.")


elif page == "Email Scanner":
    st.header("📧 Email Scanner")
    st.markdown("---")
    
    # Scanner Mode
    scanner_mode = st.radio(
        "Scanner Mode",
        ["Single Email", "Batch Upload (CSV)"],
        horizontal=True
    )
    
    if scanner_mode == "Single Email":
        # Single Email Scanner
        col1, col2 = st.columns(2)
        
        with col1:
            sender = st.text_input("Sender Email", placeholder="sender@example.com")
            recipient = st.text_input("Recipient Email", placeholder="recipient@example.com")
            subject = st.text_input("Subject", placeholder="Email subject")
        
        with col2:
            st.markdown("### Email Text")
            email_text = st.text_area(
                "Enter email text",
                height=300,
                placeholder="Subject: URGENT: Your Account Will Be Suspended\n\nDear Customer,\n\nYour account will be suspended. Click here to verify: http://fake-link.com"
            )
        
        if st.button("🔍 Scan Email", type="primary", use_container_width=True):
            if email_text:
                with st.spinner("Scanning email..."):
                    result = scan_email(email_text, sender, recipient, subject)
                    
                    if result:
                        st.markdown("---")
                        st.subheader("📊 Scan Results")
                        
                        # Prediction Box
                        decision = result.get("zero_trust_decision", "Unknown")
                        action = result.get("action", "Unknown")
                        confidence_class = decision.lower()
                        
                        st.markdown(f"""
                        <div class="prediction-box {confidence_class}">
                            <h2>Decision: {decision} - Action: {action}</h2>
                            <p><strong>AI Prediction:</strong> {result.get('ai_prediction', 'Unknown')}</p>
                            <p><strong>AI Confidence:</strong> {result.get('ai_confidence', 0):.2%}</p>
                            <p><strong>Trust Score:</strong> {result.get('trust_score', 0):.2%}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Metrics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("AI Confidence", f"{result.get('ai_confidence', 0):.2%}")
                        with col2:
                            st.metric("Trust Score", f"{result.get('trust_score', 0):.2%}")
                        with col3:
                            st.metric("Domain", result.get('domain', 'Unknown'))
                        
                        # Explainability
                        with st.expander("🔍 Explainability", expanded=True):
                            st.markdown("### Reasons for Decision")
                            reasons = result.get('reasons', [])
                            for reason in reasons:
                                st.write(f"• {reason}")
                            
                            st.markdown("### Features")
                            features = result.get('features', {})
                            if features:
                                st.json(features)
                        
                        # Trust Components
                        with st.expander("🛡️ Zero-Trust Analysis"):
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.write(f"**SPF Check:** {'✅ Pass' if result.get('spf_check') else '❌ Fail'}")
                            with col2:
                                st.write(f"**DKIM Check:** {'✅ Pass' if result.get('dkim_check') else '❌ Fail'}")
                            with col3:
                                st.write(f"**Domain:** {result.get('domain', 'Unknown')}")
            else:
                st.warning("Please enter email text to scan.")
        
        # Example Emails
        st.markdown("---")
        st.subheader("🧪 Example Emails")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Phishing Email:**")
            example_phishing = """Subject: URGENT: Your Account Will Be Suspended

Dear Customer,

We have detected unusual activity on your account. To prevent suspension, please verify your account immediately by clicking the link below:

http://verify-account-now.com/urgent

If you do not verify within 24 hours, your account will be permanently suspended.

Best regards,
Security Team"""
            if st.button("📌 Load Example (Phishing)", use_container_width=True):
                st.session_state.example_email = example_phishing
                st.session_state.example_sender = "noreply@suspicious.com"
                st.session_state.example_subject = "URGENT: Your Account Will Be Suspended"
        
        with col2:
            st.markdown("**Legitimate Email:**")
            example_legitimate = """Subject: Meeting Reminder - Project Update

Hi Team,

This is a reminder about our scheduled meeting tomorrow at 2 PM to discuss the project update.

Please review the attached documents before the meeting.

See you there!

Best regards,
John Doe
Project Manager"""
            if st.button("📌 Load Example (Safe)", use_container_width=True):
                st.session_state.example_email = example_legitimate
                st.session_state.example_sender = "john.doe@company.com"
                st.session_state.example_subject = "Meeting Reminder - Project Update"
        
        # Load example if selected
        if 'example_email' in st.session_state:
            email_text = st.text_area("Email Text", value=st.session_state.example_email, height=200)
            sender = st.text_input("Sender", value=st.session_state.get('example_sender', ''))
            subject = st.text_input("Subject", value=st.session_state.get('example_subject', ''))
            del st.session_state.example_email
    
    else:
        # Batch Upload
        st.subheader("📁 Batch Email Upload")
        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
        
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                st.dataframe(df.head())
                
                if st.button("🔍 Scan Batch", type="primary"):
                    # Process batch
                    with st.spinner("Scanning batch..."):
                        results = []
                        for idx, row in df.iterrows():
                            email_text = str(row.get('text', row.get('body', '')))
                            sender = str(row.get('sender', ''))
                            recipient = str(row.get('recipient', ''))
                            subject = str(row.get('subject', ''))
                            
                            result = scan_email(email_text, sender, recipient, subject)
                            if result:
                                results.append(result)
                        
                        if results:
                            st.success(f"Scanned {len(results)} emails")
                            
                            # Display results
                            results_df = pd.DataFrame(results)
                            st.dataframe(results_df[['ai_prediction', 'zero_trust_decision', 'action', 'ai_confidence', 'trust_score']])
                            
                            # Download results
                            csv = results_df.to_csv(index=False)
                            st.download_button(
                                label="📥 Download Results",
                                data=csv,
                                file_name=f"scan_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime="text/csv"
                            )
            except Exception as e:
                st.error(f"Error processing file: {e}")


elif page == "Analytics":
    st.header("📊 Analytics")
    st.markdown("---")
    
    analytics = get_analytics()
    
    if analytics:
        # Metrics Overview
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total", analytics.get("total_emails", 0))
        with col2:
            st.metric("Safe", analytics.get("safe_emails", 0))
        with col3:
            st.metric("Suspicious", analytics.get("suspicious_emails", 0))
        with col4:
            st.metric("Phishing", analytics.get("phishing_emails", 0))
        with col5:
            st.metric("Blocked", analytics.get("blocked_emails", 0))
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribution Pie Chart
            fig = px.pie(
                values=[
                    analytics.get("safe_emails", 0),
                    analytics.get("suspicious_emails", 0),
                    analytics.get("phishing_emails", 0)
                ],
                names=["Safe", "Suspicious", "Phishing"],
                title="Email Classification Distribution",
                color_discrete_map={
                    "Safe": "#4caf50",
                    "Suspicious": "#ff9800",
                    "Phishing": "#f44336"
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Action Distribution
            fig = px.bar(
                x=["Allowed", "Quarantined", "Blocked"],
                y=[
                    analytics.get("safe_emails", 0),
                    analytics.get("quarantined_emails", 0),
                    analytics.get("blocked_emails", 0)
                ],
                title="Action Distribution",
                color_discrete_sequence=["#4caf50", "#ff9800", "#f44336"]
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Score Metrics
        st.markdown("### Score Metrics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Average AI Confidence", f"{analytics.get('avg_confidence', 0):.2%}")
        with col2:
            st.metric("Average Trust Score", f"{analytics.get('avg_trust_score', 0):.2%}")
    else:
        st.warning("Unable to load analytics.")


elif page == "Logs":
    st.header("📋 Email Logs")
    st.markdown("---")
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        limit = st.slider("Number of logs", 10, 500, 100)
    with col2:
        decision_filter = st.selectbox("Filter by decision", ["All", "Safe", "Suspicious", "Phishing"])
    
    decision = decision_filter if decision_filter != "All" else None
    
    # Get logs
    logs = get_logs(limit, decision)
    
    if logs:
        # Convert to DataFrame
        logs_df = pd.DataFrame(logs)
        
        # Display logs
        st.dataframe(
            logs_df[['timestamp', 'sender', 'subject', 'ai_prediction', 'zero_trust_decision', 'action', 'ai_confidence', 'trust_score']],
            use_container_width=True
        )
        
        # Download logs
        csv = logs_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Logs",
            data=csv,
            file_name=f"email_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No logs found.")


elif page == "Admin Panel":
    st.header("⚙️ Admin Panel")
    st.markdown("---")
    
    # Trusted Domains Management
    st.subheader("🛡️ Trusted Domains")
    
    trusted_domains = get_trusted_domains()
    
    if trusted_domains:
        st.write(f"**Current trusted domains ({len(trusted_domains)}):**")
        for domain in trusted_domains:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"• {domain}")
            with col2:
                if st.button("Remove", key=f"remove_{domain}"):
                    if remove_trusted_domain(domain):
                        st.success(f"Removed {domain}")
                        st.rerun()
                    else:
                        st.error(f"Failed to remove {domain}")
    else:
        st.info("No trusted domains configured.")
    
    st.markdown("---")
    
    # Add Trusted Domain
    st.subheader("➕ Add Trusted Domain")
    new_domain = st.text_input("Domain", placeholder="example.com")
    if st.button("Add Domain", type="primary"):
        if new_domain:
            if add_trusted_domain(new_domain):
                st.success(f"Added {new_domain} to trusted list")
                st.rerun()
            else:
                st.error(f"Failed to add {new_domain}")
        else:
            st.warning("Please enter a domain")


# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Zero-Trust AI Email Firewall | Powered by AI & Zero-Trust Principles</div>",
    unsafe_allow_html=True
)


