import { useMemo, useState } from 'react'
import {
  ArrowUpRight, Bell, BookOpen, CheckCircle2, ChevronDown, CircleHelp, Download,
  FileText, GraduationCap, LayoutDashboard, LogOut, Menu, Search, ShieldCheck,
  Sparkles, UserRound, X,
} from 'lucide-react'
import { demoResults, demoSessions, demoStudent, loadResults, login } from './api'

const navItems = [
  { label: 'Overview', icon: LayoutDashboard },
  { label: 'My results', icon: BookOpen },
  { label: 'Transcript request', icon: FileText },
]

function App() {
  const [student, setStudent] = useState(null)
  const [activeView, setActiveView] = useState('Overview')
  const [mobileOpen, setMobileOpen] = useState(false)
  const [results, setResults] = useState(demoResults)

  const signIn = async (email, password) => {
    try {
      const profile = await login(email, password)
      setStudent(profile)
      setResults(await loadResults())
    } catch {
      setStudent(demoStudent)
      setResults(demoResults)
    }
  }

  if (!student) return <Login onSignIn={signIn} />

  return (
    <div className="app-shell">
      <Sidebar activeView={activeView} setActiveView={setActiveView} open={mobileOpen} onClose={() => setMobileOpen(false)} onLogout={() => setStudent(null)} />
      <main className="main-content">
        <header className="topbar">
          <button className="icon-button mobile-menu" onClick={() => setMobileOpen(true)} aria-label="Open navigation"><Menu size={20} /></button>
          <div className="breadcrumbs"><span>Student portal</span><span className="crumb-divider">/</span><strong>{activeView}</strong></div>
          <div className="topbar-actions">
            <button className="icon-button" aria-label="View notifications"><Bell size={19} /><span className="notification-dot" /></button>
            <div className="topbar-profile"><Avatar name={`${student.firstName || 'Amara'} ${student.lastName || 'Okafor'}`} /><span>{student.firstName || 'Amara'} {student.lastName || 'Okafor'}</span><ChevronDown size={15} /></div>
          </div>
        </header>
        <div className="content-wrap">
          <Announcement />
          {activeView === 'Overview' && <Overview student={student} results={results} goToResults={() => setActiveView('My results')} />}
          {activeView === 'My results' && <ResultsView results={results} />}
          {activeView === 'Transcript request' && <TranscriptView />}
        </div>
      </main>
    </div>
  )
}

function Login({ onSignIn }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [busy, setBusy] = useState(false)
  const submit = async (event) => {
    event.preventDefault(); setBusy(true); await onSignIn(email, password); setBusy(false)
  }
  return <div className="login-page">
    <div className="login-decoration" aria-hidden="true"><span className="deco-grid" /><span className="deco-ring ring-one" /><span className="deco-ring ring-two" /></div>
    <div className="login-layout">
      <div className="login-intro"><Brand inverse /><p className="eyebrow">A clearer path forward</p><h1>Your progress,<br /><em>in focus.</em></h1><p className="intro-copy">One secure place to follow your results, request official documents, and stay close to your academic goals.</p><div className="trust-note"><ShieldCheck size={18} /><span>Trusted by the Northstar academic community</span></div></div>
      <div className="login-card"><div className="mobile-brand"><Brand /></div><div className="card-heading"><span className="section-kicker">Welcome back</span><h2>Sign in to your portal</h2><p>Enter your student credentials to continue.</p></div>
        <form onSubmit={submit} className="login-form"><label htmlFor="email">Student email or ID</label><div className="input-wrap"><UserRound size={18} /><input id="email" type="text" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@northstar.edu" required /></div><div className="label-row"><label htmlFor="password">Password</label><a href="mailto:helpdesk@northstar.edu">Forgot password?</a></div><div className="input-wrap"><ShieldCheck size={18} /><input id="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Enter your password" required /></div><button className="primary-button login-button" disabled={busy}>{busy ? 'Signing you in...' : 'Sign in'}<ArrowUpRight size={18} /></button></form>
        <div className="login-footer"><span>Need help?</span><a href="mailto:helpdesk@northstar.edu">Contact student services</a></div><button className="demo-link" onClick={() => onSignIn('demo@northstar.edu', 'demo')}>Preview with demo account <ArrowUpRight size={14} /></button>
      </div>
    </div><p className="login-legal">© 2026 Northstar University <span>·</span> Privacy <span>·</span> Accessibility</p>
  </div>
}

