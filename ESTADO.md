# Estado atual (passagem de bastão entre chats) — atualizar no fim de cada dia

Atualizado: 13/11/2026 (12:45 Brasília, bom dia).

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
- Auditoria 13/11: tudo ok até 17/11. Corrigido: alarme falso do p002 — campo `manter_no_metricool: true` no painel e tools/auditoria.py ignora esses. 037v e 038v (dom 15/11) ainda AGUARDANDO a Yasmin; se não aprovar até sáb, domingo fica com 2 buracos. Nenhuma gravação nova no Drive (pesca ainda não chegou).
- Pauta 12/11 (rotina 10:23 PST): 037v "A CUECA do Lewis vale 750 fichas" (dom 15/11 17:00) e 038v "Minério TODO DIA: a Pedreira" (dom 15/11 13:00) no painel como AGUARDANDO — preenchem os buracos de domingo. Gravações baixadas do Drive por curl (drive.usercontent.google.com/download?id=...&confirm=t, funciona sem conector). metricool/metricas.json está VAZIO: sem números não dá pra fechar o ciclo; pedir prints.
- Auditoria 12/11: painel = Metricool. Corrigido: p034v marcado "agendado" no painel (id 425585754). Aviso da auditoria "p002 negado mas agendado" é esperado (decisão dela). Drive: painel criou as subpastas 033/031/034/035 em 11/11 (entrega funcionando).
- Buracos na agenda: dom 15/11 13:00 e 17:00 (slots de p001v/p010 foram reaproveitados). A rotina de pauta (10:23 PST) produz 2 vídeos/dia pra preencher.
- HOJE 12/11 (BRT/PST): 12:00/07:00 p006v · 17:00/12:00 p023v · 19:30/14:30 p036v (Instagram pelo Metricool; TikTok À MÃO). Pedir print das views de p024v/p022n (A/B de 11/11).
- 12/11: p002 (6 presentes, sáb 14/11 09:00) fica agendado mesmo repetido — decisão da Yasmin ("deixa, vamos melhorar pros próximos"). Daqui pra frente a rotina diária de pauta barra repetição ANTES de agendar. p034v pedido como post novo à Claude do Vitor.
- 11/11: Yasmin vai gravar HOJE a pesca (Esgoto e/ou píer leste) pro vídeo-resposta "Pegou o lendário de primeira? Sorte ou truque?" (comentários de Davi e Klebson). Quando aparecer na pasta de gravações do Drive: baixar, montar com tools/gameplay.py e mandar pro painel (postar_a_mao, resposta a comentário). Fatos já conferidos: Carpa Mutante = Esgoto, qualquer estação, dificuldade 80, 1.000g; Peixe-Carmesim = fim do píer leste da praia, verão, pesca nível 5, dificuldade 95, 1.500g; lançar mais longe da margem aumenta a chance (wiki Fishing); 1 por save (exceto Isca de Desafio).
- Próxima pauta: 1.7 "maior atualização da história" (notícia Red Rocks, parte 2 do 024v). Precisa gravação/cena da Yasmin ou reusar gameplay.
- Série vida real: 025–030 agendados; 032 filhos espera gravação dela com o marido.
- Pendências dela: decidir com o Vitor Metricool próprio x upgrade; gravar: casa do Lewis (porão), atalhos, pesca, arroz no barril, começo de save, Clint, Sandy, pelúcia na cama.
