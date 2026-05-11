import { useState, useRef, useEffect } from "react";

// ─── THEME & CONSTANTS ───────────────────────────────────────────────────────
const SKILLS_OPTIONS = [
  "Python","JavaScript","React","Node.js","TypeScript","Java","C++","C#","Go","Rust",
  "SQL","MongoDB","PostgreSQL","AWS","GCP","Azure","Docker","Kubernetes","Machine Learning",
  "Deep Learning","NLP","Computer Vision","Data Analysis","TensorFlow","PyTorch",
  "Django","FastAPI","Spring Boot","GraphQL","REST APIs","Git","CI/CD","Agile","Scrum",
];

const EXPERIENCE_LEVELS = ["Entry Level (0-2 yrs)", "Mid Level (2-5 yrs)", "Senior (5-10 yrs)", "Principal / Lead (10+ yrs)"];
const WORK_MODES = ["Remote", "Hybrid", "On-site"];
const INDUSTRIES = ["Tech / Software","Finance / FinTech","Healthcare","E-Commerce","Gaming","EdTech","AI / ML","Cybersecurity","Consulting","Startup"];

// ─── ICON COMPONENTS ─────────────────────────────────────────────────────────
const BriefcaseIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/><line x1="12" y1="12" x2="12" y2="12"/><line x1="12" y1="12" x2="12.01" y2="12"/></svg>
);
const StarIcon = ({ filled }) => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill={filled ? "currentColor" : "none"} stroke="currentColor" strokeWidth="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
);
const ChevronDown = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polyline points="6 9 12 15 18 9"/></svg>
);
const SparkleIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2l2.4 7.4H22l-6.2 4.5 2.4 7.4L12 17l-6.2 4.3 2.4-7.4L2 9.4h7.6z"/></svg>
);
const MapPin = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
);
const DollarSign = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
);