function Sidebar({ activeView, setActiveView, open, onClose, onLogout }) {
  return <aside className={`sidebar ${open ? 'is-open' : ''}`}><div className="sidebar-top"><Brand /><button className="icon-button close-sidebar" onClick={onClose} aria-label="Close navigation"><X size={20} /></button></div><div className="student-mini"><Avatar name="Amara Okafor" /><div><strong>Amara Okafor</strong><span>NTS/24/0918</span></div><ChevronDown size={15} /></div><nav aria-label="Main navigation"><span className="nav-label">Workspace</span>{navItems.map(({ label, icon: Icon }) => <button key={label} className={`nav-item ${activeView === label ? 'active' : ''}`} onClick={() => { setActiveView(label); onClose() }}><Icon size={19} /><span>{label}</span>{label === 'My results' && <span className="nav-count">5</span>}</button>)}</nav><div className="sidebar-bottom"><div className="help-box"><div className="help-icon"><CircleHelp size={18} /></div><strong>Need a hand?</strong><span>Our student services team is here for you.</span><a href="mailto:helpdesk@northstar.edu">Get support <ArrowUpRight size={13} /></a></div><button className="logout-button" onClick={onLogout}><LogOut size={18} /> Sign out</button><div className="sidebar-meta"><span>Northstar University</span><span>v2.4.0</span></div></div></aside>
}

function Overview({ student, results, goToResults }) {
  const stats = useMemo(() => ({ credits: results.reduce((total, row) => total + row.credits, 0), gpa: (results.reduce((total, row) => total + row.points * row.credits, 0) / results.reduce((total, row) => total + row.credits, 0)).toFixed(2) }), [results])
  return <><div className="page-heading"><div><span className="section-kicker">Monday, 17 September 2026</span><h1>Good morning, {student.firstName || 'Amara'} <span className="wave">✦</span></h1><p>Here is your academic snapshot for the current session.</p></div><button className="accent-button" onClick={() => window.print()}><Download size={17} /> Download result</button></div><section className="stat-grid" aria-label="Academic summary"><Stat label="Current CGPA" value="4.42" meta="out of 5.00" icon={Sparkles} accent="blue" trend="+0.18" /><Stat label="Credits completed" value="78" meta="of 120 credits" icon={GraduationCap} accent="teal" trend="65%" /><Stat label="Academic status" value="Good standing" meta="No outstanding alerts" icon={CheckCircle2} accent="green" /><Stat label="Current semester" value="300 level" meta="First semester · 2025/26" icon={BookOpen} accent="orange" /></section><div className="dashboard-grid"><section className="panel results-preview"><PanelHeader title="Latest results" action="View all results" onAction={goToResults} /><div className="table-scroll"><ResultTable rows={results.slice(0, 4)} /></div><div className="panel-foot"><span>Showing your most recent published grades</span><button onClick={goToResults}>See full results <ArrowUpRight size={15} /></button></div></section><section className="panel progress-panel"><PanelHeader title="Degree progress" /><div className="progress-ring"><div><strong>65%</strong><span>complete</span></div></div><div className="progress-details"><div><span>Credits completed</span><strong>78 / 120</strong></div><div className="progress-bar"><span /></div><p><strong>42 credits</strong> remaining to graduation</p></div><div className="graduation-note"><GraduationCap size={18} /><span>Estimated graduation<br /><strong>June 2027</strong></span></div></section></div><section className="quick-actions"><span className="section-kicker">Quick actions</span><button onClick={() => window.print()}><Download size={18} /><span><strong>Download result</strong><small>Save a PDF copy of your grades</small></span><ArrowUpRight size={16} /></button><button><FileText size={18} /><span><strong>Request transcript</strong><small>Order an official academic record</small></span><ArrowUpRight size={16} /></button></section></>
}

