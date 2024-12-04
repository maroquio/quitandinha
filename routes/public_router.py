from datetime import date
import bcrypt
from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from models.usuario_model import Usuario
from repos.produto_repo import ProdutoRepo
from repos.usuario_repo import UsuarioRepo
from util.mensagens import *


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
def get_root(request: Request):
    produtos = ProdutoRepo.obter_todos()
    response = templates.TemplateResponse(
        "index.html", {"request": request, "produtos": produtos})
    return response

@router.get("/produto/{id}")
def get_root(request: Request, id: int):
    produto = ProdutoRepo.obter_por_id(id)
    response = templates.TemplateResponse(
        "produto.html", {"request": request, "produto": produto})
    return response

@router.get("/entrar")
def get_entrar(request: Request):
    response = templates.TemplateResponse(
        "entrar.html", {"request": request})
    return response

@router.post("/entrar")
def post_entrar(
    request: Request, 
    email: str = Form(),
    senha: str = Form()):
    senha_hash = UsuarioRepo.obter_senha_por_email(email)
    # se não encontrou senha para o e-mail, 
    # é porque não está cadastrado
    if not senha_hash:
        response = RedirectResponse("/entrar", 303)
        adicionar_mensagem_erro(response, "Credenciais inválidas!")
        return response
    # se encontrou senha e ela não confere com a cadastrada,
    # permanece no formulário de login
    if not bcrypt.checkpw(senha.encode(), senha_hash.encode()):
        response = RedirectResponse("/entrar", 303)
        adicionar_mensagem_erro(response, "Credenciais inválidas!")
        return response
    # se encontrou o usuário e a senha confere,
    # cria a sessão e manda o usuário para a página principal
    usuario = UsuarioRepo.obter_dados_por_email(email)
    request.session["usuario"] = {
        "nome": usuario.nome,
        "email": usuario.email, 
        "perfil": usuario.perfil
    }
    response = RedirectResponse("/", 303)
    adicionar_mensagem_sucesso(response, f"Olá, <b>{usuario.nome}</b>. Você está autenticado!")
    return response   
    
@router.get("/sair")
def get_sair(request: Request):
    request.session.clear()
    response = RedirectResponse("/", 303)
    adicionar_mensagem_info(response, "Você não está mais autenticado.")
    return response

@router.get("/cadastrar")
def get_cadastrar(request: Request):
    response = templates.TemplateResponse(
        "cadastrar.html", {"request": request})
    return response

@router.post("/cadastrar")
def post_cadastrar(
    request: Request, 
    nome: str = Form(),
    data_nascimento: date = Form(),
    email: str = Form(),
    telefone: str = Form(),
    senha: str = Form(),
    confirmacao_senha: str = Form()):
    if senha != confirmacao_senha:
        response = RedirectResponse("/cadastrar", 303)
        adicionar_mensagem_erro(response, "Senha e confirmação de senha não conferem.")
        return response
    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
    novo_usuario = Usuario(None, nome, data_nascimento, email, telefone, senha_hash.decode(), 1)
    novo_usuario = UsuarioRepo.inserir(novo_usuario)
    if novo_usuario:
        response = RedirectResponse("/entrar", 303)
        adicionar_mensagem_sucesso(response, "Cadastro realizado com sucesso! Use suas credenciais para entrar.")
        return response
    else:
        response = RedirectResponse("/cadastrar", 303)
        adicionar_mensagem_erro(response, "Ocorreu algum problema ao tentar realizar seu cadastro. Tente novamente.")
        return response