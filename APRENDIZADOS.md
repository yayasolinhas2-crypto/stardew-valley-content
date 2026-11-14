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
8. **(Corrigido 11/11) A Yasmin NÃO quer o mesmo título, capa, gancho ou conteúdo duas vezes (tema, clipe e música podem voltar com ângulo novo). Conferir "Temas usados" no PERFIL.md antes de criar.** O texto antigo abaixo vale só pra reusar a mesma GRAVAÇÃO em temas diferentes. ~~Reaproveitar a ideia, nunca repostar igual:~~ a cada versão, troca UMA variável grande (gancho, formato, ângulo) e nunca repete a primeira frase. Repost idêntico é punido (regras de originalidade da Meta em 2026). Bate com a regra da Yasmin de usar a mesma gravação até 5 vezes de jeitos diferentes. (content-recycling)
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

## Rodada diária 11/11 (06:48 PST)
- Auditoria: 23 vídeos da agenda ok (capa, duração, volume), painel = Metricool até 15/11, nenhum horário duplicado. Rotinas rodando (bom dia + fila 4x/dia). Pasta "Para agendar": só "Agendados", sem status.txt (esperado: é só cópia).
- Referências: nenhuma nova na pasta do Drive desde 09/11.
- Notícia (GamesRadar 03/11 + Gameluster + Xboxygen): no show "Symphony of Seasons" em Red Rocks, o ConcernedApe disse que a 1.7 vai ser a MAIOR atualização da história do jogo, provavelmente em 2027; e Clint e Sandy não serão as únicas novidades. → parte 2 do 024v ("1.7: o Clint vai casar").
- Reddit viral (comicbook/destructoid, datas incertas): dá pra "cobrir" pelúcias na cama; segredo no porão do Lewis (1.6). → precisam gravação dela; conferir na wiki antes.

## Pauta 12/11 (rotina diária, 10:23 PST)
- Gringa (sem prova forte nos últimos 7 dias): a busca não trouxe post datado desta semana. Ranking mensal do r/StardewValley (leadhoot.com/r/stardewvalley, sem data confirmada): xarope de bordo/resina/alcatrão na vida real (~38 mil votos), pedido de casamento com Pingente de Sereia (~23 mil), ConcernedApe e Haunted Chocolatier (~19 mil), info da 1.7 (~17 mil). → reforça a série "vida real" (itens de produção do jogo na vida real) e o gancho da 1.7.
- 3 ideias mais fortes: (1) "Xarope de bordo, resina e alcatrão na VIDA REAL" (série vida real, parte nova); (2) "1.7: a MAIOR atualização da história" (notícia Red Rocks, parte 2 do 024v); (3) "Pedido de casamento com o Pingente de Sereia" (POV, precisa gravação).
- Fato forte achado na wiki: cueca roxa do Lewis na exposição da Feira = desclassificada, mas ele paga 750 fichas (2º lugar = 500). Virou o 037v.
- Download das gravações do Drive funciona por curl direto (sem conector): drive.usercontent.google.com/download?id=<id>&export=download&confirm=t.

## Números TikTok 06–12/11 (print da Yasmin, 13/11)
- 10,8 mil views · 671 curtidas (6,2%) · 103 compartilhamentos (~1%) · 13 comentários · só **57 visitas ao perfil (0,5%)**. Pico ~3,3 mil em 09/11, caindo até ~1,6 mil em 12/11 (lido do gráfico).
- 96,5% vem do Para Você → o algoritmo está distribuindo. Problema é CONVERSÃO: quase ninguém abre o perfil (diagnóstico nº 4 do CLAUDE.md: "tem views, mas ninguém segue").
- Busca (2%) pede: **"onde pescar"**, **"pescando peixe lenda"**, **"como liberar o porão"**. → prioridade: vídeo de pesca/lendário (gravação dela) e "como liberar o porão" (wiki Cellar: 3ª reforma da casa com a Robin, 100.000g, 3 dias, vem com 33 barris e cabe até 189).
- Ações: série com "parte 2 no perfil" e fala final "me segue pra parte 2"; capa/título com a palavra que a pessoa busca; fixar 3 melhores vídeos; bio clara.

## Números Instagram (30 dias até 12/11, print da Yasmin 13/11)
- 2.914 views · 1.916 contas · **22 seguidores** · 93% das views de NÃO seguidores · 68 visitas ao perfil (3,5% de quem viu, 7x melhor que no TikTok) · 1 toque no link da bio.
- **Reels 2,8 mil × posts de foto 108 (26x)**; interações: Reels 111, fotos 15. Confirma a regra: só vídeo. Carrossel de foto no Instagram não vale a pena.
- TikTok tem 3,7x mais alcance (10,8 mil/semana), mas converte pior em visita ao perfil (0,5%). Foco do TikTok: CTA de perfil/série ("parte 2 no perfil").

