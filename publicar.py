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
# manifiesto: la huella de cada archivo del programa, para que cada lab revise que sigue siendo el original
import tarfile
huellas = {}
with tarfile.open(tgz, 'r:gz') as t:
    for m_ in t.getmembers():
        n = m_.name[2:] if m_.name.startswith('./') else m_.name
        if not m_.isfile() or not n.startswith('.the-edit-lab/plugin/'):
            continue
        rel = n[len('.the-edit-lab/plugin/'):]
        if '__pycache__' in rel.split('/') or 'node_modules' in rel.split('/') or rel.endswith('.pyc') or rel.endswith('.DS_Store'):
            continue
        huellas[rel] = hashlib.sha256(t.extractfile(m_).read()).hexdigest()
os.makedirs(os.path.join(aqui, 'manifiestos'), exist_ok=True)
json.dump({'version': ver, 'archivos': huellas}, open(os.path.join(aqui, 'manifiestos', ver + '.json'), 'w', encoding='utf-8'), indent=0)
if not os.path.exists(os.path.join(aqui, 'canceladas.json')):
    json.dump({'numeros': [], 'correos': []}, open(os.path.join(aqui, 'canceladas.json'), 'w', encoding='utf-8'), indent=1)
if len(sys.argv) > 4:
    shutil.copy(sys.argv[4], os.path.join(aqui, 'noticias.json'))
print('Listo para subir:', ver, sha)
