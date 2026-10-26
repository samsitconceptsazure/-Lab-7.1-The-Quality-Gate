import React, { useEffect, useMemo, useState } from 'react'
import { createRoot } from 'react-dom/client'
import { Activity, Boxes, ClipboardList, LogIn, LogOut, PackageCheck, RefreshCw, ShieldCheck, ShoppingCart, Truck } from 'lucide-react'
import './styles.css'

const API = import.meta.env.VITE_API_BASE_URL ?? (window.location.hostname === 'localhost' ? 'http://localhost:8000' : '')
const money = n => new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(Number(n || 0))

function App() {
  const [token, setToken] = useState(localStorage.getItem('retailops_token') || '')
  const [user, setUser] = useState(null)
  const [products, setProducts] = useState([])
  const [orders, setOrders] = useState([])
  const [summary, setSummary] = useState(null)
  const [username, setUsername] = useState('admin')
  const [password, setPassword] = useState('')
  const [quantities, setQuantities] = useState({})
  const [message, setMessage] = useState('')
  const [busy, setBusy] = useState(false)

  async function request(path, options = {}) {
    const response = await fetch(`${API}${path}`, {
      ...options,
      headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}), ...(options.headers || {}) }
    })
    const body = await response.json().catch(() => ({}))
    if (!response.ok) throw new Error(body.detail || `Request failed (${response.status})`)
    return body
  }
  async function refresh(currentToken = token) {
    const headers = currentToken ? { Authorization: `Bearer ${currentToken}` } : {}
    const [p, o] = await Promise.all([
      fetch(`${API}/api/products`).then(r => r.json()),
      currentToken ? fetch(`${API}/api/orders`, { headers }).then(r => r.ok ? r.json() : []) : Promise.resolve([])
    ])
    setProducts(Array.isArray(p) ? p : [])
    setOrders(Array.isArray(o) ? o : [])
    if (currentToken) {
      const me = await fetch(`${API}/api/auth/me`, { headers })
      if (me.ok) setUser(await me.json())
    }
    if (currentToken) {
      const s = await fetch(`${API}/api/admin/summary`, { headers })
      setSummary(s.ok ? await s.json() : null)
    }
  }
  useEffect(() => { refresh().catch(e => setMessage(e.message)) }, [])
  useEffect(() => {
    if (token) {
      localStorage.setItem('retailops_token', token)
      refresh(token).catch(e => { setMessage(e.message); setToken(''); localStorage.removeItem('retailops_token') })
    } else {
      setUser(null); setOrders([]); setSummary(null); localStorage.removeItem('retailops_token')
    }
  }, [token])

  async function login(e) {
    e.preventDefault(); setBusy(true); setMessage('')
    try {
      const data = await request('/api/auth/login', { method: 'POST', body: JSON.stringify({ username, password }) })
      setToken(data.access_token); setPassword(''); setMessage(`Signed in as ${username} (${data.role}).`)
    } catch (e) { setMessage(e.message) } finally { setBusy(false) }
  }
  function logout() { setToken(''); setUser(null); setMessage('Signed out.') }
  async function placeOrder(product) {
    const quantity = Number(quantities[product.id] || 1)
    setBusy(true); setMessage('')
    try {
      await request('/api/orders', { method: 'POST', body: JSON.stringify({ items: [{ product_id: product.id, quantity }] }) })
      setMessage(`Order placed for ${product.name}.`)
      setQuantities(q => ({ ...q, [product.id]: 1 }))
      await refresh()
    } catch (e) { setMessage(e.message) } finally { setBusy(false) }
  }
  async function changeStatus(order, status) {
    try {
      await request(`/api/orders/${order.id}/status?status_value=${status}`, { method: 'PATCH' })
      setMessage(`Order #${order.id} updated to ${status}.`)
      await refresh()
    } catch (e) { setMessage(e.message) }
  }
  const totalInventory = useMemo(() => products.reduce((n, p) => n + p.stock, 0), [products])
  const pendingOrders = orders.filter(o => !['DELIVERED', 'CANCELLED'].includes(o.status)).length

  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand"><div className="brand-mark"><Boxes size={23}/></div><div><strong>RetailOps</strong><span>ORDER MANAGEMENT</span></div></div>
      <div className="nav-label">WORKSPACE</div>
      <a className="nav-item active"><Activity size={18}/> Overview</a>
      <a className="nav-item"><PackageCheck size={18}/> Inventory</a>
      <a className="nav-item"><ClipboardList size={18}/> Orders</a>
      <div className="sidebar-bottom"><div className="secure"><ShieldCheck size={18}/><div><strong>Security enabled</strong><span>JWT · Role-based access</span></div></div><span className="version">RETAILOPS v1.0 · DEVSECOPS LAB</span></div>
    </aside>
    <main className="main">
      <header className="topbar"><div><span className="eyebrow">OPERATIONS / DASHBOARD</span><h1>Order Management</h1><p>Monitor inventory, place orders, and manage fulfillment from one workspace.</p></div><div className="account">{user ? <><span className="avatar">{user.username.slice(0,1).toUpperCase()}</span><div><strong>{user.username}</strong><span>{user.role}</span></div><button className="icon-button" onClick={logout} title="Sign out"><LogOut size={18}/></button></> : <span className="signed-out">Read-only demo · sign in to order</span>}</div></header>
      {message && <div className="notice" role="status">{message}<button onClick={() => setMessage('')}>×</button></div>}
      <section className="metrics">
        <Metric icon={<Boxes/>} label="Products" value={products.length} note="Active catalog"/>
        <Metric icon={<ShoppingCart/>} label="Orders" value={orders.length} note="Visible to your role"/>
        <Metric icon={<Truck/>} label="In fulfillment" value={pendingOrders} note="Not yet terminal"/>
        <Metric icon={<PackageCheck/>} label="Units in stock" value={totalInventory.toLocaleString()} note="Across all products"/>
      </section>
      <div className="content-grid">
        <section className="panel catalog"><div className="panel-heading"><div><h2>Product catalog</h2><p>Browse available warehouse products</p></div><button className="refresh" onClick={() => refresh()}><RefreshCw size={15}/> Refresh</button></div>
          <div className="product-list">{products.map(p => <article className="product" key={p.id}><div className="product-icon"><Boxes size={22}/></div><div className="product-info"><strong>{p.name}</strong><span>{p.sku} · {p.description}</span><div className="product-bottom"><b>{money(p.price)}</b><span className={p.stock < 15 ? 'stock low' : 'stock'}>{p.stock} in stock</span></div></div><div className="buy-control"><input aria-label={`Quantity for ${p.name}`} type="number" min="1" max={Math.max(1,p.stock)} value={quantities[p.id] ?? 1} onChange={e => setQuantities(q => ({...q,[p.id]:e.target.value}))}/><button disabled={!user || busy || p.stock < 1} onClick={() => placeOrder(p)}>{user ? 'Order' : 'Sign in'}</button></div></article>)}
          {!products.length && <p className="empty">Loading catalog…</p>}</div>
        </section>
        <section className="right-column">
          {!user ? <section className="panel login-panel"><div className="login-icon"><LogIn size={21}/></div><h2>Sign in to RetailOps</h2><p>Use a lab account to place orders or manage fulfillment.</p><form onSubmit={login}><label>Username<input value={username} onChange={e => setUsername(e.target.value)} autoComplete="username" required/></label><label>Password<input type="password" value={password} onChange={e => setPassword(e.target.value)} autoComplete="current-password" required/></label><button className="primary" disabled={busy}>{busy ? 'Signing in…' : 'Sign in securely'}</button></form><div className="demo-hint"><strong>Local demo accounts</strong><span>admin · warehouse · customer</span><small>Passwords are in your local .env.example file.</small></div></section> :
            <section className="panel role-panel"><div className="panel-heading"><div><h2>Access profile</h2><p>Permissions are enforced by the API.</p></div><ShieldCheck className="green"/></div><div className="role-chip">{user.role.toUpperCase()}</div><ul className="permissions"><li>View product catalog</li><li>View permitted orders</li>{user.role !== 'customer' && <li>Update stock and fulfillment via API</li>}{user.role === 'admin' && <li>View administrative summary via API</li>}</ul>{summary && <div className="summary-grid"><div><span>Users</span><b>{summary.users}</b></div><div><span>Inventory units</span><b>{summary.inventory_units}</b></div></div>}</section>}
          <section className="panel orders-panel"><div className="panel-heading"><div><h2>Recent orders</h2><p>{user ? 'Orders available to your role' : 'Sign in to view orders'}</p></div><ClipboardList size={20} className="muted-icon"/></div>{orders.length ? <div className="order-list">{orders.slice(0,6).map(o => <div className="order-row" key={o.id}><div><strong>Order #{o.id}</strong><span>{o.items?.length || 0} line item(s) · {o.customer_username}</span></div><div className="order-meta"><b>{money(o.total)}</b><span className={`status ${o.status.toLowerCase()}`}>{o.status}</span>{user.role !== 'customer' && !['DELIVERED','CANCELLED'].includes(o.status) && <select aria-label={`Change status for order ${o.id}`} value={o.status} onChange={e => changeStatus(o,e.target.value)}><option value="PLACED">PLACED</option><option value="PROCESSING">PROCESSING</option><option value="SHIPPED">SHIPPED</option><option value="DELIVERED">DELIVERED</option><option value="CANCELLED">CANCELLED</option></select>}</div></div>)}</div> : <div className="empty-orders"><ClipboardList size={25}/><span>No orders to show yet.</span><small>Sign in and place an order to get started.</small></div>}</section>
        </section>
      </div>
      <footer>RetailOps Enterprise · Training environment <span>● API-driven · JWT protected</span></footer>
    </main>
  </div>
}
function Metric({icon,label,value,note}) { return <div className="metric"><div className="metric-top"><span>{label}</span><i>{icon}</i></div><strong>{value}</strong><small>{note}</small></div> }
createRoot(document.getElementById('root')).render(<App/>)
