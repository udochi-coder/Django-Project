const API_URL = (import.meta.env.VITE_API_URL || '').replace(/\/$/, '')

export const demoStudent = {
  firstName: 'Amara',
  lastName: 'Okafor',
  matricNumber: 'NTS/24/0918',
  department: 'Computer Science',
  level: '300',
  status: 'Good standing',
}

export const demoResults = [
  { code: 'CSC 301', title: 'Data Structures & Algorithms', credits: 3, grade: 'A', points: 5.0, score: 84, semester: 'First' },
  { code: 'CSC 305', title: 'Operating Systems', credits: 3, grade: 'A', points: 5.0, score: 78, semester: 'First' },
  { code: 'CSC 307', title: 'Database Management Systems', credits: 3, grade: 'B', points: 4.0, score: 68, semester: 'First' },
  { code: 'MTH 301', title: 'Numerical Analysis', credits: 3, grade: 'B', points: 4.0, score: 64, semester: 'First' },
  { code: 'GST 301', title: 'Entrepreneurship Studies', credits: 2, grade: 'A', points: 5.0, score: 82, semester: 'First' },
]

export const demoSessions = [
  { id: '2025-first', label: '2025 / 2026 · First semester', year: 2025, semester: 'First' },
  { id: '2024-second', label: '2024 / 2025 · Second semester', year: 2024, semester: 'Second' },
]

async function request(path, options = {}) {
  if (!API_URL) throw new Error('Demo mode')
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
  })
  if (!response.ok) throw new Error(`Request failed with ${response.status}`)
  return response.json()
}

export async function login(email, password) {
  const data = await request('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  })
  localStorage.setItem('access_token', data.access)
  localStorage.setItem('refresh_token', data.refresh)
  return { ...demoStudent, ...(data.user || {}) }
}

export async function loadResults() {
  const token = localStorage.getItem('access_token')
  const rows = await request('/api/result/', { headers: { Authorization: `Bearer ${token}` } })
  const items = Array.isArray(rows) ? rows : rows.results || []
  return items.map((item) => ({
    code: item.course_code,
    title: item.course_title,
    credits: item.credit_units,
    grade: item.grade,
    points: Number(item.grade_point),
    score: Number(item.score),
    semester: 'First',
  }))
}