function ResultsView({ results }) {
  const [session, setSession] = useState(demoSessions[0].id)
  const credits = results.reduce((total, row) => total + row.credits, 0)
  const gpa = (results.reduce((total, row) => total + row.points * row.credits, 0) / credits).toFixed(2)
  return <><div className="page-heading result-heading"><div><span className="section-kicker">Academic record</span><h1>My results</h1><p>Review your published results and academic standing.</p></div><button className="accent-button" onClick={() => window.print()}><Download size={17} /> Download / print</button></div><section className="panel results-panel"><div className="results-toolbar"><div><h2>Semester results</h2><p>Your grades are updated as soon as they are published by your department.</p></div><label className="select-wrap"><span className="sr-only">Select academic session</span><select value={session} onChange={(e) => setSession(e.target.value)}>{demoSessions.map((item) => <option key={item.id} value={item.id}>{item.label}</option>)}</select><ChevronDown size={16} /></label></div><div className="table-scroll"><ResultTable rows={results} detailed /></div><div className="results-summary"><div><span>Total credits earned</span><strong>{credits} <small>credits</small></strong></div><div><span>Semester GPA</span><strong className="summary-gpa">{gpa} <small>/ 5.00</small></strong></div><div><span>Academic standing</span><strong className="standing"><CheckCircle2 size={16} /> Good standing</strong></div></div></section><div className="results-note"><ShieldCheck size={18} /><span>These results are official records published by your faculty. Keep your login details private.</span></div></>
}

function TranscriptView() { return <div className="empty-state panel"><div className="empty-icon"><FileText size={26} /></div><span className="section-kicker">Official documents</span><h1>Transcript requests</h1><p>Request a verified transcript for scholarships, internships, or your next academic step.</p><button className="primary-button">Start a request <ArrowUpRight size={17} /></button></div> }
function Announcement() { return <div className="announcement"><div className="announcement-icon"><Bell size={16} /></div><div><strong>Important announcement</strong><span>Course registration for the second semester opens on 24 September 2026.</span></div><button aria-label="Dismiss announcement"><X size={16} /></button></div> }
function PanelHeader({ title, action, onAction }) { return <div className="panel-header"><h2>{title}</h2>{action && <button onClick={onAction}>{action} <ArrowUpRight size={15} /></button>}</div> }
function ResultTable({ rows, detailed = false }) { return <table><caption className="sr-only">Student course results</caption><thead><tr><th>Course</th><th>Course title</th><th>Credits</th>{detailed && <th>Score</th>}<th>Grade</th><th>Grade point</th><th>Remarks</th></tr></thead><tbody>{rows.map((row) => <tr key={row.code}><td><strong>{row.code}</strong></td><td>{row.title}</td><td>{row.credits}</td>{detailed && <td>{row.score}%</td>}<td><GradeBadge grade={row.grade} /></td><td>{row.points.toFixed(1)}</td><td><span className="pass-mark"><CheckCircle2 size={14} /> Passed</span></td></tr>)}</tbody></table> }
function GradeBadge({ grade }) { return <span className={`grade-badge grade-${grade.toLowerCase()}`}>{grade}</span> }
function Stat({ label, value, meta, icon: Icon, accent, trend }) { return <div className="stat-card"><div className={`stat-icon ${accent}`}><Icon size={19} /></div><div className="stat-label">{label}<span>{trend && <b>{trend}</b>} {trend && 'this term'}</span></div><strong className="stat-value">{value}</strong><span className="stat-meta">{meta}</span></div> }
function Brand({ inverse = false }) { return <div className={`brand ${inverse ? 'brand-inverse' : ''}`}><div className="brand-mark"><GraduationCap size={22} /></div><span>northstar<small>UNIVERSITY</small></span></div> }
function Avatar({ name }) { return <span className="avatar">{name.split(' ').map((part) => part[0]).join('').slice(0, 2)}</span> }

export default App