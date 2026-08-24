# Vídeos de prova social — design

Data: 24/08/2026  
Produto: Kit de Ferramentas Pós-Divórcio  
Página: `public/index.html`

## Objetivo

Substituir os três placeholders de depoimentos da seção `#prova` pelos quatro vídeos reais já publicados na página original de Sirlene Vilela. A seção deve preservar a força visual dos relatos sem carregar quatro players do YouTube durante a abertura da página.

## Abordagens consideradas

1. **Quatro iframes imediatos:** implementação curta, mas aumenta o custo inicial de rede, scripts de terceiros e tempo de interação.
2. **Thumbnail local + player sob demanda:** mantém a prova visível, evita custo do YouTube antes do clique e oferece controle de acessibilidade. Abordagem escolhida.
3. **Carrossel ou modal único:** economiza espaço vertical, mas oculta parte da prova e adiciona navegação, foco e estados desnecessários para quatro itens.

## Componente escolhido

A seção continuará no mesmo ponto da narrativa, entre autoridade e stack do produto. O grid passa de três placeholders para quatro cards em duas colunas no desktop e uma coluna no mobile.

Cada card terá:

- thumbnail WebP original copiada para `public/assets/proof/`;
- botão semântico com nome acessível `Reproduzir depoimento N`;
- ícone de play com contraste suficiente;
- legenda curta `Relato em vídeo · metodologia Cura Energética`;
- proporção `16 / 9`, bordas e cores integradas ao design pine/coral existente.

## Fontes preservadas

| Ordem | YouTube ID | Thumbnail original |
|---|---|---|
| 1 | `NjGfd9zKDf4` | `WhatsApp-Image-2026-08-21-at-22.06.09-3.webp` |
| 2 | `KLxQ5Dr6W8s` | `WhatsApp-Image-2026-08-21-at-22.06.08.webp` |
| 3 | `XrZHAOsWbcs` | `WhatsApp-Image-2026-08-21-at-22.06.09.webp` |
| 4 | `__rkMASEkDc` | `WhatsApp-Image-2026-08-21-at-22.06.09-1.webp` |

## Fluxo de interação

1. A página entrega somente HTML, CSS, JavaScript local e as thumbnails WebP.
2. Ao clicar no botão, o script lê `data-youtube-id`.
3. O botão é substituído por um iframe com `youtube-nocookie.com/embed/{id}?autoplay=1&rel=0`.
4. O iframe recebe `title`, `allow`, `allowfullscreen` e ocupa exatamente a área da thumbnail, sem deslocamento de layout.
5. Se JavaScript estiver indisponível, o botão permanece dentro de um link direto para o vídeo no YouTube, garantindo acesso à prova.

## Performance e privacidade

- Nenhum iframe ou script do YouTube será carregado antes da interação.
- As quatro thumbnails serão servidas localmente pelo Cloudflare Pages.
- O embed usará `youtube-nocookie.com`.
- As imagens terão `loading="lazy"`, `decoding="async"`, largura e altura declaradas.
- O restante da LP, checkout, UTMs, FAQ e CTA sticky permanecerá inalterado.

## Acessibilidade

- Os cards usarão `article` e o acionador será um `button` real.
- O foco terá outline visível e área mínima de 44 × 44 px.
- Cada player terá título específico.
- A troca thumbnail → iframe será anunciada por um texto de status somente para leitores de tela.
- O comportamento será operável por teclado via Enter e Espaço, herdado do botão nativo.

## Tratamento de falhas

- ID ausente ou fora da allowlist: o script não cria o iframe e preserva o link direto.
- Thumbnail ausente: o teste estrutural falha antes do commit e do deploy.
- Falha de rede do YouTube: o usuário ainda terá o link `Abrir no YouTube` na legenda.
- Embed bloqueado pelo navegador: o link direto continuará disponível.

## Contrato de testes

O ciclo TDD começa com testes que devem falhar no HTML atual por ausência dos vídeos. Depois da implementação, os testes devem comprovar:

- quatro IDs exatos presentes;
- quatro thumbnails locais existentes;
- zero placeholder de depoimento pendente;
- zero iframe do YouTube no HTML inicial;
- quatro botões com `data-youtube-id` e nomes acessíveis;
- uso de `youtube-nocookie.com` apenas no JavaScript de ativação;
- fallback para quatro URLs diretas do YouTube;
- teste estrutural anterior continua passando;
- produção responde 200 e contém os quatro IDs após o deploy;
- DOM inicial em produção contém zero iframe e, após um clique, exatamente um iframe com o ID acionado.

## Fora de escopo

- editar ou transcrever o conteúdo dos vídeos;
- inventar nomes, resultados ou falas das participantes;
- criar carrossel, modal ou autoplay sem interação;
- alterar hero, oferta, checkout ou ordem das demais seções.
