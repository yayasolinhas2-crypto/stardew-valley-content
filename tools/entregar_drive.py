"""Prepara a entrega dos posts aprovados na pasta do Drive "Stardew - Para agendar".

Uso: python3 tools/entregar_drive.py <out_dir>/posts
Lê os posts do painel (JSON salvos com ArtifactData out_dir) e imprime um JSON com o que criar
no Drive para cada post APROVADO (ainda não agendado no Metricool), com vídeo, que ainda não tem "drive_pasta" e sai no futuro.
Quem executa as chamadas do Drive é a rotina (conector Google Drive):
  1. create_file title=<pasta> contentMimeType=application/vnd.google-apps.folder parentId=PASTA_RAIZ
  2. create_file title=legenda.txt textContent=<legenda_txt> contentMimeType=text/plain disableConversionToGoogleType=true parentId=<id da pasta>
  3. create_file title=<video_nome> base64Content=<video_ref> contentMimeType=video/mp4 disableConversionToGoogleType=true parentId=<id da pasta>
  4. create_file title=capa.jpg base64Content=<capa_ref> contentMimeType=image/jpeg disableConversionToGoogleType=true parentId=<id da pasta> (se houver capa)
  5. ArtifactData update no post: {"drive_pasta": "<pasta>", "drive_id": "<id da pasta>"} (com if_version)
Regra da Yasmin (10/11): subpasta AAAA-MM-DD_HHMM_titulo no horário da Califórnia; só criar com o post
completo (aprovado); depois de criada, nunca mexer nela.
"""
import glob, hashlib, json, os, re, sys, unicodedata
from datetime import datetime
from zoneinfo import ZoneInfo

PASTA_RAIZ = "15NSbgqH7wwM5fTf02_hNEXu0KDm8k5vn"
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def slug(t):
    t = re.sub(r"✋.*?·", "", t)
    t = re.sub(r"·\s*marcar como IA|\(tela cheia\)|ALTERNATIVA\s*·", "", t, flags=re.I)
    t = unicodedata.normalize("NFD", t).encode("ascii", "ignore").decode().lower()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return t[:40].rstrip("-") or "post"


def ref(path):
    p = os.path.join(REPO, path)
    if not os.path.isfile(p):
        return None
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return f"sha256:{h}:{os.path.abspath(p)}"


def main(d):
    agora = datetime.now(ZoneInfo("America/Sao_Paulo"))
    out = []
    for f in sorted(glob.glob(os.path.join(d, "*.json"))):
        p = json.load(open(f))
        # só aprovados que AINDA NÃO estão no Metricool (agendado = já agendado; entregar duplicaria)
        if p.get("status") != "aprovado" or p.get("drive_pasta") or p.get("postar_a_mao") or p.get("metricool"):
            continue
        if not p.get("video_repo") or not p.get("data") or not p.get("hora"):
            continue
        brt = datetime.fromisoformat(f"{p['data']}T{p['hora']}").replace(tzinfo=ZoneInfo("America/Sao_Paulo"))
        if brt <= agora:
            continue
        ca = brt.astimezone(ZoneInfo("America/Los_Angeles"))
        pasta = f"{ca:%Y-%m-%d_%H%M}_{slug(p.get('titulo', ''))}"
        tipo = "Reels"
        legenda = f"{tipo}\n{p.get('legenda', '').strip()}\n"
        if p.get("conteudo_gerado_por_ia"):
            legenda += "\n[Marcar como conteúdo gerado por IA]\n"
        video = ref(p["video_repo"])
        capa_path = os.path.join(os.path.dirname(p["video_repo"]), "video-capa.jpg")
        item = {"post": os.path.basename(f)[:-5], "version_hint": "releia o post antes do update",
                "pasta": pasta, "parentId": PASTA_RAIZ, "legenda_txt": legenda,
                "video_nome": f"{pasta}.mp4", "video_ref": video, "capa_ref": ref(capa_path)}
        if not video:
            item["ERRO"] = f"vídeo não está no repositório: {p['video_repo']}"
        out.append(item)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
