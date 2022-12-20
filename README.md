# terrariumtarget
Repositório para código da aplicação para o projeto de monitoramento da estufa (Terrarium).

## Passos de construção da pipeline com arquivo yml 

É visto a seguir o arquivo de configuração yml file,  que executa a automatização do processo de integração, teste e entrega da imagem docker. 
A seguir serão explicados cada parte do arquivo yml responsável pela automatização dos processos.

É inicialmente descrito o nome do fluxo de trabalho. Logo após são especificados os eventos que darão início a execução da pipeline, sendo esses o push no branch “main” e o pull request no mesmo branch.

```yaml
name: Pipeline CI
 
on:
 push:
   branches: [ "main" ]
 pull_request:
   branches: [ "main" ] 
```

Logo em seguida são definidos os jobs a serem executados, criando cada um deles uma action com seus respectivos passos.

Para execução dos processos se faz necessário definir um ambiente de execução, para este, foi utilizado o linux Ubuntu na versão 20.04, sendo esta configuração utilizada em todos os jobs neste pipeline. Internamente a action `build` foi declarada uma variável ambiente `DOCKER_IMAGE: env.DOCKER_IMAGE` utilizada para armazenar o nome da imagem docker que será criada.

```yml
jobs:
 build:
 
   runs-on: ubuntu-20.04
   env:          
     DOCKER_IMAGE: bhpdocker/terrarium_target
```

Nos primeiros passos de execução é obtido o código do repositório e configurado o ambiente e instaladas dependências necessárias para execução.

```yml
 steps:
 
   # Get the repository's code
   - name: Checkout
     uses: actions/checkout@v2
```


