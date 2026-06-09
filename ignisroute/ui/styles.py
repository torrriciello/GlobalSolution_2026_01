CUSTOM_CSS = """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

:root{
    --bg-primary:#020617;
    --bg-secondary:#0f172a;
    --bg-card:rgba(15,23,42,.75);

    --danger:#ef4444;
    --danger-soft:rgba(239,68,68,.15);

    --warning:#f59e0b;
    --warning-soft:rgba(245,158,11,.15);

    --success:#22c55e;
    --success-soft:rgba(34,197,94,.15);

    --info:#3b82f6;
    --info-soft:rgba(59,130,246,.15);

    --text:#f8fafc;
    --muted:#94a3b8;
}

html,
body,
[class*="css"]{
    font-family:'Inter',sans-serif;
}

/* ======================================================
   APP
====================================================== */

.stApp{
    background:
        radial-gradient(circle at top right,
            rgba(239,68,68,.12),
            transparent 30%),

        radial-gradient(circle at bottom left,
            rgba(59,130,246,.10),
            transparent 25%),

        linear-gradient(
            135deg,
            #020617 0%,
            #0f172a 40%,
            #111827 100%
        );
}

.block-container{
    max-width:1560px;
    padding-top:.75rem;
    padding-bottom:2rem;
}

/* ======================================================
   HERO
====================================================== */

.hero-banner{

    position:relative;

    background:
        linear-gradient(
            135deg,
            #ea580c 0%,
            #dc2626 50%,
            #991b1b 100%
        );

    border-radius:24px;

    padding:3rem;

    overflow:hidden;

    border:1px solid rgba(255,255,255,.12);

    box-shadow:
        0 30px 80px rgba(220,38,38,.35),
        inset 0 1px 0 rgba(255,255,255,.15);

    margin-bottom:2rem;
}

.hero-banner::before{

    content:"";

    position:absolute;

    top:-120px;
    right:-120px;

    width:300px;
    height:300px;

    border-radius:50%;

    background:rgba(255,255,255,.08);
}

.hero-banner h1{

    color:white !important;

    font-size:3rem !important;

    font-weight:900 !important;

    margin-bottom:.6rem !important;

    letter-spacing:-1px;
}

.hero-banner p{

    color:rgba(255,255,255,.92);

    font-size:1.1rem;

    max-width:800px;

    line-height:1.8;
}

/* ======================================================
   METRIC CARDS
====================================================== */

.metric-card{

    background:var(--bg-card);

    backdrop-filter:blur(18px);

    border:1px solid rgba(255,255,255,.08);

    border-radius:20px;

    padding:1.4rem;

    height:100%;

    transition:all .25s ease;

    box-shadow:
        0 10px 30px rgba(0,0,0,.35);
}

.metric-card:hover{

    transform:translateY(-5px);

    box-shadow:
        0 20px 40px rgba(0,0,0,.45);
}

.metric-card .label{

    color:var(--muted);

    text-transform:uppercase;

    letter-spacing:1.5px;

    font-size:.75rem;

    font-weight:700;

    margin-bottom:.7rem;
}

.metric-card .value{

    font-size:2rem;

    font-weight:800;
}

.status-livre{
    color:var(--success);
}

.status-interditada{
    color:var(--danger);
}

.status-info{
    color:var(--info);
}

.status-warn{
    color:var(--warning);
}

/* ======================================================
   SECTION TITLE
====================================================== */

.section-title{

    color:white !important;

    font-size:1.3rem !important;

    font-weight:800 !important;

    margin-top:2rem !important;

    margin-bottom:1rem !important;

    padding-bottom:.8rem;

    border-bottom:1px solid rgba(255,255,255,.08);
}

.section-title--inline{
    margin-top:1.5rem !important;
    margin-bottom:0 !important;
    padding-bottom:0 !important;
    border-bottom:none !important;
}

.soc-section-head{
    display:flex;
    align-items:flex-end;
    justify-content:space-between;
    gap:1rem;
    margin-bottom:1rem;
    padding-bottom:.75rem;
    border-bottom:1px solid rgba(255,255,255,.08);
}

.soc-section-head__hint{
    color:var(--muted);
    font-size:.75rem;
    font-weight:500;
    white-space:nowrap;
}

.soc-chart-panel{
    background:var(--bg-card);
    border:1px solid rgba(255,255,255,.07);
    border-radius:16px;
    padding:1rem 1.1rem 0.5rem;
    backdrop-filter:blur(14px);
}

.soc-route-summary--highlight{
    background:rgba(59,130,246,.08);
    border:1px solid rgba(59,130,246,.18);
    border-radius:14px;
    padding:.85rem 1rem;
    margin-bottom:1rem;
}

/* ======================================================
   ALERTAS
====================================================== */

.alert-box{

    padding:1rem 1.25rem;

    border-radius:14px;

    margin:1rem 0;

    font-size:.95rem;

    line-height:1.6;
}

.alert-success{

    background:var(--success-soft);

    border:1px solid rgba(34,197,94,.25);

    color:#bbf7d0;
}

.alert-warning{

    background:var(--warning-soft);

    border:1px solid rgba(245,158,11,.25);

    color:#fde68a;
}

.alert-danger{

    background:var(--danger-soft);

    border:1px solid rgba(239,68,68,.25);

    color:#fecaca;
}

.alert-info{

    background:var(--info-soft);

    border:1px solid rgba(59,130,246,.25);

    color:#bfdbfe;
}

/* ======================================================
   MAPA
====================================================== */

/* Iframe do Folium */

iframe[title="streamlit_folium.st_folium"] {
    border-radius: 24px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.45) !important;
    overflow: hidden !important;
    margin-top: 1rem !important;
}

div[data-testid="stElementContainer"]:has(iframe[title="streamlit_folium.st_folium"]) {
    border-radius: 24px !important;
    overflow: hidden !important;
}

.map-container{
    background:rgba(15,23,42,.75);
    border:1px solid rgba(255,255,255,.08);
    border-radius:24px;
    padding:16px;
    overflow:hidden;

    box-shadow:
        0 20px 60px rgba(0,0,0,.45);
}

.map-container--hero{
    border:1px solid rgba(52,211,153,.18);
    box-shadow:
        0 24px 70px rgba(0,0,0,.5),
        0 0 0 1px rgba(52,211,153,.08),
        inset 0 1px 0 rgba(255,255,255,.04);
}

/* ======================================================
   HOTSPOTS
====================================================== */

.hotspot-item{

    background:rgba(15,23,42,.7);

    border-left:4px solid #f97316;

    border-radius:10px;

    padding:1rem;

    margin-bottom:.8rem;

    color:#cbd5e1;

    transition:.2s;
}

.hotspot-item:hover{

    background:rgba(30,41,59,.85);
}

.hotspot-item strong{

    color:white;
}

/* ======================================================
   SIDEBAR
====================================================== */

[data-testid="stSidebar"]{

    background:
        linear-gradient(
            180deg,
            #111827 0%,
            #020617 100%
        );

    border-right:
        1px solid rgba(255,255,255,.08);
}

[data-testid="stSidebar"] *{

    color:#f8fafc;
}

/* ======================================================
   BUTTONS
====================================================== */

.stDownloadButton button{

    width:100%;

    border-radius:14px !important;

    font-weight:700 !important;

    background:
        linear-gradient(
            135deg,
            #ea580c,
            #dc2626
        ) !important;

    color:white !important;

    border:none !important;

    transition:.2s;
}

.stDownloadButton button:hover{

    transform:translateY(-2px);

    box-shadow:
        0 10px 30px rgba(220,38,38,.35);
}

/* ======================================================
   EXPANDER
====================================================== */

.streamlit-expanderHeader{

    font-weight:700;
}

/* ======================================================
   SCROLLBAR
====================================================== */

::-webkit-scrollbar{
    width:10px;
}

::-webkit-scrollbar-track{
    background:#0f172a;
}

::-webkit-scrollbar-thumb{

    background:#334155;

    border-radius:8px;
}

::-webkit-scrollbar-thumb:hover{

    background:#475569;
}

/* ======================================================
   STREAMLIT
====================================================== */

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}

/* ======================================================
   SOC TOP BAR
====================================================== */

.soc-topbar{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:1rem;
    background:rgba(15,23,42,.85);
    backdrop-filter:blur(20px);
    border:1px solid rgba(255,255,255,.08);
    border-radius:16px;
    padding:.9rem 1.4rem;
    margin-bottom:1.25rem;
    box-shadow:0 8px 32px rgba(0,0,0,.35);
}

.soc-topbar__brand{
    display:flex;
    align-items:center;
    gap:.75rem;
}

.soc-topbar__logo{
    font-size:1.8rem;
    filter:drop-shadow(0 0 8px rgba(239,68,68,.5));
}

.soc-topbar__title{
    color:#fff;
    font-weight:800;
    font-size:1.05rem;
    letter-spacing:.5px;
}

.soc-topbar__subtitle{
    color:var(--muted);
    font-size:.72rem;
    font-weight:500;
}

.soc-topbar__center{
    flex:1;
    text-align:center;
}

.soc-topbar__region{
    color:var(--muted);
    font-size:.85rem;
    font-weight:600;
}

.soc-topbar__status{
    display:flex;
    align-items:center;
    gap:.6rem;
    flex-wrap:wrap;
    justify-content:flex-end;
}

.soc-topbar__clock{
    color:var(--muted);
    font-size:.78rem;
    font-weight:600;
    font-variant-numeric:tabular-nums;
}

.soc-badge{
    font-size:.65rem;
    font-weight:700;
    letter-spacing:.8px;
    padding:.35rem .7rem;
    border-radius:999px;
    white-space:nowrap;
}

.soc-badge--online{
    background:rgba(34,197,94,.12);
    color:#4ade80;
    border:1px solid rgba(34,197,94,.3);
}

.soc-badge--offline{
    background:rgba(245,158,11,.12);
    color:#fbbf24;
    border:1px solid rgba(245,158,11,.3);
}

.soc-risk--baixo{background:rgba(34,197,94,.15);color:#86efac;border:1px solid rgba(34,197,94,.3);}
.soc-risk--moderado{background:rgba(59,130,246,.15);color:#93c5fd;border:1px solid rgba(59,130,246,.3);}
.soc-risk--alto{background:rgba(245,158,11,.15);color:#fde68a;border:1px solid rgba(245,158,11,.3);}
.soc-risk--crítico,.soc-risk--critico{
    background:rgba(239,68,68,.18);
    color:#fca5a5;
    border:1px solid rgba(239,68,68,.4);
    animation:soc-pulse-red 2s ease-in-out infinite;
}

@keyframes soc-pulse-green {
    0%, 100% { 
        box-shadow: 0 0 0 0 rgba(0, 255, 157, 0.3); 
    }
    50% { 
        box-shadow: 0 0 12px 2px rgba(0, 255, 157, 0.25); 
    }
}

@keyframes soc-pulse-red {
    0%, 100% { 
        box-shadow: 0 0 0 0 rgba(255, 77, 77, 0.3); 
    }
    50% { 
        box-shadow: 0 0 12px 2px rgba(255, 77, 77, 0.25); 
    }
}

/* ======================================================
   MISSION PANELS
====================================================== */

.soc-mission-grid{
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:1rem;
    margin-bottom:1.25rem;
}

@media(max-width:900px){
    .soc-mission-grid{grid-template-columns:1fr;}
}

.soc-panel{
    background:var(--bg-card);
    backdrop-filter:blur(18px);
    border:1px solid rgba(255,255,255,.08);
    border-radius:18px;
    padding:1.4rem 1.6rem;
    box-shadow:0 10px 30px rgba(0,0,0,.3);
}

.soc-panel__label{
    color:var(--muted);
    font-size:.68rem;
    font-weight:700;
    letter-spacing:1.8px;
    margin-bottom:.5rem;
}

.soc-panel__title{
    color:#fff;
    font-size:1.35rem;
    font-weight:800;
    margin-bottom:1rem;
}

.soc-mission-route{
    display:flex;
    align-items:center;
    gap:.5rem;
    margin-bottom:1rem;
}

.soc-mission-route__point{
    display:flex;
    align-items:flex-start;
    gap:.6rem;
    flex:1;
}

.soc-mission-route__line{
    width:40px;
    height:2px;
    background:linear-gradient(90deg,#22c55e,#ef4444);
    border-radius:2px;
    flex-shrink:0;
    margin-top:1rem;
}

.soc-dot{
    width:10px;
    height:10px;
    border-radius:50%;
    margin-top:.35rem;
    flex-shrink:0;
}

.soc-dot--origin{background:#22c55e;box-shadow:0 0 8px rgba(34,197,94,.6);}
.soc-dot--dest{background:#ef4444;box-shadow:0 0 8px rgba(239,68,68,.6);}

.soc-mission-route__label{
    color:var(--muted);
    font-size:.7rem;
    font-weight:600;
    text-transform:uppercase;
    letter-spacing:1px;
}

.soc-mission-route__value{
    color:#e2e8f0;
    font-size:.9rem;
    font-weight:600;
}

.soc-mission-meta{
    display:flex;
    flex-wrap:wrap;
    gap:.8rem;
    color:var(--muted);
    font-size:.78rem;
    font-weight:500;
    padding-top:.8rem;
    border-top:1px solid rgba(255,255,255,.06);
}

.soc-panel--decision{
    border-left:4px solid var(--info);
}

.soc-decision--prosseguir{border-left-color:var(--success)!important;}
.soc-decision--desviar{border-left-color:var(--warning)!important;}
.soc-decision--reavaliar,.soc-decision--aguardar{border-left-color:var(--danger)!important;}

.soc-decision-action{
    font-size:1.6rem;
    font-weight:900;
    color:#fff;
    letter-spacing:1px;
    margin-bottom:.4rem;
}

.soc-decision-title{
    color:#e2e8f0;
    font-size:1rem;
    font-weight:700;
    margin-bottom:.5rem;
}

.soc-decision-detail{
    color:var(--muted);
    font-size:.88rem;
    line-height:1.6;
}

/* ======================================================
   KPI DASHBOARD
====================================================== */

.soc-kpi{
    background:var(--bg-card);
    backdrop-filter:blur(14px);
    border:1px solid rgba(255,255,255,.07);
    border-radius:16px;
    padding:1rem 1.1rem;
    height:100%;
    transition:transform .2s,box-shadow .2s;
}

.soc-kpi:hover{
    transform:translateY(-3px);
    box-shadow:0 12px 28px rgba(0,0,0,.35);
}

.soc-kpi__label{
    color:var(--muted);
    font-size:.65rem;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:1.2px;
    margin-bottom:.4rem;
}

.soc-kpi__value{
    font-size:1.5rem;
    font-weight:800;
    line-height:1.2;
}

.soc-kpi__sub{
    color:#64748b;
    font-size:.7rem;
    margin-top:.35rem;
    font-weight:500;
}

.soc-kpi--compact{
    padding:.85rem 1rem;
}

.soc-kpi--compact .soc-kpi__value{
    font-size:1.25rem;
}

.soc-analytics-source{
    color:var(--muted);
    font-size:.8rem;
    margin-bottom:1rem;
    padding:.6rem .9rem;
    background:rgba(15,23,42,.5);
    border:1px solid rgba(255,255,255,.06);
    border-radius:10px;
}

.soc-analytics-source strong{
    color:var(--text);
}

/* ======================================================
   MAP & INTEL PANELS
====================================================== */

.soc-panel-header{
    display:flex;
    align-items:center;
    justify-content:space-between;
    margin-bottom:.75rem;
}

.soc-panel-header__title{
    color:#fff;
    font-weight:800;
    font-size:1.05rem;
}

.soc-panel-header--map{
    align-items:flex-end;
    margin-bottom:1rem;
}

.soc-panel-header__caption{
    display:block;
    color:var(--muted);
    font-size:.75rem;
    font-weight:500;
    margin-top:.2rem;
}

.soc-panel-header__badge--live{
    animation:soc-pulse-green 2s ease-in-out infinite;
}

.soc-route-preview{
    display:grid;
    gap:.45rem;
    background:rgba(15,23,42,.65);
    border:1px solid rgba(52,211,153,.15);
    border-radius:12px;
    padding:.75rem .85rem;
    margin-bottom:1rem;
    font-size:.78rem;
}

.soc-route-preview div{
    display:flex;
    justify-content:space-between;
    gap:.75rem;
    color:var(--muted);
}

.soc-route-preview strong{
    color:#34d399;
    font-weight:700;
}

.soc-panel-header__badge {
    font-size: .62rem;
    font-weight: 800;
    letter-spacing: 1px;
    /* Verde Neon para contraste em fundos escuros */
    color: #00FF9D; 
    background: rgba(0, 255, 157, 0.1);
    border: 1px solid rgba(0, 255, 157, 0.3);
    padding: .25rem .6rem;
    border-radius: 999px;
    display: inline-block;
    animation: soc-pulse-green 2s ease-in-out infinite;
}

.soc-intel-summary{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:.6rem;
    margin-bottom:1rem;
}

.soc-intel-stat{
    background:rgba(15,23,42,.8);
    border:1px solid rgba(255,255,255,.06);
    border-radius:12px;
    padding:.8rem;
    text-align:center;
}

.soc-intel-stat__val{
    color:#fff;
    font-size:1.4rem;
    font-weight:800;
}

.soc-intel-stat__lbl{
    color:var(--muted);
    font-size:.65rem;
    font-weight:600;
    text-transform:uppercase;
    letter-spacing:.8px;
    margin-top:.2rem;
}

.soc-intel-section{
    color:var(--muted);
    font-size:.72rem;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:1.2px;
    margin:1rem 0 .6rem;
}

.soc-route-summary{
    background:rgba(15,23,42,.6);
    border:1px solid rgba(255,255,255,.06);
    border-radius:12px;
    padding:.5rem 1rem;
}

.soc-route-summary div{
    display:flex;
    justify-content:space-between;
    padding:.45rem 0;
    border-bottom:1px solid rgba(255,255,255,.04);
    font-size:.82rem;
}

.soc-route-summary div:last-child{border-bottom:none;}
.soc-route-summary span{color:var(--muted);}
.soc-route-summary strong{color:#e2e8f0;}

.soc-intel-empty{
    color:#86efac;
    background:rgba(34,197,94,.08);
    border:1px solid rgba(34,197,94,.2);
    border-radius:10px;
    padding:1rem;
    font-size:.85rem;
    text-align:center;
}

.hotspot-item--critical{
    border-left-color:#ef4444!important;
    background:rgba(239,68,68,.06)!important;
}

.hotspot-item__header{
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:.5rem;
    margin-bottom:.4rem;
}

.hotspot-item__metrics{
    display:flex;
    gap:1rem;
    font-size:.78rem;
    color:var(--muted);
}

.soc-severity{
    font-size:.62rem;
    font-weight:700;
    padding:.2rem .5rem;
    border-radius:6px;
    letter-spacing:.5px;
    white-space:nowrap;
}

.soc-severity--critical{background:rgba(127,29,29,.35);color:#fecaca;border:1px solid rgba(239,68,68,.35);}
.soc-severity--high{background:rgba(239,68,68,.2);color:#fca5a5;}
.soc-severity--medium{background:rgba(245,158,11,.2);color:#fde68a;}
.soc-severity--low{background:rgba(34,197,94,.2);color:#86efac;}

.soc-export-meta{
    display:flex;
    flex-direction:column;
    gap:.3rem;
    margin-top:.6rem;
    color:#64748b;
    font-size:.72rem;
}

/* ======================================================
   SIDEBAR
====================================================== */

.soc-sidebar-header{
    display:flex;
    align-items:center;
    gap:.75rem;
    margin-bottom:1.5rem;
    padding-bottom:1rem;
    border-bottom:1px solid rgba(255,255,255,.08);
}

.soc-sidebar-header__icon{font-size:1.5rem;}

.soc-sidebar-header__title{
    color:#fff;
    font-weight:800;
    font-size:1rem;
}

.soc-sidebar-header__sub{
    color:var(--muted);
    font-size:.75rem;
}

.soc-sidebar-section{
    color:var(--muted);
    font-size:.7rem;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:1.2px;
    margin-bottom:.4rem;
}

.soc-radius-display{
    color:var(--muted);
    font-size:.82rem;
    margin-top:.3rem;
    margin-bottom:.5rem;
}

.soc-radius-display strong{color:#f97316;}

.soc-sidebar-db{
    font-size:.78rem;
    color:var(--muted);
    padding:.55rem .75rem;
    border-radius:10px;
    margin-bottom:1rem;
    border:1px solid rgba(255,255,255,.06);
}

.soc-sidebar-db strong{color:var(--text);}

.soc-sidebar-db--online{
    background:rgba(34,197,94,.08);
    border-color:rgba(34,197,94,.15);
}

.soc-sidebar-db--offline{
    background:rgba(245,158,11,.08);
    border-color:rgba(245,158,11,.15);
}

.soc-sidebar-help{
    background:rgba(15,23,42,.6);
    border:1px solid rgba(255,255,255,.06);
    border-radius:12px;
    padding:1rem;
    font-size:.8rem;
    color:var(--muted);
}

.soc-sidebar-help__title{
    color:#e2e8f0;
    font-weight:700;
    margin-bottom:.5rem;
    font-size:.85rem;
}

.soc-sidebar-help ol{
    margin:0;
    padding-left:1.2rem;
    line-height:1.8;
}

/* ======================================================
   LOADING OVERLAY
====================================================== */

@keyframes soc-spin{
    to{transform:rotate(360deg);}
}

@keyframes soc-bar{
    0%{transform:translateX(-100%);}
    100%{transform:translateX(250%);}
}

.soc-loader{
    position:relative;
    min-height:320px;
    display:flex;
    align-items:center;
    justify-content:center;
    margin:1rem 0 1.5rem;
    border-radius:20px;
    background:rgba(2,6,23,.55);
    border:1px solid rgba(52,211,153,.15);
    backdrop-filter:blur(10px);
}

.soc-loader__card{
    text-align:center;
    padding:2rem;
    max-width:420px;
}

.soc-loader__spinner{
    width:52px;height:52px;
    margin:0 auto 1.2rem;
    border:3px solid rgba(52,211,153,.15);
    border-top-color:#34d399;
    border-radius:50%;
    animation:soc-spin .9s linear infinite;
}

.soc-loader__title{
    color:#fff;
    font-weight:800;
    font-size:1.1rem;
    letter-spacing:.5px;
}

.soc-loader__step{
    color:#34d399;
    font-weight:700;
    font-size:.95rem;
    margin-top:.5rem;
}

.soc-loader__detail{
    color:var(--muted);
    font-size:.82rem;
    margin-top:.35rem;
    line-height:1.5;
}

.soc-loader__bar{
    height:4px;
    background:rgba(255,255,255,.08);
    border-radius:999px;
    overflow:hidden;
    margin:1rem auto .6rem;
    max-width:280px;
}

.soc-loader__bar-fill{
    width:40%;
    height:100%;
    background:linear-gradient(90deg,transparent,#34d399,transparent);
    animation:soc-bar 1.4s ease-in-out infinite;
}

.soc-loader__hint{
    color:#64748b;
    font-size:.72rem;
}

/* ======================================================
   MISSION STRIP
====================================================== */

.soc-mission-strip{
    display:grid;
    grid-template-columns:1.6fr 1.4fr auto;
    gap:1rem;
    align-items:center;
    background:var(--bg-card);
    border:1px solid rgba(255,255,255,.08);
    border-radius:16px;
    padding:.9rem 1.1rem;
    margin-bottom:1rem;
    backdrop-filter:blur(12px);
}

.soc-mission-strip__route{
    display:flex;
    align-items:center;
    gap:.5rem;
    flex-wrap:wrap;
    color:#e2e8f0;
    font-size:.85rem;
    font-weight:600;
}

.soc-mission-strip__arrow{color:#64748b;}

.soc-mission-strip__metrics{
    display:flex;
    flex-wrap:wrap;
    gap:.55rem 1rem;
    color:var(--muted);
    font-size:.75rem;
}

.soc-mission-strip__metrics b{color:#34d399;}

.soc-mission-strip__decision{
    text-align:right;
    padding:.55rem .85rem;
    border-radius:12px;
    border:1px solid rgba(255,255,255,.08);
}

.soc-mission-strip__decision-label{
    display:block;
    font-size:.62rem;
    letter-spacing:1px;
    color:var(--muted);
    font-weight:700;
    text-transform:uppercase;
}

.soc-mission-strip__decision-value{
    font-size:1rem;
    font-weight:800;
    color:#fff;
}

.soc-strip-decision--desviar{background:rgba(245,158,11,.12);border-color:rgba(245,158,11,.25);}
.soc-strip-decision--prosseguir{background:rgba(34,197,94,.1);border-color:rgba(34,197,94,.22);}
.soc-strip-decision--reavaliar{background:rgba(239,68,68,.12);border-color:rgba(239,68,68,.25);}

/* ======================================================
   MAP HERO
====================================================== */

.map-hero-head{
    display:flex;
    justify-content:space-between;
    align-items:flex-end;
    gap:1rem;
    margin:1.2rem 0 .85rem;
    flex-wrap:wrap;
}

.map-hero-head__title{
    color:#fff;
    font-size:1.35rem;
    font-weight:900;
    letter-spacing:-.3px;
}

.map-hero-head__sub{
    color:var(--muted);
    font-size:.82rem;
    margin-top:.2rem;
}

.map-hero-head__meta{
    display:flex;
    gap:.5rem;
    flex-wrap:wrap;
}

.map-hero-chip{
    font-size:.7rem;
    font-weight:700;
    padding:.35rem .7rem;
    border-radius:999px;
    border:1px solid rgba(255,255,255,.1);
}

.map-hero-chip--route{
    color:#34d399;
    background:rgba(52,211,153,.1);
    border-color:rgba(52,211,153,.2);
}

.map-hero-chip--safe{
    color:#86efac;
    background:rgba(34,197,94,.1);
}

.map-hero-chip--danger{
    color:#fca5a5;
    background:rgba(239,68,68,.12);
    border-color:rgba(239,68,68,.25);
}

.map-container--xl{
    min-height:820px;
}

/* ======================================================
   RISK NARRATIVE
====================================================== */

.soc-narrative-summary{
    border-radius:14px;
    padding:1rem 1.1rem;
    margin-bottom:1rem;
    border:1px solid rgba(255,255,255,.08);
}

.soc-narrative-summary--success{background:rgba(34,197,94,.08);border-color:rgba(34,197,94,.18);}
.soc-narrative-summary--warning{background:rgba(245,158,11,.08);border-color:rgba(245,158,11,.2);}
.soc-narrative-summary--danger{background:rgba(239,68,68,.1);border-color:rgba(239,68,68,.22);}

.soc-narrative-summary__status{
    font-weight:800;
    color:#fff;
    font-size:.95rem;
    margin-bottom:.35rem;
}

.soc-narrative-summary__text{
    color:var(--muted);
    font-size:.82rem;
    line-height:1.55;
}

.soc-rationale{
    background:rgba(15,23,42,.7);
    border:1px solid rgba(255,255,255,.07);
    border-radius:14px;
    padding:1rem;
    margin-bottom:1rem;
}

.soc-rationale__action{
    font-size:1.1rem;
    font-weight:900;
    color:#34d399;
}

.soc-rationale__title{
    color:#fff;
    font-weight:700;
    margin-top:.25rem;
}

.soc-rationale__detail{
    color:var(--muted);
    font-size:.82rem;
    margin-top:.4rem;
    line-height:1.55;
}

.soc-impact-card{
    background:rgba(15,23,42,.75);
    border:1px solid rgba(255,255,255,.07);
    border-left:4px solid #f59e0b;
    border-radius:12px;
    padding:.85rem 1rem;
    margin-bottom:.55rem;
}

.soc-impact-card--critical{border-left-color:#ef4444;background:rgba(127,29,29,.15);}
.soc-impact-card--high{border-left-color:#f97316;}
.soc-impact-card--medium{border-left-color:#f59e0b;}
.soc-impact-card--low{border-left-color:#22c55e;}

.soc-impact-card__head{
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:.5rem;
}

.soc-impact-card__detail{
    color:var(--muted);
    font-size:.8rem;
    margin-top:.35rem;
    line-height:1.5;
}

.soc-impact-card__meta{
    display:flex;
    gap:1rem;
    color:#64748b;
    font-size:.72rem;
    margin-top:.45rem;
}

/* ======================================================
   FOOTER
====================================================== */

.soc-footer{
    display:flex;
    justify-content:center;
    gap:2rem;
    flex-wrap:wrap;
    color:#475569;
    font-size:.75rem;
    font-weight:500;
    margin-top:2.5rem;
    padding-top:1.2rem;
    border-top:1px solid rgba(255,255,255,.06);
}

</style>
"""