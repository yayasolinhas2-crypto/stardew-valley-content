# Para a Claude do Vitor: agendar os posts da @segredosdovalley no Metricool

Este repositório é da Yasmin. A **Claude da Yasmin** cuida de todo o planejamento (roteiros, vídeos, agenda).
A Yasmin aprova cada post no painel dela; só o que ela aprovou entra em `fila.json`.
Você (que tem o conector do Metricool na conta do Vitor) **só executa o agendamento**, quando o Vitor pedir.

## O que fazer
1. Leia `metricool/fila.json` (branch `claude/new-session-05qpg7`).
2. Para cada post com `"status": "pronto_para_agendar"` e horário no futuro:
   - Marca do Metricool: **"Segredos do valley"** (não usar outras marcas do Vitor).
   - Data/hora: `quando_brasilia`, fuso **America/Sao_Paulo**.
   - Redes: as de `redes` (vídeo → TikTok + Instagram como Reel; carrossel de fotos → só TikTok).
   - Mídia: os arquivos de `midia_no_repositorio`, **na ordem**. Use estes arquivos originais (nunca um vídeo baixado do TikTok).
   - Texto: `legenda` exatamente como está.
   - Se `conteudo_gerado_por_ia` = true, ative a etiqueta de conteúdo gerado por IA, se a rede/Metricool oferecer.
   - Antes de criar, confira os já agendados no Metricool para **não duplicar** nem colocar 2 posts no mesmo horário.
3. Registre o resultado em `metricool/agendados.json` (crie/atualize a lista): `{"id","rede","quando_brasilia","metricool_post_id","status":"agendado"|"erro","obs"}`.
4. Se puder, salve números dos posts publicados em `metricool/metricas.json` (views, retenção, salvos, compartilhamentos, comentários, seguidores ganhos), com a data da leitura.
5. Faça commit e push só desses arquivos de `metricool/` (`agendados.json`, `metricas.json`). **Não mexa no resto do repositório.**

## Não fazer
- Não alterar legenda, horário ou mídia por conta própria. Se algo não der certo, registre como `"erro"` com o motivo em `obs`; a Claude da Yasmin resolve.
- Não apagar nem mudar posts que já estão agendados no Metricool sem a Yasmin pedir.
- O comentário fixado (`comentario_fixado`) é colocado pela Yasmin à mão depois que o post sai.
