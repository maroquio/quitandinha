from fastapi import APIRouter, Form, Path, Query, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from models.produto_model import ProdutoModel
from repos.produto_repo import ProdutoRepo
from util.mensagens import *


router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="templates")

@router.get("/")
def get_root(request: Request):
    produtos = ProdutoRepo.obter_todos()
    response = templates.TemplateResponse(
        "admin/index.html", {"request": request, "produtos": produtos})
    return response

@router.get("/alterar_produto/{id}")
def get_alterar_produto(request: Request, id: int = Path(...)):
    produto = ProdutoRepo.obter_por_id(id)
    response = templates.TemplateResponse(
        "admin/alterar_produto.html", {"request": request, "produto": produto}
    )
    return response

@router.post("/alterar_produto/{id}")
def post_alterar_produto(
    request: Request, 
    id: int = Path(...),
    nome: str = Form(...),
    descricao: str = Form(...),
    estoque: int = Form(...),
    preco: float = Form(...)):
    produto = ProdutoModel(id, nome, descricao, preco, estoque)
    if ProdutoRepo.alterar(produto):
        response = RedirectResponse("/admin", 303)
        adicionar_mensagem_sucesso(response, "Produto alterado com sucesso!")
        return response
    else:
        response = templates.TemplateResponse("/admin/alterar_produto.html", {"request": request, "produto": produto})
        adicionar_mensagem_erro(response, "Corrija os campos e tente novamente.")
        return response
    
@router.get("/inserir_produto")
def get_inserir_produto(request: Request):
    produto = ProdutoModel(None, None, None, None, None)
    response = templates.TemplateResponse(
        "admin/inserir_produto.html", {"request": request, "produto": produto}
    )
    return response

@router.post("/inserir_produto")
def post_inserir_produto(
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(...),
    estoque: int = Form(...),
    preco: float = Form(...)):
    produto = ProdutoModel(None, nome, descricao, preco, estoque)
    if ProdutoRepo.inserir(produto):
        response = RedirectResponse("/admin", 303)
        adicionar_mensagem_sucesso(response, "Produto inserido com sucesso!")
        return response
    else:
        response = templates.TemplateResponse("/admin/inserir_produto.html", {"request": request, "produto": produto})
        adicionar_mensagem_erro(response, "Corrija os campos e tente novamente.")
        return response
    
@router.get("/excluir_produto/{id}")
def get_excluir_produto(request: Request, id: int = Path(...)):
    produto = ProdutoRepo.obter_por_id(id)
    if produto:
        response = templates.TemplateResponse(
            "admin/excluir_produto.html", {"request": request, "produto": produto}
        )
        return response
    else:
        response = RedirectResponse("/admin", 303)
        adicionar_mensagem_erro(response, "O produto que você tentou excluir não existe!")
        return response
    
@router.post("/excluir_produto")
def post_excluir_produto(id: int = Form(...)):
    if ProdutoRepo.excluir(id):
        response = RedirectResponse("/admin", 303)
        adicionar_mensagem_sucesso(response, "Produto excluído com sucesso!")
        return response
    else:
        response = RedirectResponse("/admin", 303)
        adicionar_mensagem_erro(response, "Não foi possível excluir o produto!")
        return response