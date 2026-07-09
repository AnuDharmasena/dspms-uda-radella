import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import math

st.set_page_config(
    page_title="DSPMS - Uda Radella Estate",
    page_icon="🍃",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
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
    .kpi-card {
        background: white; border-radius: 10px;
        padding: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #2d8a45; margin-bottom: 10px;
    }
    .approx-box {
        background: #fff8e1; border: 2px dashed #f39c12;
        border-radius: 8px; padding: 15px; margin: 10px 0;
    }
    .user-badge {
        background: #e8f5e9; border-radius: 8px;
        padding: 8px 12px; margin-bottom: 8px;
        font-size: 0.85rem; color: #1a5c2a;
    }
</style>
""", unsafe_allow_html=True)

# ── USERS ─────────────────────────────────────────────────────
USERS = {
    'admin':    {'password':'admin123',   'name':'Estate Manager',      'role':'admin',         'division': None},
    'manager':  {'password':'manager123', 'name':'Manoj Wijewardhana',  'role':'manager',       'division': None},
    'fo_lower': {'password':'lower123',   'name':'K.G.D.K.Ekanayaka',  'role':'field_officer', 'division':'Lower'},
    'fo_upper': {'password':'upper123',   'name':'Field Officer Upper', 'role':'field_officer', 'division':'Upper'},
}

# ── SESSION STATE ─────────────────────────────────────────────
if 'logged_in'   not in st.session_state: st.session_state.logged_in = False
if 'user'        not in st.session_state: st.session_state.user = None
if 'pluck_log'   not in st.session_state: st.session_state.pluck_log = []
if 'nitro_log'   not in st.session_state: st.session_state.nitro_log = []
if 'act_log'     not in st.session_state: st.session_state.act_log = []

# ── FIELD MASTER DATA ─────────────────────────────────────────
FIELDS = pd.DataFrame([
    # Lower Division
    {'field_id':'1A',   'field_name':'1A',   'division':'Lower','type':'SD','extent_ha':4.85},
    {'field_id':'16B',  'field_name':'16B',  'division':'Lower','type':'VP','extent_ha':4.50},
    {'field_id':'8B',   'field_name':'8B',   'division':'Lower','type':'VP','extent_ha':4.85},
    {'field_id':'16A',  'field_name':'16A',  'division':'Lower','type':'VP','extent_ha':5.75},
    {'field_id':'1B',   'field_name':'1B',   'division':'Lower','type':'VP','extent_ha':4.00},
    {'field_id':'10B1', 'field_name':'10B1', 'division':'Lower','type':'VP','extent_ha':4.00},
    {'field_id':'10B',  'field_name':'10B',  'division':'Lower','type':'VP','extent_ha':4.00},
    {'field_id':'3A',   'field_name':'3A',   'division':'Lower','type':'VP','extent_ha':6.50},
    {'field_id':'10A1', 'field_name':'10A1', 'division':'Lower','type':'VP','extent_ha':4.00},
    {'field_id':'10A',  'field_name':'10A',  'division':'Lower','type':'VP','extent_ha':4.25},
    {'field_id':'1D',   'field_name':'1D',   'division':'Lower','type':'VP','extent_ha':4.75},
    {'field_id':'17C',  'field_name':'17C',  'division':'Lower','type':'VP','extent_ha':0.75},
    {'field_id':'1C',   'field_name':'1C',   'division':'Lower','type':'VP','extent_ha':5.75},
    {'field_id':'3B',   'field_name':'3B',   'division':'Lower','type':'VP','extent_ha':7.00},
    {'field_id':'16B1', 'field_name':'16B1', 'division':'Lower','type':'VP','extent_ha':4.00},
    {'field_id':'8A',   'field_name':'8A',   'division':'Lower','type':'VP','extent_ha':7.00},
    # Upper Division
    {'field_id':'1_7',  'field_name':'1./7', 'division':'Upper','type':'VP','extent_ha':1.00},
    {'field_id':'4_7',  'field_name':'4./7', 'division':'Upper','type':'VP','extent_ha':1.00},
    {'field_id':'14_7B','field_name':'14/7B','division':'Upper','type':'VP','extent_ha':2.00},
    {'field_id':'14_7', 'field_name':'14/7', 'division':'Upper','type':'VP','extent_ha':4.00},
    {'field_id':'3_7',  'field_name':'3./7', 'division':'Upper','type':'VP','extent_ha':1.00},
    {'field_id':'14_7E','field_name':'14/7E','division':'Upper','type':'VP','extent_ha':2.00},
    {'field_id':'14_7D','field_name':'14/7D','division':'Upper','type':'VP','extent_ha':1.00},
    {'field_id':'14_7C','field_name':'14/7C','division':'Upper','type':'VP','extent_ha':2.00},
    {'field_id':'2_7',  'field_name':'2./7', 'division':'Upper','type':'VP','extent_ha':1.00},
    {'field_id':'11B',  'field_name':'11B',  'division':'Upper','type':'SD','extent_ha':4.75},
    {'field_id':'9B',   'field_name':'9B',   'division':'Upper','type':'SD','extent_ha':2.00},
    {'field_id':'15A',  'field_name':'15A',  'division':'Upper','type':'SD','extent_ha':4.00},
    {'field_id':'5B',   'field_name':'5B',   'division':'Upper','type':'SD','extent_ha':3.50},
    {'field_id':'9A',   'field_name':'9A',   'division':'Upper','type':'SD','extent_ha':5.75},
    {'field_id':'5B1',  'field_name':'5B/1', 'division':'Upper','type':'SD','extent_ha':3.50},
    {'field_id':'4B',   'field_name':'4B',   'division':'Upper','type':'SD','extent_ha':4.00},
])

# Auto calculate pct_division
div_totals = FIELDS.groupby('division')['extent_ha'].sum().reset_index()
div_totals.columns = ['division','div_total']
FIELDS = FIELDS.merge(div_totals, on='division')
FIELDS['pct_division'] = (FIELDS['extent_ha']/FIELDS['div_total']*100).round(0).astype(int)
FIELDS['pct_estate']   = (FIELDS['extent_ha']/123.45*100).round(0).astype(int)

# ── SAMPLE KPI DATA (from M FORMAT) ──────────────────────────
FIELD_KPI = pd.DataFrame([
    # Lower Division fields
    {'field_id':'1A',  'yph_m_bud':200,'yph_m_act':214,'yph_td_bud':1200,'yph_td_act':1165,'rounds_m':3,'rounds_td':9, 'n_ratio':18.93,'ph':5.19,'fert_days':17,'weed_days':25},
    {'field_id':'16B', 'yph_m_bud':200,'yph_m_act':182,'yph_td_bud':1200,'yph_td_act':1145,'rounds_m':3,'rounds_td':9, 'n_ratio':21.20,'ph':5.42,'fert_days':39,'weed_days':63},
    {'field_id':'8B',  'yph_m_bud':200,'yph_m_act':269,'yph_td_bud':1200,'yph_td_act':1635,'rounds_m':4,'rounds_td':10,'n_ratio':6.39, 'ph':5.93,'fert_days':32,'weed_days':38},
    {'field_id':'16A', 'yph_m_bud':250,'yph_m_act':144,'yph_td_bud':1500,'yph_td_act':1300,'rounds_m':3,'rounds_td':9, 'n_ratio':16.17,'ph':5.55,'fert_days':25,'weed_days':35},
    {'field_id':'1B',  'yph_m_bud':240,'yph_m_act':244,'yph_td_bud':1440,'yph_td_act':1810,'rounds_m':4,'rounds_td':10,'n_ratio':13.41,'ph':5.42,'fert_days':17,'weed_days':84},
    {'field_id':'10B1','yph_m_bud':220,'yph_m_act':221,'yph_td_bud':1320,'yph_td_act':1912,'rounds_m':4,'rounds_td':10,'n_ratio':13.54,'ph':5.63,'fert_days':14,'weed_days':21},
    {'field_id':'10B', 'yph_m_bud':240,'yph_m_act':236,'yph_td_bud':1440,'yph_td_act':2159,'rounds_m':4,'rounds_td':10,'n_ratio':10.40,'ph':5.70,'fert_days':16,'weed_days':32},
    {'field_id':'3A',  'yph_m_bud':300,'yph_m_act':246,'yph_td_bud':1800,'yph_td_act':2038,'rounds_m':3,'rounds_td':10,'n_ratio':30.13,'ph':5.20,'fert_days':30,'weed_days':54},
    {'field_id':'10A1','yph_m_bud':250,'yph_m_act':248,'yph_td_bud':1500,'yph_td_act':1507,'rounds_m':3,'rounds_td':9, 'n_ratio':15.32,'ph':5.31,'fert_days':22,'weed_days':32},
    {'field_id':'10A', 'yph_m_bud':280,'yph_m_act':289,'yph_td_bud':1680,'yph_td_act':1788,'rounds_m':4,'rounds_td':10,'n_ratio':11.38,'ph':5.68,'fert_days':16,'weed_days':25},
    {'field_id':'1D',  'yph_m_bud':220,'yph_m_act':219,'yph_td_bud':1320,'yph_td_act':1727,'rounds_m':4,'rounds_td':10,'n_ratio':13.44,'ph':5.87,'fert_days':17,'weed_days':49},
    {'field_id':'17C', 'yph_m_bud':200,'yph_m_act':309,'yph_td_bud':1200,'yph_td_act':1645,'rounds_m':3,'rounds_td':9, 'n_ratio':16.76,'ph':5.64,'fert_days':69,'weed_days':21},
    {'field_id':'1C',  'yph_m_bud':180,'yph_m_act':180,'yph_td_bud':1080,'yph_td_act':1716,'rounds_m':4,'rounds_td':10,'n_ratio':21.58,'ph':5.42,'fert_days':14,'weed_days':18},
    {'field_id':'3B',  'yph_m_bud':260,'yph_m_act':254,'yph_td_bud':1560,'yph_td_act':2600,'rounds_m':4,'rounds_td':10,'n_ratio':8.64, 'ph':5.65,'fert_days':18,'weed_days':69},
    {'field_id':'16B1','yph_m_bud':100,'yph_m_act':107,'yph_td_bud':600, 'yph_td_act':428, 'rounds_m':2,'rounds_td':6, 'n_ratio':0,    'ph':5.44,'fert_days':13,'weed_days':21},
    {'field_id':'8A',  'yph_m_bud':0,  'yph_m_act':0,  'yph_td_bud':0,   'yph_td_act':0,   'rounds_m':0,'rounds_td':0, 'n_ratio':0,    'ph':5.19,'fert_days':0, 'weed_days':0},
    # Upper Division fields
    {'field_id':'1_7', 'yph_m_bud':180,'yph_m_act':178,'yph_td_bud':1080,'yph_td_act':681, 'rounds_m':3,'rounds_td':8, 'n_ratio':26.42,'ph':5.19,'fert_days':16,'weed_days':35},
    {'field_id':'4_7', 'yph_m_bud':180,'yph_m_act':154,'yph_td_bud':1080,'yph_td_act':782, 'rounds_m':2,'rounds_td':7, 'n_ratio':23.02,'ph':5.93,'fert_days':25,'weed_days':16},
    {'field_id':'14_7B','yph_m_bud':180,'yph_m_act':165,'yph_td_bud':1080,'yph_td_act':933,'rounds_m':3,'rounds_td':8, 'n_ratio':25.72,'ph':5.38,'fert_days':28,'weed_days':38},
    {'field_id':'14_7','yph_m_bud':200,'yph_m_act':156,'yph_td_bud':1200,'yph_td_act':1200,'rounds_m':3,'rounds_td':9,'n_ratio':19.67,'ph':5.31,'fert_days':11,'weed_days':25},
    {'field_id':'3_7', 'yph_m_bud':160,'yph_m_act':157,'yph_td_bud':960, 'yph_td_act':1130,'rounds_m':3,'rounds_td':8,'n_ratio':15.37,'ph':5.16,'fert_days':32,'weed_days':18},
    {'field_id':'14_7E','yph_m_bud':200,'yph_m_act':165,'yph_td_bud':1200,'yph_td_act':1361,'rounds_m':3,'rounds_td':9,'n_ratio':18.13,'ph':5.56,'fert_days':37,'weed_days':0},
    {'field_id':'14_7D','yph_m_bud':180,'yph_m_act':175,'yph_td_bud':1080,'yph_td_act':1489,'rounds_m':3,'rounds_td':9,'n_ratio':18.35,'ph':6.47,'fert_days':39,'weed_days':16},
    {'field_id':'14_7C','yph_m_bud':200,'yph_m_act':192,'yph_td_bud':1200,'yph_td_act':1507,'rounds_m':3,'rounds_td':9,'n_ratio':19.63,'ph':5.63,'fert_days':17,'weed_days':79},
    {'field_id':'2_7', 'yph_m_bud':180,'yph_m_act':168,'yph_td_bud':1080,'yph_td_act':1266,'rounds_m':3,'rounds_td':9,'n_ratio':20.62,'ph':5.31,'fert_days':24,'weed_days':56},
    {'field_id':'11B', 'yph_m_bud':300,'yph_m_act':241,'yph_td_bud':1800,'yph_td_act':1855,'rounds_m':2,'rounds_td':6,'n_ratio':11.08,'ph':5.52,'fert_days':16,'weed_days':21},
    {'field_id':'9B',  'yph_m_bud':280,'yph_m_act':207,'yph_td_bud':1680,'yph_td_act':1194,'rounds_m':2,'rounds_td':5,'n_ratio':9.47, 'ph':5.37,'fert_days':25,'weed_days':21},
    {'field_id':'15A', 'yph_m_bud':300,'yph_m_act':248,'yph_td_bud':1800,'yph_td_act':1779,'rounds_m':2,'rounds_td':6,'n_ratio':10.12,'ph':5.12,'fert_days':13,'weed_days':0},
    {'field_id':'5B',  'yph_m_bud':280,'yph_m_act':214,'yph_td_bud':1680,'yph_td_act':1497,'rounds_m':2,'rounds_td':6,'n_ratio':11.45,'ph':5.18,'fert_days':11,'weed_days':18},
    {'field_id':'9A',  'yph_m_bud':300,'yph_m_act':254,'yph_td_bud':1800,'yph_td_act':2095,'rounds_m':3,'rounds_td':8,'n_ratio':8.49, 'ph':5.30,'fert_days':37,'weed_days':49},
    {'field_id':'5B1', 'yph_m_bud':280,'yph_m_act':207,'yph_td_bud':1680,'yph_td_act':2119,'rounds_m':3,'rounds_td':8,'n_ratio':8.48, 'ph':5.36,'fert_days':32,'weed_days':35},
    {'field_id':'4B',  'yph_m_bud':260,'yph_m_act':241,'yph_td_bud':1560,'yph_td_act':2238,'rounds_m':3,'rounds_td':8,'n_ratio':10.11,'ph':5.15,'fert_days':32,'weed_days':56},
])

# Merge with field master
DF = FIELDS.merge(FIELD_KPI, on='field_id', how='left')
DF['pct_ach_m']  = (DF['yph_m_act']/DF['yph_m_bud']*100).round(1).where(DF['yph_m_bud']>0, 0)
DF['pct_ach_td'] = (DF['yph_td_act']/DF['yph_td_bud']*100).round(1).where(DF['yph_td_bud']>0, 0)
DF['label']      = DF['field_name'] + ' (' + DF['type'] + ')'

# ══ LOGIN ════════════════════════════════════════════════════
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1,1.5,1])
    with col2:
        st.markdown("""
        <div class="login-box">
            <div class="login-title">🍃 DSPMS</div>
            <div class="login-sub">Uda Radella Estate<br>Kelani Valley Plantations PLC</div>
        </div>""", unsafe_allow_html=True)
        username = st.text_input("👤 Username", placeholder="Enter username")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter password")
        if st.button("Login →", use_container_width=True, type="primary"):
            if username in USERS and USERS[username]['password'] == password:
                st.session_state.logged_in = True
                st.session_state.user = {
                    'username': username, **USERS[username]
                }
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
        st.caption("© 2025 Uda Radella Estate | DSPMS v1.0")

# ══ MAIN APP ═════════════════════════════════════════════════
else:
    user   = st.session_state.user
    role   = user['role']
    div    = user['division']

    with st.sidebar:
        st.markdown("### 🍃 DSPMS")
        st.markdown("**Uda Radella Estate**")
        st.markdown("*Kelani Valley Plantations PLC*")
        st.divider()
        role_icon = {"admin":"👑","manager":"📊","field_officer":"🌿"}.get(role,"👤")
        st.markdown(
            f'<div class="user-badge">{role_icon} <b>{user["name"]}</b><br>'
            f'<small>{role.replace("_"," ").title()}'
            f'{" | "+div if div else ""}</small></div>',
            unsafe_allow_html=True
        )

        if role in ('admin','manager'):
            pages = [
                "🏠 Executive Summary",
                "🌿 Field Performance",
                "⚗️ Nitrogen & Inputs",
                "👷 Labour & Plucking",
                "📊 Made Tea Outturn",
                "📋 Daily Plucking Entry",
                "🌱 Nitrogen Entry",
                "🔧 Activity Entry",
            ]
        else:
            pages = [
                "📋 Daily Plucking Entry",
                "🌱 Nitrogen Entry",
                "🔧 Activity Entry",
            ]

        page = st.radio("Navigation", pages)
        st.divider()

        if role in ('admin','manager'):
            div_filter = st.selectbox("Division",
                ["All Divisions","Lower (ULD)","Upper (UUD)"])
        else:
            div_filter = div

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()

    def filter_df(div_filter):
        if div_filter == "All Divisions": return DF
        d = "Lower" if "Lower" in str(div_filter) else "Upper"
        return DF[DF['division']==d]

    # ── EXECUTIVE SUMMARY ────────────────────────────────────
    if page == "🏠 Executive Summary":
        st.markdown("""<div class="main-header">
            <h2 style="margin:0">🍃 DSPMS — Uda Radella Estate</h2>
            <p style="margin:4px 0 0 0;opacity:0.85">
            Kelani Valley Plantations PLC | Executive Summary | June 2026</p>
        </div>""", unsafe_allow_html=True)

        df_all = DF.copy()
        lo = DF[DF['division']=='Lower']
        up = DF[DF['division']=='Upper']

        # Estate KPIs
        def w_yph(df, col):
            s = df['extent_ha'].sum()
            return round((df[col]*df['extent_ha']).sum()/s,1) if s>0 else 0
        def w_n(df):
            df2 = df[df['n_ratio']>0]
            s = df2['extent_ha'].sum()
            return round((df2['n_ratio']*df2['extent_ha']).sum()/s,2) if s>0 else 0

        est_yph_td  = w_yph(df_all[df_all['yph_td_act']>0],'yph_td_act')
        est_yph_bud = w_yph(df_all[df_all['yph_td_bud']>0],'yph_td_bud')
        est_n       = w_n(df_all)
        est_pct     = round(est_yph_td/est_yph_bud*100,1) if est_yph_bud>0 else 0

        st.markdown('<p class="section-title">📊 Estate KPIs — June 2026</p>',
                    unsafe_allow_html=True)
        c1,c2,c3,c4,c5 = st.columns(5)
        c1.metric("Estate Todate YPH", f"{est_yph_td} kg/ha",
                  delta=f"{round(est_yph_td-est_yph_bud,1)} vs Budget")
        c2.metric("% Achievement TD", f"{est_pct}%")
        c3.metric("Estate N Ratio",   f"{est_n}",
                  delta="⚠️ High" if est_n>30 else "✅ Normal",
                  delta_color="inverse")
        c4.metric("Total Extent",     "123.45 ha")
        c5.metric("Total Fields",     "32")

        st.divider()
        st.markdown('<p class="section-title">🏭 Division Comparison</p>',
                    unsafe_allow_html=True)
        rows=[]
        for dn,dd,code,ha in [
            ('Lower','Lower','ULD',75.95),
            ('Upper','Upper','UUD',47.50)
        ]:
            df_d = DF[DF['division']==dd]
            for t in ['VP','SD']:
                df_t = df_d[df_d['type']==t]
                if len(df_t)==0: continue
                ya=w_yph(df_t[df_t['yph_td_act']>0],'yph_td_act')
                yb=w_yph(df_t[df_t['yph_td_bud']>0],'yph_td_bud')
                rows.append({
                    'Division':dn,'Code':code,'Type':t,
                    'Extent(ha)':round(df_t['extent_ha'].sum(),2),
                    'YPH TD Budget':round(yb,1),
                    'YPH TD Actual':round(ya,1),
                    '% Achieved':round(ya/yb*100,1) if yb>0 else 0,
                    'N Ratio':w_n(df_t)
                })
        df_s = pd.DataFrame(rows)
        st.dataframe(df_s, use_container_width=True, hide_index=True)

        fig = go.Figure()
        for t,c in [('VP','#2d8a45'),('SD','#e67e22')]:
            d = df_s[df_s['Type']==t]
            fig.add_trace(go.Bar(name=f'{t} Budget', x=d['Division'],
                                 y=d['YPH TD Budget'], marker_color='lightgray',
                                 text=d['YPH TD Budget'], textposition='auto'))
            fig.add_trace(go.Bar(name=f'{t} Actual', x=d['Division'],
                                 y=d['YPH TD Actual'], marker_color=c,
                                 text=d['YPH TD Actual'], textposition='auto'))
        fig.update_layout(barmode='group', height=380,
                          title='Todate YPH — Budget vs Actual',
                          plot_bgcolor='white', paper_bgcolor='white',
                          font=dict(size=13))
        st.plotly_chart(fig, use_container_width=True)

        # N Ratio Gauges
        st.markdown('<p class="section-title">⚗️ N Ratio Gauges — MD/CEO View</p>',
                    unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        for col,(lbl,val) in zip([c1,c2,c3],[
            ('Estate Overall', est_n),
            ('Lower Division (ULD)', w_n(lo)),
            ('Upper Division (UUD)', w_n(up))
        ]):
            fg = go.Figure(go.Indicator(
                mode="gauge+number", value=val,
                title={'text':lbl,'font':{'size':15}},
                number={'font':{'size':30}},
                gauge={'axis':{'range':[0,50]},
                       'bar':{'color':'#e74c3c' if val>30 else '#2d8a45'},
                       'steps':[{'range':[0,25],'color':'#d5f5e3'},
                                 {'range':[25,35],'color':'#fef9e7'},
                                 {'range':[35,50],'color':'#fadbd8'}],
                       'threshold':{'line':{'color':'red','width':4},'value':30}}
            ))
            fg.update_layout(height=260, margin=dict(t=60,b=10,l=30,r=30))
            col.plotly_chart(fg, use_container_width=True)

    # ── FIELD PERFORMANCE ────────────────────────────────────
    elif page == "🌿 Field Performance":
        st.markdown("""<div class="main-header">
            <h2 style="margin:0">🌿 Field Performance — YPH Analysis</h2>
        </div>""", unsafe_allow_html=True)

        df = filter_df(div_filter)
        df = df[df['yph_td_bud']>0].copy()
        df['color'] = df.apply(
            lambda r: '#27ae60' if r['yph_td_act']>=r['yph_td_bud'] else '#e74c3c', axis=1)

        st.markdown('<p class="section-title">Todate YPH — Budget vs Actual</p>',
                    unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(name='TD Budget', x=df['label'], y=df['yph_td_bud'],
                             marker_color='lightblue',
                             text=df['yph_td_bud'], textposition='auto'))
        fig.add_trace(go.Bar(name='TD Actual', x=df['label'], y=df['yph_td_act'],
                             marker_color=df['color'].tolist(),
                             text=df['yph_td_act'], textposition='auto'))
        fig.update_layout(barmode='group', height=440, xaxis_tickangle=-45,
                          plot_bgcolor='white', paper_bgcolor='white', font=dict(size=11))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('<p class="section-title">% Achievement Todate</p>',
                    unsafe_allow_html=True)
        df_s = df.sort_values('pct_ach_td', ascending=True)
        fig2 = px.bar(df_s, x='pct_ach_td', y='label', orientation='h',
                      color='pct_ach_td',
                      color_continuous_scale=['#e74c3c','#f39c12','#27ae60'],
                      range_color=[50,130], text='pct_ach_td')
        fig2.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig2.add_vline(x=100, line_dash='dash', line_color='black')
        fig2.update_layout(height=600, plot_bgcolor='white', paper_bgcolor='white',
                           coloraxis_showscale=False, font=dict(size=11))
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown('<p class="section-title">Field Data Table</p>',
                    unsafe_allow_html=True)
        cols = ['field_name','division','type','extent_ha','yph_m_bud','yph_m_act',
                'pct_ach_m','yph_td_bud','yph_td_act','pct_ach_td','rounds_td']
        df_t = df[cols].round(1).copy()
        df_t.columns = ['Field','Division','Type','Extent','YPH Bud(M)','YPH Act(M)',
                         '%Ach(M)','YPH Bud(TD)','YPH Act(TD)','%Ach(TD)','Rounds(TD)']
        st.dataframe(df_t, use_container_width=True, hide_index=True)

    # ── NITROGEN & INPUTS ────────────────────────────────────
    elif page == "⚗️ Nitrogen & Inputs":
        st.markdown("""<div class="main-header">
            <h2 style="margin:0">⚗️ Nitrogen Ratio & Input Monitoring</h2>
        </div>""", unsafe_allow_html=True)

        df = filter_df(div_filter)
        df = df[df['n_ratio']>0].copy()
        df['label'] = df['field_name']+' ('+df['type']+')'

        st.markdown('<p class="section-title">N Ratio by Field</p>',
                    unsafe_allow_html=True)
        st.caption("🔴 Red = N Ratio > 30 | 🟢 Green = Normal")
        df_n = df.sort_values('n_ratio', ascending=False)
        fig = go.Figure(go.Bar(
            x=df_n['label'], y=df_n['n_ratio'],
            marker_color=df_n['n_ratio'].apply(
                lambda x: '#e74c3c' if x>30 else '#27ae60').tolist(),
            text=df_n['n_ratio'].round(2), textposition='auto'
        ))
        fig.add_hline(y=30, line_dash='dash', line_color='red',
                      annotation_text='Threshold: 30')
        fig.update_layout(xaxis_tickangle=-45, height=420,
                          plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('<p class="section-title">Days Since Last Fertilizer</p>',
                    unsafe_allow_html=True)
        df_f = df[df['fert_days']>0].sort_values('fert_days', ascending=False)
        if len(df_f)>0:
            fig2 = go.Figure(go.Bar(
                x=df_f['label'], y=df_f['fert_days'],
                marker_color=df_f['fert_days'].apply(
                    lambda x: '#e74c3c' if x>45 else '#27ae60').tolist(),
                text=df_f['fert_days'].astype(int), textposition='auto'
            ))
            fig2.add_hline(y=45, line_dash='dash', line_color='orange',
                           annotation_text='45 days')
            fig2.update_layout(xaxis_tickangle=-45, height=380,
                               plot_bgcolor='white', paper_bgcolor='white')
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown('<p class="section-title">Soil pH Values</p>',
                    unsafe_allow_html=True)
        df_ph = df[df['ph']>0].sort_values('ph')
        fig3 = px.scatter(df_ph, x='label', y='ph', color='division',
                          color_discrete_map={'Lower':'#1a5c2a','Upper':'#5dade2'},
                          title='Soil pH (Ideal: 4.5–5.5)')
        fig3.add_hline(y=4.5, line_dash='dot', line_color='orange')
        fig3.add_hline(y=5.5, line_dash='dot', line_color='orange')
        fig3.update_layout(xaxis_tickangle=-45, height=380,
                           plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig3, use_container_width=True)

    # ── LABOUR & PLUCKING ────────────────────────────────────
    elif page == "👷 Labour & Plucking":
        st.markdown("""<div class="main-header">
            <h2 style="margin:0">👷 Labour & Plucking Performance</h2>
        </div>""", unsafe_allow_html=True)

        df = filter_df(div_filter)
        df['label'] = df['field_name']+' ('+df['type']+')'

        st.markdown('<p class="section-title">Plucking Rounds — Month & Todate</p>',
                    unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(name='This Month', x=df['label'], y=df['rounds_m'],
                             marker_color='#2d8a45',
                             text=df['rounds_m'], textposition='auto'))
        fig.add_trace(go.Bar(name='Todate', x=df['label'], y=df['rounds_td'],
                             marker_color='#85c17e',
                             text=df['rounds_td'], textposition='auto'))
        fig.update_layout(barmode='group', xaxis_tickangle=-45, height=420,
                          plot_bgcolor='white', paper_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown('<p class="section-title">Days Since Last Weeding</p>',
                    unsafe_allow_html=True)
        df_w = df[df['weed_days']>0].sort_values('weed_days', ascending=False)
        if len(df_w)>0:
            fig2 = go.Figure(go.Bar(
                x=df_w['label'], y=df_w['weed_days'],
                marker_color=df_w['weed_days'].apply(
                    lambda x: '#e74c3c' if x>60 else '#27ae60').tolist(),
                text=df_w['weed_days'].astype(int), textposition='auto'
            ))
            fig2.add_hline(y=60, line_dash='dash', line_color='red',
                           annotation_text='60 days')
            fig2.update_layout(xaxis_tickangle=-45, height=400,
                               plot_bgcolor='white', paper_bgcolor='white')
            st.plotly_chart(fig2, use_container_width=True)

    # ── MADE TEA OUTTURN ─────────────────────────────────────
    elif page == "📊 Made Tea Outturn":
        st.markdown("""<div class="main-header">
            <h2 style="margin:0">📊 Made Tea Outturn Calculator</h2>
        </div>""", unsafe_allow_html=True)
        st.info("📌 Use when outturn from outside factories is not yet finalized.")

        st.markdown('<div class="approx-box">', unsafe_allow_html=True)
        st.markdown("### ⚠️ Quick Outturn Calculator")
        c1,c2,c3 = st.columns(3)
        gl = c1.number_input("Green Leaf (kg)", value=0.0, format="%.2f")
        ot = c2.number_input("Outturn %", value=21.50, format="%.2f")
        if gl>0:
            mt = (gl*ot)/100
            c3.metric("Estimated Made Tea", f"{mt:,.1f} kg")
        st.markdown('</div>', unsafe_allow_html=True)

        st.divider()
        st.markdown('<p class="section-title">Batch Calculator</p>',
                    unsafe_allow_html=True)
        n = int(st.number_input("Number of batches", min_value=1, max_value=10, value=3))
        batch=[]
        for i in range(n):
            c1,c2,c3 = st.columns(3)
            gl_b = c1.number_input(f"Batch {i+1} GL (kg)", value=0.0,
                                    key=f"gl{i}", format="%.2f")
            ot_b = c2.number_input("Outturn %", value=21.50,
                                    key=f"ot{i}", format="%.2f")
            mt_b = (gl_b*ot_b)/100
            c3.metric("Made Tea", f"{mt_b:,.1f} kg")
            batch.append({'Batch':i+1,'GL(kg)':gl_b,'Outturn%':ot_b,
                          'Made Tea(kg)':round(mt_b,2)})
        df_b = pd.DataFrame(batch)
        tgl=df_b['GL(kg)'].sum(); tmt=df_b['Made Tea(kg)'].sum()
        st.dataframe(df_b, use_container_width=True, hide_index=True)
        c1,c2,c3 = st.columns(3)
        c1.metric("Total GL",      f"{tgl:,.1f} kg")
        c2.metric("Total Made Tea",f"{tmt:,.1f} kg")
        c3.metric("Avg Outturn",   f"{(tmt/tgl*100):.2f}%" if tgl>0 else "0%")

    # ── DAILY PLUCKING ENTRY ─────────────────────────────────
    elif page == "📋 Daily Plucking Entry":
        st.markdown("""<div class="main-header">
            <h2 style="margin:0">📋 Daily Plucking Entry</h2>
        </div>""", unsafe_allow_html=True)

        df_fields = FIELDS[FIELDS['division']==div] if div else FIELDS
        field_opts = {
            f"{r['field_name']} ({r['type']}) {r['extent_ha']}ha": r['field_id']
            for _,r in df_fields.iterrows()
        }

        with st.form("pluck_form", clear_on_submit=True):
            c1,c2,c3 = st.columns(3)
            sel_field    = c1.selectbox("Field", list(field_opts.keys()))
            harvest_date = c2.date_input("Date")
            pluck_type   = c3.selectbox("Type", ["Checkroll","Shear","Cash"])
            round_no     = c1.number_input("Round No.", min_value=1, max_value=6, value=1)

            st.markdown('<p class="section-title">Registered Workers</p>',
                        unsafe_allow_html=True)
            c1,c2,c3 = st.columns(3)
            reg_pl  = c1.number_input("Reg. Pluckers", min_value=0, value=0)
            kang    = c2.number_input("Kanganies",      min_value=0, value=0)
            reg_gl  = c3.number_input("Reg. GL (kg)",   min_value=0.0, format="%.2f")

            st.markdown('<p class="section-title">Cash Workers</p>',
                        unsafe_allow_html=True)
            c1,c2,c3,c4 = st.columns(4)
            cash_pl = c1.number_input("Cash Pluckers",  min_value=0, value=0)
            sack    = c2.number_input("Sack Labourers", min_value=0, value=0)
            cash_gl = c3.number_input("Cash GL (kg)",   min_value=0.0, format="%.2f")
            rate    = c4.selectbox("Rate (Rs.)", [150.0, 75.0])

            total_gl     = reg_gl + cash_gl
            cash_mdays   = math.ceil((cash_gl*rate)/1550) if cash_gl>0 else 0
            total_pl     = reg_pl + cash_pl
            plk_avg      = round(total_gl/total_pl,2) if total_pl>0 else 0
            kg_sack      = round(total_gl/sack,2) if sack>0 else 0
            kg_kang      = round(total_gl/kang,2) if kang>0 else 0

            st.markdown('<p class="section-title">Auto Calculated</p>',
                        unsafe_allow_html=True)
            cc1,cc2,cc3,cc4,cc5 = st.columns(5)
            cc1.metric("Total GL",      f"{total_gl:,.1f} kg")
            cc2.metric("Cash Mandays",  f"{cash_mdays}")
            cc3.metric("Plucking Avg",  f"{plk_avg} kg")
            cc4.metric("Kg/Sack",       f"{kg_sack}")
            cc5.metric("Kg/Kangany",    f"{kg_kang}")

            notes = st.text_area("Notes", height=60)
            if st.form_submit_button("✅ Save Entry",
                                      use_container_width=True, type="primary"):
                st.session_state.pluck_log.append({
                    'Date': harvest_date, 'Field': sel_field,
                    'Type': pluck_type, 'Round': round_no,
                    'Total GL': total_gl, 'Cash Mandays': cash_mdays,
                    'Plk Avg': plk_avg, 'Entered By': user['name']
                })
                st.success(f"✅ Saved! GL: {total_gl} kg | Plk Avg: {plk_avg} kg")

        if st.session_state.pluck_log:
            st.markdown('<p class="section-title">Today\'s Entries</p>',
                        unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(st.session_state.pluck_log),
                         use_container_width=True, hide_index=True)

    # ── NITROGEN ENTRY ───────────────────────────────────────
    elif page == "🌱 Nitrogen Entry":
        st.markdown("""<div class="main-header">
            <h2 style="margin:0">🌱 Nitrogen Application Entry</h2>
        </div>""", unsafe_allow_html=True)

        df_fields = FIELDS[FIELDS['division']==div] if div else FIELDS
        field_opts = {
            f"{r['field_name']} ({r['type']})": (r['field_id'], r['type'])
            for _,r in df_fields.iterrows()
        }

        with st.form("nitro_form", clear_on_submit=True):
            c1,c2 = st.columns(2)
            sel_f = c1.selectbox("Field", list(field_opts.keys()))
            app_date = c2.date_input("Date")
            ftype = field_opts[sel_f][1]
            fert_opts = ['U901','U877'] if ftype=='VP' else ['U709','U877']
            c1,c2,c3 = st.columns(3)
            fert  = c1.selectbox("Fertilizer", fert_opts)
            n_qty = c2.selectbox("N Qty (kg)", [60, 80])
            custom= c3.number_input("Custom N Qty", min_value=0, value=0)
            final_n = custom if custom>0 else n_qty
            st.info(f"📌 **{final_n} kg** nitrogen | **{fert}** | Field type: **{ftype}**")
            notes = st.text_area("Notes", height=60)
            if st.form_submit_button("✅ Save",
                                      use_container_width=True, type="primary"):
                st.session_state.nitro_log.append({
                    'Date': app_date, 'Field': sel_f,
                    'Fertilizer': fert, 'N Qty': final_n,
                    'Entered By': user['name']
                })
                st.success(f"✅ Saved! {sel_f} | {fert} | {final_n} kg N")

        if st.session_state.nitro_log:
            st.markdown('<p class="section-title">Recent Entries</p>',
                        unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(st.session_state.nitro_log),
                         use_container_width=True, hide_index=True)

    # ── ACTIVITY ENTRY ───────────────────────────────────────
    elif page == "🔧 Activity Entry":
        st.markdown("""<div class="main-header">
            <h2 style="margin:0">🔧 Field Activity Entry</h2>
        </div>""", unsafe_allow_html=True)

        ACTS = ["Foliar Application","Blister Blight","Chemical Weeding",
                "Manual Weeding","Pruning","Ravines & Boundaries","Roads",
                "Dolomite Application","Bush Sanitation","Lungs Pruning",
                "Forking","Hydrated Lime","Draining","Soil Conservation",
                "Shade Lopping","Shade Planting","Composting"]

        df_fields = FIELDS[FIELDS['division']==div] if div else FIELDS
        field_opts = {f"{r['field_name']} ({r['type']})": r['field_id']
                      for _,r in df_fields.iterrows()}

        with st.form("act_form", clear_on_submit=True):
            c1,c2,c3 = st.columns(3)
            sel_f    = c1.selectbox("Field", list(field_opts.keys()))
            act_date = c2.date_input("Date")
            act_type = c3.selectbox("Activity", ACTS)
            c1,c2,c3 = st.columns(3)
            qty_kg   = c1.number_input("Qty (kg)", min_value=0.0, format="%.2f")
            mandays  = c2.number_input("Mandays",  min_value=0.0, format="%.1f")
            chem     = c3.text_input("Chemical Name")
            notes    = st.text_area("Notes", height=60)
            if st.form_submit_button("✅ Save",
                                      use_container_width=True, type="primary"):
                st.session_state.act_log.append({
                    'Date': act_date, 'Field': sel_f,
                    'Activity': act_type, 'Qty(kg)': qty_kg,
                    'Mandays': mandays, 'Chemical': chem,
                    'Entered By': user['name']
                })
                st.success(f"✅ Saved! {act_type} | {sel_f}")

        if st.session_state.act_log:
            st.markdown('<p class="section-title">Recent Activities</p>',
                        unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(st.session_state.act_log),
                         use_container_width=True, hide_index=True)

    st.divider()
    st.markdown(
        "<p style='text-align:center;color:#aaa;font-size:0.75rem'>"
        "DSPMS v1.0 | Uda Radella Estate | "
        "G.A.A.U.Dharmasena | BSc Data Science 2025</p>",
        unsafe_allow_html=True)
