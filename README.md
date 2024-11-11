# Estrutura e governança para análise de dados

<p align="center">
  <img src="https://i.imgur.com/aIfBsxk.png" alt="Inteli logo" border="0" width="312px">
</p>

## Grupo Vizion

### 🚀 Integrantes

- <a href="https://www.linkedin.com/in/arthur-fraige/">Arthur Fraige</a>
- <a href="https://www.linkedin.com/in/beatriz-hirasaki-leite-b2261923a/">Beatriz Hirasaki</a>
- <a href="https://www.linkedin.com/in/daniel-eduardocunha/">Daniel Cunha</a>
- <a href="https://www.linkedin.com/in/gabrielriostorres/">Gabriel Torres</a>
- <a href="https://www.linkedin.com/in/livia-bonotto-9064641a3/">Livia Bonotto</a>
- <a href="https://www.linkedin.com/in/victor-severiano-de-carvalho/">Victor Carvalho</a>
- <a href="https://www.linkedin.com/in/wagner-estevam/">Wagner Estevam</a>

## 🔍 Sumário

- [Descrição](#-descrição)
- [Documentos](#-documentos)
- [Estrutura de pastas](#-estrutura-de-pastas)
- [Instruções para acesso do projeto](#-instruções-para-acesso-do-projeto)
- [Histórico de lançamentos](#-histórico-de-lançamentos)
- [Licença/License](#-licençalicense)
- [Referências bibliográficas](#referências-bibliográficas)

## 📜 Descrição
O projeto Vizion é uma aplicação de mecanismos e ferramentas de estruturação e análise e governança de dados, possibilitando a identificação de oportunidades de negócios, a otimização de processos e a conformidade regulatória, permitindo que as organizações obtenham insights confiáveis e tomem decisões informadas com base nos dados disponíveis.

## 📝 Documentos
Existem três documentos em nosso projeto:
* [Arquitetura de negócio](docs/arquitetura_negocio.md): Define a forma de medição da qualidade dos dados, o que é extremamente importante para o entendimento dos próximos documentos.
* [Template de Arquitetura](docs/template_arquitetura.md): É a estrutura do documento principal de arquitetura de dados criada pelo grupo Vizion.
* [Arquitetura de dados](docs/arquitetura_dados.md): O maior e mais importante documento do projeto, ele aborda todas as fases, nuances, decisões arquiteturais, referências bibliográficas e especificações do projeto. 

## 📁 Estrutura de pastas

- 📂 **Vizion**
  - 📁 **[docs](docs/)**
      - 📄 [arquitetura_dados.md](docs/arquitetura_dados.md)
      - 📄 [template_arquitetura.md](docs/template_arquitetura.md)
      - 📄 [arquitetura_negocios.md](docs/arquitetura_negocio.md)
    - 📁 **[src](src/)**
        - 📁 **[eda](src/eda)**
          - 📁 **[features](src/eda/features)**
            - 📁 [profit_margin](src/eda/features/profit_margin/)
            - 📁 [projecao_vendas_vendedores](src/eda/features/projecao_vendas_vendedores/)
            - 📁 [projecao_vendas_gerente](src/eda/features/projecao_vendas_gerente)
            - 📁 [regions_compaired](src/eda/features/regions_compaired)
            - 📁 [cross-sell_substitutos](src/eda/features/cross-sell_substitutos)
            - 📁 [melhoras_lojas_mes](src/eda/features/melhoras_lojas_mes)
        - 📁 **[data_app](src/data_app)**
            - 📁 [app](src/data_app/app) | lógica da aplicação (padrão MVC)
            - 📁 [client](src/data_app/client) | front-end da aplicação
            - 📁 [config](src/data_app/config) | configuração do clickhouse
  - 📄 README.md


## 🔧 Instruções para acesso do projeto
Para acessar o projeto, há algum passos devem ser tomados:
1. Configurar um bucket S3 na AWS, contendo todos os datasets enviados pelo parceiro de projeto.
2. Preencher o .env da aplicação com os dados necessários. Um modelo de [env](./src/data_app/) pode ser encontrado na pasta do Data App.
3. Dentro da pasta Data App, deve-se executar o comando `docker compose up --build` no terminal, para que a aplicação seja construída e por fim, acessada!
4. Aproveite o Vizion!


## 🗃 Histórico de Lançamentos

**1.0 — 16/08/2024 (Sprint 1)**

1. Preenchimento do [template da arquitetura](docs/template_arquitetura.md) que guia a construção do documento de arquitetura de dados.
2. Preenchimento das seções 1, 2, 3, 4 e 5 do documento de [arquitetura de dados](docs/arquitetura_dados.md).
3. [Análise exploratória inicial por features demandadas pelo parceiro](src/eda).

**2.0 — 30/08/2024 (Sprint 2)**
1. Preenchimento das seções 6, 7 e 8 do documento de [arquitetura de dados](docs/arquitetura_dados.md).
2. Criação do módulo de ingestão e transformação de dados da pipeline, disponível na camada de lógica da aplicação em [app](./src/data_app/app/).

**3.0 — 13/09/2024 (Sprint 3)**
1. Criação de um wireframe agnóstico de dashboard, disponível no [Figma](https://www.figma.com/design/RpNuZTOI9lBQp82drcZFv1/Interface-Vizion---M11?node-id=102-432&t=DxwuTMk0XSbCOmlL-1)
2. Continuação do desenvolvimento das features iniciadas na análise exploratória.
3. Revisão das seções 1, 5, 6, 7 e 8 do documento de [arquitetura de dados](docs/arquitetura_dados.md).
4. Preenchimento das seções 9 e 10 do documento de [arquitetura de dados](docs/arquitetura_dados.md).

**4.0 — 27/09/2024 (Sprint 4)**
1. Implantação do pipeline na nuvem, disponível em um repositório privado disponibilizado apenas para os professores instrutores e orientadora.
2. Preenchimento das seções 11 e 12 do documento de [arquitetura de dados](docs/arquitetura_dados.md).
3. Primeira versão do dashboard, contendo o [front-end](src/data_app/client/) e [backend](src/data_app/app/) integrados, mas no momento, não fiel a prototipação.
4. Revisão das seções 1, 7, 8, 9 e 10 do documento de [arquitetura de dados](docs/arquitetura_dados.md).
5. Realização de testes de usabilidade na instrução da professora Laíza Ribeiro, presente também no documento de arquitetura de dados.

**4.0 — 10/10/2024 (Sprint 5)**
1. Versão final do dashboard, disponível na pasta [data_app](src/data_app/).
2. Preenchimento das sub-seções faltantes do documento de [arquitetura de dados](docs/arquitetura_dados.md).
3. Revisão geral dos documentos do projeto, disponíveis na pasta [docs](docs/).
4. Apresentação final do projeto.
5. Modificação do Readme.
 

## 📋 Licença/License
<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><span property="dct:title">Grupo Vizion</span> by <span property="cc:attributionName">Inteli, Arthur Fraige, Beatriz Hirasaki, Daniel Cunha, Gabriel Torres, Livia Bonotto, Victor Carvalho e Wagner Estevam</span> is licensed under <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"></a></p>

## 👩‍🔬 Referências bibliográficas
MACHADO, Patricia. Política de governança de dados: o que é e como construir uma? Leega, 29 jul. 2024. Disponível em: https://leega.com.br/governanca-de-dados/2024/07/29/politica-de-governanca-de-dados/. Acesso em: 16 ago. 2024.

SAP. Master Data Governance: O que é governança de dados? Disponível em: https://www.sap.com/brazil/products/technology-platform/master-data-governance/what-is-data-governance.html. Acesso em: 16 ago. 2024.

THE OPEN GROUP. TOGAF® Standard, Version 9.2. 2018. Disponível em: https://pubs.opengroup.org/togaf-standard. Acesso em: 8 ago. 2024.

IEEE. IEEE Standard 1233-1998: Guide for Developing System Requirements Specifications. New York: IEEE, 1998.