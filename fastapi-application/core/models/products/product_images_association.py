from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.models.base import Base
from core.models.mixins import IntIdPkMixin


class ProductImagesAssociation(IntIdPkMixin, Base):
    """
    Association between Product and ImagePath
    """

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
    )
    image_id: Mapped[int] = mapped_column(
        ForeignKey("image_paths.id"),
    )
