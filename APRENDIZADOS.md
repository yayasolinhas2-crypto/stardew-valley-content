# Aprendizados de fora (skills do GitHub + o que bomba em inglês) — 09/11/2026

Pedido da Yasmin: "procure skills no GitHub pra te ajudar a melhorar" e "traga do inglês o que ainda não existe em PT".
As skills foram LIDAS como referência (não instaladas nem executadas). Fontes no fim.

## Regras que viram checklist (aplicar em todo vídeo)
1. **Teste dos 3 segundos:** "nos 3 primeiros segundos a pessoa já está convencida de que precisa ver até o fim?" Antes de efeito, polimento ou música. (herk-edit-kit / short-form-edit)
2. **Laço aberto (open loop):** todo vídeo planta UMA pergunta honesta no começo e fecha ela antes do CTA. No máximo 1 laço principal + 1 secundário. A resposta nunca pode ser "comenta". (short-form-edit)
3. **3 aberturas diferentes** com a mesma fala verdadeira; escolher a que entende sem som e cria mais curiosidade. Anotar o porquê. (short-form-edit)
4. **Primeiro quadro com significado:** ação surpreendente, contradição ou o resultado aparecendo. Nada de vinheta ou tela parada antes do assunto. Nossa capa de 0,7 s fica, mas sempre em cima da gameplay e já dizendo o gancho.
5. **Conclusão ~70%+ e reassistir** são os sinais que mais pesam no TikTok; like é o mais fraco. Vídeo curto, sem ar morto, e um **gatilho de loop** (o fim conversa com o começo). (tiktok-growth)
6. **Tripla menção da palavra-chave** (falada + texto na tela + legenda) pra cair na BUSCA do TikTok. Ex.: "Stardew Valley" + "chá da Caroline" dito, escrito e na 1ª linha da legenda. (tiktok-growth)
7. **Séries / "Parte 2"** fazem a pessoa maratonar e seguir. Se tem view e não tem seguidor → falta motivo pra seguir (perfil + série). (tiktok-growth)
8. **Reaproveitar a ideia, nunca repostar igual:** a cada versão, troca UMA variável grande (gancho, formato, ângulo) e nunca repete a primeira frase. Repost idêntico é punido (regras de originalidade da Meta em 2026). Bate com a regra da Yasmin de usar a mesma gravação até 5 vezes de jeitos diferentes. (content-recycling)
9. **Comentário fixado** e **Stitch/Dueto** com vídeos em alta do nicho ajudam a pegar carona. (tiktok-growth)
10. **Legenda sincronizada pela fala real** (marcação de tempo palavra por palavra a partir da transcrição), não estimada. → melhoria técnica a fazer no nosso gerador. (short-form-edit)
11. **Narração e legenda dizem a fala; o gráfico mostra a PROVA** (o item, o diálogo do jogo, o número). Não repetir a mesma frase 3 vezes na tela. (short-form-edit)
12. **Julgar por padrão de vários vídeos, não por 1 flop.** Volume consistente = mais "tentativas" no algoritmo. (tiktok-growth)

## O que bomba em inglês e quase não existe em PT (pautas)
| Pauta | Por que | Precisa gravar? |
|---|---|---|
| **Os calções roxos do Lewis** (onde acha, o que acontece se puser no Festival/Luau) | tema recorrente com milhares de curtidas | sim: casa do Lewis / festival |
| **"Só existem 5 atalhos na vila"** (mostrar cada um) | dica rápida com muito salvamento | sim: andar pelos atalhos |
| **Glitches/truques de 2026** (só os confirmados na wiki) | categoria em alta | sim |
| **Pesca: dicas que ninguém conta** | sempre procurado | sim: pescando |
| **"Coisas que todo iniciante sofre"** (POV/identificação) | gera envio pra amigo | sim: qualquer começo de save |
| **1.7 (Clint e Sandy casáveis, fazenda nova)** | notícia do momento | já feito (024) |
| **Haunted Chocolatier** (próximo jogo do ConcernedApe) | discutido no TikTok | não (só notícia) |
| **Jogo de tabuleiro de Stardew** | novidade | não |

## Fontes
- Skills: github.com/nateherkai/herk-edit-kit (short-form-edit, short-form-video, video-storytelling) · github.com/social-media-skills/skills (tiktok-growth, content-recycling, caption-writer, hashtag-strategy, thumbnail-design) · github.com/zenstory-ai/video-recap-skills (narração em cima de vídeo) · github.com/ScrapeCreators/social-media-research-skills (achar posts fora da curva; precisa da API paga da ScrapeCreators — não usar sem OK)
- Tendências: páginas de descoberta do TikTok (stardew-valley-purple-shorts, stardew-shortcuts, stardew-valley-glitches-2026), consultadas em 09/11/2026.

