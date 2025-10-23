from django.urls import path
from .views import index, buscar_dados_da_outra_api, cadastrar_pessoa, detalhes_pessoa, excluir_pessoa


urlpatterns = [

    # Se acessar http://localhost:8000/
    path('index', index, name='index'), 
    
    # Se acessar http://localhost:8000/pessoas/
    # path('pessoas/', listar_pessoas_da_api, name='lista_pessoas'),
    
    # Se acessar http://localhost:8000/api/dados-externos/
    path('api/dados-externos/', buscar_dados_da_outra_api, name='api_externa'),

    path('cadastrarPessoa/', cadastrar_pessoa, name='cadastrarPessoa'),

    path('detalhes/<int:pk>/', detalhes_pessoa, name='detalhes_pessoa'),
    
    # (Opcional, mas recomendado - adicione também o excluir)
    path('excluir/<int:pk>/', excluir_pessoa, name='excluir_pessoa'),

    
    

]