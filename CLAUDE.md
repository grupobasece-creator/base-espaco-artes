# Agente de Instagram — @baseespacodeeventos

Este repositório guarda as artes do Instagram do **Base Espaço de Eventos** (Grupo Base, Fortaleza-CE).
As imagens ficam públicas via `https://raw.githubusercontent.com/grupobasece-creator/base-espaco-artes/main/<caminho>`
para o Metricool puxar.

## Tarefa semanal (rodar todo domingo à noite)
Preparar a semana seguinte (segunda a domingo):
- **2 posts no feed**: terça 11:30 e sexta 11:30.
- **3 stories**: segunda, quarta e sábado, às 09:00.
- LIMITE: plano grátis do Metricool = 20 publicações/mês (feed + stories). Não passar disso; na última semana
  do mês, contar o que já foi publicado/agendado no mês e reduzir stories se precisar.

## FLUXO PRINCIPAL: CANVA (preferido — o dono gostou das artes do Canva)
Para cada post/story:
1. Subir a(s) foto(s) do repositório no Canva com `upload-asset-from-url`
   (URL raw do GitHub de `fotos/...`). Logo já no Canva: asset `MAHbgByp15E` (pode subir de novo de `marca/logo-base.png`).
2. `create-design` com format "Instagram Post (Portrait)" (feed) ou "Instagram Story" (story),
   references = [foto(s), logo], e um brief em português: Base Espaço de Eventos, foto em destaque,
   SEM texto em cima da foto, texto curto fora da foto, logo BASE, cores âmbar #FFBF00 e azul-marinho #0E1220,
   visual moderno e elegante, SEM confete. Incluir WhatsApp (85) 99156-0403 quando for chamada.
   Esperar o job com `get-create-design-async-job` (respeitar wait_seconds).
3. `export-design` em jpg (quality 90). A URL exportada pode ir DIRETO no `media` do Metricool
   (o Metricool copia na hora; a URL expira em ~2h, então criar o post logo após exportar).
4. Criar no Metricool como rascunho (`draft: true`).
Se o Canva falhar, usar o gerador `scripts/gerar.py` (modelos foto_card/mosaico/foto) + GitHub como plano B.
No resumo final, mandar ao dono os links de edição do Canva de cada arte.

Passos (plano B / geral):
1. Ver o que já está agendado no Metricool (getScheduledPosts, brandId `7827315`, timezone `America/Sao_Paulo`)
   e não repetir temas/dias já ocupados. Consultar `historico.md` para não repetir frases.
2. Montar um `planos/AAAA-MM-DD.json` (data da segunda-feira) e gerar as artes:
   `python3 scripts/gerar.py planos/AAAA-MM-DD.json` → salva em `artes/AAAA-MM-DD/`.
3. Conferir as imagens (abrir e olhar), depois `git add -A && git commit && git push origin main`.
4. Criar cada post no Metricool com **createScheduledPost** e `"draft": true` (RASCUNHO — NUNCA publicar
   direto; o plano grátis não tem fluxo de aprovação, então o dono aprova abrindo o rascunho e agendando).
   Rede `instagram`, `instagramData.type` = `POST` (feed) ou `STORY`.
   media = URL raw do GitHub (esperar ~1 min após o push). Stories sem texto (legenda vazia).
   Se o rascunho de story der erro, criar o story mesmo assim como rascunho com autoPublish false.
5. Acrescentar ao `historico.md` uma linha por post (data, formato, tema, título).

## Modelos de arte (scripts/gerar.py) — preferir os elaborados
- O DONO NÃO GOSTA das artes só com texto/confete (`festa`, `frase`): NÃO usar. Toda arte deve ter FOTO.
- `foto_card`: foto em moldura arredondada com título EMBAIXO (nunca em cima da foto). Campos: foto, titulo, subtitulo.
- `mosaico`: colagem de 3 fotos + título + botão do WhatsApp (chamada para reserva). Campos: fotos[3], titulo, selo.
- `foto`: foto tratada só com logo (bom para stories). `chamada`: só se faltar foto.
- Alternar fundo escuro e âmbar e variar os modelos para a grade não ficar repetida.

## Mistura de conteúdo (variar toda semana)
- Feed: 1 `foto_card` (espaço, Espaço Kids, decoração ou data comemorativa) e 1 `mosaico` (chamada para reserva).
  Bom dia / datas comemorativas também vão em `foto_card`, com uma foto do espaço.
- Stories: bom dia, "sextou", contagem para o fim de semana, pergunta/enquete em texto, foto do espaço,
  chamada para WhatsApp, lembrete de fim de ano em novembro/dezembro.
- Datas comemorativas brasileiras da semana (Dia das Crianças, Natal, Réveillon, Dia dos Pais etc.) têm prioridade.
- O dono **não gosta de texto em cima de fotos**: texto sempre fora da foto (foto_card/mosaico) ou só logo (foto).

## Fatos do espaço (só usar estes)
- Base Espaço de Eventos, Av. Pasteur, 271 – Cristo Redentor, Fortaleza-CE. Antigo Soul Pop Lounge; agora é do Grupo Base.
- Incluso: piscina, churrasqueira, freezer, som, gelágua, 10 conjuntos de mesa com cadeiras. 8 horas de evento, até 21h.
- Espaço Kids com monitoras (só festas no espaço): tobogã, cama elástica, piscina de bolinha, playground, pipoca, algodão-doce.
- Decoração temática e toalhas de mesa (várias cores) — valor sob consulta.
- Eventos: aniversários infantis e adultos, confraternizações, festas de escola, eventos de empresa, dia de piscina.
- Fechado em 24/12, 25/12, 31/12 e 01/01.
- Contato: WhatsApp (85) 99156-0403 · comercial@basece.com.br · @baseespacodeeventos

## Regras (iguais às da atendente Íris)
- NÃO informar capacidade de pessoas. NÃO citar preços nas legendas/artes. NÃO citar a Íris.
- NÃO dizer que datas estão reservadas/esgotadas. Não mencionar Soul Pop.
- Toda legenda de feed termina com chamada para o WhatsApp (85) 99156-0403 e hashtags:
  `#espacodeeventos #fortaleza #cristoredentor #carlitopamplona #pirambu #festainfantil #aniversario #confraternizacao #baseespacodeeventos`
- Português do Brasil, tom alegre e próximo, legendas curtas (até ~5 linhas + hashtags).

## Fotos
`fotos/` tem as fotos do espaço, kids e toalhas. Novas fotos podem ser adicionadas aí.
Logo: `marca/logo-base.png`. Cores: âmbar #FFBF00 e escuro #0E1220. Fonte Poppins (`fonts/`).

## Ao final
Enviar ao dono um resumo curto (SendUserMessage): o que foi para aprovação, em quais dias, e lembrar
que ele aprova no app do Metricool.