## Referências da Yasmin (pasta do Drive, 09/11) — "faça o mais parecido possível"
**Vídeos (4 gravações):** Junimo B (1.7, 26,8 mil curtidas), Daily Cozy Games (1.7, 14 mil), Duda Gaspar (PT, "5 piores eventos aleatórios", 6,2 mil), Alex ("Ultimate Artisan Guide", 69 mil).
- Gameplay em **TELA CHEIA, com zoom no personagem**, pixel nítido. Nada de moldura, caixa de título ou fundo desfocado.
- Legenda **grande, 1–2 palavras por vez**, branca com contorno preto (Duda) ou na **caixa de diálogo do próprio jogo** (Alex).
- **Item/personagem aparece GRANDE no meio da tela** quando é citado.
- Corte a cada 1–2 s; voz de gente falando, animada.
- Notícia (1.7) intercala gameplay com print do Discord / foto do ConcernedApe.
→ Virou o estilo `"estilo": "nativo"` no `tools/gameplay.py` (cena com diálogo usa `"recorte"` pra mostrar a caixa de diálogo grande).

**Carrosséis de foto (30 prints) — no TikTok bombam:** elyslin "tips and tricks" (123 mil curtidas, 94 mil salvos), Graze Junimo "Secret Items" (85 mil, 62 mil salvos), mochiebubbles (11,5 mil), aalaeex "Beginner tips" (8 mil). Formatos:
- **Print da gameplay + 1 dica em caixa branca** ("Foraging always resets on Saturdays", "Pierre's is closed on Wednesdays").
- **Item secreto:** ícone em pixel + nome + Local + Como (✔) + print do lugar.
- **Tabelas no estilo do menu do jogo** (checklist do ano 1, melhores plantações com preço no barril/jarra).
- Guias claros com ícones grandes e setas (Sonniegaming, mochiebubbles, VAL&MADZ).
→ No TikTok, carrossel de foto (Modo Foto) pode render muito; no Instagram, não. Fazer carrossel SÓ pro TikTok nesses estilos.
Regra: copiar o FORMATO (enquadramento, ritmo, tipo de legenda), nunca o texto, a arte nem a marca de outro perfil.

## Referências novas (09/11, 2ª leva — "vida real")
- **realcartoons.ai "I FOUND STARDEW VALLEY IN REAL LIFE"** — 118,9 mil curtidas, 8,5 mil salvos, 31,7 mil envios. VÍDEO de IA em 1ª pessoa, como um parque temático: Pelican Town com gente andando, Gus servindo cerveja, pelúcia Junimo, JojaMart, Pierre's, os calções roxos do Lewis na sopa do Luau. Cortes de 1–2 s. → formato mais forte de todos (vídeo gerado por IA; tem custo).
- **RYoung "If Stardew characters were real (Bachelors)"** — retrato em pixel do jogo → pessoa real (vídeo de IA com movimento leve). Série por solteiro(a).
- **"the poke cards girl" — Personagens na vida real** — retratos realistas (Lewis, Marnie, Gus, Clint, Pam, Harvey) no cenário de cada um.
- **"my farm" — Peixes do Stardew x na vida real** (2,1 mil curtidas) — tela dividida: pixel à esquerda, foto real à direita, "parte 2".
- **Yas cozy games (PT!)** — infográficos de IA "Tudo sobre o deserto" (273 salvos). Concorrente em PT fazendo guia em carrossel.
- Ideias da Yasmin (09/11): festa de aniversário tema Stardew, receitas na vida real, peixes na vida real, flores na vida real, "você sabia que dá pra ter filhos?".

## Rodada diária 09/11 (15:14 BRT)
- Auditoria: 22 vídeos da agenda ok (capa, 1080×1920, áudio, ≤35 s, volume), 1 post por horário, painel = Metricool. Bloqueio: crédito do Gemini do Vitor esgotado (402) — sem voz/imagem/vídeo IA até recarregar.
- Referências: nenhuma nova na pasta desde a 2ª leva.
- Notícias: Switch 2 recebeu upgrade grátis do Stardew (confirmar detalhes antes de usar); ConcernedApe desmentiu boatos do Haunted Chocolatier; 1.7 segue sem data (provável 2027).
- Skills GitHub: busca semanal feita hoje cedo (ver seção acima).

## Pesquisa 09/11 noite (inglês)
- **Segredo que ninguém achou:** ConcernedApe (entrevista IGN dos 10 anos, fev/2026) disse que há uma mensagem secreta que ninguém achou, impossível de achar por datamining, e que "revela algo que nem é mais verdade". Fontes: PC Gamer, GamesRadar, OpenCritic. → vídeo 033.
- **Arroz vira Vinagre no barril** (Reddit viral fev/2026; wiki: 1 Arroz → 2 Vinagre em 10 h). → precisa gravação do barril com arroz.
- **Robin manda a receita da Sopa de abóbora com 7 corações** (wiki confirma). → dá pra juntar com a série receitas.
- **Criador que recria todas as receitas na vida real** tem 88 mil seguidores no TikTok (GamesRadar) → nossa série de receitas tem demanda comprovada.
- Crescimento (guias 2026): ficar num jogo só (✔), gancho no pico da ação, fixar 3 melhores vídeos, responder comentários na 1ª hora, 3–5 hashtags específicas, julgar por % de quem assiste até o fim e não por views.
