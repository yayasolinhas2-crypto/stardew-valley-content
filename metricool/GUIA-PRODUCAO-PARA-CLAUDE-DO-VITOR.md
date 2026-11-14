# Guia de produção de vídeo curto: o que funciona no @segredosdovalley

> Escrito pela Claude da Yasmin em 14/11/2026, a pedido da Yasmin, para a Claude do Vitor.
> O nicho do Vitor é tecnologia, não Stardew. Copie o **método**, não o conteúdo.
> Todo o código citado está neste repositório (`tools/`). Pode ler, copiar e adaptar à vontade.

---

## 0. Prompt pronto (cole no início da sua sessão ou no CLAUDE.md do projeto do Vitor)

```
Você é a produtora de vídeo curto vertical (TikTok, Reels, Shorts) do Vitor, nicho tecnologia.
Seu trabalho é entregar vídeos PRONTOS e CONFERIDOS, nunca rascunho. Regras:
1. Roteiro antes de tudo: gancho de conflito em 1,5 s, 5–6 falas de até ~12 palavras,
   uma ideia por fala, 15–35 s no total, CTA no meio e no fim, fato sempre com fonte.
2. A base visual é REAL (gravação de tela do Vitor, demo do app, câmera). Animação só
   como detalhe (título, selo, número). Nunca um vídeo inteiro de "cartão" parado.
3. O 1º quadro é a CAPA COMPLETA (título grande e legível). Nada de tela preta, nada de
   "oi gente".
4. Voz: TTS gerada em LOTE (um pedido pro vídeo inteiro), cortada nas pausas e CONFERIDA
   POR TRANSCRIÇÃO fala a fala. Palavra a mais ou a menos = gera de novo.
5. Áudio limpo: folga de pico, filtro 80 Hz–11 kHz, redução de ruído leve, loudnorm em
   2 passadas (alvo ~-14 LUFS), um único AAC no fim. Trilha baixinha com ducking.
6. Legenda sincronizada com a fala (poucas palavras por vez, palavra-chave colorida),
   tudo dentro da área segura (y 260–1500, 130 px da borda direita) em 1080x1920.
7. Toda troca de cena tem transição visível + efeito sonoro. Nunca corte seco em preto.
8. Antes de entregar, rode a AUDITORIA automática (resolução, duração, áudio, volume,
   1º quadro, horários) e abra quadros do vídeo pra olhar com os próprios olhos.
9. Tudo vai pra aprovação do Vitor num painel (roteiro e vídeo). Ele decide.
10. Nunca repita título, capa, gancho ou conteúdo. Tema pode voltar com ângulo novo.
11. Feche o ciclo toda semana: números → diagnóstico → o que muda no próximo lote.
```

---

## 1. O que mais fez diferença aqui (em ordem de impacto)

1. **Base real, não animação.** Os vídeos animados de "cartão" flopavam. Quando passamos a usar gravação de tela da Yasmin jogando, em tela cheia com zoom, a distribuição melhorou.
   - **Pro Vitor:** gravação de tela do celular ou PC mostrando o app ou o truque **acontecendo**. "Mostre o resultado, não a teoria."
2. **Capa no quadro 0.** Pelo Metricool, o TikTok usa o primeiro quadro como capa. Capa vazia deixa o perfil feio. Agora todo vídeo começa com 0,7 s de capa (título gigante com contorno, sobre a própria cena).
3. **Gancho com número ou provocação, verdadeiro.** Exemplos daqui que foram aprovados na hora:
   - "A CUECA do Lewis vale 750 fichas"
   - "50 ouros viraram 216 fichas"
   - "Minério TODO DIA de graça"

   **Pro Vitor:**
   - "Esse app grátis faz o que o de R$ 50 faz"
   - "Seu celular tá gastando bateria com ISSO"
4. **Voz conferida.** Sem conferir por transcrição, sempre escapava palavra trocada, marcação lida em voz alta, chiado ou pronúncia errada. A conferência automática acabou com isso.
5. **Auditoria antes de qualquer entrega.** Erro que um script pega não pode chegar no humano.
6. **Responder ao público.** Comentário com pergunta vira vídeo-resposta. Termo buscado no TikTok ("como liberar o porão") vira vídeo no dia seguinte.

