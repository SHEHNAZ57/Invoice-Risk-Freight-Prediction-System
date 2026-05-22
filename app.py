import streamlit as st
import numpy as np

from inference.predict_freight      import predict_freight_cost
from inference.predict_invoice_flag import predict_invoice_flag

# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Vendor Invoice Intelligence",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"], .stApp { font-family:'Inter',sans-serif !important; }
[data-testid="stAppViewContainer"],
[data-testid="stMain"]             { background-color:#F1F5F9 !important; }
[data-testid="stMain"]>div>div     { padding-top:1rem !important; }
[data-testid="stDecoration"]       { display:none !important; }
footer                             { visibility:hidden !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background-color:#0F172A !important;
    border-right:1px solid #1E293B !important;
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown li,
[data-testid="stSidebar"] label    { color:#94A3B8 !important; font-family:'Inter',sans-serif !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3       { color:#F1F5F9 !important; font-family:'Inter',sans-serif !important; }
[data-testid="stSidebar"] hr       { border-color:#1E293B !important; }

/* Sidebar nav buttons */
[data-testid="stSidebar"] .stButton > button {
    background:rgba(15,23,42,0.75) !important;
    color:#cbd5e1 !important;
    border:1px solid rgba(148,163,184,0.2) !important;
    border-radius:8px !important;
    font-size:0.82rem !important;
    font-weight:700 !important;
    padding:0.55rem 1rem !important;
    transition:all 0.18s ease !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background:rgba(255,255,255,0.06) !important;
    color:#ffffff !important;
    border-color:#5b7ef6 !important;
}

/* ── INPUTS ── */
.stNumberInput input {
    background:#FFFFFF !important; border:1.5px solid #E2E8F0 !important;
    border-radius:8px !important; color:#1E293B !important;
    font-family:'Space Mono',monospace !important; font-size:0.9rem !important;
}
.stNumberInput input:focus {
    border-color:#3B82F6 !important;
    box-shadow:0 0 0 3px #3B82F620 !important; outline:none !important;
}
.stNumberInput>div>div>button {
    background:#F8FAFC !important; border:1.5px solid #E2E8F0 !important;
    color:#64748B !important; border-radius:6px !important;
}
.stNumberInput>div>div>button:hover { border-color:#3B82F6 !important; color:#2563EB !important; }

label[data-testid="stWidgetLabel"]>div>p,
label[data-testid="stWidgetLabel"]>p {
    font-size:0.72rem !important; font-weight:600 !important;
    letter-spacing:0.06em !important; text-transform:uppercase !important;
    color:#64748B !important;
}

/* ── BUTTONS ── */
.stFormSubmitButton>button, .stButton>button {
    background:linear-gradient(135deg,#1E3A8A,#2563EB) !important;
    color:#FFFFFF !important; border:none !important; border-radius:8px !important;
    font-family:'Inter',sans-serif !important; font-weight:600 !important;
    font-size:0.85rem !important; padding:0.6rem 1.8rem !important;
    box-shadow:0 2px 8px #2563EB30 !important; transition:all 0.15s ease !important;
}
.stFormSubmitButton>button:hover, .stButton>button:hover {
    transform:translateY(-1px) !important; box-shadow:0 5px 16px #2563EB40 !important;
}

/* ── FORM / METRIC ── */
[data-testid="stForm"] {
    background:#FFFFFF !important; border:1.5px solid #E2E8F0 !important;
    border-radius:12px !important; padding:1.25rem 1.4rem !important;
    box-shadow:0 1px 6px rgba(0,0,0,0.05) !important;
}
[data-testid="metric-container"],
[data-testid="stMetric"] {
    background:#FFFFFF !important; border:1.5px solid #E2E8F0 !important;
    border-radius:10px !important; padding:1rem 1.25rem !important;
}

hr { border-color:#E2E8F0 !important; }
::-webkit-scrollbar { width:5px; }
::-webkit-scrollbar-track { background:#F1F5F9; }
::-webkit-scrollbar-thumb { background:#CBD5E1; border-radius:99px; }
::-webkit-scrollbar-thumb:hover { background:#3B82F6; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
st.sidebar.markdown(
    "<div style='padding:0.75rem 0 1.3rem;border-bottom:1px solid #1E293B;margin-bottom:0.3rem;'>"
    "<div style='display:flex;align-items:center;gap:12px;margin-bottom:10px;'>"
    "<div style='width:52px;height:52px;border-radius:14px;"
    "background:linear-gradient(135deg,#2563EB,#1E3A8A);"
    "display:flex;align-items:center;justify-content:center;"
    "font-size:26px;flex-shrink:0;'>📦</div>"
    "<div>"
    "<div style='font-size:17px;font-weight:700;color:#F1F5F9;letter-spacing:-0.35px;line-height:1.2;'>InvoiceIQ</div>"
    "<div style='font-size:10.5px;color:#94A3B8;letter-spacing:2px;text-transform:uppercase;margin-top:1px;'>Vendor Intelligence</div>"
    "</div>"
    "</div>"
    "</div>",
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    "<p style='font-size:9px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;"
    "color:#334155;margin:0.8rem 0 0.4rem 0;'>Navigation</p>",
    unsafe_allow_html=True,
)

if "page" not in st.session_state:
    st.session_state.page = "freight"

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("🚚 Freight", use_container_width=True, key="freight_btn"):
        st.session_state.page = "freight"
    if st.session_state.page == "freight":
        st.sidebar.markdown(
            "<div style='height:3px;background:linear-gradient(135deg,#2563EB,#1E40AF);"
            "border-radius:2px;margin-top:0.25rem;'></div>",
            unsafe_allow_html=True,
        )
with col2:
    if st.button("🔍 Invoice", use_container_width=True, key="invoice_btn"):
        st.session_state.page = "invoice"
    if st.session_state.page == "invoice":
        st.sidebar.markdown(
            "<div style='height:3px;background:linear-gradient(135deg,#2563EB,#1E40AF);"
            "border-radius:2px;margin-top:0.25rem;'></div>",
            unsafe_allow_html=True,
        )

st.sidebar.markdown(
    "<div style='border-top:1px solid #1E293B;margin:1rem 0 0.6rem;'></div>"
    "<p style='font-size:9px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;"
    "color:#334155;margin:0 0 0.5rem 2px;'>Model Registry</p>",
    unsafe_allow_html=True,
)
for _name, _algo, _metric, _icon in [
    ("Freight Model",      "Random Forest Regressor",  "MAE optimised",      "🚚"),
    ("Invoice Classifier", "Random Forest Classifier", "F1 · StandardScaler", "🔍"),
]:
    st.sidebar.markdown(
        f"<div style='background:#0F1F3D;border:1px solid #1E3A8A;"
        f"border-left:3px solid #3B82F6;border-radius:8px;padding:9px 11px;margin-bottom:6px;'>"
        f"<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;'>"
        f"<span style='font-size:12px;font-weight:600;color:#CBD5E1;'>{_icon} {_name}</span>"
        f"<span style='background:#052e16;color:#4ade80;border:1px solid #166534;"
        f"font-size:8px;font-weight:700;letter-spacing:0.8px;padding:1px 7px;border-radius:99px;'>LIVE</span>"
        f"</div>"
        f"<div style='font-size:10px;color:#475569;font-family:monospace;margin-bottom:2px;'>{_algo}</div>"
        f"<div style='font-size:10px;color:#3B82F6;font-family:monospace;'>{_metric}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

st.sidebar.markdown(
    "<div style='border-top:1px solid #1E293B;margin:0.9rem 0 0.6rem;'></div>"
    "<p style='font-size:9px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;"
    "color:#334155;margin:0 0 0.45rem 2px;'>Business Impact</p>",
    unsafe_allow_html=True,
)
for _ico, _txt in [
    ("📉", "Improved cost forecasting"),
    ("🧾", "Reduced invoice anomalies"),
    ("⚙️",  "Faster finance operations"),
]:
    st.sidebar.markdown(
        f"<div style='display:flex;align-items:center;gap:8px;padding:4px 6px;margin-bottom:2px;'>"
        f"<span style='font-size:13px;'>{_ico}</span>"
        f"<span style='font-size:12px;color:#64748B;'>{_txt}</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

st.sidebar.markdown(
    "<div style='border-top:1px solid #1E293B;margin:1.2rem 0 0;padding-top:0.7rem;'>"
    "<p style='font-size:9.5px;color:#334155;text-align:center;margin:0;font-family:monospace;'>"
    "Finance Ops · v3.2.0 · 2025</p></div>",
    unsafe_allow_html=True,
)


# ══════════════════════════════════════════════════════════════════════════════
#  HERO HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="background:linear-gradient(135deg,#1E3A8A 0%,#1D4ED8 60%,#2563EB 100%);
             border-radius:14px;padding:1.9rem 2.2rem;margin-bottom:1.6rem;
             position:relative;overflow:hidden;text-align:center;">
  <div style="position:absolute;top:-55px;right:-30px;width:200px;height:200px;
               border-radius:50%;background:rgba(255,255,255,0.05);pointer-events:none;"></div>
  <div style="position:absolute;bottom:-60px;right:140px;width:160px;height:160px;
               border-radius:50%;background:rgba(255,255,255,0.04);pointer-events:none;"></div>
  <div style="position:relative;z-index:1;">
    <p style="margin:0 0 0.35rem;font-family:'Inter',sans-serif;font-size:0.65rem;
               font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:#93C5FD;">
      Finance Operations · AI Suite</p>
    <h1 style="font-family:'Inter',sans-serif;font-size:1.85rem;font-weight:700;
                color:#FFFFFF;margin:0 0 0.45rem;letter-spacing:-0.02em;">
      Vendor Invoice Intelligence Portal</h1>
    <p style="margin:0 auto;font-size:0.86rem;color:#BFDBFE;max-width:520px;line-height:1.6;">
      ML-powered freight cost forecasting and invoice risk classification —
      purpose-built for Finance Operations.
    </p>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def page_title(icon: str, title: str, subtitle: str) -> None:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.2rem;">
      <div style="width:34px;height:34px;border-radius:9px;
                   background:linear-gradient(135deg,#EFF6FF,#DBEAFE);
                   border:1.5px solid #BFDBFE;display:flex;align-items:center;
                   justify-content:center;font-size:1.05rem;">{icon}</div>
      <h2 style="font-family:'Inter',sans-serif;font-size:1.2rem;font-weight:700;
                  color:#1E293B;margin:0;">{title}</h2>
    </div>
    <p style="font-family:'Inter',sans-serif;font-size:0.81rem;color:#64748B;
               margin:0 0 1.25rem 2.65rem;line-height:1.55;">{subtitle}</p>
    """, unsafe_allow_html=True)


def result_row(label: str, value: str, color: str = "#1E293B") -> str:
    return (
        f'<div style="display:flex;justify-content:space-between;align-items:center;'
        f'padding:0.42rem 0;border-bottom:1px solid #F1F5F9;">'
        f'<span style="font-family:\'Inter\',sans-serif;font-size:0.77rem;color:#64748B;">{label}</span>'
        f'<span style="font-family:\'Space Mono\',monospace;font-size:0.8rem;'
        f'font-weight:700;color:{color};">{value}</span></div>'
    )


def empty_state(icon: str, msg: str, height: int = 300) -> None:
    st.markdown(f"""
    <div style="height:{height}px;background:#FFFFFF;border:2px dashed #E2E8F0;
                 border-radius:12px;display:flex;flex-direction:column;
                 align-items:center;justify-content:center;gap:0.7rem;">
      <span style="font-size:2.2rem;">{icon}</span>
      <p style="font-family:'Inter',sans-serif;font-size:0.85rem;color:#94A3B8;margin:0;">{msg}</p>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  FREIGHT COST PREDICTION
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "freight":

    page_title("🚚", "Freight Cost Prediction",
               "Predict carrier freight cost from invoice value — supports budgeting & vendor negotiations.")

    _lc, _rc = st.columns([1, 1], gap="large")

    with _lc:
        st.markdown(
            '<p style="font-family:\'Inter\',sans-serif;font-size:0.63rem;font-weight:700;'
            'letter-spacing:0.1em;text-transform:uppercase;color:#94A3B8;margin:0 0 0.4rem;">'
            'Invoice Parameters</p>',
            unsafe_allow_html=True,
        )
        with st.form("freight_form"):
            dollars = st.number_input(
                "Invoice Dollars (USD)",
                min_value=1.0, max_value=10_000_000.0,
                value=18_500.0, step=500.0, format="%.2f",
            )
            submit_freight = st.form_submit_button(
                "🔮  Predict Freight Cost", use_container_width=True,
            )

    with _rc:
        if submit_freight:
            with st.spinner("Running model…"):
                result = predict_freight_cost({"Dollars": [dollars]})
                pred   = float(result["Predicted_Freight"].iloc[0])

            rate     = pred / dollars * 100
            rate_clr = "#DC2626" if rate > 10 else "#D97706" if rate > 7 else "#059669"

            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#EFF6FF,#F0FDF4);
                         border:1.5px solid #BFDBFE;border-radius:12px;
                         padding:1.5rem;margin-bottom:0.85rem;
                         box-shadow:0 4px 18px rgba(59,130,246,0.09);">
              <p style="margin:0 0 0.28rem;font-family:'Inter',sans-serif;
                         font-size:0.62rem;font-weight:600;letter-spacing:0.1em;
                         text-transform:uppercase;color:#3B82F6;">Predicted Freight Cost</p>
              <p style="margin:0;font-family:'Space Mono',monospace;font-size:2.5rem;
                         font-weight:700;color:#1E3A8A;line-height:1.1;">${pred:,.2f}</p>
              <p style="margin:0.22rem 0 1rem;font-family:'Inter',sans-serif;
                         font-size:0.73rem;color:#64748B;">
                Model output for invoice value of ${dollars:,.2f}</p>
              {result_row("Invoice Value", f"${dollars:,.2f}")}
              {result_row("Freight Rate",  f"{rate:.2f}%", rate_clr)}
            </div>""", unsafe_allow_html=True)

            pct = min(rate / 15 * 100, 100)
            st.markdown(f"""
            <div style="background:#FFFFFF;border:1.5px solid #E2E8F0;border-radius:10px;
                         padding:0.95rem 1.15rem;box-shadow:0 1px 4px rgba(0,0,0,.04);">
              <div style="display:flex;justify-content:space-between;margin-bottom:0.45rem;">
                <span style="font-family:'Inter',sans-serif;font-size:0.7rem;
                              font-weight:600;color:#64748B;">Freight Rate Indicator</span>
                <span style="font-family:'Space Mono',monospace;font-size:0.76rem;
                              font-weight:700;color:{rate_clr};">{rate:.2f}%</span>
              </div>
              <div style="background:#F1F5F9;border-radius:99px;height:8px;">
                <div style="width:{pct:.1f}%;height:8px;border-radius:99px;
                             background:linear-gradient(90deg,#22C55E,{rate_clr});"></div>
              </div>
              <div style="display:flex;justify-content:space-between;margin-top:0.3rem;">
                <span style="font-size:0.6rem;color:#94A3B8;">0% — Normal</span>
                <span style="font-size:0.6rem;color:#94A3B8;">15%+ — High</span>
              </div>
            </div>""", unsafe_allow_html=True)
        else:
            empty_state("🚚", "Enter an invoice value and click Predict")


# ══════════════════════════════════════════════════════════════════════════════
#  INVOICE RISK DETECTION
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "invoice":

    page_title("🔍", "Invoice Risk Detection",
               "Classify vendor invoices as auto-approvable or requiring manual review before payment.")

    _lc2, _rc2 = st.columns([1, 1], gap="large")

    with _lc2:
        st.markdown(
            '<p style="font-family:\'Inter\',sans-serif;font-size:0.63rem;font-weight:700;'
            'letter-spacing:0.1em;text-transform:uppercase;color:#94A3B8;margin:0 0 0.4rem;">'
            'Invoice Parameters</p>',
            unsafe_allow_html=True,
        )
        with st.form("invoice_flag_form"):
            c1, c2 = st.columns(2)
            with c1:
                invoice_quantity = st.number_input("Invoice Quantity",    min_value=1,   value=50)
                invoice_dollars  = st.number_input("Invoice Dollars ($)", min_value=1.0, value=352.95)
            with c2:
                freight             = st.number_input("Freight Cost ($)",    min_value=0.0, value=1.73)
                total_item_quantity = st.number_input("Total Item Qty",      min_value=1,   value=162)

            total_item_dollars = st.number_input(
                "Total Item Dollars ($)", min_value=1.0, value=2476.0,
            )

            _fr = freight / invoice_dollars          if invoice_dollars > 0        else 0
            _qr = invoice_quantity / total_item_quantity if total_item_quantity > 0 else 0
            _dd = abs(invoice_dollars - total_item_dollars)

            for _cond, _msg in [
                (_dd > 5,                  f"Dollar delta ${_dd:,.2f} triggers the risk label (rule: |invoice − total| > 5)"),
                (_fr > 0.15,               f"Freight ratio {_fr:.1%} — unusually high"),
                (_qr > 0.80,               "Invoice qty > 80% of total item qty"),
                (invoice_dollars > 50_000, "High-value invoice — review advised"),
            ]:
                if _cond:
                    st.markdown(
                        f'<div style="background:#FFFBEB;border:1px solid #FDE68A;'
                        f'border-radius:7px;padding:0.4rem 0.75rem;margin:0.2rem 0;'
                        f'display:flex;align-items:center;gap:0.45rem;">'
                        f'<span style="font-size:0.8rem;">⚠️</span>'
                        f'<span style="font-family:\'Inter\',sans-serif;font-size:0.74rem;'
                        f'color:#92400E;">{_msg}</span></div>',
                        unsafe_allow_html=True,
                    )

            submit_flag = st.form_submit_button(
                "🧠  Evaluate Invoice Risk", use_container_width=True,
            )

    with _rc2:
        if submit_flag:
            with st.spinner("Running classifier…"):
                flag_result = predict_invoice_flag({
                    "invoice_quantity":    [invoice_quantity],
                    "invoice_dollars":     [invoice_dollars],
                    "Freight":             [freight],
                    "total_item_quantity": [total_item_quantity],
                    "total_item_dollars":  [total_item_dollars],
                })
                # ── CHANGE 1: also read Predicted_Probability ────────────── #
                is_flagged = bool(flag_result["Predicted_Flag"].iloc[0])
                risk_prob  = float(flag_result["Predicted_Probability"].iloc[0])

            if is_flagged:
                _bg, _brd, _acc = "linear-gradient(135deg,#FEF2F2,#FFF7ED)", "#FCA5A5", "#DC2626"
                _bbd, _bbc       = "#FEE2E2", "#DC2626"
                _ico, _verdict   = "🚨", "MANUAL APPROVAL REQUIRED"
                _sub             = "This invoice was flagged by the classifier. Review before processing payment."
                _badge           = "HIGH RISK"
            else:
                _bg, _brd, _acc = "linear-gradient(135deg,#F0FDF4,#ECFDF5)", "#86EFAC", "#16A34A"
                _bbd, _bbc       = "#DCFCE7", "#16A34A"
                _ico, _verdict   = "✅", "SAFE · AUTO-APPROVED"
                _sub             = "This invoice passed all classifier checks and can be auto-processed."
                _badge           = "LOW RISK"

            # Verdict card
            st.markdown(f"""
            <div style="background:{_bg};border:1.5px solid {_brd};border-radius:12px;
                         padding:1.5rem;margin-bottom:0.85rem;
                         box-shadow:0 4px 18px {_acc}12;">
              <div style="display:flex;align-items:center;gap:0.55rem;margin-bottom:0.75rem;">
                <span style="font-size:1.5rem;">{_ico}</span>
                <div>
                  <span style="background:{_bbd};color:{_bbc};border:1px solid {_brd};
                                font-size:0.6rem;font-weight:700;letter-spacing:0.08em;
                                padding:0.14rem 0.55rem;border-radius:99px;
                                font-family:'Inter',sans-serif;">{_badge}</span>
                  <p style="margin:0.18rem 0 0;font-family:'Inter',sans-serif;
                             font-size:0.9rem;font-weight:700;color:{_acc};">{_verdict}</p>
                </div>
              </div>
              <p style="margin:0 0 0.9rem;font-family:'Inter',sans-serif;
                         font-size:0.77rem;color:#475569;line-height:1.5;">{_sub}</p>
              {result_row("Invoice Dollars",    f"${invoice_dollars:,.2f}"   )}
              {result_row("Total Item Dollars", f"${total_item_dollars:,.2f}")}
              {result_row("Dollar Delta",       f"${_dd:,.2f}",
                          "#DC2626" if _dd > 5 else "#475569")}
              {result_row("Freight Cost",       f"${freight:,.2f}"           )}
              {result_row("Invoice Quantity",   str(invoice_quantity)        )}
              {result_row("Total Item Qty",     str(total_item_quantity)     )}
            </div>""", unsafe_allow_html=True)

            # ── CHANGE 2: Risk probability bar (real model output) ────────── #
            pct       = int(risk_prob * 100)
            bar_color = "#DC2626" if pct > 65 else "#D97706" if pct > 35 else "#16A34A"
            st.markdown(f"""
            <div style="background:#FFFFFF;border:1.5px solid #E2E8F0;border-radius:10px;
                         padding:0.95rem 1.15rem;box-shadow:0 1px 4px rgba(0,0,0,.04);">
              <div style="display:flex;justify-content:space-between;margin-bottom:0.45rem;">
                <span style="font-family:'Inter',sans-serif;font-size:0.7rem;
                              font-weight:600;color:#64748B;">
                  Model Risk Probability</span>
                <span style="font-family:'Space Mono',monospace;font-size:0.76rem;
                              font-weight:700;color:{bar_color};">{pct}%</span>
              </div>
              <div style="background:#F1F5F9;border-radius:99px;height:8px;">
                <div style="width:{pct}%;height:8px;border-radius:99px;
                             background:{bar_color};"></div>
              </div>
              <div style="display:flex;justify-content:space-between;margin-top:0.3rem;">
                <span style="font-size:0.6rem;color:#94A3B8;">0% — Safe</span>
                <span style="font-size:0.6rem;color:#94A3B8;">100% — High Risk</span>
              </div>
            </div>""", unsafe_allow_html=True)

        else:
            empty_state("🔍", "Fill in the parameters and click Evaluate")