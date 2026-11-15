#!/usr/bin/env python3
"""Publica una versión nueva de The Edit Lab para todas las clientas.
Uso (desde esta carpeta):  python3 publicar.py <actualizacion-X.Y.Z.tgz> <X.Y.Z> <CAMBIOS.md> [noticias.json]
Copia el paquete a paquetes/, escribe ultima.json (versión, novedades, enlace y huella sha256) y, si se da, noticias.json.
Después: git add -A && git commit -m "Versión X.Y.Z" && git push.  Cada lab lo encuentra solo (lo revisa cada 6 horas)
y se instala solo con respaldo cuando Claude no está editando."""
import hashlib, json, os, re, shutil, sys
REPO = 'clarisaflores/the-edit-lab-actualizaciones'
tgz, ver, cambios = sys.argv[1], sys.argv[2], sys.argv[3]
aqui = os.path.dirname(os.path.abspath(__file__))
t = open(cambios, encoding='utf-8').read()
m = re.search(r'^## ' + re.escape(ver) + r'\s*$(.*?)(?=^## |\Z)', t, re.M | re.S)
notas = [re.sub(r'\*\*(.+?)\*\*', r'\1', l.strip()[2:]) for l in (m.group(1).splitlines() if m else []) if l.strip().startswith('- ')]
nombre = 'actualizacion-%s.tgz' % ver
os.makedirs(os.path.join(aqui, 'paquetes'), exist_ok=True)
shutil.copy(tgz, os.path.join(aqui, 'paquetes', nombre))
sha = hashlib.sha256(open(tgz, 'rb').read()).hexdigest()
json.dump({'version': ver, 'notas': notas, 'archivo': 'https://raw.githubusercontent.com/%s/main/paquetes/%s' % (REPO, nombre), 'sha256': sha},
          open(os.path.join(aqui, 'ultima.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
if len(sys.argv) > 4:
    shutil.copy(sys.argv[4], os.path.join(aqui, 'noticias.json'))
print('Listo para subir:', ver, sha)