// ─── MAIN APP ─────────────────────────────────────────────────────────────────
export default function App() {
  const [step, setStep] = useState("form"); // form | loading | results
  const [profile, setProfile] = useState({
    name: "",
    title: "",
    experience: "",
    skills: [],
    workMode: "",
    industry: "",
    location: "",
    salaryMin: "",
    salaryMax: "",
    bio: "",
  });
  const [jobs, setJobs] = useState([]);
  const [error, setError] = useState("");
  const [expandedJob, setExpandedJob] = useState(null);
  const [loadingMsg, setLoadingMsg] = useState("Analyzing your profile…");
  const loadingMsgs = [
    "Analyzing your profile…",
    "Scanning thousands of job patterns…",
    "Matching your skill fingerprint…",
    "Ranking opportunities by fit score…",
    "Crafting personalized insights…",
  ];
  const loadingRef = useRef(null);

  useEffect(() => {
    if (step === "loading") {
      let i = 0;
      loadingRef.current = setInterval(() => {
        i = (i + 1) % loadingMsgs.length;
        setLoadingMsg(loadingMsgs[i]);
      }, 1800);
    } else {
      clearInterval(loadingRef.current);
    }
    return () => clearInterval(loadingRef.current);
  }, [step]);

  const toggleSkill = (skill) => {
    setProfile((p) => ({
      ...p,
      skills: p.skills.includes(skill) ? p.skills.filter((s) => s !== skill) : [...p.skills, skill],
    }));
  };

  const validate = () => {
    if (!profile.name.trim()) return "Please enter your name.";
    if (!profile.experience) return "Please select your experience level.";
    if (profile.skills.length < 2) return "Select at least 2 skills.";
    if (!profile.workMode) return "Select a preferred work mode.";
    return null;
  };

  const fetchJobs = async () => {
    const err = validate();
    if (err) { setError(err); return; }
    setError("");
    setStep("loading");

    const prompt = `You are an expert job recommendation AI. Based on the candidate profile below, generate exactly 6 highly tailored job recommendations.

CANDIDATE PROFILE:
- Name: ${profile.name}
- Current/Desired Title: ${profile.title || "Not specified"}
- Experience: ${profile.experience}
- Skills: ${profile.skills.join(", ")}
- Preferred Work Mode: ${profile.workMode}
- Industry Interest: ${profile.industry || "Open to all"}
- Location: ${profile.location || "Flexible"}
- Salary Range: ${profile.salaryMin && profile.salaryMax ? `$${profile.salaryMin}k - $${profile.salaryMax}k` : "Not specified"}
- About: ${profile.bio || "Not provided"}

Return ONLY a valid JSON array (no markdown, no explanation) with exactly 6 objects, each with these fields:
{
  "title": "Job Title",
  "company": "Company Name (realistic tech company)",
  "location": "City, Country or Remote",
  "workMode": "Remote|Hybrid|On-site",
  "salary": "$X0k - $Y0k",
  "matchScore": 85,
  "industry": "Industry",
  "tags": ["tag1","tag2","tag3"],
  "whyMatch": "2-3 sentence personalized explanation of why this role fits the candidate",
  "responsibilities": ["resp 1","resp 2","resp 3","resp 4"],
  "requirements": ["req 1","req 2","req 3"],
  "growth": "Short statement about growth potential",
  "urgent": true or false
}

Make match scores vary realistically between 72-98. Make companies and roles feel real and diverse.`;

    try {
      const res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 4000,
          messages: [{ role: "user", content: prompt }],
        }),
      });
      const data = await res.json();
      const text = data.content?.map((b) => b.text || "").join("") || "";
      const clean = text.replace(/```json|```/g, "").trim();
      const parsed = JSON.parse(clean);
      setJobs(parsed);
      setStep("results");
    } catch (e) {
      setError("Failed to get recommendations. Please try again.");
      setStep("form");
    }
  };

  // ── RENDER ──────────────────────────────────────────────────────────────────
  return (
    <div style={styles.root}>
      {/* Background mesh */}
      <div style={styles.bgMesh} />

      {/* Header */}
      <header style={styles.header}>
        <div style={styles.headerInner}>
          <div style={styles.logo}>
            <div style={styles.logoIcon}><BriefcaseIcon /></div>
            <span style={styles.logoText}>JobMatch<span style={styles.logoAI}>AI</span></span>
          </div>
          {step === "results" && (
            <button style={styles.backBtn} onClick={() => { setStep("form"); setJobs([]); }}>
              ← New Search
            </button>
          )}
        </div>
      </header>

      <main style={styles.main}>
        {/* ── FORM ── */}
        {step === "form" && (
          <div style={styles.formWrap}>
            <div style={styles.formHero}>
              <div style={styles.badge}><SparkleIcon /> AI-Powered Matching</div>
              <h1 style={styles.heroTitle}>Find Your <span style={styles.heroAccent}>Perfect Role</span></h1>
              <p style={styles.heroSub}>Tell us about yourself and our AI will surface the best-fit opportunities from thousands of roles.</p>
            </div>

            <div style={styles.card}>
              {/* Basic Info */}
              <SectionTitle>Your Profile</SectionTitle>
              <div style={styles.grid2}>
                <Field label="Full Name *" value={profile.name} onChange={(v) => setProfile(p => ({...p, name: v}))} placeholder="e.g. Priya Sharma" />
                <Field label="Current / Desired Title" value={profile.title} onChange={(v) => setProfile(p => ({...p, title: v}))} placeholder="e.g. Senior Backend Engineer" />
              </div>
              <div style={styles.grid2}>
                <Field label="Location" value={profile.location} onChange={(v) => setProfile(p => ({...p, location: v}))} placeholder="e.g. Mumbai, India" />
                <SelectField label="Experience Level *" value={profile.experience} onChange={(v) => setProfile(p => ({...p, experience: v}))} options={EXPERIENCE_LEVELS} />
              </div>

              {/* Skills */}
              <SectionTitle>Skills *</SectionTitle>
              <p style={styles.hint}>Select at least 2 skills that represent you best</p>
              <div style={styles.skillsGrid}>
                {SKILLS_OPTIONS.map((s) => (
                  <button key={s} style={{...styles.skillChip, ...(profile.skills.includes(s) ? styles.skillChipActive : {})}} onClick={() => toggleSkill(s)}>
                    {s}
                  </button>
                ))}
              </div>

              {/* Preferences */}
              <SectionTitle>Preferences</SectionTitle>
              <div style={styles.grid3}>
                <SelectField label="Work Mode *" value={profile.workMode} onChange={(v) => setProfile(p => ({...p, workMode: v}))} options={WORK_MODES} />
                <SelectField label="Industry" value={profile.industry} onChange={(v) => setProfile(p => ({...p, industry: v}))} options={INDUSTRIES} />
                <div style={styles.fieldWrap}>
                  <label style={styles.label}>Salary Range (USD k)</label>
                  <div style={{display:"flex",gap:"8px",alignItems:"center"}}>
                    <input style={{...styles.input, flex:1}} type="number" placeholder="Min" value={profile.salaryMin} onChange={e => setProfile(p=>({...p,salaryMin:e.target.value}))} />
                    <span style={{color:"#94a3b8"}}>–</span>
                    <input style={{...styles.input, flex:1}} type="number" placeholder="Max" value={profile.salaryMax} onChange={e => setProfile(p=>({...p,salaryMax:e.target.value}))} />
                  </div>
                </div>
              </div>

              <div style={styles.fieldWrap}>
                <label style={styles.label}>Brief Bio / Career Goals</label>
                <textarea style={styles.textarea} rows={3} placeholder="Tell us what you're looking for in your next role, your proudest achievement, or your career vision…" value={profile.bio} onChange={e => setProfile(p=>({...p,bio:e.target.value}))} />
              </div>

              {error && <div style={styles.errorBox}>{error}</div>}

              <button style={styles.submitBtn} onClick={fetchJobs}>
                <SparkleIcon /> Get AI Job Recommendations
              </button>
            </div>
          </div>
        )}

        {/* ── LOADING ── */}
        {step === "loading" && (
          <div style={styles.loadingWrap}>
            <div style={styles.loadingCard}>
              <div style={styles.spinner}>
                <div style={styles.spinnerRing} />
                <div style={{...styles.spinnerRing, ...styles.spinnerRing2}} />
                <div style={styles.spinnerDot} />
              </div>
              <h2 style={styles.loadingTitle}>Finding Your Matches</h2>
              <p style={styles.loadingMsg}>{loadingMsg}</p>
              <div style={styles.loadingSteps}>
                {loadingMsgs.slice(0,4).map((m,i) => (
                  <div key={i} style={{...styles.loadingStep, opacity: loadingMsgs.indexOf(loadingMsg) >= i ? 1 : 0.3}}>
                    <div style={{...styles.loadingDot, background: loadingMsgs.indexOf(loadingMsg) >= i ? "#6366f1" : "#334155"}} />
                    <span>{m}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* ── RESULTS ── */}
        {step === "results" && (
          <div style={styles.resultsWrap}>
            <div style={styles.resultsHeader}>
              <div>
                <h1 style={styles.resultsTitle}>Your Top Matches, <span style={styles.heroAccent}>{profile.name.split(" ")[0]}</span></h1>
                <p style={styles.resultsSub}>AI found {jobs.length} roles tailored to your profile · Ranked by compatibility</p>
              </div>
              <div style={styles.profilePill}>
                <strong>{profile.skills.length}</strong> skills · <strong>{profile.experience.split("(")[0].trim()}</strong> · <strong>{profile.workMode}</strong>
              </div>
            </div>

            <div style={styles.jobsGrid}>
              {jobs.map((job, i) => (
                <JobCard key={i} job={job} rank={i+1} expanded={expandedJob === i} onToggle={() => setExpandedJob(expandedJob === i ? null : i)} />
              ))}
            </div>
          </div>
        )}
      </main>

      <footer style={styles.footer}>
        <p>JobMatch AI · Powered by Claude · Recommendations are AI-generated for demonstration purposes</p>
      </footer>
    </div>
  );
}

// ─── JOB CARD ──────────────────────────────────────────────────────────────────
function JobCard({ job, rank, expanded, onToggle }) {
  const score = job.matchScore || 80;
  const scoreColor = score >= 90 ? "#10b981" : score >= 80 ? "#6366f1" : "#f59e0b";

  return (
    <div style={{...styles.jobCard, ...(rank === 1 ? styles.jobCardTop : {}), ...(expanded ? styles.jobCardExpanded : {})}}>
      {rank === 1 && <div style={styles.topBadge}>🏆 Best Match</div>}
      {job.urgent && <div style={styles.urgentBadge}>🔥 Urgently Hiring</div>}

      <div style={styles.jobHeader} onClick={onToggle}>
        <div style={styles.jobLeft}>
          <div style={styles.companyLogo}>{job.company?.[0] || "?"}</div>
          <div>
            <h3 style={styles.jobTitle}>{job.title}</h3>
            <p style={styles.jobCompany}>{job.company}</p>
            <div style={styles.jobMeta}>
              <span style={styles.metaTag}><MapPin /> {job.location}</span>
              <span style={styles.metaTag}>{job.workMode}</span>
              <span style={styles.metaTag}><DollarSign /> {job.salary}</span>
            </div>
          </div>
        </div>
        <div style={styles.jobRight}>
          <div style={styles.scoreWrap}>
            <svg width="56" height="56" viewBox="0 0 56 56">
              <circle cx="28" cy="28" r="24" fill="none" stroke="#1e293b" strokeWidth="4"/>
              <circle cx="28" cy="28" r="24" fill="none" stroke={scoreColor} strokeWidth="4"
                strokeDasharray={`${(score/100)*150.8} 150.8`} strokeLinecap="round"
                transform="rotate(-90 28 28)" style={{transition:"stroke-dasharray 1s ease"}}/>
            </svg>
            <div style={styles.scoreInner}>
              <span style={{...styles.scoreNum, color: scoreColor}}>{score}</span>
              <span style={styles.scoreLabel}>%</span>
            </div>
          </div>
          <div style={styles.stars}>
            {[1,2,3,4,5].map(s => (
              <span key={s} style={{color: s <= Math.round(score/20) ? "#f59e0b" : "#334155"}}>
                <StarIcon filled={s <= Math.round(score/20)} />
              </span>
            ))}
          </div>
          <div style={{...styles.expandArrow, transform: expanded ? "rotate(180deg)" : "rotate(0deg)"}}>
            <ChevronDown />
          </div>
        </div>
      </div>

      <div style={styles.tagRow}>
        {(job.tags || []).map((t, i) => <span key={i} style={styles.tag}>{t}</span>)}
      </div>

      <div style={styles.whyMatch}>
        <span style={styles.whyIcon}>💡</span>
        <p style={styles.whyText}>{job.whyMatch}</p>
      </div>

      {expanded && (
        <div style={styles.expandedContent}>
          <div style={styles.expandGrid}>
            <div>
              <h4 style={styles.expandTitle}>📋 Responsibilities</h4>
              <ul style={styles.expandList}>
                {(job.responsibilities || []).map((r, i) => <li key={i} style={styles.expandItem}>{r}</li>)}
              </ul>
            </div>
            <div>
              <h4 style={styles.expandTitle}>✅ Requirements</h4>
              <ul style={styles.expandList}>
                {(job.requirements || []).map((r, i) => <li key={i} style={styles.expandItem}>{r}</li>)}
              </ul>
            </div>
          </div>
          {job.growth && (
            <div style={styles.growthBox}>
              <span style={styles.growthIcon}>📈</span>
              <p style={styles.growthText}><strong>Growth:</strong> {job.growth}</p>
            </div>
          )}
          <div style={styles.applyRow}>
            <button style={styles.applyBtn}>Apply Now</button>
            <button style={styles.saveBtn}>♡ Save</button>
          </div>
        </div>
      )}
    </div>
  );
}

// ─── FORM HELPERS ──────────────────────────────────────────────────────────────
function SectionTitle({ children }) {
  return <h2 style={styles.sectionTitle}>{children}</h2>;
}
function Field({ label, value, onChange, placeholder }) {
  return (
    <div style={styles.fieldWrap}>
      <label style={styles.label}>{label}</label>
      <input style={styles.input} value={value} onChange={e => onChange(e.target.value)} placeholder={placeholder} />
    </div>
  );
}
function SelectField({ label, value, onChange, options }) {
  return (
    <div style={styles.fieldWrap}>
      <label style={styles.label}>{label}</label>
      <div style={styles.selectWrap}>
        <select style={styles.select} value={value} onChange={e => onChange(e.target.value)}>
          <option value="">Select…</option>
          {options.map(o => <option key={o} value={o}>{o}</option>)}
        </select>
        <div style={styles.selectArrow}><ChevronDown /></div>
      </div>
    </div>
  );
}

// ─── STYLES ───────────────────────────────────────────────────────────────────
const styles = {
  root: { minHeight: "100vh", background: "#080f1a", color: "#e2e8f0", fontFamily: "'DM Sans', 'Segoe UI', sans-serif", position: "relative", overflowX: "hidden" },
  bgMesh: { position: "fixed", inset: 0, background: "radial-gradient(ellipse 80% 50% at 20% -10%, rgba(99,102,241,0.15) 0%, transparent 60%), radial-gradient(ellipse 60% 50% at 80% 110%, rgba(16,185,129,0.1) 0%, transparent 60%)", pointerEvents: "none", zIndex: 0 },
  header: { position: "sticky", top: 0, zIndex: 100, background: "rgba(8,15,26,0.85)", backdropFilter: "blur(16px)", borderBottom: "1px solid rgba(99,102,241,0.15)" },
  headerInner: { maxWidth: "1100px", margin: "0 auto", padding: "14px 24px", display: "flex", alignItems: "center", justifyContent: "space-between" },
  logo: { display: "flex", alignItems: "center", gap: "10px" },
  logoIcon: { width: "36px", height: "36px", borderRadius: "10px", background: "linear-gradient(135deg,#6366f1,#8b5cf6)", display: "flex", alignItems: "center", justifyContent: "center", color: "#fff" },
  logoText: { fontSize: "20px", fontWeight: "800", letterSpacing: "-0.5px", color: "#f1f5f9" },
  logoAI: { color: "#6366f1", marginLeft: "2px" },
  backBtn: { background: "rgba(99,102,241,0.15)", border: "1px solid rgba(99,102,241,0.3)", color: "#a5b4fc", padding: "8px 18px", borderRadius: "8px", cursor: "pointer", fontSize: "14px", fontWeight: "600" },
  main: { maxWidth: "1100px", margin: "0 auto", padding: "40px 24px 60px", position: "relative", zIndex: 1 },

  // Form
  formWrap: { maxWidth: "820px", margin: "0 auto" },
  formHero: { textAlign: "center", marginBottom: "40px" },
  badge: { display: "inline-flex", alignItems: "center", gap: "6px", background: "rgba(99,102,241,0.12)", border: "1px solid rgba(99,102,241,0.3)", color: "#a5b4fc", padding: "6px 14px", borderRadius: "100px", fontSize: "13px", fontWeight: "600", marginBottom: "20px" },
  heroTitle: { fontSize: "clamp(32px,5vw,52px)", fontWeight: "900", letterSpacing: "-1.5px", color: "#f1f5f9", margin: "0 0 16px", lineHeight: 1.1 },
  heroAccent: { background: "linear-gradient(135deg,#6366f1,#8b5cf6,#ec4899)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent" },
  heroSub: { color: "#94a3b8", fontSize: "17px", maxWidth: "500px", margin: "0 auto", lineHeight: 1.6 },
  card: { background: "rgba(15,23,42,0.8)", border: "1px solid rgba(99,102,241,0.15)", borderRadius: "20px", padding: "36px", backdropFilter: "blur(8px)" },
  sectionTitle: { fontSize: "13px", fontWeight: "700", textTransform: "uppercase", letterSpacing: "1.5px", color: "#6366f1", margin: "28px 0 16px", paddingBottom: "10px", borderBottom: "1px solid rgba(99,102,241,0.1)" },
  grid2: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", marginBottom: "16px" },
  grid3: { display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "16px", marginBottom: "16px" },
  fieldWrap: { display: "flex", flexDirection: "column", gap: "8px", marginBottom: "16px" },
  label: { fontSize: "13px", fontWeight: "600", color: "#94a3b8", letterSpacing: "0.3px" },
  input: { background: "rgba(30,41,59,0.8)", border: "1px solid rgba(99,102,241,0.2)", borderRadius: "10px", padding: "11px 14px", color: "#e2e8f0", fontSize: "14px", outline: "none", width: "100%", boxSizing: "border-box" },
  textarea: { background: "rgba(30,41,59,0.8)", border: "1px solid rgba(99,102,241,0.2)", borderRadius: "10px", padding: "11px 14px", color: "#e2e8f0", fontSize: "14px", outline: "none", resize: "vertical", fontFamily: "inherit", width: "100%", boxSizing: "border-box" },
  selectWrap: { position: "relative" },
  select: { width: "100%", background: "rgba(30,41,59,0.8)", border: "1px solid rgba(99,102,241,0.2)", borderRadius: "10px", padding: "11px 40px 11px 14px", color: "#e2e8f0", fontSize: "14px", outline: "none", appearance: "none" },
  selectArrow: { position: "absolute", right: "12px", top: "50%", transform: "translateY(-50%)", pointerEvents: "none", color: "#94a3b8" },
  hint: { fontSize: "13px", color: "#64748b", marginBottom: "12px", marginTop: "-8px" },
  skillsGrid: { display: "flex", flexWrap: "wrap", gap: "8px", marginBottom: "8px" },
  skillChip: { background: "rgba(30,41,59,0.6)", border: "1px solid rgba(99,102,241,0.2)", color: "#94a3b8", padding: "6px 14px", borderRadius: "100px", fontSize: "13px", fontWeight: "500", cursor: "pointer", transition: "all 0.15s" },
  skillChipActive: { background: "rgba(99,102,241,0.2)", border: "1px solid #6366f1", color: "#a5b4fc" },
  errorBox: { background: "rgba(239,68,68,0.12)", border: "1px solid rgba(239,68,68,0.3)", color: "#fca5a5", borderRadius: "10px", padding: "12px 16px", fontSize: "14px", marginBottom: "16px" },
  submitBtn: { width: "100%", background: "linear-gradient(135deg,#6366f1,#8b5cf6)", border: "none", color: "#fff", padding: "16px", borderRadius: "12px", fontSize: "16px", fontWeight: "700", cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center", gap: "10px", letterSpacing: "0.3px", marginTop: "8px" },

  // Loading
  loadingWrap: { display: "flex", alignItems: "center", justifyContent: "center", minHeight: "60vh" },
  loadingCard: { background: "rgba(15,23,42,0.9)", border: "1px solid rgba(99,102,241,0.2)", borderRadius: "24px", padding: "56px 48px", textAlign: "center", maxWidth: "440px", width: "100%", backdropFilter: "blur(16px)" },
  spinner: { position: "relative", width: "72px", height: "72px", margin: "0 auto 32px" },
  spinnerRing: { position: "absolute", inset: 0, borderRadius: "50%", border: "3px solid transparent", borderTopColor: "#6366f1", animation: "spin 1s linear infinite" },
  spinnerRing2: { inset: "8px", borderTopColor: "#8b5cf6", animationDuration: "0.75s", animationDirection: "reverse" },
  spinnerDot: { position: "absolute", inset: "22px", borderRadius: "50%", background: "linear-gradient(135deg,#6366f1,#8b5cf6)" },
  loadingTitle: { fontSize: "24px", fontWeight: "800", color: "#f1f5f9", marginBottom: "8px" },
  loadingMsg: { color: "#6366f1", fontSize: "15px", fontWeight: "500", marginBottom: "32px", minHeight: "24px" },
  loadingSteps: { display: "flex", flexDirection: "column", gap: "10px", textAlign: "left" },
  loadingStep: { display: "flex", alignItems: "center", gap: "10px", fontSize: "13px", color: "#94a3b8", transition: "opacity 0.3s" },
  loadingDot: { width: "8px", height: "8px", borderRadius: "50%", flexShrink: 0, transition: "background 0.3s" },

  // Results
  resultsWrap: {},
  resultsHeader: { display: "flex", alignItems: "flex-start", justifyContent: "space-between", flexWrap: "wrap", gap: "20px", marginBottom: "36px" },
  resultsTitle: { fontSize: "clamp(28px,4vw,42px)", fontWeight: "900", letterSpacing: "-1px", color: "#f1f5f9", margin: "0 0 8px" },
  resultsSub: { color: "#64748b", fontSize: "15px" },
  profilePill: { background: "rgba(99,102,241,0.1)", border: "1px solid rgba(99,102,241,0.25)", color: "#a5b4fc", padding: "10px 18px", borderRadius: "100px", fontSize: "13px", whiteSpace: "nowrap" },
  jobsGrid: { display: "grid", gap: "20px" },

  // Job Card
  jobCard: { background: "rgba(15,23,42,0.85)", border: "1px solid rgba(99,102,241,0.12)", borderRadius: "18px", padding: "28px", backdropFilter: "blur(8px)", position: "relative", transition: "border-color 0.2s, box-shadow 0.2s", cursor: "default" },
  jobCardTop: { border: "1px solid rgba(99,102,241,0.35)", boxShadow: "0 0 40px rgba(99,102,241,0.08)" },
  jobCardExpanded: { borderColor: "rgba(99,102,241,0.3)" },
  topBadge: { position: "absolute", top: "-12px", left: "24px", background: "linear-gradient(135deg,#f59e0b,#f97316)", color: "#000", fontSize: "11px", fontWeight: "800", padding: "4px 12px", borderRadius: "100px", letterSpacing: "0.5px" },
  urgentBadge: { position: "absolute", top: "-12px", right: "24px", background: "rgba(239,68,68,0.15)", border: "1px solid rgba(239,68,68,0.4)", color: "#fca5a5", fontSize: "11px", fontWeight: "700", padding: "4px 12px", borderRadius: "100px" },
  jobHeader: { display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: "16px", cursor: "pointer", userSelect: "none" },
  jobLeft: { display: "flex", gap: "16px", flex: 1, minWidth: 0 },
  companyLogo: { width: "48px", height: "48px", borderRadius: "12px", background: "linear-gradient(135deg,rgba(99,102,241,0.3),rgba(139,92,246,0.3))", border: "1px solid rgba(99,102,241,0.2)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "20px", fontWeight: "800", color: "#a5b4fc", flexShrink: 0 },
  jobTitle: { fontSize: "18px", fontWeight: "700", color: "#f1f5f9", margin: "0 0 4px", letterSpacing: "-0.3px" },
  jobCompany: { fontSize: "14px", color: "#6366f1", fontWeight: "600", margin: "0 0 10px" },
  jobMeta: { display: "flex", flexWrap: "wrap", gap: "8px" },
  metaTag: { display: "inline-flex", alignItems: "center", gap: "4px", fontSize: "12px", color: "#64748b", background: "rgba(30,41,59,0.6)", padding: "3px 10px", borderRadius: "6px" },
  jobRight: { display: "flex", flexDirection: "column", alignItems: "center", gap: "6px", flexShrink: 0 },
  scoreWrap: { position: "relative", width: "56px", height: "56px" },
  scoreInner: { position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center" },
  scoreNum: { fontSize: "13px", fontWeight: "800" },
  scoreLabel: { fontSize: "9px", color: "#64748b" },
  stars: { display: "flex", gap: "2px" },
  expandArrow: { color: "#64748b", transition: "transform 0.2s" },
  tagRow: { display: "flex", flexWrap: "wrap", gap: "6px", margin: "14px 0" },
  tag: { background: "rgba(99,102,241,0.1)", border: "1px solid rgba(99,102,241,0.2)", color: "#818cf8", fontSize: "11px", fontWeight: "600", padding: "3px 10px", borderRadius: "100px" },
  whyMatch: { display: "flex", gap: "10px", background: "rgba(16,185,129,0.05)", border: "1px solid rgba(16,185,129,0.12)", borderRadius: "10px", padding: "12px 14px" },
  whyIcon: { fontSize: "16px", flexShrink: 0, lineHeight: 1.5 },
  whyText: { fontSize: "13px", color: "#94a3b8", lineHeight: 1.6, margin: 0 },
  expandedContent: { marginTop: "20px", borderTop: "1px solid rgba(99,102,241,0.1)", paddingTop: "20px" },
  expandGrid: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: "24px", marginBottom: "16px" },
  expandTitle: { fontSize: "13px", fontWeight: "700", color: "#94a3b8", marginBottom: "10px", textTransform: "uppercase", letterSpacing: "0.8px" },
  expandList: { paddingLeft: "18px", margin: 0 },
  expandItem: { fontSize: "13px", color: "#64748b", lineHeight: 1.7 },
  growthBox: { display: "flex", gap: "10px", background: "rgba(99,102,241,0.06)", borderRadius: "10px", padding: "12px 14px", marginBottom: "16px" },
  growthIcon: { fontSize: "16px", flexShrink: 0 },
  growthText: { fontSize: "13px", color: "#94a3b8", margin: 0 },
  applyRow: { display: "flex", gap: "12px" },
  applyBtn: { background: "linear-gradient(135deg,#6366f1,#8b5cf6)", border: "none", color: "#fff", padding: "10px 28px", borderRadius: "10px", fontSize: "14px", fontWeight: "700", cursor: "pointer", flex: 1 },
  saveBtn: { background: "rgba(30,41,59,0.8)", border: "1px solid rgba(99,102,241,0.2)", color: "#94a3b8", padding: "10px 20px", borderRadius: "10px", fontSize: "14px", fontWeight: "600", cursor: "pointer" },

  footer: { textAlign: "center", padding: "24px", color: "#334155", fontSize: "12px", position: "relative", zIndex: 1 },
};
