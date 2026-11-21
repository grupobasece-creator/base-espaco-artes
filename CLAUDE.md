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

## FLUXO PRINCIPAL: EDITAR OS MODELOS DO DONO NO CANVA (aprovado em 20/11)
NUNCA usar `create-design` (a IA do Canva gerou letras sobrepostas e texto em inglês — o dono odiou).
Sempre COPIAR um modelo aprovado e EDITAR elemento por elemento:
- Story → modelo `DAHbgDzuiAk` ("Story Base - Domingo de sol"): fundo de piscina, moldura branca,
  3 linhas de texto grande (ids LBcS5fYkdzcg0b6G, LBM715FRrrgDDmZr, LB9BpkdnlPyq928T), coração, logo e WhatsApp.
  Trocar só as 3 linhas (até ~10 letras cada) — ex.: "Sextou &" / "Festa &" / "Piscina"; "Reserve" / "sua" / "data".
- Post → modelo `DAHbgLp4zng` ("Post Base - Festa na Piscina"): ilustrado pool party. Textos editáveis:
  LBrwW8wmDjjrzQSS (linha pequena de cima), LBXl29X0zjb1jVDw (título grande, 1 palavra curta),
  LBLQwcLBjBsqMZk3 (subtítulo manuscrito), LBNkgFkc83941LhV, LB966gr685JPdppZ, LBCDnsKfgf6ZL82D, LBmQ4cVPQkFV7SCh
  (4 linhas do meio, curtas), LBdFQmknsxq5lNH4 (endereço + WhatsApp — manter). Logo em faixa escura — manter.
Passos: `copy-design` → `read-design` com open_transaction (ver locator_ids e thumbnail) → `edit-design` keep_open
com replace_text (e format_text para diminuir fonte se o texto for maior) → OLHAR a thumbnail devolvida: nada
sobreposto, tudo em português → corrigir se preciso → `edit-design` commit → `update_title` com data/tema →
`export-design` jpg quality 90 (post: width 1080) → criar rascunho no Metricool na hora (URL expira).
Pode usar `update_fill` para trocar o fundo do story por uma foto do espaço (upload-asset-from-url de fotos/)
— só se o texto continuar legível.
Logo nova no Canva: asset `MAHbgJW0Yq0` (branca). Fotos do espaço: subir de `fotos/` via raw GitHub.
Variar os textos toda semana (ver historico.md). Mandar ao dono os links do Canva de cada arte.

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
