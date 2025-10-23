from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt

API_BASE_URL = "https://curly-winner-vj4gvqqjqp93x5rj-8080.app.github.dev/api/pessoas"
# def index(request):
#     return redirect('index')


# def listar_pessoas_da_api(request):
#     """
#     Esta view consome a API externa, busca a lista de pessoas
#     e a exibe em um template.
#     """
#     # A URL completa da sua API
#     api_url = "https://fantastic-enigma-7vr64vp69j653xg9g-8080.app.github.dev"
    
#     pessoas = []
#     erro = None

#     try:
#         # 1. Faz a requisição GET para a API
#         response = requests.get(api_url, timeout=10)

#         # 2. Verifica se a requisição foi bem-sucedida (status code 200)
#         response.raise_for_status()

#         # 3. Converte a resposta JSON em uma lista de dicionários Python
#         pessoas = response.json()

#     # --- CORREÇÃO AQUI ---
#     # Trocamos 'request.exceptions' por 'requests.exceptions' (com 's')
#     except requests.exceptions.HTTPError as http_err:
#         erro = f"Erro HTTP: {http_err}"
        
#     # --- CORREÇÃO AQUI ---
#     except requests.exceptions.ConnectionError as conn_err:
#         erro = f"Erro de Conexão: A API parece estar offline. ({conn_err})"
        
#     # --- CORREÇÃO AQUI ---
#     except requests.exceptions.Timeout:
#         erro = "Erro: A requisição para a API demorou muito (Timeout)."
        
#     # --- CORREÇÃO AQUI ---
#     except requests.exceptions.RequestException as req_err:
#         erro = f"Erro ao fazer a requisição: {req_err}"
    
#     # --- CORREÇÃO AQUI ---
#     except requests.exceptions.JSONDecodeError:
#         erro = "Erro: A API não retornou uma resposta em formato JSON válido."

#     # 4. Envia os dados (ou o erro) para o template
#     context = {
#         'pessoas': pessoas,
#         'erro': erro
#     }
    
#     # Renderiza a página
#     return render(request, "consumir_api.html")


def index(request):
    """
    Renderiza uma página de exemplo (ex: lista.html).
    """
    # CORREÇÃO 1: O 'request' deve ser o primeiro argumento do render.
    # CORREÇÃO 2: O caminho do template não deve começar com '/'.
    # Ajuste "template/lista.html" se o caminho estiver incorreto 
    # (ex: "registro/lista.html").
    return render(request, "lista.html")


def buscar_dados_da_outra_api(request):
    """
    Esta view (no seu Django) vai buscar os dados na API externa.
    Ela servirá como um "proxy" ou "intermediário".
    """
    
    # URL da API Spring (que usa o Postgres)
    url_api_spring = "https://curly-winner-vj4gvqqjqp93x5rj-8080.app.github.dev/api/pessoas" # Verifique se /pessoas é o caminho
    
    try:
        response = requests.get(url_api_spring, timeout=10)
        
        # Esta linha vai capturar erros 404, 500, etc.
        response.raise_for_status() 
        
        dados_externos = response.json()
        
        # Retorna os dados para o seu JavaScript
        return JsonResponse(dados_externos, safe=False)

    except requests.exceptions.RequestException as e:
        # Se o Codespace estiver offline ou a porta não for pública,
        # ainda vai cair aqui.
        return JsonResponse({"erro": f"API externa indisponível: {e}"}, status=503)

@csrf_exempt
def cadastrar_pessoa(request):
    """
    View 2: Carrega a página com o formulário (GET) e
    processa o envio do formulário (POST).
    """
    
    # Se o método for POST, o usuário enviou o formulário
    if request.method == 'POST':
        # 1. Pega os dados do formulário do Django
        nome = request.POST.get('nome')
        idade = request.POST.get('idade')

        # 2. Prepara os dados para enviar à API externa (em formato JSON)
        dados_nova_pessoa = {
            'nome': nome,
            'idade': idade
        }

        try:
            # 3. Faz a requisição POST para a API externa
            response = requests.post(API_BASE_URL, json=dados_nova_pessoa, timeout=10)
            
            # Verifica se a API retornou um erro (ex: 400, 500)
            response.raise_for_status()
            
            # 4. Se tudo deu certo, redireciona para a página de listagem
            return redirect('lista_pessoas')

        except requests.exceptions.RequestException as e:
            # 5. Se falhou, renderiza a página de cadastro de novo
            #    com uma mensagem de erro.
            contexto = {
                'erro': f"Erro ao cadastrar na API externa: {e}",
                'nome': nome, # Devolve o nome para o formulário
                'idade': idade # Devolve a idade para o formulário
            }
            return render(request, "cadastro.html", contexto)

    # Se o método for GET, apenas mostre o formulário vazio
    return render(request, "form.html")


def detalhes_pessoa(request, pk):
    """
    View 4: Busca os dados de UMA pessoa na API externa
    e exibe na página 'detalhes.html'.
    
    O 'pk' (ex: 1) vem da URL.
    """
    contexto = {} # Dicionário para enviar dados ao template
    try:
        # 1. Monta a URL para a API externa: .../api/pessoas/1
        url_pessoa = f"{API_BASE_URL}/{pk}"
        
        # 2. Busca os dados na API externa
        response = requests.get(url_pessoa, timeout=10)
        
        # Lança um erro se a API retornar 404, 500, etc.
        response.raise_for_status()
        
        # 3. Envia os dados da pessoa (em JSON) para o template
        contexto['pessoa'] = response.json()
        
    except requests.exceptions.RequestException as e:
        # 4. Se a pessoa não for encontrada ou a API falhar
        contexto['erro'] = f"Não foi possível buscar a pessoa (ID: {pk}): {e}"

    # 5. Renderiza o template 'detalhes.html' com os dados
    # (Note o 's' em 'detalhes.html')
    return render(request, "detalhe.html", contexto)

@csrf_exempt
def excluir_pessoa(request, pk):
    # (Lógica para excluir...)
    if request.method == 'POST':
        try:
            url_pessoa = f"{API_BASE_URL}/{pk}"
            response = requests.delete(url_pessoa, timeout=10)
            response.raise_for_status()
            return redirect('index')
            
        except requests.exceptions.RequestException as e:
            contexto = {'erro': f"Não foi possível excluir: {e}"}
            # Tenta buscar os dados da pessoa para exibir o erro na pág. de detalhes
            try:
                response = requests.get(f"{API_BASE_URL}/{pk}", timeout=10)
                if response.ok:
                    contexto['pessoa'] = response.json()
            except requests.exceptions.RequestException:
                pass 
            return render(request, "detalhes.html", contexto)
    return redirect('detalhes_pessoa', pk=pk)



