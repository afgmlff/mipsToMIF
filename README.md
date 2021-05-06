Um programa feito em Python para realizar a leitura de um arquivo de entrada *.asm* qualquer e retornar dois arquivos *.mif* ([Memory Initialization File](https://www.intel.com/content/www/us/en/programmable/quartushelp/13.0/mergedProjects/reference/glossary/def_mif.htm)) de saída, referentes aos campos de dados e de texto do arquivo assembly de entrada.

O mapeamento de endereços para instruções foi realizado seguindo os endereços iniciais para dados e texto do software [MARS](http://courses.missouristate.edu/kenvollmar/mars/).

# Como executar

Para a execução do programa, é necessário ter instalado o Python em qualquer versão >= 2.7. O programa foi desenvolvido em ambiente Linux (Ubuntu 16.04), mas pode ser executado em qualquer sistema operacional.

Primeiramente, deve ser clonado o repositório para uma versão local:

    $ git clone https://github.com/afgmlff/mipsToMIF/

O programa irá pedir um arquivo de entrada no formato *.asm*, que será transformado em dois arquivos *.mif*. Para isso, basta colocar o arquivo desejado no repositório e compilar o programa. (Note que este deve ser inserido COM sua extensão, ex.: exemplo.asm).

Para rodar, basta digitar no terminal:

    $ python source.py
    
dentro da raiz do repositório.

Ao ser requerido o arquivo de entrada, basta inserir o nome (sem aspas) do arquivo que fora inserido no diretório previamente (*.asm*). O programa então retornará dois arquivos resultados *.mif*, também na raiz do diretório. Exemplo:

    Insira o nome do arquivo (ex.: exemplo.asm): examples/ex1.asm
    
# Estrutura do arquivo .asm de entrada

O arquivo de entrada pode ser qualquer algoritmo desenvolvido em Assembly MIPS. Para o funcionamento correto do programa, é necessária a divisão entre os campos de Dados (.data) e Texto (.text), como segue no arquivo "examples/ex1.asm". A ordem entre esses dois campos não importa, mas as diretivas (.data/.text) devem estar explícitas no arquivo. Não foi realizado tratamento de erros (fora de escopo).

Mais informações a respeito da motivação/funcionalidade do programa (como análises de desempenho e discussões) podem ser obtidas no arquivo "mipsToMIF.PDF".
