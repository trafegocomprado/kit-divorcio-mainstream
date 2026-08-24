# Vídeos de prova social — design

Data: 24/08/2026

Produto: Kit de Ferramentas Pós-Divórcio

Página: `public/index.html`

Relatório: `outputs/kit-divorcio/reports/pagemind_kit-divorcio_m1m2m3_report.*`

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

## Correção do relatório M1+M2+M3

O relatório HTML, a versão paginada e o PDF serão regenerados depois da atualização da LP. A correção será factual, sem inventar nomes, falas ou resultados que não estejam disponíveis.

### M1 — Diagnóstico

- Registrar explicitamente que a página original contém quatro depoimentos em vídeo do YouTube.
- Preservar o score original de prova social em `4/10` e a matriz em `7/31`, pois o analyzer já havia contabilizado a existência do formato em vídeo; a penalização decorre da falta de nome, transcrição, data e resultado verificável no texto, além da posição precoce.
- Substituir qualquer leitura que sugira ausência de prova por: `prova existente, pouco contextualizada e usada cedo demais`.
- Adicionar um inventário compacto dos quatro IDs e explicar que a correção é reposicionamento + contexto, não criação de prova do zero.

### M2 — Oferta

- Manter o diagnóstico global da oferta enquanto garantia, âncora e mecanismo continuarem pendentes.
- Retirar `prova inexistente` ou `validar prova` da lista de bloqueios.
- Trocar por `contextualizar os quatro vídeos existentes com identificação e síntese autorizada`.
- Atualizar a decisão de ecossistema para priorizar mensagem, contexto da prova e garantia antes de order bump ou upsell.

### M3 — LP nova

- Registrar os quatro vídeos como elementos de prova preservados da LP original.
- Alterar a seção construída de `três placeholders` para `quatro cards de vídeo com carregamento sob demanda`.
- Atualizar melhorias, decisões do builder e pendências P0.
- Manter seis grupos operacionais de P0 — garantia, credenciais, contexto/transcrição autorizada dos vídeos, mecanismo, acesso vitalício e URLs legais — substituindo a exigência de novos depoimentos pela contextualização da prova existente.
- Substituir a frase `a prova ainda precisa ser real` por `a prova existe; ainda precisa de contexto textual autorizado`.
- Atualizar a captura da LP nova no relatório depois do deploy.

### PDF

- Regenerar o PDF a partir do HTML paginado corrigido.
- Inspecionar todas as páginas rasterizadas, com atenção às páginas de diagnóstico, oferta e comparativo antes/depois.
- Rejeitar páginas órfãs, cards cortados, texto fora da área ou imagens em branco.

### Testes adicionais do relatório

- os dois HTMLs gerados não podem conter `a prova ainda precisa ser real`;
- o relatório deve mencionar `4 depoimentos em vídeo` e os quatro IDs;
- o M2 deve reconhecer `prova existente`;
- o M3 deve mencionar `quatro cards de vídeo` e carregamento sob demanda;
- o PDF deve ter texto em todas as páginas e zero blocos fora da área;
- a inspeção visual deve confirmar ausência de cortes e páginas órfãs.

## Fora de escopo

- editar ou transcrever o conteúdo dos vídeos;
- inventar nomes, resultados ou falas das participantes;
- criar carrossel, modal ou autoplay sem interação;
- alterar hero, oferta, checkout ou ordem das demais seções.
- recalcular retroativamente o score original sem nova evidência textual;
- apresentar os vídeos como prova específica do Kit quando a página original os descreve como relatos da metodologia Cura Energética aplicada ao Divórcio Energético.
