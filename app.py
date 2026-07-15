import streamlit as st
import pandas as pd
import pyodbc
from datetime import datetime
import math

# ── PAGE CONFIG ───────────────────────────────────────────────
st.set_page_config(
    page_title="DSPMS - Uda Radella Estate",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Login page */
    .login-box {
        max-width: 420px; margin: 60px auto; padding: 40px;
        background: white; border-radius: 16px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.10);
        border-top: 6px solid #2d8a45;
    }
    .login-title {
        text-align: center; color: #1a5c2a;
        font-size: 1.8rem; font-weight: 700; margin-bottom: 4px;
    }
    .login-sub {
        text-align: center; color: #888;
        font-size: 0.9rem; margin-bottom: 28px;
    }
    /* Sidebar */
    .sidebar-logo {
        font-size: 1.8rem; font-weight: 800;
        color: #2d8a45; letter-spacing: 1px;
    }
    .sidebar-sub { font-size: 0.9rem; color: #555; margin-top: -6px; }
    .sidebar-estate { font-size: 0.8rem; color: #999; margin-bottom: 8px; }
    .user-badge {
        background: #e8f5e9; border-radius: 8px;
        padding: 8px 12px; margin-bottom: 8px;
        font-size: 0.85rem; color: #1a5c2a;
    }
    /* Main header */
    .main-header {
        background: linear-gradient(90deg, #1a5c2a 0%, #2d8a45 100%);
        padding: 18px 28px; border-radius: 10px;
        margin-bottom: 20px; color: white;
    }
    .section-title {
        font-size: 1.1rem; font-weight: 600; color: #1a5c2a;
        margin: 18px 0 10px 0; border-bottom: 2px solid #2d8a45;
        padding-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ── DATABASE CONNECTION ───────────────────────────────────────
def get_connection():
       conn = pyodbc.connect(
           "DRIVER={ODBC Driver 18 for SQL Server};"
           "SERVER=LAPTOP-LVP16JKA\\SQLEXPRESS;"
           "DATABASE=dspms_uda_radella;"
           "Trusted_Connection=yes;"
           "Encrypt=no;"
       )
       return conn

def run_query(query, params=None):
    try:
        conn = get_connection()
        if params:
            df = pd.read_sql(query, conn, params=params)
        else:
            df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()

def run_command(query, params=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Database error: {e}")
        return False

# ── SESSION STATE ─────────────────────────────────────────────
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None

# ── LOGIN FUNCTION ────────────────────────────────────────────
def login(username, password):
    df = run_query(
        "SELECT user_id, username, full_name, role, division "
        "FROM users WHERE username=? AND password_hash=? AND is_active=1",
        (username, password)
    )
    if len(df) > 0:
        st.session_state.logged_in = True
        st.session_state.user = df.iloc[0].to_dict()
        # Update last login
        run_command(
            "UPDATE users SET last_login=GETDATE() WHERE username=?",
            (username,)
        )
        return True
    return False

# ══════════════════════════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    st.markdown("""
    <div class="login-box">
        <div class="login-title">🍃 DSPMS</div>
        <div class="login-sub">Uda Radella Estate<br>Kelani Valley Plantations PLC</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("### Login")
        username = st.text_input("👤 Username", placeholder="Enter username")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter password")
        
        if st.button("Login →", use_container_width=True, type="primary"):
            if username and password:
                if login(username, password):
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
            else:
                st.warning("Please enter username and password")

        st.markdown("---")
        st.caption("© 2025 Uda Radella Estate | DSPMS v1.0")

# ══════════════════════════════════════════════════════════════
# MAIN APP (after login)
# ══════════════════════════════════════════════════════════════
else:
    user = st.session_state.user
    role = user['role']
    division = user['division']

    # ── SIDEBAR ──────────────────────────────────────────────
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">🍃 DSPMS</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-sub">Uda Radella Estate</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-estate">Kelani Valley Plantations PLC</div>',
                    unsafe_allow_html=True)
        st.divider()

        # User info badge
        role_icon = {"admin":"👑","manager":"📊","field_officer":"🌿"}.get(role,"👤")
        div_text = f" | {division}" if division else ""
        st.markdown(
            f'<div class="user-badge">{role_icon} <b>{user["full_name"]}</b><br>'
            f'<small>{role.replace("_"," ").title()}{div_text}</small></div>',
            unsafe_allow_html=True
        )

        # Navigation based on role
        if role in ('admin', 'manager'):
            pages = [
                "🏠 Executive Summary",
                "🌿 Field Performance",
                "⚗️ Nitrogen & Inputs",
                "👷 Labour & Plucking",
                "📊 Made Tea Outturn",
                "📋 Daily Plucking Entry",
                "🌱 Nitrogen Entry",
                "🔧 Activity Entry",
                "⚙️ Admin Panel"
            ]
        else:
            # Field officers only see data entry
            pages = [
                "📋 Daily Plucking Entry",
                "🌱 Nitrogen Entry",
                "🔧 Activity Entry",
            ]

        page = st.radio("Navigation", pages)
        st.divider()

        # Division filter (admin/manager only)
        if role in ('admin', 'manager'):
            div_filter = st.selectbox(
                "Division", ["All Divisions", "Lower (ULD)", "Upper (UUD)"]
            )
        else:
            div_filter = division  # field officers locked to their division

        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()

    # ── HELPER ───────────────────────────────────────────────
    def get_fields(div=None):
        if div and div != "All Divisions":
            div_name = "Lower" if "Lower" in div else "Upper"
            return run_query(
                "SELECT field_id, field_name, type, extent_ha "
                "FROM fields WHERE division=? AND is_active=1 ORDER BY type, field_id",
                (div_name,)
            )
        return run_query(
            "SELECT field_id, field_name, division, type, extent_ha "
            "FROM fields WHERE is_active=1 ORDER BY division, type, field_id"
        )

    # ══ PAGE: EXECUTIVE SUMMARY ══════════════════════════════
    if page == "🏠 Executive Summary":
        st.markdown("""
        <div class="main-header">
            <h2 style="margin:0">🍃 DSPMS — Uda Radella Estate</h2>
            <p style="margin:4px 0 0 0;opacity:0.85">
            Kelani Valley Plantations PLC | Executive Summary</p>
        </div>""", unsafe_allow_html=True)

        # Estate info
        df_est = run_query("SELECT * FROM estate_extent_summary")
        df_div = run_query(
            "SELECT * FROM division_extent_summary ORDER BY division_name"
        )

        if len(df_est) > 0:
            e = df_est.iloc[0]
            st.markdown('<p class="section-title">🏡 Estate Overview</p>',
                        unsafe_allow_html=True)
            c1,c2,c3,c4,c5 = st.columns(5)
            c1.metric("Estate", e['estate_name'])
            c2.metric("Total Extent", f"{e['estate_total_ha']} ha")
            c3.metric("VP Extent", f"{e['estate_vp_ha']} ha ({e['estate_vp_pct']}%)")
            c4.metric("SD Extent", f"{e['estate_sd_ha']} ha ({e['estate_sd_pct']}%)")
            c5.metric("Total Fields", e['total_fields'])

        if len(df_div) > 0:
            st.markdown('<p class="section-title">🏭 Division Summary</p>',
                        unsafe_allow_html=True)
            st.dataframe(df_div, use_container_width=True, hide_index=True)

        st.markdown('<p class="section-title">🌿 Field Register</p>',
                    unsafe_allow_html=True)
        df_fields = run_query(
            "SELECT field_id, field_name, division, type, extent_ha, "
            "pct_division, pct_estate, age_months "
            "FROM fields_with_pct ORDER BY division, type, field_id"
        )
        st.dataframe(df_fields, use_container_width=True, hide_index=True)

    # ══ PAGE: DAILY PLUCKING ENTRY ═══════════════════════════
    elif page == "📋 Daily Plucking Entry":
        st.markdown("""
        <div class="main-header">
            <h2 style="margin:0">📋 Daily Plucking Entry</h2>
            <p style="margin:4px 0 0 0;opacity:0.85">Enter daily green leaf and labour details</p>
        </div>""", unsafe_allow_html=True)

        df_fields = get_fields(division if role == 'field_officer' else div_filter)

        if len(df_fields) == 0:
            st.warning("No fields found.")
        else:
            field_options = {
                f"{r['field_name']} ({r['type']}) - {r['extent_ha']}ha": r['field_id']
                for _, r in df_fields.iterrows()
            }

            with st.form("plucking_form", clear_on_submit=True):
                st.markdown('<p class="section-title">Field & Date</p>',
                            unsafe_allow_html=True)
                c1, c2, c3 = st.columns(3)
                selected_field = c1.selectbox("Select Field", list(field_options.keys()))
                harvest_date   = c2.date_input("Date", value=datetime.today())
                plucking_type  = c3.selectbox(
                    "Plucking Type", ["Checkroll", "Shear", "Cash"]
                )
                round_number = c1.number_input("Round Number", min_value=1, max_value=6, value=1)

                st.markdown('<p class="section-title">Registered Workers</p>',
                            unsafe_allow_html=True)
                c1, c2, c3 = st.columns(3)
                reg_pluckers  = c1.number_input("Registered Pluckers", min_value=0, value=0)
                kangany_count = c2.number_input("Kanganies", min_value=0, value=0)
                reg_gl        = c3.number_input("Registered GL (kg)", min_value=0.0,
                                                 value=0.0, format="%.2f")

                st.markdown('<p class="section-title">Cash Workers</p>',
                            unsafe_allow_html=True)
                c1, c2, c3, c4 = st.columns(4)
                cash_pluckers = c1.number_input("Cash Pluckers", min_value=0, value=0)
                sack_labour   = c2.number_input("Sack Labourers", min_value=0, value=0)
                cash_gl       = c3.number_input("Cash GL (kg)", min_value=0.0,
                                                 value=0.0, format="%.2f")
                cash_rate     = c4.selectbox("Cash Rate (Rs.)", [150.00, 75.00])

                notes = st.text_area("Notes (optional)", height=60)

                # Show calculations preview
                total_gl = reg_gl + cash_gl
                cash_mandays = math.ceil((cash_gl * cash_rate) / 1550) if cash_gl > 0 else 0
                total_pluckers = reg_pluckers + cash_pluckers
                plk_avg = round(total_gl / total_pluckers, 2) if total_pluckers > 0 else 0
                kg_sack = round(total_gl / sack_labour, 2) if sack_labour > 0 else 0
                kg_kang = round(total_gl / kangany_count, 2) if kangany_count > 0 else 0

                st.markdown('<p class="section-title">Auto Calculated</p>',
                            unsafe_allow_html=True)
                cc1,cc2,cc3,cc4,cc5 = st.columns(5)
                cc1.metric("Total GL (kg)",    f"{total_gl:,.1f}")
                cc2.metric("Cash Mandays",     f"{cash_mandays}")
                cc3.metric("Plucking Avg",     f"{plk_avg} kg")
                cc4.metric("Kg/Sack Labour",   f"{kg_sack}")
                cc5.metric("Kg/Kangany",       f"{kg_kang}")

                submitted = st.form_submit_button(
                    "✅ Save Entry", use_container_width=True, type="primary"
                )

                if submitted:
                    field_id = field_options[selected_field]
                    total_mandays = reg_pluckers + cash_mandays + kangany_count + sack_labour
                    success = run_command("""
                        INSERT INTO harvest_log (
                            harvest_date, field_id, plucking_type, round_number,
                            reg_plucker_count, kangany_count, reg_green_leaf_kg,
                            cash_plucker_count, sack_labour_count,
                            cash_green_leaf_kg, cash_rate,
                            total_green_leaf_kg, cash_mandays, total_mandays,
                            plucking_average, kg_per_sack, kg_per_kangany,
                            entered_by, notes
                        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """, (
                        harvest_date, field_id, plucking_type, round_number,
                        reg_pluckers, kangany_count, reg_gl,
                        cash_pluckers, sack_labour, cash_gl, cash_rate,
                        total_gl, cash_mandays, total_mandays,
                        plk_avg, kg_sack, kg_kang,
                        user['user_id'], notes
                    ))
                    if success:
                        st.success(f"✅ Entry saved! Field: {selected_field} | "
                                   f"Date: {harvest_date} | GL: {total_gl} kg")

        # Recent entries
        st.markdown('<p class="section-title">Recent Entries</p>', unsafe_allow_html=True)
        df_recent = run_query("""
            SELECT TOP 10
                h.harvest_date, f.field_name, f.division, h.plucking_type,
                h.round_number, h.total_green_leaf_kg AS total_gl,
                h.reg_plucker_count AS reg_pluckers,
                h.cash_plucker_count AS cash_pluckers,
                h.plucking_average AS plk_avg,
                h.total_mandays, u.full_name AS entered_by
            FROM harvest_log h
            JOIN fields f ON h.field_id = f.field_id
            LEFT JOIN users u ON h.entered_by = u.user_id
            ORDER BY h.created_at DESC
        """)
        if len(df_recent) > 0:
            st.dataframe(df_recent, use_container_width=True, hide_index=True)
        else:
            st.info("No entries yet.")

# ══ PAGE: NITROGEN ENTRY ══════════════════════════════════
    elif page == "🌱 Nitrogen Entry":
        st.markdown("""
        <div class="main-header">
            <h2 style="margin:0">🌱 Nitrogen Application Entry</h2>
            <p style="margin:4px 0 0 0;opacity:0.85">Record fertilizer applications per field</p>
        </div>""", unsafe_allow_html=True)

        df_fields = get_fields(division if role == 'field_officer' else div_filter)

        if len(df_fields) > 0:
            field_options = {
                f"{r['field_name']} ({r['type']})": r['field_id']
                for _, r in df_fields.iterrows()
            }

            # ── OUTSIDE the form — reruns immediately on change ──
            selected_field = st.selectbox("Select Field", list(field_options.keys()))

            field_id   = field_options[selected_field]
            field_type = df_fields[df_fields['field_id'] == field_id]['type'].values
            ftype      = field_type[0] if len(field_type) > 0 else 'VP'

            if ftype == 'VP':
                fert_options = ['U901', 'U877']
            else:
                fert_options = ['U709', 'U877']

            st.caption(f"Field type detected: **{ftype}**")

            # ── Form now only holds the remaining inputs ──
            with st.form("nitrogen_form", clear_on_submit=True):
                c1, c2 = st.columns(2)
                application_date = c1.date_input("Application Date", value=datetime.today())
                fertilizer_type  = c2.selectbox("Fertilizer Type", fert_options)

                c1, c2 = st.columns(2)
                nitrogen_qty = c1.selectbox("Nitrogen Qty (kg)", [60, 80])
                custom_n     = c2.number_input("Or Custom N Qty", min_value=0,
                                                max_value=200, value=0)

                final_n = custom_n if custom_n > 0 else nitrogen_qty
                st.info(f"📌 Nitrogen to be recorded: **{final_n} kg** | "
                        f"Fertilizer: **{fertilizer_type}** | Field type: **{ftype}**")

                notes = st.text_area("Notes (optional)", height=60)

                submitted = st.form_submit_button(
                    "✅ Save Nitrogen Entry", use_container_width=True, type="primary"
                )
                if submitted:
                    success = run_command("""
                        INSERT INTO nitrogen_log (
                            application_date, field_id, fertilizer_type,
                            nitrogen_qty_kg, application_month,
                            application_year, entered_by, notes
                        ) VALUES (?,?,?,?,?,?,?,?)
                    """, (
                        application_date, field_id, fertilizer_type,
                        final_n,
                        application_date.month,
                        application_date.year,
                        user['user_id'], notes
                    ))
                    if success:
                        st.success(f"✅ Nitrogen entry saved! "
                                   f"Field: {selected_field} | N: {final_n} kg")

        # Recent nitrogen entries
        st.markdown('<p class="section-title">Recent Nitrogen Applications</p>',
                    unsafe_allow_html=True)
        df_n = run_query("""
            SELECT TOP 10
                n.application_date, f.field_name, f.division, f.type,
                n.fertilizer_type, n.nitrogen_qty_kg,
                u.full_name AS entered_by
            FROM nitrogen_log n
            JOIN fields f ON n.field_id = f.field_id
            LEFT JOIN users u ON n.entered_by = u.user_id
            ORDER BY n.created_at DESC
        """)
        if len(df_n) > 0:
            st.dataframe(df_n, use_container_width=True, hide_index=True)
        else:
            st.info("No nitrogen entries yet.")

    # ══ PAGE: ACTIVITY ENTRY ══════════════════════════════════
    elif page == "🔧 Activity Entry":
        st.markdown("""
        <div class="main-header">
            <h2 style="margin:0">🔧 Field Activity Entry</h2>
            <p style="margin:4px 0 0 0;opacity:0.85">Record field upkeep activities</p>
        </div>""", unsafe_allow_html=True)

        ACTIVITIES = [
            "Foliar Application", "Blister Blight", "Chemical Weeding",
            "Manual Weeding", "Pruning", "Ravines & Boundaries", "Roads",
            "Dolomite Application", "Bush Sanitation", "Lungs Pruning",
            "Forking", "Hydrated Lime", "Draining", "Soil Conservation",
            "Shade Lopping", "Shade Planting", "Composting"
        ]

        df_fields = get_fields(division if role == 'field_officer' else div_filter)

        if len(df_fields) > 0:
            field_options = {
                f"{r['field_name']} ({r['type']})": r['field_id']
                for _, r in df_fields.iterrows()
            }

            with st.form("activity_form", clear_on_submit=True):
                c1, c2, c3 = st.columns(3)
                selected_field  = c1.selectbox("Select Field", list(field_options.keys()))
                activity_date   = c2.date_input("Date", value=datetime.today())
                activity_type   = c3.selectbox("Activity Type", ACTIVITIES)

                # Show relevant inputs based on activity
                c1, c2, c3, c4 = st.columns(4)
                qty_kg      = c1.number_input("Quantity (kg)", min_value=0.0,
                                               value=0.0, format="%.2f")
                qty_litre   = c2.number_input("Quantity (litres)", min_value=0.0,
                                               value=0.0, format="%.2f")
                mandays     = c3.number_input("Mandays", min_value=0.0,
                                               value=0.0, format="%.1f")
                no_plants   = c4.number_input("No. of Plants", min_value=0, value=0)

                c1, c2 = st.columns(2)
                chemical_name = c1.text_input("Chemical Name (if applicable)")
                chemical_qty  = c2.number_input("Chemical Qty", min_value=0.0,
                                                 value=0.0, format="%.2f")

                notes = st.text_area("Notes", height=60)

                submitted = st.form_submit_button(
                    "✅ Save Activity", use_container_width=True, type="primary"
                )
                if submitted:
                    fid = field_options[selected_field]
                    success = run_command("""
                        INSERT INTO activity_log (
                            activity_date, field_id, activity_type,
                            quantity_kg, quantity_litre, mandays,
                            no_of_plants, chemical_name, chemical_qty,
                            entered_by, notes
                        ) VALUES (?,?,?,?,?,?,?,?,?,?,?)
                    """, (
                        activity_date, fid, activity_type,
                        qty_kg or None, qty_litre or None,
                        mandays or None, no_plants or None,
                        chemical_name or None, chemical_qty or None,
                        user['user_id'], notes
                    ))
                    if success:
                        st.success(f"✅ Activity saved! {activity_type} | {selected_field}")

        # Recent activities
        st.markdown('<p class="section-title">Recent Activities</p>',
                    unsafe_allow_html=True)
        df_act = run_query("""
            SELECT TOP 10
                a.activity_date, f.field_name, f.division,
                a.activity_type, a.quantity_kg, a.quantity_litre,
                a.mandays, a.chemical_name, u.full_name AS entered_by
            FROM activity_log a
            JOIN fields f ON a.field_id = f.field_id
            LEFT JOIN users u ON a.entered_by = u.user_id
            ORDER BY a.created_at DESC
        """)
        if len(df_act) > 0:
            st.dataframe(df_act, use_container_width=True, hide_index=True)
        else:
            st.info("No activities recorded yet.")

    # ══ PAGE: ADMIN PANEL ════════════════════════════════════
    elif page == "⚙️ Admin Panel":
        if role != 'admin':
            st.error("❌ Access denied. Admin only.")
        else:
            st.markdown("""
            <div class="main-header">
                <h2 style="margin:0">⚙️ Admin Panel</h2>
            </div>""", unsafe_allow_html=True)

            tab1, tab2, tab3 = st.tabs(["👥 Users", "🌿 Fields", "📊 Outturn"])

            with tab1:
                st.markdown('<p class="section-title">System Users</p>',
                            unsafe_allow_html=True)
                df_users = run_query(
                    "SELECT user_id, username, full_name, role, "
                    "division, contact_no, is_active, last_login FROM users"
                )
                st.dataframe(df_users, use_container_width=True, hide_index=True)

                st.markdown("**Add New User:**")
                with st.form("add_user"):
                    c1,c2 = st.columns(2)
                    new_user = c1.text_input("Username")
                    new_pass = c2.text_input("Password", type="password")
                    c1,c2,c3 = st.columns(3)
                    new_name = c1.text_input("Full Name")
                    new_role = c2.selectbox("Role",
                                ["field_officer","manager","admin"])
                    new_div  = c3.selectbox("Division",
                                ["","Lower","Upper"])
                    new_contact = st.text_input("Contact No.")
                    if st.form_submit_button("Add User", type="primary"):
                        run_command("""
                            INSERT INTO users
                            (username,password_hash,full_name,role,division,contact_no)
                            VALUES (?,?,?,?,?,?)
                        """, (new_user, new_pass, new_name, new_role,
                              new_div or None, new_contact or None))
                        st.success(f"User {new_user} added!")
                        st.rerun()

            with tab2:
                st.markdown('<p class="section-title">Field Register</p>',
                            unsafe_allow_html=True)
                df_f = run_query(
                    "SELECT field_id, field_name, division, type, "
                    "extent_ha, pct_division, pct_estate, "
                    "pruning_date, age_months "
                    "FROM fields_with_pct ORDER BY division, type, field_id"
                )
                st.dataframe(df_f, use_container_width=True, hide_index=True)

                st.markdown("**Update Pruning Date:**")
                with st.form("update_pruning"):
                    field_opts = {
                        f"{r['field_name']} ({r['division']})": r['field_id']
                        for _, r in df_f.iterrows()
                    }
                    sel_f = st.selectbox("Select Field", list(field_opts.keys()))
                    prune_date = st.date_input("Pruning Date")
                    prune_type = st.selectbox("Pruning Type",
                                ["VP Prune","SD Prune","Tipping"])
                    if st.form_submit_button("Update", type="primary"):
                        fid = field_opts[sel_f]
                        run_command(
                            "UPDATE fields SET pruning_date=? WHERE field_id=?",
                            (prune_date, fid)
                        )
                        run_command("""
                            INSERT INTO pruning_log
                            (field_id, pruning_date, pruning_type, entered_by)
                            VALUES (?,?,?,?)
                        """, (fid, prune_date, prune_type, user['user_id']))
                        st.success("Pruning date updated!")
                        st.rerun()

            with tab3:
                st.markdown('<p class="section-title">Monthly Outturn %</p>',
                            unsafe_allow_html=True)
                df_out = run_query(
                    "SELECT outturn_year, outturn_month, outturn_pct, "
                    "is_approximate, notes FROM outturn_log ORDER BY "
                    "outturn_year DESC, outturn_month DESC"
                )
                st.dataframe(df_out, use_container_width=True, hide_index=True)

                with st.form("outturn_form"):
                    c1,c2,c3 = st.columns(3)
                    ot_year  = c1.number_input("Year", value=2026,
                                                min_value=2020, max_value=2030)
                    ot_month = c2.number_input("Month", value=datetime.today().month,
                                                min_value=1, max_value=12)
                    ot_pct   = c3.number_input("Outturn %", value=21.50,
                                                format="%.2f")
                    ot_approx = st.checkbox("Is Approximate?")
                    ot_notes  = st.text_input("Notes")
                    if st.form_submit_button("Save Outturn", type="primary"):
                        run_command("""
                            MERGE outturn_log AS target
                            USING (SELECT ? AS yr, ? AS mn) AS source
                            ON target.outturn_year=source.yr
                               AND target.outturn_month=source.mn
                            WHEN MATCHED THEN
                                UPDATE SET outturn_pct=?,
                                           is_approximate=?,
                                           notes=?
                            WHEN NOT MATCHED THEN
                                INSERT (outturn_year,outturn_month,
                                        outturn_pct,is_approximate,notes)
                                VALUES (?,?,?,?,?);
                        """, (ot_year, ot_month, ot_pct, ot_approx, ot_notes,
                              ot_year, ot_month, ot_pct, ot_approx, ot_notes))
                        st.success("Outturn saved!")
                        st.rerun()

# ══ PAGE: NITROGEN & INPUTS DASHBOARD ═══════════════════
    elif page == "⚗️ Nitrogen & Inputs":
        st.markdown("""
        <div class="main-header">
            <h2 style="margin:0">⚗️ Nitrogen & Inputs</h2>
            <p style="margin:4px 0 0 0;opacity:0.85">Fertiliser application overview</p>
        </div>""", unsafe_allow_html=True)

        df_nitro = run_query("""
            SELECT
                n.application_date,
                YEAR(n.application_date)  AS log_year,
                MONTH(n.application_date) AS log_month,
                f.field_id, f.field_name, f.division, f.type,
                n.fertilizer_type, n.nitrogen_qty_kg
            FROM nitrogen_log n
            JOIN fields f ON n.field_id = f.field_id
        """)

        if len(df_nitro) == 0:
            st.info("📌 No nitrogen entries found yet. Add one via 🌱 Nitrogen Entry.")
        else:
            total_n = df_nitro['nitrogen_qty_kg'].sum()
            this_month = datetime.today().month
            this_year  = datetime.today().year
            month_n = df_nitro[
                (df_nitro['log_month'] == this_month) &
                (df_nitro['log_year']  == this_year)
            ]['nitrogen_qty_kg'].sum()

            c1, c2, c3 = st.columns(3)
            c1.metric("Total Nitrogen Applied (kg)", f"{total_n:,.1f}")
            c2.metric("This Month (kg)", f"{month_n:,.1f}")
            c3.metric("Total Applications", len(df_nitro))

            st.markdown('<p class="section-title">📈 Nitrogen Applied by Month</p>',
                        unsafe_allow_html=True)
            monthly = (
                df_nitro.groupby(['log_year', 'log_month'])['nitrogen_qty_kg']
                .sum()
                .reset_index()
            )
            monthly['period'] = (
                monthly['log_year'].astype(str) + "-" +
                monthly['log_month'].astype(str).str.zfill(2)
            )
            st.bar_chart(monthly.set_index('period')['nitrogen_qty_kg'])

            st.markdown('<p class="section-title">🌿 Nitrogen by Field</p>',
                        unsafe_allow_html=True)
            by_field = (
                df_nitro.groupby(['field_name', 'division'])['nitrogen_qty_kg']
                .sum()
                .reset_index()
                .sort_values('nitrogen_qty_kg', ascending=False)
            )
            st.bar_chart(by_field.set_index('field_name')['nitrogen_qty_kg'])

            st.markdown('<p class="section-title">📋 All Nitrogen Entries</p>',
                        unsafe_allow_html=True)
            st.dataframe(
                df_nitro.sort_values('application_date', ascending=False),
                use_container_width=True, hide_index=True
            )






  # ══ PAGE: LABOUR & PLUCKING DASHBOARD ═══════════════════
    elif page == "👷 Labour & Plucking":
        st.markdown("""
        <div class="main-header">
            <h2 style="margin:0">👷 Labour & Plucking</h2>
            <p style="margin:4px 0 0 0;opacity:0.85">Labour efficiency and plucking round analysis</p>
        </div>""", unsafe_allow_html=True)

        df_labour = run_query("""
            SELECT
                h.harvest_date,
                YEAR(h.harvest_date)  AS log_year,
                MONTH(h.harvest_date) AS log_month,
                f.field_id, f.field_name, f.division,
                h.round_number, h.reg_plucker_count, h.cash_plucker_count,
                h.kangany_count, h.sack_labour_count,
                h.total_mandays, h.total_green_leaf_kg, h.plucking_average
            FROM harvest_log h
            JOIN fields f ON h.field_id = f.field_id
        """)

        if len(df_labour) == 0:
            st.info("📌 No harvest entries found yet. Add one via 📋 Daily Plucking Entry.")
        else:
            # ── KPI row ──
            total_mandays = df_labour['total_mandays'].sum()
            avg_plk = df_labour['plucking_average'].mean()
            total_pluckers = (df_labour['reg_plucker_count'] + df_labour['cash_plucker_count']).sum()
            yield_per_manday = round(
                df_labour['total_green_leaf_kg'].sum() / total_mandays, 2
            ) if total_mandays > 0 else 0

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Mandays", f"{total_mandays:,.1f}")
            c2.metric("Avg Plucking Average", f"{avg_plk:,.2f} kg")
            c3.metric("Total Plucker-Days", f"{total_pluckers:,.0f}")
            c4.metric("Yield per Manday", f"{yield_per_manday:,.2f} kg")

            # ── Plucking average trend ──
            st.markdown('<p class="section-title">📈 Plucking Average Trend</p>',
                        unsafe_allow_html=True)
            monthly = (
                df_labour.groupby(['log_year', 'log_month'])['plucking_average']
                .mean()
                .reset_index()
            )
            monthly['period'] = (
                monthly['log_year'].astype(str) + "-" +
                monthly['log_month'].astype(str).str.zfill(2)
            )
            st.line_chart(monthly.set_index('period')['plucking_average'])

            # ── Mandays by field ──
            st.markdown('<p class="section-title">👷 Mandays by Field</p>',
                        unsafe_allow_html=True)
            by_field = (
                df_labour.groupby(['field_name', 'division'])['total_mandays']
                .sum()
                .reset_index()
                .sort_values('total_mandays', ascending=False)
            )
            st.bar_chart(by_field.set_index('field_name')['total_mandays'])

            # ── Round analysis (rounds logged per field) ──
            st.markdown('<p class="section-title">🔄 Plucking Rounds by Field</p>',
                        unsafe_allow_html=True)
            rounds = (
                df_labour.groupby('field_name')['round_number']
                .nunique()
                .reset_index()
                .rename(columns={'round_number': 'rounds_logged'})
                .sort_values('rounds_logged', ascending=False)
            )
            st.dataframe(rounds, use_container_width=True, hide_index=True)

            # ── Full labour log ──
            st.markdown('<p class="section-title">📋 Labour Entries</p>',
                        unsafe_allow_html=True)
            st.dataframe(
                df_labour.sort_values('harvest_date', ascending=False),
                use_container_width=True, hide_index=True
            )

    # ══ PAGE: MADE TEA OUTTURN DASHBOARD ═════════════════════
    elif page == "📊 Made Tea Outturn":
        st.markdown("""
        <div class="main-header">
            <h2 style="margin:0">📊 Made Tea Outturn</h2>
            <p style="margin:4px 0 0 0;opacity:0.85">Made tea production from green leaf outturn %</p>
        </div>""", unsafe_allow_html=True)

        df_outturn = run_query("""
            SELECT outturn_year, outturn_month, outturn_pct, is_approximate, notes
            FROM outturn_log
            ORDER BY outturn_year, outturn_month
        """)

        df_harvest = run_query("""
            SELECT
                YEAR(harvest_date)  AS log_year,
                MONTH(harvest_date) AS log_month,
                SUM(total_green_leaf_kg) AS total_green_leaf_kg
            FROM harvest_log
            GROUP BY YEAR(harvest_date), MONTH(harvest_date)
        """)

        if len(df_outturn) == 0 or len(df_harvest) == 0:
            st.info("📌 Enter both harvest data and monthly Outturn % (via Admin Panel) "
                    "to see made tea estimates.")
        else:
            merged = pd.merge(
                df_harvest, df_outturn,
                left_on=['log_year', 'log_month'],
                right_on=['outturn_year', 'outturn_month'],
                how='inner'
            )
            merged['made_tea_kg'] = (
                merged['total_green_leaf_kg'] * merged['outturn_pct'] / 100
            ).round(1)
            merged['period'] = (
                merged['log_year'].astype(str) + "-" +
                merged['log_month'].astype(str).str.zfill(2)
            )

            if len(merged) == 0:
                st.warning("No matching month found between harvest data and Outturn % records. "
                           "Add an Outturn % entry for the relevant month/year via Admin Panel.")
            else:
                total_made_tea = merged['made_tea_kg'].sum()
                avg_outturn = merged['outturn_pct'].mean()

                c1, c2, c3 = st.columns(3)
                c1.metric("Total Made Tea (kg)", f"{total_made_tea:,.1f}")
                c2.metric("Avg Outturn %", f"{avg_outturn:,.2f}%")
                c3.metric("Months Covered", len(merged))

                st.markdown('<p class="section-title">📈 Made Tea by Month</p>',
                            unsafe_allow_html=True)
                st.bar_chart(merged.set_index('period')['made_tea_kg'])

                st.markdown('<p class="section-title">📋 Monthly Outturn Detail</p>',
                            unsafe_allow_html=True)
                st.dataframe(
                    merged[['period', 'total_green_leaf_kg', 'outturn_pct',
                            'made_tea_kg', 'is_approximate']]
                    .sort_values('period', ascending=False),
                    use_container_width=True, hide_index=True
                )

    # ── FOOTER ───────────────────────────────────────────────
    st.divider()
    st.markdown(
        "<p style='text-align:center;color:#aaa;font-size:0.75rem'>"
        "DSPMS v1.0 | Uda Radella Estate | "
        "G.A.A.U.Dharmasena | BSc Data Science 2025</p>",
        unsafe_allow_html=True
    )
    
