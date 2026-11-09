# Checklist de qualidade (todo post passa por isto ANTES de ir pro painel)

Criado em 07/11/2026 depois do feedback da Yasmin: "sem transição, áudio com chiado, voz sem emoção — seja mais criterioso".

## Conteúdo
- [ ] **Nosso estilo, nunca cópia** (regra da Yasmin, 08/11): referência de outro perfil vira só tema; visual, texto e dados são nossos.
- [ ] Todo fato com fonte na wiki oficial (EN + nomes oficiais em PT). Nada estimado.
- [ ] Capa = gancho em pergunta/provocação (aprovado: "Você tá usando o barril errado?").
- [ ] CTA (regra da Yasmin 08/11): **sem "comenta PALAVRA"**. Meio: "♥ curte se te ajudou". Fim: "me segue pra mais dicas".

## Imagem (automático: `tools/render.js`, `tools/video.js --quadros`)
- [ ] Nada vazando do quadro; frase-ponte inteira; assinatura não encosta em nada.
- [ ] Área segura: texto entre y 290 e 1500, nada a menos de 130 px da direita.
- [ ] Fonte pixel legível (Jersey 10). Nunca Pixelify (C virava O, 5 virava S). Conferir em tamanho real.
- [ ] Sem emoji renderizado dentro da imagem (o servidor não tem fonte de emoji).

## Vídeo
- [ ] **Transição visível** em toda troca de cena (chicote, flash, íris, zoom, cortina — muda a cada cena), com a cena anterior por baixo. Nunca corte seco/fundo preto.
- [ ] **Efeito sonoro** em toda transição (whoosh) e nos destaques (pop, tum, tic, moedas, brilho) — `assets/sfx/`, sintetizados por nós.
- [ ] Duração **≤ 35 s**. Se passar, corta texto (nunca acelera a voz).
- [ ] Fala gerada a ≤ 3,0 palavras/s e o vídeo final acelerado **1,5x** (decisão da Yasmin, 07/11: "tá muito devagar"). Resultado: ~21–23 s, fala média ~3,3/s. Conferir a transcrição DO ARQUIVO 1,5x (`conferir_narracao.py post video-15x.mp4`).
- [ ] Conferir quadros no meio das transições e em cada cena (`tools/video.js --quadros`) — ele agora avisa ⚠ quando algo vaza do quadro.
- [ ] **Legenda sincronizada** (class `com-legenda` no #stage): palavra falada em dourado, palavra-chave em destaque, abaixo do quadro (quadro de vídeo com 1040 px de altura).

## Vídeos com gameplay da Yasmin (`tools/gameplay.py`)
- [ ] **Capa** de ~0,7 s no começo (título grande); `video-capa.jpg` gerada junto.
- [ ] Sem tela parada ou escura: rodar `freezedetect`/`blackdetect` e escolher trechos sem transição de mapa nem menu parado (menu só quando a fala é sobre ele).
- [ ] Curto e sem frase solta: cada fala tem que dizer algo útil que a imagem mostra.
- [ ] Gameplay recortada (centro, sem esticar, pixel nítido) dentro da moldura de madeira; fundo = a própria cena desfocada.
- [ ] Título-gancho fixo no topo, selo por cena, legenda sincronizada, CTA "comenta PALAVRA" no meio, assinatura.
- [ ] Som do jogo baixinho (12%) por baixo da voz; whoosh nas trocas.
- [ ] Se a gravação acabar antes da fala, congela o último quadro (o script para se a duração da cena não bater).
- [ ] Gravações brutas ficam em `gravacoes/bruto/` (fora do git, ~400 MB).

## Voz (Sulafat)
- [ ] Voz Sulafat (Gemini). Nada de cochicho/sussurro: emoção animada, empolgada, chocada. (Clone ElevenLabs testado e recusado em 09/11.)
- [ ] Modelo **gemini-2.5-pro-preview-tts** com instrução de interpretação por fala (`[emoção]` no `narracao.json`).
  - O 3.8 Flash pronuncia bem mas fica sem emoção e às vezes LÊ a marcação `[emoção]` em voz alta.
  - O 2.5 Flash fala "Istárdiu" (feio).
- [ ] **Cada fala conferida por transcrição** na hora (`narrar.py`): palavra a mais/a menos → gera de novo.
- [ ] Conferência final do vídeo inteiro (`tools/conferir_narracao.py`): diferenças = 0, "Stardew Valley" em inglês, sem leitura de marcação, chiado = 0.
- [ ] **Sem chiado:** áudio do Gemini chega no limite (pico ~0 dB) e com ruído em −57 dB → folga de 4 dB, filtro 80 Hz–11 kHz, redução de ruído leve, tudo em WAV até o fim, loudnorm em 2 passadas (linear) + limitador, um único AAC 192k.
- [ ] Cota: conta do Vitor é PAGA (Tier 1), mas o **2.5 Pro TTS tem 50 pedidos/dia no Tier 1, dividido com o Vitor**. Por isso `narrar.py` usa o **modo lote**: o vídeo inteiro num pedido só (pausas de 3 s entre falas), corte nas pausas e conferência de cada pedaço por transcrição; se falhar, cai no modo fala a fala. Não gastar em teste à toa; tentativas de conferência contam.

## Imagens geradas por IA
- [ ] Texto/placas em português; revisar cada imagem (a IA pode inventar nomes ruins — refazer).
- [ ] Marca "imagem gerada por IA" no slide + lembrar a Yasmin de ativar a etiqueta de IA no TikTok/Instagram.

## Capa no perfil (08/11)
- [ ] O PRIMEIRO QUADRO de todo vídeo é a capa completa (título grande). Pelo Metricool o TikTok usa o quadro 0 — capa vazia deixa o perfil feio (aconteceu com o barril).
- [ ] Tudo que importa na capa fica no centro (recorte 3:4 da grade: y 240–1680).

## Música
- [ ] Todo post sai com música (`tools/musica.py`): vídeo narrado = trilha baixinha que abaixa quando a voz fala; carrossel = vídeo de fotos com trilha. Nunca a trilha do jogo.
- [ ] Variar a trilha entre posts seguidos (primavera/verão/outono/inverno conforme o tema).
- [ ] Fotos de carrossel em vídeo: renderizar com `VIDEO=1` (sem "arrasta pro lado").

## Antes de mandar pra Yasmin
- [ ] "Nada esquisito, sempre melhorando": cada lote tem que sair melhor que o anterior. Comparar com o último aprovado.
- [ ] Testes do painel passando (`painel/teste/`), claro e escuro, iPhone.
- [ ] Mandar já corrigido — erro que dá pra pegar em checagem não chega até ela.
