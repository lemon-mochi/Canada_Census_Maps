// Vite: VITE_API_URL in .env. Next.js: NEXT_PUBLIC_API_URL. Falls back to local dev.
export const API_URL =
  import.meta.env?.VITE_API_URL ??
  (typeof process !== 'undefined' ? import.meta.env?.NEXT_PUBLIC_API_URL : undefined) ??
  'http://localhost:8000';