Como estamos executando uma aplicação que irá rodar em uma arquitetura diferente da padrão utilizada pelo runner do github actions, foi necessário utilizar  o [QEMU](https://github.com/qemu/qemu), um emulador de código aberta genérico que possibilita emular sistemas como arm64.


```yml
# https://github.com/docker/setup-qemu-action
   - name: Set up QEMU
     uses: docker/setup-qemu-action@v1

```

### Build

 Para execução de comandos e construção de containers Docker em compatibilidade do o ambiente determinado, foi utilizado o plug-in do CLI do Docker `buildx`.

```yml
  # https://github.com/docker/setup-buildx-action
   - name: Set up Docker Buildx
     id: buildx
     uses: docker/setup-buildx-action@v1  

```

 Os passos acima citados são utilizados nas 3 actions construídas, padronizando o estabelecimento do ambiente que foi utilizado no processo de CI.

Dentro da action `build` temos como último passo a construção da imagem docker, sendo definida através do Dockerfile, sendo este previamente configurado para criação dos parâmetro do sistema especificado tendo como plataforma linux arm64, bem como as dependências da aplicação e outras definições na imagem docker base utilizada.

```yml
   - name: build the image
     run: |
       docker buildx build \
         --tag ${{ env.DOCKER_IMAGE }} \
         --platform linux/arm64  .

```

### Test (Teste)

Para que seja executado a action de teste (test), é estabelecido como critério a execução com sucesso da action `build`.

```yml
 test:
 
   runs-on: ubuntu-20.04
   needs: [build]

```

Para execução de testes de lint na linguagem python atrvés do gerenciador de pacotes pip é instalado a ferramenta pylint sendo utilizada para teste de lint em todos os códigos da aplicação.

```yml
   - name: Install dependencies
     run: |
       python -m pip install --upgrade pip
       pip install pylint
    - name: Analyze code with pylint
    run: |
       pylint $(git ls-files '*.py')
```

Para execução dos testes de unidade é utilizado o doctest, sendo executados códigos de teste de unidade definidos.

```yml
- name: Analyze code with doctest
     run: |
       python -m doctest -v test/test_with_doctest.py

```

### Delivery (Entrega)


Para que seja executado a action de Delivery, é estabelecido como critério a execução com sucesso da action `test`.

```yml
delivery:
 
   runs-on: ubuntu-20.04
   needs: [test]

```


 Com o objetivo de entrega da imagem que já passou com sucesso pelo processo de construção e testes, foi estabelecido o uso do repositório de registro [Docker Hub](https://hub.docker.com/), sendo assim necessário ao acesso o login na plataforma, utilizando de credenciais predefinidas no github.

```yml 
   - name: login to docker hub
     run: echo "${{ secrets.DOCKER_TOKEN }}" | docker login -u "${{   secrets.DOCKER_USERNAME }}" --password-stdin
```

Após o login com sucesso é executado o comando de push da imagem anteriormente construída e testada ao [Docker Hub](https://hub.docker.com/), finalizando assim o processo de entrega da imagem contendo a aplicação.


```yml
- name: Push to Docker Hub
     uses: docker/build-push-action@v2
     with:
       context: .
       platforms: linux/arm64
       push: true
       tags: ${{ secrets.DOCKER_HUB_USERNAME }}/terrarium_target:latest
       cache-from: type=registry,ref=${{ secrets.DOCKER_HUB_USERNAME }}/terrarium_target:buildcache
       cache-to: type=registry,ref=${{ secrets.DOCKER_HUB_USERNAME }}/terrarium_target:buildcache,mode=max

```

Abaixo o arquivo yml completo:

```yml
name: Pipeline CI
 
on:
 push:
   branches: [ "main" ]
 pull_request:
   branches: [ "main" ]
 
 
jobs:
 build:
 
   runs-on: ubuntu-20.04
   env:          
     DOCKER_IMAGE: bhpdocker/terrarium_target
 
   steps:
 
   # Get the repository's code
   - name: Checkout
     uses: actions/checkout@v2
     # https://github.com/docker/setup-qemu-action
    
   - name: Set up QEMU
     uses: docker/setup-qemu-action@v1
     # https://github.com/docker/setup-buildx-action
   - name: Set up Docker Buildx
     id: buildx
     uses: docker/setup-buildx-action@v1
 
   - name: build the image
     run: |
       docker buildx build \
         --tag ${{ env.DOCKER_IMAGE }} \
         --platform linux/arm64  .
 
 
 
 test:
 
   runs-on: ubuntu-20.04
   needs: [build]
 
   steps:
   # Get the repository's code
   - name: Checkout
     uses: actions/checkout@v2
     # https://github.com/docker/setup-qemu-action
   - name: Set up QEMU
     uses: docker/setup-qemu-action@v1
     # https://github.com/docker/setup-buildx-action
   - name: Set up Docker Buildx
     id: buildx
     uses: docker/setup-buildx-action@v1
 
   - name: Install dependencies
     run: |
       python -m pip install --upgrade pip
       pip install pylint
    - name: Analyze code with pylint
     run: |
       pylint $(git ls-files '*.py')
   - name: Analyze code with doctest
     run: |
       python -m doctest -v test/test_with_doctest.py
 
 
 delivery:
 
   runs-on: ubuntu-20.04
   needs: [test]
 
   env:          
     DOCKER_IMAGE: env.DOCKER_IMAGE
 
   steps:
   # Get the repository's code
   - name: Checkout
     uses: actions/checkout@v2
     # https://github.com/docker/setup-qemu-action
   - name: Set up QEMU
     uses: docker/setup-qemu-action@v1
     # https://github.com/docker/setup-buildx-action
   - name: Set up Docker Buildx
     id: buildx
     uses: docker/setup-buildx-action@v1
 
   - name: login to docker hub
     run: echo "${{ secrets.DOCKER_TOKEN }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin
 
   - name: Push to Docker Hub
     uses: docker/build-push-action@v2
     with:
       context: .
       platforms: linux/arm64
       push: true
       tags: ${{ secrets.DOCKER_HUB_USERNAME }}/terrarium_target:latest
       cache-from: type=registry,ref=${{ secrets.DOCKER_HUB_USERNAME }}/terrarium_target:buildcache
       cache-to: type=registry,ref=${{ secrets.DOCKER_HUB_USERNAME }}/terrarium_target:buildcache,mode=max
 
```

Para êxito no processo de implantação e execução do container Docker, é necessário ao efetuar o `pull` da imagem a mesma deve ser feita com a `tag: –privileged`, devido acesso ao módulo para controle da GPIO ser permitido apenas como usuário root.

```yml 
    docker run  --name=terrarium --privileged --restart=always bhpdocker/terrarium_target:latest
```




# Acesso a documentação completa do projeto:

## https://www.monografias.ufop.br/handle/35400000/4794 
