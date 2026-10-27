const navigation = [
  { label: "Overview", icon: "◫", active: true },
  { label: "Jira stories", icon: "◇", disabled: true },
  { label: "Test cases", icon: "▤", disabled: true },
  { label: "Runs", icon: "▷", disabled: true },
];

const readinessItems = [
  {
    number: "01",
    title: "Product scope",
    detail: "Owner sign-off pending",
    state: "Pending",
  },
  {
    number: "02",
    title: "Environment policy",
    detail: "Staging origin not approved",
    state: "Pending",
  },
  {
    number: "03",
    title: "Jira connection",
    detail: "Integration not configured",
    state: "Not connected",
  },
];

function App() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <a className="brand" href="#" aria-label="Vehicle QA home">
          <span className="brand-mark" aria-hidden="true">
            V
          </span>
          <span>
            <strong>motion</strong>
            <small>QUALITY WORKSPACE</small>
          </span>
        </a>

        <div className="workspace-label">WORKSPACE</div>
        <div className="project-switcher">
          <span className="project-icon">VS</span>
          <span className="project-name">
            <strong>Vehicle Shop</strong>
            <small>QA project</small>
          </span>
          <span className="chevron" aria-hidden="true">
            ⌄
          </span>
        </div>

        <nav className="navigation" aria-label="Main navigation">
          {navigation.map((item) => (
            <a
              aria-current={item.active ? "page" : undefined}
              aria-disabled={item.disabled ? "true" : undefined}
              className={`nav-item${item.active ? " active" : ""}${item.disabled ? " disabled" : ""}`}
              href={item.active ? "#overview" : undefined}
              key={item.label}
              tabIndex={item.disabled ? -1 : undefined}
            >
              <span className="nav-icon" aria-hidden="true">
                {item.icon}
              </span>
              {item.label}
              {item.disabled && <span className="soon">SOON</span>}
            </a>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="help-card">
            <span className="help-icon" aria-hidden="true">
              ?
            </span>
            <div>
              <strong>Need a hand?</strong>
              <span>Setup guide</span>
            </div>
            <span className="help-arrow" aria-hidden="true">
              ↗
            </span>
          </div>
          <div className="profile">
            <span className="avatar">QA</span>
            <span>
              <strong>QA workspace</strong>
              <small>Local preview</small>
            </span>
            <span className="profile-menu" aria-hidden="true">
              ···
            </span>
          </div>
        </div>
      </aside>

      <main className="main-content" id="overview">
        <header className="topbar">
          <div className="breadcrumb">
            <span>Projects</span>
            <span className="breadcrumb-separator">/</span>
            <strong>Vehicle Shop</strong>
          </div>
          <div className="topbar-actions">
            <span className="preview-pill">
              <span className="preview-dot" />
              Setup preview
            </span>
            <button className="icon-button" aria-label="Notifications" disabled>
              ♧
            </button>
            <span className="top-avatar" aria-label="QA workspace">
              QA
            </span>
          </div>
        </header>

        <div className="page-content">
          <section className="welcome-row">
            <div>
              <div className="eyebrow">
                <span className="eyebrow-line" />
                TEST AUTOMATION
              </div>
              <h1>Your QA control room</h1>
              <p>
                A clear view of your Vehicle Shop test workflow, from Jira story
                to verified result.
              </p>
            </div>
            <button className="primary-button" disabled title="Available after setup approval">
              <span aria-hidden="true">＋</span>
              Connect Jira
            </button>
          </section>

          <section className="pilot-banner" aria-label="Pilot scope">
            <span className="banner-symbol" aria-hidden="true">
              ◈
            </span>
            <div className="banner-copy">
              <strong>Search &amp; comparison pilot</strong>
              <span>
                Configuration and booking stay out of scope until separately
                approved.
              </span>
            </div>
            <span className="approval-badge">
              <span />
              APPROVAL PENDING
            </span>
          </section>

          <section className="metrics" aria-label="Workspace summary">
            <article className="metric-card">
              <div className="metric-top">
                <span className="metric-icon lavender">▤</span>
                <span className="metric-caption">CATALOG</span>
              </div>
              <strong className="metric-value">—</strong>
              <span className="metric-label">Test cases</span>
              <span className="metric-note">No catalog connected</span>
            </article>
            <article className="metric-card">
              <div className="metric-top">
                <span className="metric-icon mint">✓</span>
                <span className="metric-caption">REVIEW</span>
              </div>
              <strong className="metric-value">—</strong>
              <span className="metric-label">Ready to run</span>
              <span className="metric-note">Requires approved cases</span>
            </article>
            <article className="metric-card">
              <div className="metric-top">
                <span className="metric-icon peach">▷</span>
                <span className="metric-caption">EXECUTION</span>
              </div>
              <strong className="metric-value">—</strong>
              <span className="metric-label">Runs this week</span>
              <span className="metric-note">Runner not connected</span>
            </article>
          </section>

          <section className="content-grid">
            <article className="panel cases-panel">
              <div className="panel-heading">
                <div>
                  <div className="panel-kicker">YOUR WORK</div>
                  <h2>Test cases</h2>
                </div>
                <button className="text-button" disabled>
                  View catalog <span aria-hidden="true">→</span>
                </button>
              </div>
              <div className="empty-state">
                <div className="empty-art" aria-hidden="true">
                  <div className="empty-sheet sheet-back" />
                  <div className="empty-sheet sheet-front">
                    <span />
                    <span />
                    <span />
                  </div>
                  <div className="empty-spark">✦</div>
                </div>
                <h3>Your catalog starts here</h3>
                <p>
                  Connect to Jira and choose a story to begin a traceable,
                  review-ready test case.
                </p>
                <button className="secondary-button" disabled>
                  Browse Jira stories
                </button>
              </div>
            </article>

            <article className="panel readiness-panel">
              <div className="panel-heading readiness-heading">
                <div>
                  <div className="panel-kicker">BEFORE YOU BEGIN</div>
                  <h2>Pilot readiness</h2>
                </div>
                <span className="readiness-count">0 / 3</span>
              </div>
              <p className="readiness-intro">
                A few approvals are needed before the team can safely get
                started.
              </p>
              <ol className="readiness-list">
                {readinessItems.map((item) => (
                  <li className="readiness-item" key={item.number}>
                    <span className="step-number">{item.number}</span>
                    <span className="readiness-copy">
                      <strong>{item.title}</strong>
                      <small>{item.detail}</small>
                    </span>
                    <span className="state-label">{item.state}</span>
                  </li>
                ))}
              </ol>
              <div className="safety-note">
                <span className="safety-lock" aria-hidden="true">
                  ◈
                </span>
                <span>
                  Runs are disabled until environment safety is approved.
                </span>
              </div>
            </article>
          </section>

          <footer className="footer">
            <span>Vehicle Shop QA workspace</span>
            <span>
              <span className="footer-dot" />
              Local preview · No external connections
            </span>
          </footer>
        </div>
      </main>
    </div>
  );
}

export default App;
