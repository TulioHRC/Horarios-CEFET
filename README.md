# Horarios-CEFET

### O que é o projeto?

Nosso objetivo é criar um gerador de horários para as matérias das turmas no CEFET-MG. Primeiramente criando horários apenas para as matérias do DEMAT, do técnico. Criando os horários de forma com que grande parte das preferencias de tanto os alunos como dos professores seja atendida.

### Resultado esperado

Gerar horários aleatoriamente, porém seguindo o maior número de preferencias possíveis.

### Notas
- Na adição de preferencias é possível adicionar um intervalo de horários que serão preferidos pelo professor, este "entre" considera os
dois valores já selecionados
- Cerca de 1000 linhas de código

### Próximas atualizações
- Rooms Logic
- Normas trabalhistas
- Excel styling

### Explicação da lógica por trás do programa
O que o projeto recebe:
-  horários em que os professores preferem dar aula
-  horários em que o professor prefere não dar aulas
-  horarios em que o professor não pode dar aulas por quaisquer limitações

O que o programa valoriza:
-   Além de buscar seguir, mas não necessariamente, as preferências acima solicitadas, o nosso projeto possui outras formas de avaliar se um determinado horário é bom ou ruim
1) Horários de uma mesma matéria seguidos são valorizados.
2) Os primeiros horários da manhã e da tarde, bem como os últimos tendem a não ser preenchidos.
3) Quanto maior a quantidade de horários em um dia, mais desvalorizado esse horário se torna, isso é usado para fazer com que eles fiquem mais distribuidos pelos dias da semana, ocorrendo uma desvalorização extra quando passa de 3 horários por turno (manhã, tarde).

Como ele cria um horário:
Criamos uma lista com todos os professores e a embaralhamos
   - Pegamos um horário da lista e então o removemos
   - Analizamos se é válido ele ser colocado nessa posição(Se não há outro horário já colocado nessa mesma posição, se essa posição não está nas limitações do professor, tudo isso é feito pela função validation() no logic.py) 
   - Vemos com base nos critérios acima qual posição seria a melhor para ele:
   - Colocamos o horário naquela posição
Repetimos esse processo até que todos os horários tenham sido colocados em alguma posição.
Avaliamos com base nos padrões já citados o horário e atribuimos um valor a ele. Se for o maior até o momento nós o salvamos, se não o discartamos. Isso é a função cost_board() também encontrada no logic.py.
Embaralhamos a lista novamente e repetimos esse processo 100 vêzes, esse elevado número é para dar uma maior segurança quanto ao resultado, mas se acabar causando muita lentidão esse valor pode ser reduzido.

## Release Notes

### 1.0v (Final Version)
- Some simple clean coding

### 0.9.4v (Geral fix)
- Bug fix
- Tests
- Excel display fix
- Validation fix

### 0.9.3v (Bimestral)
- App adaptation
- Read
- Logic on the bimestral hours (validation and costs)
- Bimestral hours display on excel

### 0.9.2v (More specific hours preferences)
- App adaptation for specific hour preference (like monday on the first hour)

### 0.9.1v (Six hours)
- General fix from five hours to six hours

### 0.9v (Rooms)
- Rooms read
- Rooms creation (on app)
Obs.: The rooms logic needed more data, so it'll be for the future

### 0.8.1v (Hotfix)
- Some errors fix

### 0.8v (Costs)
- Cost individual hour (using the preferences)
- Cost board (of all the hours choose)

### 0.7.2v (Get Better Hour)
- Function to choose the best class hour for each teacher and turm

### 0.7.1v (Prefereces .txt)
- Created file to store the preferences values on the pontuation
- Edit option on configs

### 0.7v (No random mode)
- Generating results not randonly
- Pontuation system

### 0.6.1v (Teachers saving)
- Full functional teachers saving tab
- Limitations and Preferences

### 0.6v (Random classes)
- Random mode of generating classes
- Creating sheets of turms and teachers

### 0.5.1v (App adapt)
- Adaptation to the new teachers sheet, with type (morning or afternoon)

### 0.5v (New Room)
- New room tab
- New room functions
- New room Limitations
- Save teacher fixed error

### 0.4v
- Selecionamento de arquivo para arquivo de planilha
- Estilo básico no aplicativo

### 0.3v
- Upgrade nas funções básicas criadas (Review)
- Criação da planilha de salas e melhora nas outras
- App função para adição de aulas/professores
![image](https://user-images.githubusercontent.com/62257920/138364396-9e40b620-c60b-4cac-99a5-ef3c660c2297.png)

### 0.2v
- Organização inicial das funções (para o processamento dos dados)
- App básico, com funções somente básicas

### 0.1v
- Demonstranção de utilização do pandas
- Criação da planilha esperada e resultado com o código de prefêrencias
- Criação de funções organizadoras (organização das funções que seram utilizadas)
- Criação básica do app
