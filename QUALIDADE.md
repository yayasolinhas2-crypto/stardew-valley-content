# Checklist de qualidade (todo post passa por isto ANTES de ir pro painel)

Criado em 07/11/2026 depois do feedback da Yasmin: "sem transição, áudio com chiado, voz sem emoção — seja mais criterioso".

## Conteúdo
- [ ] Todo fato com fonte na wiki oficial (EN + nomes oficiais em PT). Nada estimado.
- [ ] Capa = gancho em pergunta/provocação (aprovado: "Você tá usando o barril errado?").
- [ ] CTA "Comenta PALAVRA" no meio E no fim. Envio com pessoa nomeada ("manda pro amigo que…").

## Imagem (automático: `tools/render.js`, `tools/video.js --quadros`)
- [ ] Nada vazando do quadro; frase-ponte inteira; assinatura não encosta em nada.
- [ ] Área segura: texto entre y 290 e 1500, nada a menos de 130 px da direita.
- [ ] Fonte pixel legível (Jersey 10). Nunca Pixelify (C virava O, 5 virava S). Conferir em tamanho real.
- [ ] Sem emoji renderizado dentro da imagem (o servidor não tem fonte de emoji).

## Vídeo
- [ ] **Transição visível** em toda troca de cena (chicote, flash, íris, zoom, cortina — muda a cada cena), com a cena anterior por baixo. Nunca corte seco/fundo preto.
- [ ] **Efeito sonoro** em toda transição (whoosh) e nos destaques (pop, tum, tic, moedas, brilho) — `assets/sfx/`, sintetizados por nós.
- [ ] Duração **≤ 35 s**. Se passar, corta texto (nunca acelera a voz).
- [ ] Fala **≤ 3,0 palavras/s** em cada cena (`tools/narrar.py` só desacelera).
- [ ] Conferir quadros no meio das transições e em cada cena (`tools/video.js --quadros`).

## Voz (Sulafat)
- [ ] Modelo **gemini-2.5-pro-preview-tts** com instrução de interpretação por fala (`[emoção]` no `narracao.json`).
  - O 3.8 Flash pronuncia bem mas fica sem emoção e às vezes LÊ a marcação `[emoção]` em voz alta.
  - O 2.5 Flash fala "Istárdiu" (feio).
- [ ] **Cada fala conferida por transcrição** na hora (`narrar.py`): palavra a mais/a menos → gera de novo.
- [ ] Conferência final do vídeo inteiro (`tools/conferir_narracao.py`): diferenças = 0, "Stardew Valley" em inglês, sem leitura de marcação, chiado = 0.
- [ ] **Sem chiado:** áudio do Gemini chega no limite (pico ~0 dB) e com ruído em −57 dB → folga de 4 dB, filtro 80 Hz–11 kHz, redução de ruído leve, tudo em WAV até o fim, loudnorm em 2 passadas (linear) + limitador, um único AAC 192k.
- [ ] Cota grátis do Gemini: **100 áudios/dia por modelo**. Não gastar em teste à toa; tentativas de conferência contam.

## Antes de mandar pra Yasmin
- [ ] Testes do painel passando (`painel/teste/`), claro e escuro, iPhone.
- [ ] Mandar já corrigido — erro que dá pra pegar em checagem não chega até ela.