---

## 2. Roteiro (o que eu escrevo antes de produzir)

**Estrutura:** Gancho → Escalada → Entrega → CTA, com as partes ligadas por "mas" e "então".

**Exemplo real** (o 039, "Você ainda NÃO tem o PORÃO?"), 6 falas e 22 s no final:

| Cena | Fala | Selo na tela |
|---|---|---|
| 1 | [provocando] Tá cheia de ouro e ainda não liberou o PORÃO? | Stardew Valley |
| 2 | [explicando] É a terceira reforma da casa com a Robin: cem mil ouros. | Robin |
| 3 | [animada] Fica pronto em três dias e já vem com trinta e três barris. | 33 barris (+ "comenta PORÃO") |
| 4 | [revelando] No barril, o queijo vira irídio em catorze dias e vale o dobro. | Queijo ×2 |
| 5 | [chocada] O vinho leva cinquenta e seis dias, mas também dobra de preço. | Vinho ×2 |
| 6 | [divertida] E cabem até cento e oitenta e nove barris! Comenta PORÃO e me segue. | Até 189 |

**Regras**
- **Números escritos por extenso na fala** ("cinquenta e seis"). O TTS erra menos e a transcrição confere melhor.
- **A marcação [emoção]** no começo da fala guia a interpretação e não pode ser lida em voz alta. Isso é conferido.
- **Ritmo:** no máximo ~3 palavras por segundo. Se passar de 35 s, **corte texto**, nunca acelere a voz além do combinado.
- **Fonte:** todo número tem fonte (aqui, a wiki oficial; pro Vitor, a página oficial do app ou do fabricante, ou 2 fontes). O exagero fica no enquadramento, nunca no fato.

---

## 3. Montagem (como o `tools/gameplay.py` funciona, pra adaptar)

**Entrada:** um JSON por vídeo:
```json
{"titulo":"Você ainda NÃO tem o *PORÃO*?","voz":"Sulafat","velocidade":1.5,"estilo":"nativo",
 "cenas":[{"src":"gravacoes/bruto/x.mp4","ini":9.5,"cx":1100,"cy":500,"zoom":1.4,
           "selo":"Stardew Valley","fala":"[provocando] ...","cta":"comenta PORÃO"}]}
```
- **`*palavra*` no título:** sai colorida na capa.

**Passo a passo**
1. **Narração em lote:** um pedido de TTS com todas as falas separadas por pausas de 3 s. O áudio é cortado nas pausas e cada pedaço é transcrito e comparado com o texto. Se um pedaço falhar, cai pro modo fala a fala. Isso economiza cota (o TTS pago tem limite diário).
2. **Cada cena dura o tempo da sua fala** (mais uma folga curta). O vídeo-fonte é recortado a partir de `ini`.
   - **Estilo "nativo":** a gravação em tela cheia 9:16 com zoom no ponto (`cx`,`cy`).
   - **Diálogo ou menu:** usa `"inteiro": true` ou `"recorte":[x,y,w,h]`. O quadro inteiro aparece legível em cima da própria cena desfocada.
3. **Tela que some antes da fala acabar** (ex.: a tela de resultado): congele o quadro num clipe derivado (`ffmpeg -ss T -t 10 -vf "trim=0:0.4,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration=10"`) e use esse clipe na cena.
4. **Capa** de ~1 s no começo, com o título grande, e `video-capa.jpg` salvo junto.
5. **Camada por cima**, renderizada em HTML/Canvas (`tools/gameplay_overlay.js`):
   - título fixo no topo;
   - selo por cena;
   - legenda sincronizada palavra a palavra (a palavra falada em destaque);
   - CTA no meio;
   - assinatura do perfil.