## Referências novas (13/11, 12 prints da Yasmin) — guias infográficos em FOTO no TikTok
- Todas são carrosséis de guia (arte da @Sonniegaming repostada por outros perfis). Números vistos nos prints: "Stardew Valley Guides" (Indie_content) 68,1 mil curtidas · 45,1 mil salvos · 5.781 envios; allyplaysstardew "Loved Gifts" (tabela de presentes amados) 65,7 mil · 48,3 mil salvos · 4.735 envios; The_Killer_Bunnyy "Money Tips" 34,6 mil · 18,8 mil salvos; "Ore Mining Levels" 8.260 · 5.341 salvos.
- Temas: o que cada máquina transforma (barril, jarra, moinho, prensa de óleo), o que fazer na Chuva Verde, Desidratador + Fruta Antiga/Fruta-estrela, Viveiro de Slime (custo e drops por cor), minério por andar da mina, árvores e torneira (resina, alcatrão, xarope; Torneira Pesada), mel por flor, Fruta Antiga (28 dias, colhe a cada 7), tabela de presentes amados de todos os moradores.
- Padrão: SALVAMENTO altíssimo (salvos ≈ 60–75% das curtidas) → é "guia pra consultar depois". Fundo claro, ícones grandes do jogo, setas, pouco texto. No TikTok, Modo Foto.
- Nosso dado bate: o nosso carrossel "5 peixes lendários" (p004) é o que mais gera comentário no TikTok. No Instagram, foto não pega (Reels 26x).
- Decisão: guias de 1 página no NOSSO visual (assets/guia.css), postados como FOTO só no TikTok e como vídeo de 10 s (gameplay dela no fundo + guia) no Instagram. Nunca copiar arte/texto de outro perfil; ícones da wiki com crédito. Temas que ainda não fizemos: "O que cada máquina faz", "Viveiro de Slime: o que cada cor dá", "Minério: em que andar achar", "Árvores e torneira", "Mel: qual flor rende mais", "Chuva Verde: o que fazer".

## Referências 13/11 (2ª leva, 16 imagens) — "coisas que eu queria saber" com PRINT DA GAMEPLAY
- **saturn_poke "Things I wish I knew when starting stardew valley"** (TikTok, Modo Foto): **194,2 mil curtidas · 104,9 mil salvos · 13 mil envios · 694 comentários**. Formato: print da gameplay (tela cheia, sem moldura) + 1 dica em texto branco GRANDE com contorno, uma por slide (ex.: "o Carrinho Viajante vem sexta e domingo", "não precisa ter pressa nem deixar tudo perfeito"). Simples e pessoal.
- **Seraphinexx "Beginner Tips" (parte 1 e 2)**: cartão de madeira com a dica + print da gameplay embaixo, enfeites em pixel (coração, galinha, cacto). Dicas: não doar tudo ao Gunther, não vender a 1ª Semente Antiga (planta e multiplica no Fabricante de Sementes), não doar o 1º Ovo de Dinossauro (chocar antes), 1º Fragmento Prismático → Espada Galáxia no deserto, irrigador de qualidade cedo, guardar 1 de cada peixe, dias de sorte, calendário (aniversário 8x).
- **Tabela "melhores coisas pro barril e jarra"** (preço por fruta, por estação) e **tabela de presentes amados de todos** (de novo — 2 versões diferentes bombando).
- Conclusão: o que mais salva/compartilha é "dica de iniciante" em lista, com PRINT DA GAMEPLAY real. Encaixa perfeito na regra da Yasmin (90% gameplay dela): tiramos os quadros das gravações dela e fazemos "Coisas que eu queria saber quando comecei Stardew" (parte 1, 2, 3 = série → puxa pro perfil). TikTok em foto, Instagram em vídeo com narração. Fatos sempre conferidos na wiki (não copiar as dicas deles sem conferir).

## Pauta 14/11
- Novo: tools/carrossel_dicas.py (carrossel de FOTOS pro TikTok: quadro da gravação dela em tela cheia + dica em texto grande com contorno, selo da série, JPEG 1080x1920; sem emoji na imagem). Primeiro: p041c (fotos, TikTok) + p041v (vídeo narrado, só Instagram). exportar_fila.py agora aceita o campo `redes` no post do painel.
- Gringa: nada confirmado desta semana. Achado (GamesRadar, data não confirmada): jogadora levou a mãe pro Stardew e a mãe passou 1.000 h se divorciando de todo mundo pra virar INIMIGA da cidade → ideia "Dá pra ser odiada pela cidade inteira?" (conferir regras de divórcio na wiki antes).
