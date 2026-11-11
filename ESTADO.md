# Estado atual (passagem de bastão entre chats) — atualizar no fim de cada dia

Atualizado: 11/11/2026 (11:50 Brasília, bom dia).

## Quem / o quê
- Perfil @segredosdovalley (TikTok + Instagram), Stardew Valley em PT-BR. Meta: **10.000 seguidores até 09/12/2026**.
- Yasmin mora na Califórnia (PST = Brasília − 5 h). Joga no Switch 2; tem notebook Windows.
- Ler SEMPRE antes de agir: `CLAUDE.md`, `PERFIL.md` (gosto dela), `PRIORIDADES.md` (ordem e regras), `APRENDIZADOS.md` (o que funciona), `QUALIDADE.md`, `CALENDARIO.md`.

## Ferramentas
- Painel de aprovação: https://claude.ai/artifact/VcfHJ9URGoLjqq9kzcaCX9 (collection `posts`). Tudo pra aprovar vai pro painel, nunca só no chat. Seção "Agendamento no Metricool" (Início) lê a pasta do Drive "Stardew - Para agendar": status.txt (linha "Ultima execucao: AAAA-MM-DD HH:MM", linhas "ERRO <nome-da-subpasta>: <motivo>") e a subpasta "Agendados".
- Agendamento: Metricool do Vitor via a Claude dele (arquivo `metricool/fila.json` com `recado_para_claude_do_vitor`; resposta em `metricool/agendados.json`). Rodadas da Claude do Vitor: 08:41/12:41/17:41/22:41 BRT (às vezes falha — conferir).
- Gemini (voz Sulafat, imagem, vídeo Omni) na conta paga do Vitor; cota diária: TTS flash 100, pro 50 (divididas com o Vitor). Se der 429, usar o outro modelo ou esperar 05:00 BRT.
- ElevenLabs conectado (voz "yaya" = clone da Yasmin) — ela NÃO gostou; usar só Sulafat.
- Montadores: `tools/gameplay.py` (gameplay dela; `"estilo":"nativo"` = tela cheia, aprovado), `tools/vida_real.py` (jogo × vida real), `tools/video_ia.py` (vídeo IA), `tools/auditoria.py`, `tools/exportar_fila.py`.
- Gravações dela: pasta do Drive https://drive.google.com/drive/folders/1s03hdm7bwQFwLvH_fmWJ8iviBai2dpGc (catálogo em `gravacoes/CATALOGO.md`). Referências: https://drive.google.com/drive/folders/1TrVmAiokyeqNUQ3El77jJnivn3CtEl_I

## Rotinas automáticas (corrigido 11/11)
Erro de 10/11: as rotinas abriam chat novo SEM o repositório e não faziam nada (o "bom dia" e a montagem de 031/033/034/035 falharam). Agora disparam em 2 chats fixos que já têm o repositório:
- "Stardew Valley · bom dia + melhoria (chat do dia)" trig_01K2V8D4Uv1KsUMZEygTbtYj, 6:47 PST, no chat session_019zpqkZFfQZKhZX8KiqVa34.
- "Fila do Metricool + Drive (4x/dia)" trig_01JuBetktjCpd1vmPZF8nbBz, 08:07/12:07/17:07/22:07 BRT, no chat session_019zpqka7WYUMdRAR3G3Jkw9 (silenciosa).
- Antigas trig_01YbYmoCs56ZWREsPZkHiRWh e trig_011wFxqfPRbBto1aMxDXJGVQ desligadas. Não usar "chat novo a cada disparo": não tem repositório.
- Claude do Vitor RODA SOZINHA 4x/dia (08:41/12:41/17:41/22:41 BRT; confirmado por print do Vitor em 11/11). Rodada 'sem mudança' não gera commit, então falta de commit NÃO é falha. Ela não lê a pasta do Drive; status.txt é do PC do Vitor.

- "Stardew · pauta da gringa + anti-repetição (diária)" trig_013AkYWhJMKpEFVbBTQSrhdz, 10:23 PST, no chat do bom dia: confere repetidos, pesquisa o que bomba lá fora (com prova), produz 2 vídeos/dia. Pedido da Yasmin 11/11, foco na meta de 10 mil.

## Em andamento
- Auditoria 11/11: tudo ok. Agenda aprovada e agendada até 15/11; 16/11 só tem 06:00 (p027v).
- HOJE 11/11 (A/B remarcado): Yasmin posta À MÃO no TikTok p024v 14:00 BRT (09:00 PST) e p022n 20:30 BRT (15:30 PST); Instagram deles já saiu 10/11. Pedir print de views em 24 h e comparar com p021v/p019v (Metricool).
- Aguardando aprovação no painel: 031v festa (16/11 17:00), 033v segredo dos 10 anos (16/11 12:00), 034v roleta (16/11 19:30), 035v 1º lugar Feira (17/11 12:00).
- Próxima pauta: 1.7 "maior atualização da história" (notícia Red Rocks, parte 2 do 024v). Precisa gravação/cena da Yasmin ou reusar gameplay.
- Série vida real: 025–030 agendados; 032 filhos espera gravação dela com o marido.
- Pendências dela: decidir com o Vitor Metricool próprio x upgrade; gravar: casa do Lewis (porão), atalhos, pesca, arroz no barril, começo de save, Clint, Sandy, pelúcia na cama.
