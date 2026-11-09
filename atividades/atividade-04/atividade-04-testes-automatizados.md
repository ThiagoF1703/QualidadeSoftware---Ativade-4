# Atividade 4: Testes Automatizados do LocalEats

**Unidade Curricular:** Qualidade de Software
**Projeto:** LocalEats — <https://local-eats-unisenac.vercel.app/>
**Modalidade:** Dupla

| Integrante | Regra unitária (Parte 1) | Fluxo funcional (Parte 2) |
|---|---|---|
| Thiago Figueiredo | Regra 1 — `pedido_atingiu_valor_minimo(valor_pedido)` | Filtrar restaurantes pela categoria "Brasileira" |
| Gabriel Matiolla | Regra 2 — `calcular_desconto(valor_pedido)` | Pesquisar restaurantes pela localização "Centro" |

---

## 1. Estrutura do projeto

```
atividade-04/
├── atividade-04-testes-automatizados.md
├── relatorio-pytest.txt
├── requirements.txt
├── pytest.ini
├── src/
│   ├── __init__.py
│   └── regras_localeats.py          # Regras 1 e 2 (Parte 1)
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # fixture usuario_autenticado (cria conta de teste)
│   ├── test_regras_localeats.py     # testes unitários (TU)
│   ├── test_localeats.py            # testes funcionais Playwright (TF01, TF02)
│   └── test_restaurante_bdd.py      # steps pytest-bdd (TF03, TF04)
├── features/
│   └── restaurante.feature          # cenários BDD em Gherkin
├── pages/                           # Page Object Model
│   ├── login_page.py
│   ├── home_page.py
│   └── restaurante_page.py
└── evidencias/                      # screenshots gerados pelos testes funcionais
```

### Como executar

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
python -m pytest -v | Tee-Object -FilePath relatorio-pytest.txt
```

> Observação: no Windows, se a pasta do projeto tiver um caminho muito longo, o Playwright pode falhar ao carregar a DLL do `greenlet` (`ImportError: DLL load failed ... O nome do arquivo ou a extensão é muito grande`). A solução é criar o `.venv` em um caminho mais curto.

---

## 2. Identificação das responsabilidades

| ID | Integrante | Tipo | Comportamento verificado | Arquivo e função |
|---|---|---|---|---|
| TU01 | Thiago Figueiredo | Unitário | Pedido acima do mínimo (R$ 50) retorna `True` | `tests/test_regras_localeats.py::test_pedido_acima_do_minimo_retorna_true` |
| TU02 | Thiago Figueiredo | Unitário | Pedido abaixo do mínimo (R$ 29,99) retorna `False` | `tests/test_regras_localeats.py::test_pedido_abaixo_do_minimo_retorna_false` |
| TU03 | Thiago Figueiredo | Unitário (borda) | Pedido exatamente no mínimo (R$ 30) retorna `True` | `tests/test_regras_localeats.py::test_pedido_exatamente_no_valor_minimo_retorna_true` |
| TU04 | Thiago Figueiredo | Unitário (exceção) | Valor negativo gera `ValueError` | `tests/test_regras_localeats.py::test_valor_minimo_rejeita_valor_negativo` |
| TU05 | Gabriel Matiolla | Unitário | Pedido abaixo de R$ 100 (R$ 80) não recebe desconto | `tests/test_regras_localeats.py::test_pedido_abaixo_de_cem_nao_recebe_desconto` |
| TU06 | Gabriel Matiolla | Unitário | Pedido de R$ 150 recebe desconto de R$ 15 | `tests/test_regras_localeats.py::test_pedido_de_cem_ou_mais_recebe_dez_porcento_de_desconto` |
| TU07 | Gabriel Matiolla | Unitário (parametrizado/borda) | Limites 99,99 → 0; 100 → 10; 101 → 10,10 | `tests/test_regras_localeats.py::test_desconto_nos_limites_da_regra` |
| TU08 | Gabriel Matiolla | Unitário (exceção) | Valor negativo gera `ValueError` | `tests/test_regras_localeats.py::test_desconto_rejeita_valor_negativo` |
| TF01 | Thiago Figueiredo | Funcional | Filtro da categoria "Brasileira" exibe somente restaurantes brasileiros | `tests/test_localeats.py::test_filtrar_categoria_brasileira_exibe_somente_restaurantes_brasileiros` |
| TF02 | Gabriel Matiolla | Funcional | Pesquisa por "Centro" exibe somente restaurantes do Centro | `tests/test_localeats.py::test_pesquisar_por_localizacao_centro_exibe_restaurantes_do_centro` |
| TF03 | Thiago Figueiredo | Funcional (BDD) | Consultar as avaliações de um restaurante | `tests/test_restaurante_bdd.py::test_consultar_avaliacoes_de_um_restaurante` |
| TF04 | Gabriel Matiolla | Funcional (BDD) | Adicionar um prato ao carrinho | `tests/test_restaurante_bdd.py::test_adicionar_prato_ao_carrinho` |

Mínimo exigido para dupla: 2 funções, 4 testes unitários e 2 testes funcionais com pelo menos 2 assertions cada. Os itens TU03, TU04, TU07, TU08, TF03 e TF04 são diferenciais opcionais.

---

## 3. Parte 1 — Testes unitários e TDD

Código: [`src/regras_localeats.py`](src/regras_localeats.py) · Testes: [`tests/test_regras_localeats.py`](tests/test_regras_localeats.py)

### TDD de Thiago Figueiredo

**Regra escolhida:** Regra 1 — verificar valor mínimo do pedido, `pedido_atingiu_valor_minimo(valor_pedido)`.

**Primeiro teste escrito:** `test_pedido_acima_do_minimo_retorna_true` — `pedido_atingiu_valor_minimo(50)` deve retornar `True`.

**Por que o teste falhou inicialmente:** a função ainda não existia no módulo `src/regras_localeats.py`. O pytest apresentou um erro de execução na coleta:
```
E   ImportError: cannot import name 'pedido_atingiu_valor_minimo' from 'src.regras_localeats'
1 error in 0.41s
```

**Implementação mínima realizada:** criamos a função retornando sempre `True`, o suficiente para o primeiro teste passar (`1 passed`).
```python
def pedido_atingiu_valor_minimo(valor_pedido):
    return True
