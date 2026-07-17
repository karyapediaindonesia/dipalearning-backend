import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export default function proxy(request: NextRequest) {
  // Cek apakah ada token akses di cookies
  const token = request.cookies.get('access_token')?.value;

  // Jika mengakses halaman admin tapi belum login
  if (request.nextUrl.pathname.startsWith('/admin') && !token) {
    return NextResponse.redirect(new URL('/auth/login', request.url));
  }

  // Jika mengakses root path ('/')
  if (request.nextUrl.pathname === '/') {
    if (token) {
      // Jika sudah login, lempar ke dashboard admin
      return NextResponse.redirect(new URL('/admin/dashboard', request.url));
    } else {
      // Jika belum login, paksa ke login dan hilangkan cache
      const response = NextResponse.redirect(new URL('/auth/login', request.url));
      response.headers.set('Cache-Control', 'no-store, max-age=0');
      return response;
    }
  }
}

export const config = {
  // Jalankan middleware ini pada root path '/' dan semua halaman admin
  matcher: ['/', '/admin/:path*'],
};
