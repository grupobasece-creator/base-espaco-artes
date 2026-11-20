# Agente de Instagram — @baseespacodeeventos

Este repositório guarda as artes do Instagram do **Base Espaço de Eventos** (Grupo Base, Fortaleza-CE).
As imagens ficam públicas via `https://raw.githubusercontent.com/grupobasece-creator/base-espaco-artes/main/<caminho>`
para o Metricool puxar.

## Tarefa semanal (rodar todo domingo à noite)
Preparar a semana seguinte (segunda a domingo):
- **3 posts no feed**: segunda 11:30, quarta 18:30, sexta 11:30.
- **1 story por dia** (7), às 09:00.

Passos:
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

## Mistura de conteúdo (variar toda semana)
- Feed: 1 arte de frase/bom dia ou data comemorativa da semana; 1 de dica para festas, Espaço Kids ou decoração
  (pode ser `tipo: foto` com foto de `fotos/`, sem texto por cima); 1 chamada para reserva.
- Stories: bom dia, "sextou", contagem para o fim de semana, pergunta/enquete em texto, foto do espaço,
  chamada para WhatsApp, lembrete de fim de ano em novembro/dezembro.
- Datas comemorativas brasileiras da semana (Dia das Crianças, Natal, Réveillon, Dia dos Pais etc.) têm prioridade.
- O dono **não gosta de texto em cima de fotos**: com foto, use `tipo: foto` (só logo); texto vai em artes `frase`/`chamada`.

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
