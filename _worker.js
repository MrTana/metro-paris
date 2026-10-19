// Cloudflare Pages (modo avanzado): sirve index.html y reenvía /api/* a la API de PRIM.
// Prueba dos rutas base habituales de Navitia en PRIM y recuerda la que funciona.
const BASES = [
  'https://prim.iledefrance-mobilites.fr/marketplace/v2/navitia',
  'https://prim.iledefrance-mobilites.fr/marketplace/v2/navitia/coverage/fr-idf'
];
let good = 0;

async function upstream(path, key) {
  const order = [good, ...BASES.keys()].filter((v, i, a) => a.indexOf(v) === i);
  let last;
  for (const i of order) {
    const r = await fetch(BASES[i] + path, { headers: { apikey: key, accept: 'application/json' } });
    if (r.status !== 404) { good = i; return r; }
    last = r;
  }
  return last;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === '/api/ping') {
      return Response.json({ ok: true }, { headers: { 'cache-control': 'no-store' } });
    }

    if (url.pathname.startsWith('/api/')) {
      if (request.method !== 'GET') return new Response('Method not allowed', { status: 405 });
      const key = request.headers.get('apikey') || '';
      try {
        const r = await upstream(url.pathname.slice(4) + url.search, key);
        return new Response(r.body, {
          status: r.status,
          headers: {
            'content-type': r.headers.get('content-type') || 'application/json',
            'cache-control': 'no-store'
          }
        });
      } catch (e) {
        return Response.json({ error: String(e) }, { status: 502 });
      }
    }

    return env.ASSETS.fetch(request);
  }
};
