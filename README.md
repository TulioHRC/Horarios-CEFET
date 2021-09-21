# Horarios-CEFET

### O que é o projeto?

Nosso objetivo é criar um gerador de horários para as matérias das turmas no CEFET-MG. Primeiramente criando horários apenas para as matérias do DEMAT, do técnico. Criando os horários de forma com que grande parte das preferencias de tanto os alunos como dos professores seja atendida.

### Resultado esperado

Gerar horários aleatoriamente, porém seguindo o maior número de preferencias possíveis.


## Explicando
Há dois programas, o "runner" e o "functions". O runner é o principal, enquanto o functions possui apenas as bibliotecas necessárias para fazer o programa funcionar
### Runner
Até a linha xx o programa possui o objetivo é de armazenas as informações da planilha de uma forma que facilite o posterior processamento da informação.
Depois disso se cria o primeiro node e o frontier, que será usado para expandir os nodes.
Para espandir os nodes fazemos da seguinte forma.
- Selecionamos dentro do frontier o node com menor custo
- quardamos suas informações em uma variável e depois excluimos esse node do frontier para que não haja lupins
- Colocamos todos os possíveis estados que podem serivar do inicial
- Avaliamos se esses possíveis estados são válidos, respeitam as regras e também determinamos o seu custo
- Criamos os nodes com as informações obtidas, os que forem válidos.
- Adicionamos os nodes válidos ao frontier




## Release Notes
### 0.0.1v
- Demonstranção de utilização do pandas
- Criação da planilha esperada com o código de prefêrencias
- Para a criação desse código foram usados conhecimentos obitidos no curso CS50 de inteligencia artifical com Python que está disponível no canal no YouTube CS50. Pode ser necessário ver a aula Search para auxiliar a compreensão do código