```

**Segundo teste escrito:** `test_pedido_abaixo_do_minimo_retorna_false` — `pedido_atingiu_valor_minimo(29.99)` deve retornar `False`. Ele falhou (Red) com `E  assert True is False`, o que forçou a implementação da comparação real: `return valor_pedido >= 30` (`2 passed`).

**Melhoria ou refatoração realizada:** depois de escrever os testes de borda (R$ 30 exatos) e de valor negativo com `pytest.raises` — este último falhou com `Failed: DID NOT RAISE ValueError` —, o código foi reorganizado: o valor 30 virou a constante `VALOR_MINIMO_PEDIDO` e a verificação de negativo foi extraída para a função `_validar_valor_pedido`, reutilizada também pela regra do Gabriel. A suíte inteira foi executada novamente e permaneceu aprovada.

### TDD de Gabriel Matiolla

**Regra escolhida:** Regra 2 — calcular o desconto do pedido, `calcular_desconto(valor_pedido)`.

**Primeiro teste escrito:** `test_pedido_abaixo_de_cem_nao_recebe_desconto` — `calcular_desconto(80)` deve retornar `0`.

**Por que o teste falhou inicialmente:** a função `calcular_desconto` ainda não existia; o pytest interrompeu a coleta com:
```
E   ImportError: cannot import name 'calcular_desconto' from 'src.regras_localeats'
```

**Implementação mínima realizada:** função retornando sempre `0` (`3 passed` somando os testes da Regra 1).
```python
def calcular_desconto(valor_pedido):
    return 0
