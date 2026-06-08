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
    max-width:1400px;
    padding-top:1rem;
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

.map-container{

    border-radius:24px;

    overflow:hidden;

    border:1px solid rgba(255,255,255,.08);

    box-shadow:
        0 20px 60px rgba(0,0,0,.45);

    margin-top:1rem;
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