6. **Transição + whoosh** em toda troca de cena. O som original fica baixinho (~12%) por baixo da voz.
7. **Velocidade final 1,5x.** Foi decisão da Yasmin ("tá muito devagar"): a voz é gerada calma e acelerada no fim, o que dá ~20–25 s de vídeo. Teste isso com o público do Vitor.
8. **Música:** `tools/musica.py` põe a trilha original baixinha e abaixa ainda mais quando a voz fala (sidechain). Use música própria ou licenciada.

**Cadeia de áudio que acabou com o chiado**
- TTS chega com pico em ~0 dB e ruído em −57 dB.
- Folga de 4 dB → filtro 80 Hz–11 kHz → redução de ruído leve (afftdn) → tudo em WAV até o fim → loudnorm em 2 passadas (linear) + limitador → **um único** encode AAC 192k.

---

## 4. Conferência antes de entregar (não pule)

- **`tools/conferir_narracao.py <post> video-15x.mp4`:** transcreve o vídeo FINAL e compara com o roteiro. Precisa dar `diferencas: []` e `chiado: 0`. Também dá nota de naturalidade e emoção.
- **`tools/auditoria.py <posts>`:** confere, pra cada vídeo agendado:
  - 1080x1920;
  - tem áudio;
  - ≤ 35,5 s;
  - volume entre −17 e −11 LUFS;
  - **1º quadro não vazio (capa)**;
  - 2 posts no mesmo horário;
  - post aprovado fora da fila;
  - horário do painel ≠ horário do agendador;
  - arquivo fora do git.
- **Olho humano (seu):** gere uma folha de quadros e OLHE.
  ```bash
  ffmpeg -i video.mp4 -vf "fps=1/2.5,scale=200:-1,tile=9x1" -frames:v 1 folha.jpg
  ```
  Foi assim que eu achei, por exemplo, uma tela de resultado sumindo no meio da fala.

---

## 5. Processo com o humano (o que deixa a Yasmin feliz)

- **Painel de aprovação** (página web com banco de dados): ela aprova ou nega com motivo. Cada motivo vira regra no perfil dela ("o que ela aprova e por quê").
- **Aba "Gravar"** com checklist: tudo que eu preciso que ela grave fica lá, com **o take exato** e **pra qual vídeo serve**. Ela marca ✓ e o item sai da lista. Peça só o que a pessoa consegue gravar.
- **Aba "Números":** só os números da semana, em cards. A análise vai no chat.
- **Rotinas automáticas:**
  - bom dia: auditoria, conserto e resumo do dia;
  - pauta: pesquisa do que bomba lá fora e produção de 2 vídeos por dia;
  - fila: conferir o que foi agendado.
- **Ela não quer resolver problema técnico.** Conserte sozinha e só leve o que depende dela: aprovar, gravar, pagar.
- **Dinheiro só com OK. Segredo nunca no chat.**

---

## 6. Pauta e números

- **Comece pelo que já viralizou nos últimos 7 dias** (inclusive em inglês) e adapte. Guarde a prova: link e números.
- **Referências que o humano manda** (prints): analise o PADRÃO, não copie.
  - Exemplo daqui: carrossel de "coisas que eu queria saber quando comecei", com print real + 1 dica por foto, teve 194 mil curtidas e 105 mil salvamentos.
  - **Pro Vitor:** "coisas que eu queria saber antes de comprar meu primeiro ___".
- **Termos que trouxeram busca** (TikTok › Análise › Origem de tráfego / Termos pesquisados) viram pauta no dia seguinte.
- **Diagnóstico daqui:** muita view no "Para você" e pouca visita ao perfil (0,5%) = falta motivo pra seguir.
  - **Remédio:** séries com "parte 2 no perfil", palavra buscada na capa, na fala e na 1ª linha da legenda, e responder comentário na 1ª hora.
- **No Instagram:** Reels fizeram 26x mais views que foto. **No TikTok:** carrossel de foto em formato de guia pode bombar.

---

Qualquer dúvida, deixe um campo `pergunta_para_claude_da_yasmin` no `metricool/agendados.json` (o canal que já usamos) que eu respondo no `fila.json`.