```

**Segundo teste escrito:** `test_pedido_de_cem_ou_mais_recebe_dez_porcento_de_desconto` — `calcular_desconto(150)` deve retornar `15`. Falhou com `E  assert 0 == 15`. A implementação foi ajustada para `if valor_pedido >= 100: return valor_pedido * 0.1`, e o teste passou.

**Melhoria ou refatoração realizada:** ao acrescentar o teste parametrizado dos limites (99,99 / 100 / 101), o caso de R$ 101 falhou por erro de ponto flutuante (ver seção 6). A função foi refatorada para usar as constantes `VALOR_MINIMO_PARA_DESCONTO` e `PERCENTUAL_DESCONTO`, arredondar o desconto em 2 casas (`round(..., 2)`, por representar dinheiro) e reutilizar `_validar_valor_pedido` para gerar `ValueError` com valores negativos. Toda a suíte foi executada novamente: `10 passed`.

---

## 4. Parte 2 — Testes funcionais com Playwright

Os fluxos foram definidos depois de explorar o LocalEats. Todas as páginas exigem sessão (o `auth.js` redireciona para `login.html` sem `userId`), então a fixture `usuario_autenticado` ([`tests/conftest.py`](tests/conftest.py)) **cria uma conta nova pela interface** (aba "Criar Conta" → "Registrar") com e-mail único gerado por `uuid`. Assim cada teste é independente e não depende de dados de outra execução.

Nenhum teste usa `time.sleep`: as esperas são feitas pelos próprios locators e pelas assertions `expect(...)`, que repetem a verificação até passar ou atingir o timeout. Os locators ficam centralizados em Page Objects ([`pages/`](pages/)).

### TF01 — Filtrar por categoria (Thiago Figueiredo)

- **Fluxo:** criar conta → aguardar a grade de restaurantes → clicar no botão de categoria **"Brasileira"**.
- **Locators:** `get_by_role("button", name="Brasileira", exact=True)`, `locator("#restaurantGrid").get_by_role("link")`.
- **Assertions (4):**
  1. o botão "Brasileira" fica com a classe `active`;
  2. a grade exibe exatamente 2 restaurantes (Restaurante Sabor 5 e Restaurante Sabor 8, conforme dados atuais do sistema);
  3. cada card exibido contém o texto "Brasileira";
  4. nenhum card exibido contém "Japonesa".
- **Evidência:** `evidencias/tf01_categoria_brasileira.png`.

### TF02 — Pesquisar por localização (Gabriel Matiolla)

- **Fluxo:** criar conta → aguardar a grade → preencher o campo "Buscar por culinária ou localização..." com **"Centro"** → clicar em **"Buscar"**.
- **Locators:** `get_by_placeholder("Buscar por culinária ou localização...")`, `get_by_role("button", name="Buscar", exact=True)`.
- **Assertions (4):**
  1. a grade exibe exatamente 4 restaurantes;
  2. cada card exibido contém "Centro";
  3. nenhum card exibido contém "Zona Sul";
  4. o campo de busca mantém o valor "Centro".
- **Evidência:** `evidencias/tf02_pesquisa_centro.png`.

### Execução em caso de falha

O [`pytest.ini`](pytest.ini) ativa `--screenshot=only-on-failure` e `--tracing=retain-on-failure`: quando um teste funcional falha, o screenshot e o trace do Playwright ficam em `evidencias/test-results/` (o trace pode ser aberto com `python -m playwright show-trace <arquivo>.zip`).

---

## 5. Diferencial — BDD com pytest-bdd e Page Object Model

Cenários em Gherkin: [`features/restaurante.feature`](features/restaurante.feature) · Steps: [`tests/test_restaurante_bdd.py`](tests/test_restaurante_bdd.py)

```gherkin
# language: pt

Funcionalidade: Detalhes de um restaurante
  Como cliente do LocalEats
  Quero consultar um restaurante
  Para conhecer suas avaliações e montar meu pedido

  # Responsável: Thiago Figueiredo
  Cenário: Consultar as avaliações de um restaurante
    Dado que estou autenticado no LocalEats
    E que abri os detalhes do restaurante "Restaurante Sabor 5"
    Quando seleciono a aba "Avaliações"
    Então a aba "Avaliações" deve estar selecionada
    E a avaliação "Muito bom, recomendo fortemente!" deve ser apresentada

  # Responsável: Gabriel Matiolla
  Cenário: Adicionar um prato ao carrinho
    Dado que estou autenticado no LocalEats
    E que abri os detalhes do restaurante "Restaurante Sabor 5"
    Quando adiciono o prato "Prato Especial 0" ao carrinho
    Então o carrinho deve indicar "1 itens"
    E o carrinho deve listar "1x Prato Especial 0"
