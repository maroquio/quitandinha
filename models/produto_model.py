from dataclasses import dataclass
from typing import Optional


@dataclass
class ProdutoModel:
    id: Optional[int] = None
    nome: Optional[str] = None
    descricao: Optional[str] = None
    preco: Optional[float] = None
    estoque: Optional[int] = None