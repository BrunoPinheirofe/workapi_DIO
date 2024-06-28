from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from workoutapi.contrib.models import BaseModel


class AtletaModel(BaseModel):
    __tablename__ = "atleta"
    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), nullable=False)
    idade: Mapped[int] = mapped_column(Integer, nullable=False)
    peso: Mapped[float] = mapped_column(Float, nullable=False)
    altura: Mapped[float] = mapped_column(Float, nullable=False)
    sexo: Mapped[str] = mapped_column(String(1), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    categoria: Mapped['CategoriaModel'] = relationship('CategoriaModel', back_populates="atleta",lazy='selectin')
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categoria.pk_id"))
    centro_treinamento: Mapped['CentroTreinamentoModel'] = relationship('CentroTreinamentoModel', back_populates="atleta",lazy='selectin')
    centro_treinamento_id: Mapped[int] = mapped_column(ForeignKey("centro_treinamentos.pk_id"))
