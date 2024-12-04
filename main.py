from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from repos.produto_repo import ProdutoRepo
from repos.usuario_repo import UsuarioRepo
from routes.admin_router import router as admin_router
from routes.public_router import router as public_router

ProdutoRepo.criar_tabela()
ProdutoRepo.inserir_produtos_iniciais()
UsuarioRepo.criar_tabela()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"))
app.add_middleware(SessionMiddleware, secret_key="a4cc060da26e3251a72b73e241147adb7e050ac6b979911370744fb6ebbd16d46f420e480b83480f7242347f02688eda8712a7121c4611dc8743d17c607c7589")
app.include_router(public_router)
app.include_router(admin_router)