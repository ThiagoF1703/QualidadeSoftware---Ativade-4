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