```

O arquivo `.feature` descreve apenas comportamento; os detalhes técnicos (locators e `expect`) ficam nos steps Python, que reutilizam os Page Objects `HomePage` e `RestaurantePage`. O passo "que abri os detalhes do restaurante" navega **clicando no card** da página inicial, e não por URL direta.

---

## 6. Falha encontrada e corrigida

Durante o TDD da Regra 2, o teste parametrizado `test_desconto_nos_limites_da_regra[101-10.1]` falhou:

```
E       assert 10.100000000000001 == 10.1
E        +  where 10.100000000000001 = calcular_desconto(101)
FAILED tests/test_regras_localeats.py::test_desconto_nos_limites_da_regra[101-10.1]
```

**Causa:** `101 * 0.1` em ponto flutuante resulta em `10.100000000000001`. O teste com R$ 150 não revelou o problema porque `150 * 0.1` resulta exatamente em `15.0`.
**Correção:** o desconto passou a ser calculado como `round(valor_pedido * PERCENTUAL_DESCONTO / 100, 2)`. O esperado do teste **não** foi alterado para "passar"; a implementação foi corrigida.

### Falha nos testes funcionais (fixture de autenticação)

Na primeira execução completa, os 4 testes funcionais falharam no mesmo ponto, `tests\conftest.py:23` (2 como `ERROR` no setup da fixture e 2 BDD como `FAILED`):

```
E       AssertionError: Page URL expected to be '**/static/index.html'
E       Actual value: https://local-eats-unisenac.vercel.app/static/index.html
```

**Causa:** a conta era criada e o sistema redirecionava corretamente para a página inicial (o snapshot mostrava "Olá, Dupla"), mas no Playwright para Python `expect(page).to_have_url("...")` com texto compara a URL **exata**; o `**` não funciona como curinga nessa assertion. Ou seja, era um defeito do teste, não do LocalEats.
**Correção:** a assertion passou a usar expressão regular: `expect(page).to_have_url(re.compile(r"/static/index\.html$"))`. Depois disso o relatório foi gerado novamente.

### Observações sobre o LocalEats identificadas na exploração

Não fazem parte dos testes obrigatórios, mas foram percebidas ao estudar o sistema:

1. **Busca por culinária não funciona:** o campo diz "Buscar por culinária ou localização...", mas o botão "Buscar" envia apenas o filtro `location`. Pesquisar "Italiana" retorna "Nenhum restaurante encontrado.", mesmo havendo restaurantes italianos. Por isso o TF02 usa uma localização.
2. **Abas sem efeito visual:** os botões "Cardápio" e "Avaliações" trocam a classe `active`, mas o CSS não oculta o conteúdo da aba inativa, então cardápio e avaliações aparecem juntos. Por isso o TF03 verifica a aba selecionada e não só a visibilidade da avaliação, que passaria mesmo sem o clique.
3. **Texto do carrinho:** o contador exibe "1 itens" (concordância incorreta no singular). O TF04 verifica o texto como ele é exibido hoje.

---

## 7. Explicação individual

### Thiago Figueiredo — TF01 (`test_filtrar_categoria_brasileira_exibe_somente_restaurantes_brasileiros`)

O teste verifica se o filtro de categoria da página inicial realmente restringe a lista de restaurantes. No **Arrange**, a fixture `usuario_autenticado` cria uma conta de teste pela tela "Criar Conta", e espero a grade carregar com `expect(cards.first).to_be_visible()` — isso evita clicar no filtro enquanto a carga inicial ainda está em andamento. No **Act**, clico no botão "Brasileira", localizado pelo papel (`get_by_role("button", name="Brasileira", exact=True)`); o `exact=True` evita confundir com outros botões. No **Assert**, uso quatro verificações: o botão fica com a classe `active`; a grade passa a ter exatamente 2 cards; todos os cards contêm "Brasileira"; e nenhum contém "Japonesa". A contagem sozinha não bastaria, porque 2 cards de outra categoria também passariam; por isso conferi também o conteúdo. Como o `expect` repete a verificação até o timeout, não precisei de `time.sleep`, mesmo com a grade passando por "Buscando..." antes de mostrar o resultado.

### Gabriel Matiolla — TU07 (`test_desconto_nos_limites_da_regra`)

Este teste usa `@pytest.mark.parametrize` para verificar a regra de desconto nos valores próximos ao limite de R$ 100: R$ 99,99 não recebe desconto, R$ 100 recebe exatamente R$ 10 e R$ 101 recebe R$ 10,10. A parametrização gera três casos independentes no relatório, e cada um mostra seus próprios dados de entrada. Foi o caso de R$ 101 que revelou a falha de ponto flutuante (`10.100000000000001 == 10.1`), que o teste com R$ 150 não tinha mostrado. Em vez de mudar o valor esperado, corrigimos a função para arredondar o desconto em duas casas. Isso mostra a importância de testar os limites da regra e não apenas um valor "confortável".

---

## 8. Relatório da execução

O relatório foi gerado com:

```powershell
python -m pytest -v | Tee-Object -FilePath relatorio-pytest.txt
```

Arquivo: [`relatorio-pytest.txt`](relatorio-pytest.txt). Ele lista os 14 testes coletados (10 execuções unitárias, contando os 3 casos parametrizados do TU07, e 4 funcionais), o resultado de cada um e o resumo final. Todos os IDs da tabela da seção 2 aparecem no relatório.

**Resultado final:** `14 passed, 1 warning`. O aviso (`PytestRemovedIn10Warning` sobre a fixture `base_url`) vem do plugin `pytest-base-url`, instalado como dependência do `pytest-playwright`, e não do código da dupla; ele não afeta o resultado dos testes.

---

## 9. Uso de inteligência artificial

**Ferramenta utilizada:** Claude (Anthropic), via Claude Code.

**Como a ferramenta foi utilizada:** para resumir o material das aulas 11, 12 e 14 e a atividade, para explorar o código público do LocalEats (`login.html`, `api.js`, `auth.js`, `app.js`, `restaurant.html`) e descobrir textos e elementos reais, e para propor a estrutura do projeto, os testes, os Page Objects e os cenários BDD. Os ciclos Red/Green foram executados um teste por vez, e a saída real do pytest foi registrada neste documento.

**Uma sugestão que precisou ser alterada ou rejeitada:**
1. A IA propôs inicialmente R$ 110 como exemplo do erro de ponto flutuante no desconto. Ao executar, `110 * 0.1` resultou exatamente em `11.0`, então a sugestão estava errada. Testamos vários valores e substituímos por R$ 101, que realmente produz `10.100000000000001`.
2. A IA sugeriu `expect(page).to_have_url("**/static/index.html")` na fixture de login. Na execução real os 4 testes funcionais falharam, porque no Python essa assertion compara o texto exato da URL. Trocamos por `re.compile(r"/static/index\.html$")` (ver seção 6).
3. Para o cenário de avaliações, a sugestão inicial verificava apenas se o comentário estava visível. Ao analisar o CSS do sistema, vimos que a aba de avaliações nunca fica oculta, então essa assertion passaria mesmo sem clicar na aba. Ela foi complementada com a verificação da classe `active` nos botões das abas.

**Como o código sugerido foi verificado:** executando o pytest a cada etapa do TDD e conferindo a falha esperada antes de cada implementação; conferindo locators e textos diretamente no HTML e no JavaScript do LocalEats; executando a suíte completa para gerar o `relatorio-pytest.txt`; e revisando cada arquivo para entender o que faz cada locator e cada assertion.
