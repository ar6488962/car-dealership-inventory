import { useCallback, useEffect, useMemo, useState } from 'react';
import {
  AlertCircle,
  ArrowRight,
  CarFront,
  CheckCircle2,
  LogOut,
  Menu,
  RefreshCw,
  Search,
  ShieldCheck,
  SlidersHorizontal,
  UserRound,
  X,
} from 'lucide-react';
import { api, clearSession, getToken, getUser } from './api';
import AuthModal from './components/AuthModal';
import VehicleCard from './components/VehicleCard';
import AdminPanel from './components/AdminPanel';

const categories = ['SUV', 'Sedan', 'Hatchback', 'Coupe', 'Electric', 'Pickup', 'Wagon', 'Other'];

export default function App() {
  const [vehicles, setVehicles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [user, setUser] = useState(getUser());
  const [authMode, setAuthMode] = useState(null);
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('All vehicles');
  const [maxPrice, setMaxPrice] = useState('');
  const [sort, setSort] = useState('featured');
  const [busyId, setBusyId] = useState(null);
  const [toast, setToast] = useState(null);
  const [mobileNav, setMobileNav] = useState(false);

  const notify = useCallback((message, isError = false) => {
    setToast({ message, isError });
    window.setTimeout(() => setToast(null), 3600);
  }, []);

  const loadVehicles = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      setVehicles(await api('/api/vehicles'));
    } catch (err) {
      setError(err.message || 'The inventory service is unavailable.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadVehicles();
  }, [loadVehicles]);

  useEffect(() => {
    const handleAuthExpired = () => {
      setUser(null);
      setAuthMode('login');
      notify('Your session expired. Please sign in again.', true);
    };
    window.addEventListener('motorstock:auth-expired', handleAuthExpired);
    return () => window.removeEventListener('motorstock:auth-expired', handleAuthExpired);
  }, [notify]);

  const shownVehicles = useMemo(() => {
    const search = query.trim().toLowerCase();
    const filtered = vehicles.filter((vehicle) => {
      const matchesSearch =
        !search ||
        `${vehicle.make} ${vehicle.model} ${vehicle.category}`.toLowerCase().includes(search);
      const matchesCategory = category === 'All vehicles' || vehicle.category === category;
      const matchesPrice = !maxPrice || vehicle.price <= Number(maxPrice);
      return matchesSearch && matchesCategory && matchesPrice;
    });
    if (sort === 'price-low') filtered.sort((a, b) => a.price - b.price);
    if (sort === 'price-high') filtered.sort((a, b) => b.price - a.price);
    if (sort === 'stock') filtered.sort((a, b) => b.quantity - a.quantity);
    return filtered;
  }, [vehicles, query, category, maxPrice, sort]);

  async function purchase(vehicle) {
    if (!getToken()) {
      setAuthMode('login');
      notify('Sign in to purchase a vehicle', true);
      return;
    }
    setBusyId(vehicle.id);
    try {
      const result = await api(`/api/vehicles/${vehicle.id}/purchase`, { method: 'POST' });
      notify(result.message || 'Purchase recorded');
      await loadVehicles();
    } catch (err) {
      notify(err.message, true);
      await loadVehicles();
    } finally {
      setBusyId(null);
    }
  }

  function logout() {
    clearSession();
    setUser(null);
    notify('You have signed out');
  }

  function clearFilters() {
    setQuery('');
    setCategory('All vehicles');
    setMaxPrice('');
  }

  const isAdmin = user?.role === 'admin';

  return (
    <div className="app-shell">
      <div className="topline">
        <span>THE MOTORSTOCK COLLECTION</span>
        <span className="topline-right"><span className="live-dot" /> INVENTORY UPDATED LIVE</span>
      </div>
      <header className="site-header">
        <a href="#top" className="brand">
          <span className="brand-mark"><CarFront size={25} /></span>
          <span>MOTOR<span className="brand-light">STOCK</span><small>DRIVE SOMETHING DIFFERENT</small></span>
        </a>
        <button className="mobile-toggle icon-button" onClick={() => setMobileNav(!mobileNav)} aria-label="Toggle navigation">
          {mobileNav ? <X /> : <Menu />}
        </button>
        <nav className={mobileNav ? 'nav-links nav-open' : 'nav-links'}>
          <a href="#inventory" onClick={() => setMobileNav(false)}>Inventory</a>
          <a href="#about" onClick={() => setMobileNav(false)}>Our approach</a>
          {isAdmin && <a href="#admin" onClick={() => setMobileNav(false)}>Manage stock</a>}
        </nav>
        <div className="header-actions">
          {user ? (
            <>
              <span className="user-chip"><UserRound size={16} />{user.name}</span>
              {isAdmin && <span className="admin-chip"><ShieldCheck size={14} /> ADMIN</span>}
              <button className="button button-outline sign-button" onClick={logout}><LogOut size={16} /> Sign out</button>
            </>
          ) : (
            <>
              <button className="button button-quiet" onClick={() => setAuthMode('login')}>Sign in</button>
              <button className="button button-dark" onClick={() => setAuthMode('register')}>Create account <ArrowRight size={16} /></button>
            </>
          )}
        </div>
      </header>

      <main id="top">
        <section className="hero">
          <div className="hero-copy">
            <div className="hero-kicker"><span /> YOUR NEXT CHAPTER STARTS HERE</div>
            <h1>Find the car<br />that feels <em>like you.</em></h1>
            <p>A considered collection of exceptional vehicles. Explore the inventory, compare your favourites and find your next drive.</p>
            <div className="hero-actions">
              <a href="#inventory" className="button button-primary">Explore inventory <ArrowRight size={17} /></a>
              <span className="hero-note"><ShieldCheck size={16} /> A simpler way to shop</span>
            </div>
            <div className="hero-stats">
              <div><strong>{String(vehicles.length).padStart(2, '0')}</strong><span>VEHICLES TO EXPLORE</span></div>
              <div><strong>01</strong><span>PLACE TO START</span></div>
              <div><strong>100%</strong><span>YOUR NEXT MOVE</span></div>
            </div>
          </div>
          <div className="hero-visual">
            <img src="https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1600&q=90" alt="Silver sports car on a mountain road" />
            <div className="hero-image-label"><span>EDITOR'S PICK</span><strong>Built for the journey.</strong></div>
            <div className="hero-index">COLLECTION <strong>01 / 06</strong></div>
          </div>
          <div className="hero-watermark">M</div>
        </section>

        <section className="trust-strip">
          <div><ShieldCheck /><span><strong>Clear inventory</strong><small>Know what's available</small></span></div>
          <div><RefreshCw /><span><strong>Stock that stays current</strong><small>Updates after each purchase</small></span></div>
          <div><CheckCircle2 /><span><strong>Simple by design</strong><small>Less friction, more clarity</small></span></div>
          <div className="trust-end">GOOD CARS.<br /><strong>GOOD DECISIONS.</strong></div>
        </section>

        <section id="inventory" className="inventory-section">
          <div className="section-heading">
            <div><p className="eyebrow">THE COLLECTION <span>— 2026</span></p><h2>Find your kind of drive.</h2><p className="muted">Explore our current collection and find the right fit.</p></div>
            <div className="inventory-count"><strong>{String(shownVehicles.length).padStart(2, '0')}</strong><span>VEHICLES FOUND</span></div>
          </div>
          <div className="filter-bar">
            <div className="search-box"><Search size={18} /><input aria-label="Search vehicles" placeholder="Search make, model or category…" value={query} onChange={(event) => setQuery(event.target.value)} />{query && <button className="clear-search" onClick={() => setQuery('')}>Clear</button>}</div>
            <div className="filter-control"><SlidersHorizontal size={16} /><select aria-label="Filter by category" value={category} onChange={(event) => setCategory(event.target.value)}><option>All vehicles</option>{categories.map((item) => <option key={item}>{item}</option>)}</select></div>
            <div className="filter-control price-filter"><span>MAX PRICE</span><select aria-label="Maximum price" value={maxPrice} onChange={(event) => setMaxPrice(event.target.value)}><option value="">Any price</option><option value="30000">$30,000</option><option value="50000">$50,000</option><option value="75000">$75,000</option><option value="100000">$100,000</option></select></div>
            <div className="filter-control sort-control"><select aria-label="Sort vehicles" value={sort} onChange={(event) => setSort(event.target.value)}><option value="featured">Featured</option><option value="price-low">Price: low to high</option><option value="price-high">Price: high to low</option><option value="stock">Most in stock</option></select></div>
          </div>
          {error && <div className="api-banner"><div><AlertCircle size={19} /><span>{error}</span></div><button className="button button-outline small-button" onClick={loadVehicles}>Retry</button></div>}
          {loading ? <div className="loading-state"><span className="spinner" /> Loading inventory…</div> : shownVehicles.length ? (
            <div className="vehicle-grid">{shownVehicles.map((vehicle) => <VehicleCard key={vehicle.id} vehicle={vehicle} onPurchase={purchase} busy={busyId === vehicle.id} isLoggedIn={!!user} />)}</div>
          ) : (
            <div className="empty-state"><div className="empty-icon"><Search size={25} /></div><h3>{error ? 'Inventory is unavailable' : 'No vehicles found'}</h3><p>{error ? 'Start the backend and retry to load persistent inventory.' : 'Try another search or clear your filters to see the full collection.'}</p><button className="button button-outline" onClick={clearFilters}>Clear all filters</button></div>
          )}
          <div className="inventory-foot"><span>Showing {shownVehicles.length} of {vehicles.length} vehicles</span><span>PRICES DISPLAYED IN USD</span></div>
        </section>

        {isAdmin && <div id="admin" className="admin-wrap"><AdminPanel vehicles={vehicles} onChanged={loadVehicles} notify={notify} /></div>}
        <section id="about" className="closing-banner"><div className="closing-mark"><CarFront size={30} /></div><div><p className="eyebrow">A BETTER WAY TO FIND YOUR NEXT CAR</p><h2>Good things happen<br />when the fit is right.</h2><p>Browse at your own pace. The right drive is out there.</p></div><a href="#inventory" className="button button-light">Back to inventory <ArrowRight size={17} /></a><span className="closing-watermark">M</span></section>
      </main>
      <footer className="site-footer"><a href="#top" className="brand footer-brand"><span className="brand-mark"><CarFront size={22} /></span><span>MOTOR<span className="brand-light">STOCK</span><small>DRIVE SOMETHING DIFFERENT</small></span></a><span>BUILT WITH CARE. DESIGNED TO KEEP MOVING.</span><span>© 2026 MOTORSTOCK</span></footer>
      {authMode && <AuthModal mode={authMode} setMode={setAuthMode} onClose={() => setAuthMode(null)} onSuccess={(nextUser) => { setUser(nextUser); notify(`Welcome, ${nextUser.name}`); }} />}
      {toast && <div className={`toast ${toast.isError ? 'toast-error' : ''}`}>{toast.isError ? <AlertCircle size={18} /> : <CheckCircle2 size={18} />} {toast.message}</div>}
    </div>
  );
}
